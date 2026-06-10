from pathlib import Path

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

        self.process = QProcess(self)

        self.process.readyReadStandardOutput.connect(self.handle_stdout)

        self.process.readyReadStandardError.connect(self.handle_stderr)

        self.process.finished.connect(self.handle_finished)

        self.process.errorOccurred.connect(self.handle_process_error)

        self.output_pdf = ""

    def handle_stdout(self):
        # Function that reads whole process output and sends it to log

        data = self.process.readAllStandardOutput()

        # text = bytes(data).decode()

        text = bytes(data).decode("utf-8", errors="ignore")

        self.log_received.emit(text)

    def handle_stderr(self):
        # Function that reads and sends all compilation errors to log

        data = self.process.readAllStandardError()

        text = bytes(data).decode()

        self.log_received.emit(text)

    def handle_finished(self, exit_code, exit_status):
        # Function that reads and handle the code in the end of compilation

        if exit_code == 0:
            self.compilation_finished.emit(self.output_pdf)

        else:
            self.compilation_failed.emit(f"Compilation error (code = {exit_code})")

    def handle_process_error(self, error):

        self.compilation_failed.emit(f"Process error: {error}")

    def stop(self):

        if self.process.state() != QProcess.NotRunning:
            self.process.kill()

    def compile(self, tex_file):

        if self.process.state() != QProcess.NotRunning:
            self.process.kill()

        tex_path = Path(tex_file)

        if not tex_path.exists():
            print("ARQUIVO NÃO EXISTE")
            self.compilation_failed.emit(f"File not found: {tex_file}")
            return

        self.compilation_started.emit()

        directory = tex_path.parent

        filename = tex_path.name

        self.output_pdf = str(tex_path.with_suffix(".pdf"))

        args = ["-interaction=nonstopmode", "-file-line-error", "-synctex=1", filename]

        self.process.setWorkingDirectory(str(directory))

        self.process.start("pdflatex", args)
