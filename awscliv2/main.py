"""
Main entrypoint for CLI.
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence

from awscliv2.exceptions import AWSCLIError, ExecutableNotFoundError, SubprocessError
from awscliv2.interactive_process import InteractiveProcess

IMAGE_NAME = "amazon/aws-cli"
DOCKER_PATH = "docker"


def parse_args(args: Sequence[str]) -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser("awsv2", description="Can be used as a regular AWS CLI v2")
    parser.add_argument(
        "--configure", nargs="+", help="Configure profile: <name> <access_key> <secret_key>"
    )
    parser.add_argument("-V", "--version", action="store_true", help="Show version")
    parser.add_argument(
        "-U", "--update", action="store_true", help=f"Pull latest {IMAGE_NAME} docker image"
    )
    namespace, other = parser.parse_known_args(args)
    namespace.other = other
    return namespace


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

    if namespace.configure:
        try:
            profile_name, key, secret = namespace.configure[:3]
        except ValueError:
            raise AWSCLIError("Use --configure <profile_name> <access_key> <secret_key>")

        aws_path = Path.home() / ".aws"
        aws_path.mkdir(exist_ok=True)
        creds_path = aws_path / "creds.csv"
        creds_path.write_text(
            "User Name,Access Key ID,Secret Access key\n" f"{profile_name},{key},{secret}\n"
        )
        run_awscli_v2(["configure", "import", "--csv", "file:///root/.aws/creds.csv"])
        creds_path.unlink()
        return

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
            logging.error(message)
        sys.exit(e.returncode)
