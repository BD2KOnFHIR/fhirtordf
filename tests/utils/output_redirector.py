import sys
import io as sio
from typing import List


class OutputRedirector:
    save_stdout = []
    save_stderr = []

    def _push_stdout(self) -> sio.StringIO:
        self.save_stdout.append(sys.stdout)
        output = sio.StringIO()
        sys.stdout = output
        return output

    def _pop_stdout(self) -> None:
        if self.save_stdout:
            sys.stdout = self.save_stdout.pop()

    def _push_stderr(self) -> sio.StringIO:
        self.save_stderr.append(sys.stdout)
        output = sio.StringIO()
        sys.stderr = output
        return output

    def _pop_stderr(self) -> None:
        if self.save_stderr:
            sys.stderr = self.save_stderr.pop()

    def tearDown(self):
        self._pop_stdout()
        self._pop_stderr()
