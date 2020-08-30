class AWSCLIError(BaseException):
    """
    Main error for awscliv2.
    """

    def __init__(self, msg: str = "", returncode: int = 1) -> None:
        self.msg = msg
        self.returncode = returncode

    def __str__(self) -> str:
        return self.msg


class SubprocessError(BaseException):
    pass


class ExecutableNotFoundError(BaseException):
    pass
