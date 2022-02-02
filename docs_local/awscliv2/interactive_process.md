# InteractiveProcess

> Auto-generated documentation for [awscliv2.interactive_process](blob/main/awscliv2/interactive_process.py) module.

Wrapper for subrocess.Popen with interactive input support.

- [Awscliv2](../README.md#aws-cli-v2-for-python-) / [Modules](../MODULES.md#awscliv2-modules) / [Awscliv2](index.md#awscliv2) / InteractiveProcess
    - [InteractiveProcess](#interactiveprocess)
        - [InteractiveProcess().readall](#interactiveprocessreadall)
        - [InteractiveProcess().run](#interactiveprocessrun)
        - [InteractiveProcess().writeall](#interactiveprocesswriteall)

## InteractiveProcess

[[find in source code]](blob/main/awscliv2/interactive_process.py#L14)

```python
class InteractiveProcess():
    def __init__(command: Sequence[str]) -> None:
```

Wrapper for subrocess.Popen with interactive input support.

### InteractiveProcess().readall

[[find in source code]](blob/main/awscliv2/interactive_process.py#L36)

```python
def readall(process: Popen[bytes], stdin: TextIO) -> None:
```

### InteractiveProcess().run

[[find in source code]](blob/main/awscliv2/interactive_process.py#L52)

```python
def run(
    stdin: TextIO = default_stdin,
    stdout: TextIO = default_stdout,
) -> int:
```

### InteractiveProcess().writeall

[[find in source code]](blob/main/awscliv2/interactive_process.py#L27)

```python
def writeall(process: Popen[bytes], stdout: TextIO) -> None:
```
