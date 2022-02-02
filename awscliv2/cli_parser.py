"""
Parse CLI arguments.
"""
import argparse
from typing import Sequence

import pkg_resources

from awscliv2.constants import ENCODING, PACKAGE_NAME, PROG_NAME


def get_version() -> str:
    """
    Get awscliv2 package version.

    Returns:
        Version as a string.
    """
    try:
        return pkg_resources.get_distribution(PACKAGE_NAME).version
    except pkg_resources.DistributionNotFound:
        return "0.0.0"


class CLINamespace:
    """
    Main CLI Namespace.
    """

    def __init__(
        self,
        configure: Sequence[str],
        assume_role: Sequence[str],
        encoding: str,
        install: bool,
        update: bool,
        version: bool,
        other: Sequence[str],
    ) -> None:
        self.configure = configure
        self.assume_role = assume_role
        self.encoding = encoding
        self.install = install
        self.update = update
        self.version = version
        self.other = other


def parse_args(args: Sequence[str]) -> CLINamespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(PROG_NAME, description="Can be used as a regular AWS CLI v2")
    parser.add_argument(
        "--configure", nargs="+", help="Configure profile: <name> <access_key> <secret_key>"
    )
    parser.add_argument(
        "--assume-role",
        nargs="+",
        help="Configure assume role profile: <name> <source_profile> <role_arn>",
    )
    parser.add_argument("-V", "--version", action="store_true", help="Show version")
    parser.add_argument(
        "-U", "--update", action="store_true", help="Install AWS CLI v2 (deprecated)"
    )
    parser.add_argument("-i", "--install", action="store_true", help="Install AWS CLI v2")
    parser.add_argument("--encoding", help="File and stream encoding", default=ENCODING)
    namespace, other = parser.parse_known_args(args)
    namespace.other = other
    return CLINamespace(
        configure=namespace.configure,
        assume_role=namespace.assume_role,
        encoding=namespace.encoding,
        install=namespace.install,
        update=namespace.update,
        version=namespace.version,
        other=namespace.other,
    )
