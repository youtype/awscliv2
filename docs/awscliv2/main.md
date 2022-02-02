# Main

> Auto-generated documentation for [awscliv2.main](https://github.com/vemel/awscliv2/blob/main/awscliv2/main.py) module.

Main entrypoint for CLI.

- [Awscliv2](../README.md#aws-cli-v2-for-python-) / [Modules](../MODULES.md#awscliv2-modules) / [Awscliv2](index.md#awscliv2) / Main
    - [get_awscli_v2_cmd](#get_awscli_v2_cmd)
    - [main](#main)
    - [main_cli](#main_cli)
    - [run_assume_role](#run_assume_role)
    - [run_awscli_v2](#run_awscli_v2)
    - [run_subprocess](#run_subprocess)
    - [set_credentials](#set_credentials)

## get_awscli_v2_cmd

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/main.py#L32)

```python
def get_awscli_v2_cmd() -> List[str]:
```

## main

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/main.py#L136)

```python
def main(args: Sequence[str]) -> None:
```

Main program entrypoint.

## main_cli

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/main.py#L178)

```python
def main_cli() -> None:
```

Main entrypoint for CLI.

## run_assume_role

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/main.py#L68)

```python
def run_assume_role(
    profile_name: str,
    source_profile: str,
    role_arn: str,
) -> None:
```

## run_awscli_v2

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/main.py#L54)

```python
def run_awscli_v2(args: Sequence[str], stdout: TextIO = sys.stdout) -> int:
```

Run dockerized AWS CLI.

## run_subprocess

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/main.py#L19)

```python
def run_subprocess(cmd: Sequence[str], stdout: TextIO = sys.stdout) -> int:
```

Run interactive subprocess.

## set_credentials

[[find in source code]](https://github.com/vemel/awscliv2/blob/main/awscliv2/main.py#L103)

```python
def set_credentials(
    profile_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_session_token: Optional[str] = None,
) -> None:
```

Add or update credentials in `~/.aws/credentials`
