from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from utils.resources import image_path
import datetime


class AboutDialog(QDialog):
    def __init__(self, parent=None, version: str = "0.1.0"):
        super().__init__(parent)
        self.setWindowTitle("About AI Automation Suite")
        self.resize(540, 360)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(14)

        banner = QLabel()
        pix = QPixmap(image_path("ramidos_bg.png"))
        if not pix.isNull():
            pix = pix.scaled(540, 170, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        banner.setPixmap(pix)
        banner.setMinimumHeight(170)
        banner.setStyleSheet("QLabel { border-radius:6px; background:#222; }")
        layout.addWidget(banner)

        year = datetime.datetime.now().year
        info = QLabel(
            f"""<b>AI Automation Suite</b><br>
            Version: {version}<br>
            Brand: RAMIDOS<br>
            Intelligent file organization & PDF utilities.<br><br>
            © {year} RAMIDOS. All rights reserved.
            """
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)
