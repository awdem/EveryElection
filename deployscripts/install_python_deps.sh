#!/usr/bin/env bash
set -xeE

# should we delete the env and recreate?
cd /var/www/every_election/repo/
uv venv
. .venv/bin/activate
uv sync --extra production --no-dev
