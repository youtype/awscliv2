# InteractiveProcess

[Awscliv2 Index](../README.md#awscliv2-index) /
[Awscliv2](./index.md#awscliv2) /
InteractiveProcess

> Auto-generated documentation for [awscliv2.interactive_process](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py) module.

## InteractiveProcess

[Show source in interactive_process.py:15](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py#L15)

Wrapper for subrocess.Popen with interactive input support.

#### Signature

```python
class InteractiveProcess:
    def __init__(self, command: Sequence[str], encoding: str = ENCODING) -> None: ...
```

#### See also

- [ENCODING](./constants.md#encoding)

### InteractiveProcess().readall

[Show source in interactive_process.py:53](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py#L53)

Write input from `stdin` stream to `process`.

#### Arguments

- `process` - Popen process
- `stdin` - Stream to read

#### Signature

```python
def readall(self, process: Popen, stdin: ignore) -> None: ...
```

### InteractiveProcess().run

[Show source in interactive_process.py:76](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py#L76)

Run interactive process with input from `stdin` and output to `stdout`.

#### Arguments

- `stdin` - Process stdin text stream
- `stdout` - Process stdout text stream

#### Raises

- `ExecutableNotFoundError` - Process executable not found
- `SubprocessError` - Process error

#### Returns

Process status code

#### Signature

```python
def run(self, stdin: TextIO = default_stdin, stdout: TextIO = default_stdout) -> int: ...
```

### InteractiveProcess().writeall

[Show source in interactive_process.py:29](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py#L29)

Read output from `process` to `stdout` stream.

#### Arguments

- `process` - Popen process
- `stdout` - Stream to write

#### Signature

```python
def writeall(self, process: Popen, stdout: ignore) -> None: ...
```
