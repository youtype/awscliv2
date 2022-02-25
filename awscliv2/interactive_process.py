"""
Wrapper for subrocess.Popen with interactive input support.
"""
import select
import subprocess
import sys
import threading
from subprocess import Popen
from typing import Sequence, TextIO

from awscliv2.constants import ENCODING
from awscliv2.exceptions import ExecutableNotFoundError, SubprocessError


class InteractiveProcess:
    """
    Wrapper for subrocess.Popen with interactive input support.
    """

    read_timeout = 0.2
    default_stdout: TextIO = sys.stdout
    default_stdin: TextIO = sys.stdin

    def __init__(self, command: Sequence[str], encoding: str = ENCODING) -> None:
        self.command = list(command)
        self.finished = True
        self.encoding = encoding

    def writeall(self, process: Popen, stdout: TextIO) -> None:  # type: ignore
        """
        Read output from `process` to `stdout` stream.

        Arguments:
            process -- Popen process
            stdout -- Stream to write
        """
        assert process.stdout
        output = ""
        while True:
            if self.finished:
                break

            output_data = process.stdout.read(1)
            if not output_data:
                break
            output_data_dec = output_data.decode(self.encoding)
            if output.endswith("\n") and not output_data_dec.strip():
                continue
            output = f"{output[-10:]}{output_data_dec}"
            stdout.write(output_data_dec)
            stdout.flush()

    def readall(self, process: Popen, stdin: TextIO) -> None:  # type: ignore
        """
        Write input from `stdin` stream to `process`.

        Arguments:
            process -- Popen process
            stdin -- Stream to read
        """
        assert process.stdin
        while True:
            if self.finished:
                break

            rlist = select.select([stdin], [], [], self.read_timeout)[0]
            if not rlist:
                continue

            input_data = stdin.readline()
            if not input_data:
                break
            process.stdin.write(input_data.encode())
            process.stdin.flush()

    # pylint: disable=consider-using-with
    def run(self, stdin: TextIO = default_stdin, stdout: TextIO = default_stdout) -> int:
        self.finished = False
        try:
            process = Popen(
                self.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except FileNotFoundError as e:
            raise ExecutableNotFoundError(self.command[0]) from e

        writer = threading.Thread(target=self.writeall, args=(process, stdout))
        reader = threading.Thread(target=self.readall, args=(process, stdin))
        reader.start()
        writer.start()
        try:
            process.wait()
        except KeyboardInterrupt as e:
            raise SubprocessError("Keyboard interrupt") from e
        finally:
            self.finished = True
            reader.join()
            writer.join()

        return process.returncode
