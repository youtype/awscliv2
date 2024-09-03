"""
Runner for all AWS CLI v2 commands.
"""

import json
import shlex
import subprocess
import sys
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import List, Optional, Sequence, TextIO

from awscliv2.constants import DOCKER_PATH, ENCODING, IMAGE_NAME
from awscliv2.exceptions import AWSCLIError, ExecutableNotFoundError, SubprocessError
from awscliv2.interactive_process import InteractiveProcess
from awscliv2.logger import get_logger


class AWSAPI:
    """
    API for all AWS CLI v2 commands.

    Supports installed and dockerized AWS CLI v2.

    Arguments:
        encoding -- Input/output encoding, default utf-8.
        output -- Output stream, default sys.stdout.
    """

    def __init__(self, encoding: str = ENCODING, output: Optional[TextIO] = None) -> None:
        self.encoding = encoding
        self.output = output
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

    def _run_subprocess(self, cmd: Sequence[str]) -> int:
        process = InteractiveProcess(cmd, encoding=self.encoding)
        try:
            return_code = process.run(stdout=self.output or sys.stdout)
        except SubprocessError as e:
            raise AWSCLIError(str(e)) from e

        return return_code

    def _run_detached_subprocess(self, cmd: Sequence[str]) -> int:
        p = subprocess.Popen(cmd, encoding=self.encoding)
        return_code: Optional[int] = None
        while return_code is None:
            return_code = p.poll()

        if return_code:
            raise AWSCLIError(f"Command {shlex.join(cmd)} failed with code {return_code}")

        return return_code

    def execute(self, args: Sequence[str]) -> str:
        """
        Execute AWS CLI v2 command.

        Returns:
            Command output.
        """
        old_output = self.output
        self.output = StringIO()
        return_code = self.run_awscli_v2(args)
        if return_code:
            self.output.seek(0)
            raise AWSCLIError(
                f"Command {shlex.join(args)} failed with code {return_code}: {self.output.read()}"
            )
        self.output.seek(0)
        result = self.output.read()
        self.output = old_output
        return result

    def run_awscli_v2(self, args: Sequence[str]) -> int:
        """
        Run AWS CLI.

        Returns:
            Process exit code.
        """
        cmd = [
            *self.get_awscli_v2_cmd(),
            *args,
        ]
        try:
            return self._run_subprocess(cmd)
        except ExecutableNotFoundError as e:
            raise AWSCLIError(f"Executable not found: {cmd[0]}") from e

    def run_awscli_v2_detached(self, args: Sequence[str]) -> int:
        """
        Run AWS CLI as a detached subprocess.

        Returns:
            Process exit code.
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

    def assume_role(self, profile_name: str, source_profile: str, role_arn: str) -> None:
        """
        Add assume role to credentials.
        """
        aws_path = Path.home() / ".aws"
        if not aws_path.exists():
            aws_path.mkdir(parents=True, exist_ok=True)
        credentials_path = aws_path / "credentials"
        if not credentials_path.exists():
            credentials_path.write_text("", encoding=self.encoding)

        credentials_json = self.execute(
            (
                "--profile",
                source_profile,
                "sts",
                "assume-role",
                "--role-arn",
                role_arn,
                "--role-session-name",
                f"{profile_name}-{source_profile}",
            )
        )

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
        aws_session_token: str = "",
        region: str = "",
    ) -> None:
        """
        Add or update credentials in `~/.aws/credentials`.
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
        if region:
            credentials["region"] = region

        config[profile_name] = credentials

        output = StringIO()
        config.write(output)
        credentials_path.write_text(output.getvalue(), encoding=self.encoding)
        self.logger.info(
            f"Successfully added {profile_name} profile to {credentials_path.as_posix()}"
        )
