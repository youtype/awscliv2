"""
Main entrypoint for CLI.
"""

import sys
from typing import Sequence

from awscliv2.api import AWSAPI
from awscliv2.cli_parser import get_version, parse_args
from awscliv2.exceptions import AWSCLIError
from awscliv2.installers import install_multiplatform
from awscliv2.logger import get_logger


def main(args: Sequence[str]) -> int:
    """
    Entrypoint for API.
    """
    namespace = parse_args(args)
    runner = AWSAPI(encoding=namespace.encoding, output=sys.stdout)

    if namespace.install or namespace.update:
        install_multiplatform()
        runner.print_version()
        return 0

    if namespace.version:
        version = get_version()
        sys.stdout.write(f"{version}\n")
        cmd = " ".join(runner.get_awscli_v2_cmd())
        sys.stdout.write(f"AWS CLI v2 command: {cmd}\n")
        runner.print_version()
        return 0

    if namespace.assume_role:
        try:
            runner.assume_role(*namespace.assume_role[:3])
        except TypeError:
            raise AWSCLIError("Use --assume-role <name> <source_profile> <role_arn>") from None
        return 0

    if namespace.configure:
        try:
            runner.set_credentials(*namespace.configure[:5])
        except TypeError:
            raise AWSCLIError(
                "Use --configure <profile_name> <access_key>"
                " <secret_key> [<session_token>] [<region>]"
            ) from None
        return 0

    if not namespace.other:
        raise AWSCLIError("No command provided")

    return runner.run_awscli_v2_detached(namespace.other)


def main_cli() -> None:
    """
    Entrypoint for CLI.
    """
    try:
        sys.exit(main(sys.argv[1:]))
    except AWSCLIError as e:
        message = str(e)
        if message:
            logger = get_logger()
            logger.exception(message)
        sys.exit(e.returncode)
