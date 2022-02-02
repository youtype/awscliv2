# Exceptions

> Auto-generated documentation for [awscliv2.exceptions](https://github.com/vemel/awscliv2/blob/main/awscliv2/exceptions.py) module.

All exceptions for programmatical usage.

- [Awscliv2](../README.md#aws-cli-v2-for-python-) / [Modules](../MODULES.md#awscliv2-modules) / [Awscliv2](index.md#awscliv2) / Exceptions
    - [AWSCLIError](#awsclierror)
    - [ExecutableNotFoundError](#executablenotfounderror)
    - [InstallError](#installerror)
    - [SubprocessError](#subprocesserror)

## AWSCLIError

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/exceptions.py#L6)

```python
class AWSCLIError(BaseException):
    def __init__(msg: str = '', returncode: int = 1) -> None:
```

Main error for awscliv2.

## ExecutableNotFoundError

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/exceptions.py#L31)

```python
class ExecutableNotFoundError(BaseException):
```

Subprocess cannot find an executable error.

## InstallError

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/exceptions.py#L19)

```python
class InstallError(AWSCLIError):
```

AWS CLi v2 installer error.

#### See also

- [AWSCLIError](#awsclierror)

## SubprocessError

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/exceptions.py#L25)

```python
class SubprocessError(BaseException):
```

Subprocess interrupted error.
