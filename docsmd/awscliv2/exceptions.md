# Exceptions

[Awscliv2 Index](../README.md#awscliv2-index) / [Awscliv2](./index.md#awscliv2) / Exceptions

> Auto-generated documentation for [awscliv2.exceptions](https://github.com/youtype/awscliv2/blob/main/awscliv2/exceptions.py) module.

## AWSCLIError

[Show source in exceptions.py:6](https://github.com/youtype/awscliv2/blob/main/awscliv2/exceptions.py#L6)

Main error for awscliv2.

#### Signature

```python
class AWSCLIError(BaseException):
    def __init__(self, msg: str = "", returncode: int = 1) -> None: ...
```

### AWSCLIError().__str__

[Show source in exceptions.py:16](https://github.com/youtype/awscliv2/blob/main/awscliv2/exceptions.py#L16)

Represent as a string.

#### Signature

```python
def __str__(self) -> str: ...
```



## ExecutableNotFoundError

[Show source in exceptions.py:35](https://github.com/youtype/awscliv2/blob/main/awscliv2/exceptions.py#L35)

Subprocess cannot find an executable error.

#### Signature

```python
class ExecutableNotFoundError(BaseException): ...
```



## InstallError

[Show source in exceptions.py:23](https://github.com/youtype/awscliv2/blob/main/awscliv2/exceptions.py#L23)

AWS CLi v2 installer error.

#### Signature

```python
class InstallError(AWSCLIError): ...
```

#### See also

- [AWSCLIError](#awsclierror)



## SubprocessError

[Show source in exceptions.py:29](https://github.com/youtype/awscliv2/blob/main/awscliv2/exceptions.py#L29)

Subprocess interrupted error.

#### Signature

```python
class SubprocessError(BaseException): ...
```
