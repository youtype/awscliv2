# Api

> Auto-generated documentation for [awscliv2.api](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py) module.

Runner for all AWS CLI v2 commands.

- [Awscliv2](../README.md#aws-cli-v2-for-python) / [Modules](../MODULES.md#awscliv2-modules) / [Awscliv2](index.md#awscliv2) / Api
    - [AWSAPI](#awsapi)
        - [AWSAPI().assume_role](#awsapiassume_role)
        - [AWSAPI().execute](#awsapiexecute)
        - [AWSAPI.get_awscli_v2_cmd](#awsapiget_awscli_v2_cmd)
        - [AWSAPI().print_version](#awsapiprint_version)
        - [AWSAPI().run_awscli_v2](#awsapirun_awscli_v2)
        - [AWSAPI().run_awscli_v2_detached](#awsapirun_awscli_v2_detached)
        - [AWSAPI().set_credentials](#awsapiset_credentials)

## AWSAPI

[[find in source code]](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L19)

```python
class AWSAPI():
    def __init__(
        encoding: str = ENCODING,
        output: Optional[TextIO] = None,
    ) -> None:
```

API for all AWS CLI v2 commands.

Supports installed and dockerized AWS CLI v2.

#### Arguments

- `encoding` - Input/output encoding, default utf-8.
- `output` - Output stream, default sys.stdout.

#### See also

- [ENCODING](constants.md#encoding)

### AWSAPI().assume_role

[[find in source code]](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L134)

```python
def assume_role(
    profile_name: str,
    source_profile: str,
    role_arn: str,
) -> None:
```

Add assume role to credentials.

### AWSAPI().execute

[[find in source code]](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L78)

```python
def execute(args: Sequence[str]) -> str:
```

Execute AWS CLI v2 command.

#### Returns

Command output.

### AWSAPI.get_awscli_v2_cmd

[[find in source code]](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L35)

```python
@staticmethod
def get_awscli_v2_cmd() -> List[str]:
```

Get command to run AWS CLI v2.

### AWSAPI().print_version

[[find in source code]](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L125)

```python
def print_version() -> int:
```

Print AWS CLI v2 version.

#### Returns

Process exit code.

### AWSAPI().run_awscli_v2

[[find in source code]](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L93)

```python
def run_awscli_v2(args: Sequence[str]) -> int:
```

Run AWS CLI.

#### Returns

Process exit code.

### AWSAPI().run_awscli_v2_detached

[[find in source code]](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L109)

```python
def run_awscli_v2_detached(args: Sequence[str]) -> int:
```

Run AWS CLI as a detached subprocess.

#### Returns

Process exit code.

### AWSAPI().set_credentials

[[find in source code]](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L170)

```python
def set_credentials(
    profile_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_session_token: str = '',
    region: str = '',
) -> None:
```

Add or update credentials in `~/.aws/credentials`
