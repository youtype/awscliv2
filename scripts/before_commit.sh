#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $(realpath $0)))
cd $ROOT_PATH

poetry run ruff check
poetry run ruff format --check
poetry run pytest --cov-report term --cov=awscliv2
poetry run npx pyright
