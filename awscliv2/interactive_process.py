"""
Wrapper for subrocess.Popen with interactive input support.
"""
import select
import subprocess
import sys
import threading
from subprocess import Popen
from typing import Sequence

from awscliv2.exceptions import ExecutableNotFoundError, SubprocessError


class InteractiveProcess:
    """
    Wrapper for subrocess.Popen with interactive input support.
    """

    read_timeout = 0.2

    def __init__(self, command: Sequence[str]) -> None:
        self.command = list(command)
        self.finished = True

    @staticmethod
    def writeall(process: Popen) -> None:
        while True:
            data = process.stdout.read(1).decode("utf-8")
            if not data:
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    def readall(self, process: Popen) -> None:
        while True:
            if self.finished:
                break

            rlist = select.select([sys.stdin], [], [], self.read_timeout)[0]
            if not rlist:
                continue

            data = sys.stdin.read(1)
            if not data:
                break
            process.stdin.write(data.encode())
            process.stdin.flush()

    def run(self) -> int:
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

        writer = threading.Thread(target=self.writeall, args=(process,))
        reader = threading.Thread(target=self.readall, args=(process,))
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
