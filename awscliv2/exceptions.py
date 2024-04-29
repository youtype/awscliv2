"""
All exceptions for programmatical usage.
"""


class AWSCLIError(BaseException):
    """
    Main error for awscliv2.
    """

    def __init__(self, msg: str = "", returncode: int = 1) -> None:
        super().__init__()
        self.msg = msg
        self.returncode = returncode

    def __str__(self) -> str:
        """
        Represent as a string.
        """
        return self.msg


class InstallError(AWSCLIError):
    """
    AWS CLi v2 installer error.
    """


class SubprocessError(BaseException):
    """
    Subprocess interrupted error.
    """


class ExecutableNotFoundError(BaseException):
    """
    Subprocess cannot find an executable error.
    """
