"""
Main entrypoint for CLI.
"""
import argparse
import logging
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Sequence


IMAGE_NAME = "amazon/aws-cli"


class AWSCLIError(BaseException):
    """
    Main error for awscliv2.
    """

    def __init__(self, msg: str = "", returncode: int = 1) -> None:
        self.msg = msg
        self.returncode = returncode

    def __str__(self) -> str:
        return self.msg


def parse_args(args: Sequence[str]) -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser("aws", description="Can be used as a regular AWS CLI v2")
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


def run_awscli_v2(args: Sequence[str]) -> None:
    """
    Run dockerized AWS CLI.
    """
    # raise ValueError(args)
    cmd = (
        f"docker run --rm -it -v {Path.home().as_posix()}/.aws:/root/.aws"
        f" -v {Path.cwd().as_posix()}:/aws {IMAGE_NAME}"
    )
    try:
        subprocess.check_call([*shlex.split(cmd), *args])
    except subprocess.CalledProcessError as e:
        raise AWSCLIError(returncode=e.returncode)
    except FileNotFoundError:
        raise AWSCLIError("Docker not found: https://docs.docker.com/get-docker/")


def main(args: Sequence[str]) -> None:
    """
    Main program entrypoint.
    """
    namespace = parse_args(args)

    if namespace.update:
        try:
            subprocess.check_call(["docker", "pull", IMAGE_NAME])
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
