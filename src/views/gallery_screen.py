"""Gallery screen to browse previously captured photos."""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont


class GalleryScreen(QWidget):
    """Screen that displays all saved photos."""

    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize gallery UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header_layout = QHBoxLayout()

        back_btn = QPushButton("← Retour caméra")
        back_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #f8fafc;
                border: none;
                border-radius: 12px;
                padding: 12px 22px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
        """)
        back_btn.clicked.connect(self.back_requested.emit)
        header_layout.addWidget(back_btn)

        header_layout.addStretch()

        title = QLabel("Galerie")
        title.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        title.setStyleSheet("color: #f8fafc;")
        header_layout.addWidget(title)

        header_layout.addStretch()
        header_layout.addSpacing(back_btn.sizeHint().width())

        layout.addLayout(header_layout)

        self.empty_label = QLabel("Aucune photo pour le moment")
        self.empty_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Medium))
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("color: #cbd5e1;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #1e293b;
                width: 14px;
                margin: 6px 2px 6px 2px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #3b82f6;
                min-height: 36px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setHorizontalSpacing(18)
        self.grid_layout.setVerticalSpacing(18)

        scroll_area.setWidget(self.grid_container)

        layout.addWidget(self.empty_label)
        layout.addWidget(scroll_area, 1)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #0f172a;")

    def load_photos(self, photos_directory: str):
        """Load all photos from directory into gallery grid."""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        image_paths = []
        if os.path.exists(photos_directory):
            for file_name in os.listdir(photos_directory):
                if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_paths.append(os.path.join(photos_directory, file_name))

        image_paths.sort(reverse=True)
        self.empty_label.setVisible(len(image_paths) == 0)

        for index, image_path in enumerate(image_paths):
            thumbnail = QLabel()
            thumbnail.setFixedSize(300, 220)
            thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
            thumbnail.setStyleSheet("""
                QLabel {
                    background-color: #111827;
                    border: 2px solid #334155;
                    border-radius: 14px;
                }
            """)

            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    thumbnail.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                thumbnail.setPixmap(scaled)

            row = index // 4
            col = index % 4
            self.grid_layout.addWidget(thumbnail, row, col)
