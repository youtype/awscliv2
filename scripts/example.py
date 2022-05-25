import shlex

from awscliv2.api import AWSAPI

aws_api = AWSAPI()
output = aws_api.execute(
    shlex.split("ec2 describe-instances  --filters 'Name=instance-type,Values=t2.micro'")
)

print("Output:", output)
