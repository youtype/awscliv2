"""
Main entrypoint for CLI.
"""
import sys
from typing import Sequence

from awscliv2.awscli_runner import AWSCLIRunner
from awscliv2.cli_parser import get_version, parse_args
from awscliv2.exceptions import AWSCLIError
from awscliv2.installers import install_multiplatform
from awscliv2.logger import get_logger


def main(args: Sequence[str]) -> None:
    """
    Main program entrypoint.
    """
    namespace = parse_args(args)
    runner = AWSCLIRunner(encoding=namespace.encoding)

    if namespace.install or namespace.update:
        install_multiplatform()
        runner.print_version()
        sys.exit(0)

    if namespace.version:
        version = get_version()
        print(version)
        cmd = " ".join(runner.get_awscli_v2_cmd())
        print(f"AWS CLI v2 command: {cmd}")
        runner.print_version()
        sys.exit(0)

    if namespace.assume_role:
        try:
            return runner.run_assume_role(*namespace.assume_role[:3])
        except TypeError:
            raise AWSCLIError("Use --assume-role <name> <source_profile> <role_arn>") from None

    if namespace.configure:
        try:
            return runner.set_credentials(*namespace.configure[:4])
        except TypeError:
            raise AWSCLIError(
                "Use --configure <profile_name> <access_key> <secret_key> [<session_token>]"
            ) from None

    if not namespace.other:
        raise AWSCLIError("No command provided")

    sys.exit(runner.run_awscli_v2_detached(namespace.other))


def main_cli() -> None:
    """
    Main entrypoint for CLI.
    """
    try:
        main(sys.argv[1:])
    except AWSCLIError as e:
        message = str(e)
        if message:
            logger = get_logger()
            logger.error(message)
        sys.exit(e.returncode)
