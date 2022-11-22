from aws_cdk.core import Stack, Construct, Duration

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_iam as iam
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
from aws_cdk.aws_ssm import StringParameter
import aws_cdk.aws_codedeploy as codedeploy

from cdk_imagebuilder.stacks.code_deploy_policies import (
    EE_DEPLOYER_POLICY,
    EE_CODE_DEPLOY_POLICY,
    EE_CODE_DEPLOY_EC2_POLICY,
    EE_CODE_DEPLOY_LAUNCH_TEMPLATE_POLICY,
)

EE_IMAGE = "ami-07f241317e951630b"


class EECodeDeployment(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # self.ami = ec2.MachineImage.lookup(name=EE_IMAGE, owners=["self"])
        self.ami = ec2.MachineImage.generic_linux(ami_map={"eu-west-2": EE_IMAGE})

        self.default_vpc = ec2.Vpc.from_lookup(
            scope=self, id="default-vpc-id", is_default=True
        )

        self.policies = self.create_policies()
        self.roles = self.create_roles()
        self.alb_security_group = self.create_alb_security_group()

        self.instance_security_groups = self.create_instance_security_groups(
            self.alb_security_group
        )

        self.launch_template = self.create_launch_template(
            ami=self.ami,
            security_group=self.instance_security_groups,
            role=self.roles["codedeploy-ec2-instance-profile"],
        )

        self.target_group = self.create_target_group()
        self.auto_scaling_group = self.create_scaling_group(
            vpc=self.default_vpc,
            launch_template=self.launch_template,
            target_group=self.target_group,
        )

        self.alb = self.create_alb(
            security_group=self.alb_security_group,
            target_group=self.target_group,
            https=False,
        )

        self.code_deploy = self.create_code_deploy(asg=self.auto_scaling_group)

    def create_scaling_group(
        self,
        vpc: ec2.Vpc,
        launch_template,
        target_group: elbv2.ApplicationTargetGroup,
    ):
        scaling_group = autoscaling.AutoScalingGroup(
            self,
            "ASG",
            vpc=vpc,
            launch_template=launch_template,
            min_capacity=1,
            max_capacity=10,
            desired_capacity=1,
            health_check=autoscaling.HealthCheck.elb(grace=Duration.seconds(300)),
            termination_policies=[
                autoscaling.TerminationPolicy.OLDEST_LAUNCH_TEMPLATE,
                autoscaling.TerminationPolicy.CLOSEST_TO_NEXT_INSTANCE_HOUR,
            ],
        )
        scaling_group.attach_to_application_target_group(target_group=target_group)
        return scaling_group

    def create_code_deploy(self, asg):
        application = codedeploy.ServerApplication(
            self, "CodeDeployApplicationID", application_name="EECodeDeploy"
        )

        deployment_group = codedeploy.ServerDeploymentGroup(
            self,
            "EEDeploymentGroup",
            application=application,
            deployment_group_name="EEDeploymentGroup",
            auto_scaling_groups=[asg],
            # adds EC2 instances matching tags
            # ec2_instance_tags=codedeploy.InstanceTagSet(
            #     {
            #         # any instance with tags satisfying
            #         # key1=v1 or key1=v2 or key2 (any value) or value v3 (any key)
            #         # will match this group
            #         "key1": ["v1", "v2"],
            #         "key2": [],
            #         "": ["v3"],
            #     }
            # ),
            # ignore_poll_alarms_failure=False,
            # auto-rollback configuration
            # auto_rollback=codedeploy.AutoRollbackConfig(
            #     failed_deployment=True,
            #     default: true
            # stopped_deployment=True,
            # default: false
            # deployment_in_alarm=True,
            # ),
        )

    def create_launch_template(
        self, ami: ec2.IMachineImage, security_group: ec2.SecurityGroup, role: iam.Role
    ) -> ec2.LaunchTemplate:
        lt = ec2.LaunchTemplate(
            self,
            "ee-launch-template-id",
            instance_type=ec2.InstanceType("t3a.medium"),
            machine_image=ami,
            launch_template_name="ee-launch-template",
            role=role,
            security_group=security_group,
        )
        return lt

    def create_target_group(self):
        return elbv2.ApplicationTargetGroup(
            self,
            "ee-alb-tg-id",
            port=8001,
            protocol=elbv2.ApplicationProtocol.HTTP,
            health_check=elbv2.HealthCheck(
                enabled=True,
                healthy_threshold_count=2,
                interval=Duration.seconds(100),
                port="traffic-port",
                path="/",
                protocol=elbv2.Protocol.HTTP,
                timeout=Duration.seconds(5),
                unhealthy_threshold_count=5,
                healthy_http_codes="200",
            ),
            target_group_name="ee-alb-tg",
            target_type=elbv2.TargetType.INSTANCE,
            vpc=self.default_vpc,
        )

    def create_instance_security_groups(
        self, alb_security_group: ec2.SecurityGroup
    ) -> ec2.SecurityGroup:

        instance_security_group = ec2.SecurityGroup(
            self,
            "instance-security-group",
            vpc=self.default_vpc,
            allow_all_outbound=True,
            security_group_name="Instance Security Group",
            description="Allow HTTP access for an instance from the ALB security group",
        )

        instance_security_group.add_ingress_rule(
            ec2.Peer.security_group_id(alb_security_group.security_group_id),
            ec2.Port.tcp(8001),
            "HTTP from ALB",
        )
        return instance_security_group

    def create_alb_security_group(self, https=True):
        alb_security_group = ec2.SecurityGroup(
            self,
            "alb-security-group",
            vpc=self.default_vpc,
            allow_all_outbound=True,
            security_group_name="ALB Security Group",
            description="ALB accepts all traffic",
        )
        alb_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow HTTP from anywhere"
        )
        if https:
            alb_security_group.add_ingress_rule(
                ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "allow HTTPS from anywhere"
            )

        return alb_security_group

    def create_alb(
        self,
        security_group: ec2.SecurityGroup,
        target_group: elbv2.ApplicationTargetGroup,
        https=True,
    ) -> elbv2.ApplicationLoadBalancer:
        """
        Creates an Application Load Balancer (ALB).

        If https is True then the ALB will listen on post 443. This requires a
        valid cert ARN to exist in SSM at `EE_SSL_CERTIFICATE_ARN`
        """
        subnets = ec2.SubnetSelection(
            availability_zones=["eu-west-2a", "eu-west-2b", "eu-west-2c"]
        )

        alb = elbv2.ApplicationLoadBalancer(
            self,
            "application-load-balancer-id",
            vpc=self.default_vpc,
            vpc_subnets=subnets,
            internet_facing=True,
            security_group=security_group,
            ip_address_type=elbv2.IpAddressType.IPV4,
            load_balancer_name="ee-alb",
        )

        if https:
            # Listen on HTTPS
            alb.add_listener(
                "https-listener-id",
                certificates=[
                    elbv2.ListenerCertificate.from_arn(
                        StringParameter.value_from_lookup(
                            self,
                            "SSL_CERTIFICATE_ARN",
                        )
                    )
                ],
                port=443,
                protocol=elbv2.ApplicationProtocol.HTTPS,
                default_action=elbv2.ListenerAction.forward([self.ee_alb_tg]),
            )

        # Listen on HTTP
        http_listener = alb.add_listener(
            "http-listener-id", port=80, protocol=elbv2.ApplicationProtocol.HTTP
        )

        if https:
            # Redirect from HTTP to HTTPS
            http_listener.add_action(
                "redirect-http-to-https-id",
                action=elbv2.ListenerAction.redirect(
                    port="443", protocol="HTTPS", permanent=True
                ),
            )
        else:
            http_listener.add_target_groups(
                "http-target-groups-id", target_groups=[target_group]
            )

        return alb

    def create_policies(self):
        def create_policy(policy_id, name, document):
            return iam.Policy(
                self,
                policy_id,
                document=iam.PolicyDocument.from_json(document),
                policy_name=name,
            )

        return {
            "codedeploy-launch-template-permissions": create_policy(
                "codedeploy-launch-template-permissions-id",
                "CodeDeployLaunchTemplatePermissions",
                EE_CODE_DEPLOY_LAUNCH_TEMPLATE_POLICY,
            ),
            "codedeploy-ec2-permissions": create_policy(
                "codedeploy-ec2-permissions-id",
                "CodeDeploy-EC2-Permissions",
                EE_CODE_DEPLOY_EC2_POLICY,
            ),
            "codedeploy-and-related-services": create_policy(
                "codedeploy-and-related-services-id",
                "CodeDeployAndRelatedServices",
                EE_CODE_DEPLOY_POLICY,
            ),
            "ee-deployer": create_policy(
                "ee-deployer-id",
                "EEDeployer",
                EE_DEPLOYER_POLICY,
            ),
        }

    def create_roles(self) -> [str, iam.Role]:
        roles = {
            "codedeploy-ec2-instance-profile": iam.Role(
                self,
                "codedeploy-ec2-instance-profile-id",
                assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                role_name="CodeDeployEC2InstanceProfile",
                managed_policies=[
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        "AmazonSSMReadOnlyAccess",
                    ),
                    iam.ManagedPolicy.from_aws_managed_policy_name(
                        "CloudWatchAgentServerPolicy",
                    ),
                ],
            ),
            "codedeploy-service-role": iam.Role(
                self,
                "codedeploy-service-role-id",
                assumed_by=iam.ServicePrincipal("codedeploy.amazonaws.com"),
                role_name="CodeDeployServiceRole",
            ),
        }

        roles["codedeploy-ec2-instance-profile"].attach_inline_policy(
            self.policies["codedeploy-ec2-permissions"]
        )
        roles["codedeploy-service-role"].attach_inline_policy(
            self.policies["codedeploy-launch-template-permissions"]
        )
        roles["codedeploy-service-role"].add_managed_policy(
            iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "aws-code-deploy-role-id",
                "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole",
            )
        )

        return roles
