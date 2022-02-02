# AWSCLIRunner

> Auto-generated documentation for [awscliv2.awscli_runner](blob/main/awscliv2/awscli_runner.py) module.

Runner for all AWS CLI v2 commands.

- [Awscliv2](../README.md#aws-cli-v2-for-python-) / [Modules](../MODULES.md#awscliv2-modules) / [Awscliv2](index.md#awscliv2) / AWSCLIRunner
    - [AWSCLIRunner](#awsclirunner)
        - [AWSCLIRunner.get_awscli_v2_cmd](#awsclirunnerget_awscli_v2_cmd)
        - [AWSCLIRunner().print_version](#awsclirunnerprint_version)
        - [AWSCLIRunner().run_assume_role](#awsclirunnerrun_assume_role)
        - [AWSCLIRunner().run_awscli_v2](#awsclirunnerrun_awscli_v2)
        - [AWSCLIRunner().run_subprocess](#awsclirunnerrun_subprocess)
        - [AWSCLIRunner().set_credentials](#awsclirunnerset_credentials)

## AWSCLIRunner

[[find in source code]](blob/main/awscliv2/awscli_runner.py#L17)

```python
class AWSCLIRunner():
    def __init__(encoding: str) -> None:
```

Runner for all AWS CLI v2 commands.

Supports installed and dockerized AWS CLI v2.

### AWSCLIRunner.get_awscli_v2_cmd

[[find in source code]](blob/main/awscliv2/awscli_runner.py#L28)

```python
@staticmethod
def get_awscli_v2_cmd() -> List[str]:
```

Get command to run AWS CLI v2.

### AWSCLIRunner().print_version

[[find in source code]](blob/main/awscliv2/awscli_runner.py#L78)

```python
def print_version() -> int:
```

Print AWS CLI v2 version.

#### Returns

Process exit code.

### AWSCLIRunner().run_assume_role

[[find in source code]](blob/main/awscliv2/awscli_runner.py#L87)

```python
def run_assume_role(
    profile_name: str,
    source_profile: str,
    role_arn: str,
) -> None:
```

Add assume role to credentials.

### AWSCLIRunner().run_awscli_v2

[[find in source code]](blob/main/awscliv2/awscli_runner.py#L65)

```python
def run_awscli_v2(args: Sequence[str], stdout: TextIO = sys.stdout) -> int:
```

Run AWS CLI.

### AWSCLIRunner().run_subprocess

[[find in source code]](blob/main/awscliv2/awscli_runner.py#L53)

```python
def run_subprocess(cmd: Sequence[str], stdout: TextIO = sys.stdout) -> int:
```

Run interactive subprocess.

### AWSCLIRunner().set_credentials

[[find in source code]](blob/main/awscliv2/awscli_runner.py#L124)

```python
def set_credentials(
    profile_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_session_token: Optional[str] = None,
) -> None:
```

Add or update credentials in `~/.aws/credentials`
