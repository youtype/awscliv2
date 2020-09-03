"""
Wrapper for subrocess.Popen with interactive input support.
"""
import select
import subprocess
import sys
import threading
from subprocess import Popen
from typing import Sequence, TextIO

from awscliv2.exceptions import ExecutableNotFoundError, SubprocessError


class InteractiveProcess:
    """
    Wrapper for subrocess.Popen with interactive input support.
    """

    read_timeout = 0.2
    default_stdout: TextIO = sys.stdout
    default_stdin: TextIO = sys.stdin

    def __init__(self, command: Sequence[str]) -> None:
        self.command = list(command)
        self.finished = True

    def writeall(self, process: Popen, stdout: TextIO) -> None:
        while True:
            if self.finished:
                break

            output_data = process.stdout.read(1)
            if not output_data:
                break
            stdout.write(output_data.decode("utf-8"))
            stdout.flush()

    def readall(self, process: Popen, stdin: TextIO) -> None:
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

    def run(self, stdin: TextIO = default_stdin, stdout: TextIO = default_stdout) -> int:
        self.finished = False
        try:
            process = Popen(
                self.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except FileNotFoundError:
            raise ExecutableNotFoundError(self.command[0])

        writer = threading.Thread(target=self.writeall, args=(process, stdout))
        reader = threading.Thread(target=self.readall, args=(process, stdin))
        reader.start()
        writer.start()
        try:
            process.wait()
        except KeyboardInterrupt:
            raise SubprocessError("Keyboard interrupt")
        finally:
            self.finished = True
            reader.join()
            writer.join()

        return process.returncode
