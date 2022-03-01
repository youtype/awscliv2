"""
Runner for all AWS CLI v2 commands.
"""
import json
import sys
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import List, Optional, Sequence, TextIO

import executor  # type: ignore

from awscliv2.constants import DOCKER_PATH, IMAGE_NAME
from awscliv2.exceptions import AWSCLIError, ExecutableNotFoundError, SubprocessError
from awscliv2.interactive_process import InteractiveProcess
from awscliv2.logger import get_logger


class AWSCLIRunner:
    """
    Runner for all AWS CLI v2 commands.

    Supports installed and dockerized AWS CLI v2.
    """

    def __init__(self, encoding: str) -> None:
        self.encoding = encoding
        self.logger = get_logger()

    @staticmethod
    def get_awscli_v2_cmd() -> List[str]:
        """
        Get command to run AWS CLI v2.
        """
        local_paths = [
            Path.home() / ".awscliv2" / "binaries" / "aws",
            Path.home() / "aws-cli" / "aws",
        ]
        for local_path in local_paths:
            if local_path.exists():
                return [local_path.as_posix()]

        return [
            DOCKER_PATH,
            "run",
            "-i",
            "--rm",
            "-v",
            f"{Path.home().as_posix()}/.aws:/root/.aws",
            "-v",
            f"{Path.cwd().as_posix()}:/aws",
            IMAGE_NAME,
        ]

    def _run_subprocess(self, cmd: Sequence[str], stdout: TextIO = sys.stdout) -> int:
        process = InteractiveProcess(cmd, encoding=self.encoding)
        try:
            return_code = process.run(stdout=stdout)
        except SubprocessError as e:
            raise AWSCLIError(str(e)) from e

        return return_code

    def _run_detached_subprocess(self, cmd: Sequence[str]) -> int:
        try:
            executor.execute(*cmd, encoding=self.encoding)
        except executor.ExternalCommandFailed as e:
            self.logger.error(f"Command failed with code {e.returncode}")
            return e.returncode

        return 0

    def run_awscli_v2(self, args: Sequence[str], stdout: TextIO = sys.stdout) -> int:
        """
        Run AWS CLI.
        """
        cmd = [
            *self.get_awscli_v2_cmd(),
            *args,
        ]
        try:
            return self._run_subprocess(cmd, stdout=stdout)
        except ExecutableNotFoundError as e:
            raise AWSCLIError(f"Executable not found: {cmd[0]}") from e

    def run_awscli_v2_detached(self, args: Sequence[str]) -> int:
        """
        Run AWS CLI as a detached subprocess.
        """
        cmd = [
            *self.get_awscli_v2_cmd(),
            *args,
        ]
        try:
            return self._run_detached_subprocess(cmd)
        except ExecutableNotFoundError as e:
            raise AWSCLIError(f"Executable not found: {cmd[0]}") from e

    def print_version(self) -> int:
        """
        Print AWS CLI v2 version.

        Returns:
            Process exit code.
        """
        return self.run_awscli_v2(["--version"])

    def run_assume_role(self, profile_name: str, source_profile: str, role_arn: str) -> None:
        """
        Add assume role to credentials.
        """
        aws_path = Path.home() / ".aws"
        if not aws_path.exists():
            aws_path.mkdir(parents=True, exist_ok=True)
        credentials_path = aws_path / "credentials"
        if not credentials_path.exists():
            credentials_path.write_text("", encoding=self.encoding)

        stdout = StringIO()
        return_code = self.run_awscli_v2(
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
        if return_code:
            raise AWSCLIError(stdout.getvalue().strip())

        credentials_json = stdout.getvalue()
        credentials_data = json.loads(credentials_json)
        self.set_credentials(
            profile_name=profile_name,
            aws_access_key_id=credentials_data["Credentials"]["AccessKeyId"],
            aws_secret_access_key=credentials_data["Credentials"]["SecretAccessKey"],
            aws_session_token=credentials_data["Credentials"]["SessionToken"],
        )

    def set_credentials(
        self,
        profile_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_session_token: Optional[str] = None,
    ) -> None:
        """
        Add or update credentials in `~/.aws/credentials`
        """
        aws_path = Path.home() / ".aws"
        if not aws_path.exists():
            aws_path.mkdir(parents=True, exist_ok=True)
        credentials_path = aws_path / "credentials"
        if not credentials_path.exists():
            credentials_path.write_text("", encoding=self.encoding)

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
        credentials_path.write_text(output.getvalue(), encoding=self.encoding)
        self.logger.info(
            f"Successfully added {profile_name} profile to {credentials_path.as_posix()}"
        )
