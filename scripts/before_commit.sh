#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $(realpath $0)))
cd $ROOT_PATH

poetry run black awscliv2
poetry run isort awscliv2
poetry run flake8 awscliv2
poetry run pytest --cov-report term --cov=awscliv2
poetry run npx pyright

./scripts/update_docs.sh
