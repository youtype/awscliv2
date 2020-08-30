import argparse
from typing import Sequence


from awscliv2.constants import IMAGE_NAME


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