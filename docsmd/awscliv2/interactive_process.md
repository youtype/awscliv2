# InteractiveProcess

[Awscliv2 Index](../README.md#awscliv2-index) / [Awscliv2](./index.md#awscliv2) / InteractiveProcess

> Auto-generated documentation for [awscliv2.interactive_process](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py) module.

## InteractiveProcess

[Show source in interactive_process.py:20](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py#L20)

Wrapper for subrocess.Popen with interactive input support.

#### Signature

```python
class InteractiveProcess:
    def __init__(self, command: Sequence[str], encoding: str = ENCODING) -> None: ...
```

#### See also

- [ENCODING](./constants.md#encoding)

### InteractiveProcess().get_command

[Show source in interactive_process.py:38](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py#L38)

Get command as a string.

#### Signature

```python
def get_command(self) -> str: ...
```

### InteractiveProcess().readall

[Show source in interactive_process.py:97](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py#L97)

Write input from `stdin` stream to `process`.

#### Arguments

- `process` - Popen process
- `inputs` - Streams to read

#### Signature

```python
def readall(self, process: Popen, inputs: ignore) -> None: ...
```

### InteractiveProcess().run

[Show source in interactive_process.py:124](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py#L124)

Run interactive process with input from `stdin` and output to `stdout`.

#### Arguments

- `inputs` - Input text streams
- `stdout` - Process stdout text stream

#### Raises

- `ExecutableNotFoundError` - Process executable not found
- `SubprocessError` - Process error

#### Returns

Process status code

#### Signature

```python
def run(self, inputs: Sequence[TInput] = (), stdout: TextIO = default_stdout) -> int: ...
```

#### See also

- [TInput](#tinput)

### InteractiveProcess().writeall

[Show source in interactive_process.py:44](https://github.com/youtype/awscliv2/blob/main/awscliv2/interactive_process.py#L44)

Read output from `process` to `stdout` stream.

#### Arguments

- `process` - Popen process
- `stdout` - Stream to write

#### Signature

```python
def writeall(self, process: Popen, stdout: ignore) -> None: ...
```
