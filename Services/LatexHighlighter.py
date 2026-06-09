from PySide6.QtGui import (
    QSyntaxHighlighter,
    QTextCharFormat,
    QColor
)

from PySide6.QtCore import QRegularExpression


class LatexHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        # -------------------
        # LaTeX Commands
        # -------------------

        command_format = QTextCharFormat()

        command_format.setForeground(QColor("#569CD6"))

        self.rules.append((QRegularExpression(r"\\[a-zA-Z]+"), command_format))

        # -------------------
        # Comments
        # -------------------

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))

        self.rules.append((QRegularExpression(r"%.*"), comment_format))

        # -------------------
        # Inline Math
        # -------------------

        math_format = QTextCharFormat()
        math_format.setForeground(QColor("#DCDCAA"))

        self.rules.append((QRegularExpression(r"\$[^$]+\$"), math_format))

        # -------------------
        # Arguments
        # -------------------

        argument_format = QTextCharFormat()
        argument_format.setForeground(QColor("#CE9178"))

        self.rules.append((QRegularExpression(r"\{[^{}]*\}"), argument_format))

        # -------------------
        # Optional Highlight
        # -------------------

        optional_format = QTextCharFormat()
        optional_format.setForeground(QColor("#4EC9B0"))

        self.rules.append((QRegularExpression(r"\[[^\]]*\]"), optional_format))

    def highlightBlock(self, text):

        for pattern, fmt in self.rules:

            iterator = pattern.globalMatch(text)

            while iterator.hasNext():

                match = iterator.next()

                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

