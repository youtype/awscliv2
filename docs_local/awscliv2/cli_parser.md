# Cli Parser

> Auto-generated documentation for [awscliv2.cli_parser](blob/main/awscliv2/cli_parser.py) module.

Parse CLI arguments.

- [Awscliv2](../README.md#aws-cli-v2-for-python-) / [Modules](../MODULES.md#awscliv2-modules) / [Awscliv2](index.md#awscliv2) / Cli Parser
    - [CLINamespace](#clinamespace)
    - [get_version](#get_version)
    - [parse_args](#parse_args)

## CLINamespace

[[find in source code]](blob/main/awscliv2/cli_parser.py#L25)

```python
class CLINamespace():
    def __init__(
        configure: Sequence[str],
        assume_role: Sequence[str],
        encoding: str,
        install: bool,
        update: bool,
        version: bool,
        other: Sequence[str],
    ) -> None:
```

Main CLI Namespace.

## get_version

[[find in source code]](blob/main/awscliv2/cli_parser.py#L12)

```python
def get_version() -> str:
```

Get awscliv2 package version.

#### Returns

Version as a string.

## parse_args

[[find in source code]](blob/main/awscliv2/cli_parser.py#L49)

```python
def parse_args(args: Sequence[str]) -> CLINamespace:
```

Parse CLI arguments.

#### See also

- [CLINamespace](#clinamespace)
