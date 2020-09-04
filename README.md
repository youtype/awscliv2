# AWS CLI v2

[![PyPI - awscliv2](https://img.shields.io/pypi/v/awscliv2.svg?color=blue&label=awscliv2)](https://pypi.org/project/awscliv2)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/awscliv2.svg?color=blue)](https://pypi.org/project/awscliv2)

Wrapper for dockerized [AWS CLI v2](https://awscli.amazonaws.com/v2/documentation/api/latest/index.html)
based on [amazon/aws-cli](https://hub.docker.com/r/amazon/aws-cli) Docker image.

- [AWS CLI v2](#aws-cli-v2)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Extra commands](#extra-commands)
  - [Versioning](#versioning)
  - [Latest changes](#latest-changes)

## Installation

Install [Docker](https://docs.docker.com/get-docker/).

```bash
python -m pip install awscliv2
```

You can add an alias to your `~/.bashrc` or `~/.zshrc` to use it as a regular `AWS CLI v2`

```bash
alias aws='awsv2'
```

## Usage

Container uses two volumes:

- `$HOME/.aws` -> `/root/.aws` - credentials and config store
- `$(cwd)` -> `/aws` - Docker image workdir

Pull latest `amazon/aws-cli` image:

```bash
awsv2 --update
```

Configure default frofile if needed:

```bash
AWS_ACCESS_KEY_ID='my-access-key'
AWS_SECRET_ACCESS_KEY='my-secret-key'

# --configure <profile_name> <aws_access_key_id> <aws_secret_access_key> [<aws_session_token>]
awsv2 --configure default ${AWS_ACCESS_KEY_ID} ${AWS_SECRET_ACCESS_KEY}
awsv2 configure set region us-west-1
```

Use `AWS CLI` as usual:

```bash
# alias for
# docker run --rm -i -v ~/.aws:/root/.aws -v $(pwd):/aws amazon/aws-cli $@
awsv2 s3 ls

# or as a python module
python -m awscliv2 s3 ls
```

Also, you can check [example.sh](https://github.com/vemel/awscliv2/blob/master/example.sh)

### Extra commands

`awscliv2` contains a few commands to make your life easier, especially in CI or any non-TTY environment.

- `awsv2 -U/--update` - Pull `amazon/aws-cli:latest` Docker image
- `awsv2 --configure <profile_name> <aws_access_key_id> <aws_secret_access_key> [<aws_session_token>]` - set profile in `~/.aws/credentials`
- `awsv2 --assume-role <profile_name> <source_profile> <role_arn>` - create a new profile with assume role credentials
- `awsv2 -V/--version` - Output `awscliv2` and `amazon/aws-cli` versions

## Versioning

`awscliv2` version follows [PEP 440](https://www.python.org/dev/peps/pep-0440/).

## Latest changes

Full changelog can be found in [Changelog](./CHANGELOG.md).
Release notes can be found in [Releases](https://github.com/vemel/awscliv2/releases).
