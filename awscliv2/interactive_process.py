"""
Wrapper for subrocess.Popen with interactive input support.
"""

import platform
import select
import socket
import subprocess
import sys
import threading
from subprocess import Popen
from typing import Sequence, TextIO, Union

from awscliv2.constants import ENCODING
from awscliv2.exceptions import ExecutableNotFoundError, SubprocessError

TInput = Union[TextIO, socket.socket]


class InteractiveProcess:
    """
    Wrapper for subrocess.Popen with interactive input support.
    """

    read_timeout = 0.2
    default_stdout: TextIO = sys.stdout

    def _get_default_inputs(self) -> Sequence[TInput]:
        if platform.system() == "Windows":
            return [socket.socket()]
        return [sys.stdin]

    def __init__(self, command: Sequence[str], encoding: str = ENCODING) -> None:
        self.command = list(command)
        self.finished = True
        self.encoding = encoding

    def get_command(self) -> str:
        """
        Get command as a string.
        """
        return " ".join(self.command)

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
            # if output.endswith("\n") and not output_data_dec.strip():
            #     continue
            output = f"{output[-10:]}{output_data_dec}"
            stdout.write(output_data_dec)
            stdout.flush()

    def _propagate_streams(self, process: Popen, inputs: Sequence[TInput]) -> bool:  # type: ignore
        has_input = False
        assert process.stdin
        for stream_input in inputs:
            if isinstance(stream_input, socket.socket):
                try:
                    input_data = stream_input.recv(1024)
                except OSError:
                    input_data = b""
                if input_data:
                    process.stdin.write(input_data)
                    try:
                        process.stdin.flush()
                    except BrokenPipeError:
                        continue
                    has_input = True
            else:
                input_data = stream_input.readline()
                if input_data:
                    process.stdin.write(input_data.encode())
                    try:
                        process.stdin.flush()
                    except BrokenPipeError:
                        continue
                    has_input = True
        return has_input

    def readall(self, process: Popen, inputs: Sequence[TInput]) -> None:  # type: ignore
        """
        Write input from `stdin` stream to `process`.

        Arguments:
            process -- Popen process
            inputs -- Streams to read
        """
        assert process.stdin
        while True:
            if self.finished:
                break

            rlist = select.select(inputs, [], [], self.read_timeout)[0]

            if not rlist:
                continue

            has_input = self._propagate_streams(process, inputs)
            if not has_input:
                break

        for stream_input in inputs:
            if isinstance(stream_input, socket.socket):
                stream_input.close()

    def run(self, inputs: Sequence[TInput] = (), stdout: TextIO = default_stdout) -> int:
        """
        Run interactive process with input from `stdin` and output to `stdout`.

        Args:
            inputs -- Input text streams
            stdout -- Process stdout text stream

        Raises:
            ExecutableNotFoundError: Process executable not found
            SubprocessError: Process error

        Returns:
            Process status code
        """
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

        inputs = inputs or self._get_default_inputs()

        writer = threading.Thread(target=self.writeall, args=(process, stdout))
        reader = threading.Thread(target=self.readall, args=(process, inputs))
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
