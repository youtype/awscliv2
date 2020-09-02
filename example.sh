#!/usr/bin/env bash
set -e

# check that docker is installed and running
docker ps

# install package
pip install awscliv2

# set alias to use instead of non-dockerized version
# useful if you want to use `aws` instead of `awsv2`
alias aws='awsv2'

# optionally pull latest amazon/aws-cli image
awsv2 -U

# configure your default profile
awsv2 configure
awsv2 confgiure set region us-west-1

# or in non-interactive environment
# --configure <name> <access_key> <secret_key> [<session_token>]
awsv2 --configure default access_key secret_key

# use AWS CLI v2 as usual
awsv2 s3 ls

# assume role and use it
# --assume-role <name> <source_profile> <role_arn>
awsv2 --assume-role my-role default arn:aws:iam::1234:role/my-role
awsv2 --profile my-role s3 ls
