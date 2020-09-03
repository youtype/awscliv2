"""
Main entrypoint for CLI.
"""
import json
import sys
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import Optional, Sequence, TextIO

from awscliv2.cli_parser import parse_args
from awscliv2.constants import DOCKER_PATH, IMAGE_NAME
from awscliv2.exceptions import AWSCLIError, ExecutableNotFoundError, SubprocessError
from awscliv2.interactive_process import InteractiveProcess
from awscliv2.logger import get_logger


def run_subprocess(cmd: Sequence[str], stdout: TextIO = sys.stdout) -> None:
    """
    Run interactive subprocess.
    """
    process = InteractiveProcess(cmd)
    try:
        returncode = process.run(stdout=stdout)
    except SubprocessError as e:
        raise AWSCLIError(str(e))

    if returncode:
        raise AWSCLIError(returncode=returncode)


def run_awscli_v2(args: Sequence[str], stdout: TextIO = sys.stdout) -> None:
    """
    Run dockerized AWS CLI.
    """
    try:
        run_subprocess(
            [
                DOCKER_PATH,
                "run",
                "-i",
                "--rm",
                "-v",
                f"{Path.home().as_posix()}/.aws:/root/.aws",
                "-v",
                f"{Path.cwd().as_posix()}:/aws",
                IMAGE_NAME,
                *args,
            ],
            stdout=stdout,
        )
    except ExecutableNotFoundError:
        raise AWSCLIError("Docker not found: https://docs.docker.com/get-docker/")


def run_assume_role(profile_name: str, source_profile: str, role_arn: str) -> None:
    aws_path = Path.home() / ".aws"
    if not aws_path.exists():
        aws_path.mkdir(parents=True, exist_ok=True)
    credentials_path = aws_path / "credentials"
    if not credentials_path.exists():
        credentials_path.write_text("")

    stdout = StringIO()
    run_awscli_v2(
        [
            "--profile",
            source_profile,
            "sts",
            "assume-role",
            "--role-arn",
            role_arn,
            "--role-session-name",
            f"{profile_name}-{source_profile}",
        ],
        stdout=stdout,
    )
    credentials_json = stdout.getvalue()
    credentials_data = json.loads(credentials_json)
    set_credentials(
        profile_name=profile_name,
        aws_access_key_id=credentials_data["Credentials"]["AccessKeyId"],
        aws_secret_access_key=credentials_data["Credentials"]["SecretAccessKey"],
        aws_session_token=credentials_data["Credentials"]["SessionToken"],
    )


def set_credentials(
    profile_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_session_token: Optional[str] = None,
):
    """
    Add or update credentials in `~/.aws/credentials`
    """
    aws_path = Path.home() / ".aws"
    if not aws_path.exists():
        aws_path.mkdir(parents=True, exist_ok=True)
    credentials_path = aws_path / "credentials"
    if not credentials_path.exists():
        credentials_path.write_text("")

    config = ConfigParser()
    config.read(credentials_path)
    credentials = {
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
    }
    if aws_session_token:
        credentials["aws_session_token"] = aws_session_token

    config[profile_name] = credentials

    output = StringIO()
    config.write(output)
    credentials_path.write_text(output.getvalue())
    get_logger().info(f"Successfully added {profile_name} profile to {credentials_path.as_posix()}")


def main(args: Sequence[str]) -> None:
    """
    Main program entrypoint.
    """
    namespace = parse_args(args)

    if namespace.update:
        try:
            run_subprocess([DOCKER_PATH, "pull", IMAGE_NAME])
        except FileNotFoundError:
            raise AWSCLIError("Docker not found: https://docs.docker.com/get-docker/")
        sys.exit(0)

    if namespace.version:
        version_path = Path(__file__).parent / "version.txt"
        version = version_path.read_text().strip() if version_path.exists() else "0.0.0"
        print(version)
        run_awscli_v2(["--version"])
        sys.exit(0)

    if namespace.assume_role:
        try:
            return run_assume_role(*namespace.assume_role[:3])
        except TypeError:
            raise AWSCLIError("Use --assume-role <name> <source_profile> <role_arn>")

    if namespace.configure:
        try:
            return set_credentials(*namespace.configure[:4])
        except TypeError:
            raise AWSCLIError(
                "Use --configure <profile_name> <access_key> <secret_key> [<session_token>]"
            )

    if not namespace.other:
        raise AWSCLIError("No command provided")

    run_awscli_v2(namespace.other)


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
