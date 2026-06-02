from PySide6.QtCore import Qt
from PySide6.QtPdfWidgets import QPdfView


# new_zoom = current_zoom * 1.1
#
# new_zoom = max(MIN_ZOOM, min(MAX_ZOOM, new_zoom))
#
# self.setZoomFactor(new_zoom)

class PdfView(QPdfView):
    MIN_ZOOM = 0.25
    MAX_ZOOM = 5.0

    def wheelEvent(self, event):
        if not (event.modifiers() & Qt.ControlModifier):
            return super().wheelEvent(event)

        old_zoom = self.zoomFactor()

        factor = 1.1 if event.angleDelta().y() > 0 else 1 / 1.1

        new_zoom = old_zoom * factor
        new_zoom = max(self.MIN_ZOOM, min(self.MAX_ZOOM, new_zoom))

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
