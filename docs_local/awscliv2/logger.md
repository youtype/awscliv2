# Logger

> Auto-generated documentation for [awscliv2.logger](blob/main/awscliv2/logger.py) module.

Logging utils

- [Awscliv2](../README.md#aws-cli-v2-for-python-) / [Modules](../MODULES.md#awscliv2-modules) / [Awscliv2](index.md#awscliv2) / Logger
    - [get_logger](#get_logger)

## get_logger

[[find in source code]](blob/main/awscliv2/logger.py#L9)

```python
def get_logger(level: int = logging.DEBUG) -> logging.Logger:
```

Get default logger.

#### Arguments

- `level` - Python log level

#### Returns

New or existing logger instance.
