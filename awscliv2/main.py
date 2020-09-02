"""
Main entrypoint for CLI.
"""
import sys
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import Sequence

from awscliv2.cli_parser import parse_args
from awscliv2.constants import DOCKER_PATH, IMAGE_NAME
from awscliv2.exceptions import AWSCLIError, ExecutableNotFoundError, SubprocessError
from awscliv2.interactive_process import InteractiveProcess
from awscliv2.logger import get_logger


def run_subprocess(cmd: Sequence[str]) -> None:
    """
    Run interactive subprocess.
    """
    process = InteractiveProcess(cmd)
    try:
        returncode = process.run()
    except SubprocessError as e:
        raise AWSCLIError(str(e))

    if returncode:
        raise AWSCLIError(returncode=returncode)


def run_awscli_v2(args: Sequence[str]) -> None:
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
            ]
        )
    except ExecutableNotFoundError:
        raise AWSCLIError("Docker not found: https://docs.docker.com/get-docker/")


def run_assume_role(profile_name: str, source_profile: str, role_arn: str) -> None:
    aws_path = Path.home() / ".aws"
    config_path = aws_path / "config"
    config = ConfigParser()
    if not config_path.exists():
        config_path.write_text("")

    config.read(config_path)

    section_name = f"profile {profile_name}"
    config[section_name] = {"role_arn": role_arn, "source_profile": source_profile}
    output = StringIO()
    config.write(output)
    config_path.write_text(output.getvalue())
    get_logger().info(f"Successfully added {profile_name} to {config_path.as_posix()}")


def run_configure(profile_name: str, key: str, secret: str) -> None:
    aws_path = Path.home() / ".aws"
    credentials_path = aws_path / "credentials"
    if not credentials_path.exists():
        credentials_path.write_text("")

    aws_path.mkdir(exist_ok=True)
    creds_path = aws_path / "creds.csv"
    creds_path.write_text(
        "User Name,Access Key ID,Secret Access key\n" f"{profile_name},{key},{secret}\n"
    )
    run_awscli_v2(["configure", "import", "--csv", "file:///root/.aws/creds.csv"])
    creds_path.unlink()
    get_logger().info(f"Successfully added {profile_name} to {credentials_path.as_posix()}")


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
            profile_name, source_profile, role_arn = namespace.assume_role[:3]
        except ValueError:
            raise AWSCLIError("Use --assume-role <profile_name> <access_key> <secret_key>")

        return run_assume_role(profile_name, source_profile, role_arn)

    if namespace.configure:
        try:
            profile_name, key, secret = namespace.configure[:3]
        except ValueError:
            raise AWSCLIError("Use --configure <profile_name> <access_key> <secret_key>")

        return run_configure(profile_name, key, secret)

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
