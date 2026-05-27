from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtPdfWidgets import QPdfView


class PdfView(QPdfView):

    def wheelEvent(self, event):
        # Verifies if CTRL is pressed
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()

            current_zoom = self.zoomFactor()

            if delta > 0:
                self.setZoomFactor(current_zoom * 1.1)
            else:
                self.setZoomFactor(current_zoom / 1.1)

            event.accept()
            return
        # regular scroll behaviour
        super().wheelEvent(event)
