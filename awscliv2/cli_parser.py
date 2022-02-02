"""
Parse CLI arguments.
"""
import argparse
from typing import Sequence

import pkg_resources

from awscliv2.constants import PACKAGE_NAME, PROG_NAME


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


def parse_args(args: Sequence[str]) -> argparse.Namespace:
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
    namespace, other = parser.parse_known_args(args)
    namespace.other = other
    return namespace
