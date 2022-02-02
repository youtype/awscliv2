# Installers

> Auto-generated documentation for [awscliv2.installers](blob/main/awscliv2/installers.py) module.

AWS CLI v2 installers.

- [Awscliv2](../README.md#aws-cli-v2-for-python-) / [Modules](../MODULES.md#awscliv2-modules) / [Awscliv2](index.md#awscliv2) / Installers
    - [download_file](#download_file)
    - [install_linux](#install_linux)
    - [install_linux_arm](#install_linux_arm)
    - [install_linux_x86_64](#install_linux_x86_64)
    - [install_macos](#install_macos)
    - [install_multiplatform](#install_multiplatform)

## download_file

[[find in source code]](blob/main/awscliv2/installers.py#L19)

```python
def download_file(url: str, target: Path) -> None:
```

Download file from `url` to `target` path.

## install_linux

[[find in source code]](blob/main/awscliv2/installers.py#L72)

```python
def install_linux(url: str) -> None:
```

Install AWS CLI v2 for Linux from `url`.

## install_linux_arm

[[find in source code]](blob/main/awscliv2/installers.py#L65)

```python
def install_linux_arm() -> None:
```

Install AWS CLI v2 for Linux ARM.

## install_linux_x86_64

[[find in source code]](blob/main/awscliv2/installers.py#L58)

```python
def install_linux_x86_64() -> None:
```

Install AWS CLI v2 for Linux x86_64.

## install_macos

[[find in source code]](blob/main/awscliv2/installers.py#L28)

```python
def install_macos() -> None:
```

Install AWS CLI v2 for MacOS.

## install_multiplatform

[[find in source code]](blob/main/awscliv2/installers.py#L114)

```python
def install_multiplatform() -> None:
```

Install AWS CLI v2 for Linux ar MacOS.
