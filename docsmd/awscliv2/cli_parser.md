# Cli Parser

[Awscliv2 Index](../README.md#awscliv2-index) /
[Awscliv2](./index.md#awscliv2) /
Cli Parser

> Auto-generated documentation for [awscliv2.cli_parser](https://github.com/youtype/awscliv2/blob/main/awscliv2/cli_parser.py) module.

## CLINamespace

[Show source in cli_parser.py:25](https://github.com/youtype/awscliv2/blob/main/awscliv2/cli_parser.py#L25)

Main CLI Namespace.

#### Signature

```python
class CLINamespace:
    def __init__(
        self,
        configure: Sequence[str],
        assume_role: Sequence[str],
        encoding: str,
        install: bool,
        update: bool,
        version: bool,
        other: Sequence[str],
    ) -> None:
        ...
```



## get_version

[Show source in cli_parser.py:12](https://github.com/youtype/awscliv2/blob/main/awscliv2/cli_parser.py#L12)

Get awscliv2 package version.

#### Returns

Version as a string.

#### Signature

```python
def get_version() -> str:
    ...
```



## parse_args

[Show source in cli_parser.py:49](https://github.com/youtype/awscliv2/blob/main/awscliv2/cli_parser.py#L49)

Parse CLI arguments.

#### Signature

```python
def parse_args(args: Sequence[str]) -> CLINamespace:
    ...
```

#### See also

- [CLINamespace](#clinamespace)



