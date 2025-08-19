from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QRect
from utils.resources import image_path


class BrandedBackground(QWidget):
    """Widget that paints a scaled, center-cropped background image with optional dark overlay.

    Add your regular layout/widget as a child to this container for a branded look.
    """

    def __init__(self, child_widget: QWidget, image_filename: str = "ramidos_bg.png", darken: float = 0.38, parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap(image_path(image_filename))
        self._darken = max(0.0, min(darken, 1.0))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(child_widget)

    def paintEvent(self, event):  # noqa: D401
        painter = QPainter(self)
        if not self._pixmap.isNull():
            target_rect = self.rect()
            pix = self._pixmap
            pw, ph = pix.width(), pix.height()
            rw, rh = target_rect.width(), target_rect.height()

            # Decide scaling to cover area (center-crop keep aspect)
            if pw * rh / ph < rw:  # need wider, scale by height
                scaled = pix.scaledToHeight(rh, Qt.SmoothTransformation)
            else:  # need taller, scale by width
                scaled = pix.scaledToWidth(rw, Qt.SmoothTransformation)
            sw, sh = scaled.width(), scaled.height()
            x = (rw - sw) // 2
            y = (rh - sh) // 2
            painter.drawPixmap(QRect(x, y, sw, sh), scaled)
            if self._darken > 0:
                painter.fillRect(target_rect, QBrush(QColor(0, 0, 0, int(255 * self._darken))))
        else:
            painter.fillRect(self.rect(), QBrush(QColor("#2b2b2b")))
        super().paintEvent(event)
