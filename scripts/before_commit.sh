#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $(realpath $0)))
cd $ROOT_PATH

python -m black awscliv2
python -m isort awscliv2
python -m pylint awscliv2
python -m flake8 awscliv2
python -m pytest --cov-report term --cov=awscliv2
python -m mypy awscliv2
npx pyright

./scripts/update_docs.sh
