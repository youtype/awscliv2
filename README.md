# AWS CLI v2 for Python

[![PyPI - awscliv2](https://img.shields.io/pypi/v/awscliv2.svg?color=blue&label=awscliv2)](https://pypi.org/project/awscliv2)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/awscliv2.svg?color=blue)](https://pypi.org/project/awscliv2)
[![PyPI - Downloads](https://static.pepy.tech/badge/awscliv2)](https://pepy.tech/project/awscliv2)

Wrapper for [AWS CLI v2](https://awscli.amazonaws.com/v2/documentation/api/latest/index.html).

- [AWS CLI v2 for Python](#aws-cli-v2-for-python)
  - [Features](#features)
  - [Before you start](#before-you-start)
  - [Installation](#installation)
  - [Usage](#usage)
    - [From command line](#from-command-line)
    - [Docker fallback](#docker-fallback)
    - [Extra commands](#extra-commands)
    - [As a Python module](#as-a-python-module)
  - [Development](#development)
  - [How to help](#how-to-help)
  - [Versioning](#versioning)
  - [Latest changes](#latest-changes)

## Features

- No dependency hell, like with original [awscli](https://pypi.org/project/awscli/)
- Can install and update `awscliv2` binaries
- Provides access to all AWS services
- Has Python interface `awscliv2.api.AWSAPI`

## Before you start

- This is not an official AWS CLI v2 application, [rant there](https://github.com/aws/aws-cli/issues/4947)
- Check the source code of this app, as you are working with sensitive data
- By default this app uses [amazon/aws-cli](https://hub.docker.com/r/amazon/aws-cli) Docker image
- To use [binaries for your OS](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html), run `awsv2 --install`
- Cross-check the source code again, probably I want to
  [steal your credentials](https://blog.sonatype.com/python-packages-upload-your-aws-keys-env-vars-secrets-to-web)!

## Installation

```bash
python -m pip install awscliv2
```

You can add an alias to your `~/.bashrc` or `~/.zshrc` to use it as a regular `AWS CLI v2`

```bash
alias aws='awsv2'
```

## Usage

### From command line

Install `AWS CLI v2`:

```bash
# do not worry if this fails, you can still use awsv2 if you have docker installed
awsv2 --install
```

Configure default profile if needed:

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

Also, you can check [scripts/example.sh](https://github.com/youtype/awscliv2/blob/main/scripts/example.sh)

### Docker fallback

Unless you run `awsv2 --install` once, application will use [amazon/aws-cli](https://hub.docker.com/r/amazon/aws-cli) Docker image. The image is not ideal, and it uses `root` user, so fix downloaded file permissions manually. Or just run `awsv2 --install`

Update it with `docker pull amazon/aws-cli`.

Container uses two volumes:

- `$HOME/.aws` -> `/root/.aws` - credentials and config store
- `$(cwd)` -> `/aws` - Docker image workdir

### Extra commands

`awscliv2` contains a few commands to make your life easier, especially in CI or any non-TTY environment.

- `awsv2 -U/--update/--install` - Install `AWS CLI v2`
- `awsv2 --configure <profile_name> <aws_access_key_id> <aws_secret_access_key> [<aws_session_token>] [<region>]` - set profile in `~/.aws/credentials`
- `awsv2 --assume-role <profile_name> <source_profile> <role_arn>` - create a new profile with assume role credentials
- `awsv2 -V/--version` - Output `awscliv2` and `AWS CLI v2` versions

### As a Python module

Basic usage

```python
from awscliv2.api import AWSAPI
from awscliv2.exceptions import AWSCLIError

aws_api = AWSAPI()

try:
    output = aws_api.execute(["s3", "ls"])
except AWSCLIError as e:
    print(f"Something went wrong: {e}")
else:
    print(output)
```

Install binaries for your OS from Python

```python
from awscliv2.installers import install_multiplatform

install_multiplatform()
```

You can also set credentials or assume roles

```python
from awscliv2.api import AWSAPI

aws_api = AWSAPI()

aws_api.set_credentials(
    profile_name="my_profile",
    aws_access_key_id="access_key",
    aws_secret_access_key="secret_key",
    region="us-east-1",
)
aws_api.assume_role(
    profile_name="my_profile",
    source_profile="source_profile",
    role_arn="role_arn",
)
```

## Development

- Install [poetry](https://python-poetry.org/)
- Run `poetry install`
- Use `black` formatter in your IDE

## How to help

- Ping AWS team to release an official PyPI package
- Share your experience in issues

## Versioning

`awscliv2` version follows [PEP 440](https://www.python.org/dev/peps/pep-0440/).

## Latest changes

Full changelog can be found in [Releases](https://github.com/youtype/awscliv2/releases).
