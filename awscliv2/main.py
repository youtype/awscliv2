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
    version_path = Path(__file__).parent / "version.txt"
    version = version_path.read_text() if version_path.exists() else "0.0.0"

    parser = argparse.ArgumentParser("aws", description="Can be used as a regular AWS CLI v2")
    parser.add_argument(
        "--configure", nargs="+", help="Configure a new profile <name> <key> <secret> <region>"
    )
    parser.add_argument("-V", action="version", version=version, help="Show version")
    namespace, other = parser.parse_known_args(args)
    namespace.other = other
    return namespace


def run_awscli_v2(args: Sequence[str]) -> None:
    """
    Run dockerized AWS CLI.
    """
    cmd = (
        f"docker run --rm -it -v {Path.home().as_posix()}/.aws:/root/.aws"
        f" -v {Path.cwd().as_posix()}:/aws amazon/aws-cli"
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
    if namespace.configure:
        try:
            profile_name, key, secret, region = namespace.configure[:4]
        except ValueError:
            raise AWSCLIError(
                "Use --configure <profile_name> <access_key> <secret_key> <profile_name>"
            )

        aws_path = Path.home() / ".aws"
        aws_path.mkdir(exist_ok=True)
        creds_path = aws_path / "creds.csv"
        creds_path.write_text(
            "User Name,Access Key ID,Secret Access key\n" f"{profile_name},{key},{secret}\n"
        )
        run_awscli_v2(["configure", "import", "--csv", "file:///root/.aws/creds.csv"])
        run_awscli_v2(["configure", "set", "region", region])
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
