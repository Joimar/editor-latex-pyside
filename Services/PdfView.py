from PySide6.QtCore import Qt
from PySide6.QtPdfWidgets import QPdfView


class PdfView(QPdfView):

    def wheelEvent(self, event):

        if not (event.modifiers() & Qt.ControlModifier):
            return super().wheelEvent(event)

        old_zoom = self.zoomFactor()

        factor = 1.1 if event.angleDelta().y() > 0 else 1 / 1.1

        new_zoom = old_zoom * factor

        # posição do mouse dentro da viewport
        mouse_pos = event.position()

        # scrollbars antes do zoom
        h_before = self.horizontalScrollBar().value()
        v_before = self.verticalScrollBar().value()

        ratio = new_zoom / old_zoom

        self.setZoomMode(QPdfView.ZoomMode.Custom)
        self.setZoomFactor(new_zoom)

        # compensação
        self.horizontalScrollBar().setValue(
            int((h_before + mouse_pos.x()) * ratio - mouse_pos.x())
        )

        self.verticalScrollBar().setValue(
            int((v_before + mouse_pos.y()) * ratio - mouse_pos.y())
        )

        event.accept()