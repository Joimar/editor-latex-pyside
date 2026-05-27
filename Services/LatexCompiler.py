from PySide6.QtCore import (
    QObject,
    Signal,
    QProcess
)

import os


class LatexCompiler(QObject):
    compilation_started = Signal()
    compilation_finished = Signal(str)
    compilation_failed = Signal(str)
    log_received = Signal(str)

    def __init__(self):
        super().__init__()

        self.process = QProcess()

        self.process.readyReadStandardOutput.connect(self.handle_stdout)

        self.process.readyReadStandardError.connect(self.handle_stderr)

        self.process.finished.connect(self.handle_finished)

        self.output_pdf = ""

    def handle_stdout(self):
        # Function that reads whole process output and sends it to log

        data = self.process.readAllStandardOutput()

        text = bytes(data).decode()

        self.log_received.emit(text)

    def handle_stderr(self):
        data = self.process.readAllStandardError()

        text = bytes(data).decode()

        self.log_received.emit(text)

    def handle_finished(self, exit_code, exit_status):
        if exit_code == 0:
            self.compilation_finished.emit(self.output_pdf)

        else:
            self.compilation_failed.emit(f"Compilation error (code = {exit_code})")
