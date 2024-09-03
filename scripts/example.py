"""
Example script.
"""

import json
import shlex

from awscliv2.api import AWSAPI

aws_api = AWSAPI()
output = aws_api.execute(
    shlex.split("ec2 describe-instances  --filters 'Name=instance-type,Values=t2.micro'")
)
data = json.loads(output)
instances = data["Reservations"][0]["Instances"]
instance_ids = [i["InstanceId"] for i in instances]

print("Instance IDs:", instance_ids)  # noqa: T201
