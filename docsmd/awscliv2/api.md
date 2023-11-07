# Api

[Awscliv2 Index](../README.md#awscliv2-index) /
[Awscliv2](./index.md#awscliv2) /
Api

> Auto-generated documentation for [awscliv2.api](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py) module.

## AWSAPI

[Show source in api.py:18](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L18)

API for all AWS CLI v2 commands.

Supports installed and dockerized AWS CLI v2.

#### Arguments

- `encoding` - Input/output encoding, default utf-8.
- `output` - Output stream, default sys.stdout.

#### Signature

```python
class AWSAPI:
    def __init__(
        self, encoding: str = ENCODING, output: Optional[TextIO] = None
    ) -> None: ...
```

#### See also

- [ENCODING](./constants.md#encoding)

### AWSAPI().assume_role

[Show source in api.py:135](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L135)

Add assume role to credentials.

#### Signature

```python
def assume_role(self, profile_name: str, source_profile: str, role_arn: str) -> None: ...
```

### AWSAPI().execute

[Show source in api.py:79](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L79)

Execute AWS CLI v2 command.

#### Returns

Command output.

#### Signature

```python
def execute(self, args: Sequence[str]) -> str: ...
```

### AWSAPI.get_awscli_v2_cmd

[Show source in api.py:34](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L34)

Get command to run AWS CLI v2.

#### Signature

```python
@staticmethod
def get_awscli_v2_cmd() -> List[str]: ...
```

### AWSAPI().print_version

[Show source in api.py:126](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L126)

Print AWS CLI v2 version.

#### Returns

Process exit code.

#### Signature

```python
def print_version(self) -> int: ...
```

### AWSAPI().run_awscli_v2

[Show source in api.py:94](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L94)

Run AWS CLI.

#### Returns

Process exit code.

#### Signature

```python
def run_awscli_v2(self, args: Sequence[str]) -> int: ...
```

### AWSAPI().run_awscli_v2_detached

[Show source in api.py:110](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L110)

Run AWS CLI as a detached subprocess.

#### Returns

Process exit code.

#### Signature

```python
def run_awscli_v2_detached(self, args: Sequence[str]) -> int: ...
```

### AWSAPI().set_credentials

[Show source in api.py:171](https://github.com/youtype/awscliv2/blob/main/awscliv2/api.py#L171)

Add or update credentials in `~/.aws/credentials`.

#### Signature

```python
def set_credentials(
    self,
    profile_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_session_token: str = "",
    region: str = "",
) -> None: ...
```