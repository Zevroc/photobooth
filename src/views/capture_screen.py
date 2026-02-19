"""Capture screen for taking photos with countdown."""
import os
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QFont, QPainter, QColor
from src.controllers.camera_controller import CameraController
from src.controllers.photo_controller import PhotoController
from src.models.photo import Photo


class CaptureScreen(QWidget):
    """Screen for capturing photos with countdown."""
    
    photo_captured = pyqtSignal(Photo)  # Signal when photo is captured
    frame_picker_requested = pyqtSignal()  # Signal to open frame picker
    gallery_requested = pyqtSignal()       # Signal to open gallery
    admin_requested = pyqtSignal()         # Signal to open admin
    
    def __init__(self, camera_controller: CameraController, photo_controller: PhotoController):
        super().__init__()
        self.camera = camera_controller
        self.photo_controller = photo_controller
        self.selected_frame = None
        self.countdown = 0
        self.is_capturing = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

        self.frame_preview_cache = {}
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Camera preview
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("""
            background-color: #0f172a;
            border: 2px solid #1e293b;
            border-radius: 14px;
        """)
        self.preview_label.setMinimumSize(1024, 768)
        layout.addWidget(self.preview_label, 1)
        
        # Countdown label
        self.countdown_label = QLabel("")
        self.countdown_label.setFont(QFont("Segoe UI", 108, QFont.Weight.Bold))
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("color: #f97316;")
        self.countdown_label.hide()

        # Capture button (bottom-center overlay)
        self.capture_btn = QPushButton("")
        self.capture_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.capture_btn.clicked.connect(self.start_countdown)
        self.update_capture_button_style(185)

        # Secondary buttons
        self.choose_frame_btn = QPushButton("")
        self.choose_frame_btn.clicked.connect(self.frame_picker_requested.emit)

        self.gallery_btn = QPushButton("")
        self.gallery_btn.clicked.connect(self.gallery_requested.emit)

        self.choose_frame_btn.setObjectName("chooseFrameBtn")
        self.capture_btn.setObjectName("captureBtn")
        self.gallery_btn.setObjectName("galleryBtn")

        self.choose_frame_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.capture_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.gallery_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Hidden admin hotspot (top-right)
        self.admin_hotspot_btn = QPushButton("")
        self.admin_hotspot_btn.setToolTip("Administration")
        self.admin_hotspot_btn.setFixedSize(90, 90)
        self.admin_hotspot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.admin_hotspot_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(15, 23, 42, 22);
                border-radius: 12px;
            }
        """)
        self.admin_hotspot_btn.clicked.connect(self.admin_requested.emit)

        self._style_secondary_buttons()
        self._apply_image_button_styles()
        
        # Place countdown on top of preview
        overlay_layout = QVBoxLayout()
        overlay_layout.setContentsMargins(16, 16, 16, 18)

        top_hotspot_layout = QHBoxLayout()
        top_hotspot_layout.addStretch()
        top_hotspot_layout.addWidget(self.admin_hotspot_btn)
        overlay_layout.addLayout(top_hotspot_layout)

        overlay_layout.addWidget(self.countdown_label, 0, Qt.AlignmentFlag.AlignCenter)
        overlay_layout.addStretch()

        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.setSpacing(26)
        bottom_buttons_layout.addStretch()
        bottom_buttons_layout.addWidget(self.choose_frame_btn, 0, Qt.AlignmentFlag.AlignBottom)
        bottom_buttons_layout.addWidget(self.capture_btn, 0, Qt.AlignmentFlag.AlignBottom)
        bottom_buttons_layout.addWidget(self.gallery_btn, 0, Qt.AlignmentFlag.AlignBottom)
        bottom_buttons_layout.addStretch()
        overlay_layout.addLayout(bottom_buttons_layout)

        self.preview_label.setLayout(overlay_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #0f172a;")

    def _style_secondary_buttons(self):
        """Apply style to secondary bottom buttons."""
        self.choose_frame_btn.setFixedSize(220, 76)
        self.gallery_btn.setFixedSize(220, 76)

    def _assets_path(self, filename: str) -> str:
        """Build absolute path for button assets.

        Args:
            filename: Image filename in assets/buttons

        Returns:
            Absolute path
        """
        return os.path.abspath(os.path.join("assets", "buttons", filename)).replace("\\", "/")

    def _resolve_existing_asset(self, filenames: list[str]) -> str:
        """Resolve first existing asset path from candidate file names.

        Args:
            filenames: Candidate file names in priority order

        Returns:
            Absolute path of first existing asset or empty string
        """
        for filename in filenames:
            asset_path = self._assets_path(filename)
            if os.path.exists(asset_path):
                return asset_path
        return ""

    def _set_button_image_style(
        self,
        button: QPushButton,
        normal_candidates: list[str],
        pressed_candidates: list[str],
        fallback_text: str
    ):
        """Set image-based style for a button using normal/pressed assets."""
        normal_path = self._resolve_existing_asset(normal_candidates)
        pressed_path = self._resolve_existing_asset(pressed_candidates)

        if normal_path and pressed_path:
            button.setText("")
            button.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    background: transparent;
                    border-image: url({normal_path}) 0 0 0 0 stretch stretch;
                }}
                QPushButton:hover {{
                    border-image: url({normal_path}) 0 0 0 0 stretch stretch;
                }}
                QPushButton:pressed {{
                    border-image: url({pressed_path}) 0 0 0 0 stretch stretch;
                }}
                QPushButton:disabled {{
                    border-image: url({pressed_path}) 0 0 0 0 stretch stretch;
                }}
            """)
            return

        button.setText(fallback_text)
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(15, 23, 42, 210);
                color: #f8fafc;
                border: 2px solid rgba(148, 163, 184, 170);
                border-radius: 16px;
                padding: 12px 18px;
                font-size: 18px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: rgba(30, 41, 59, 230);
                border-color: #60a5fa;
            }
            QPushButton:pressed {
                background-color: rgba(15, 23, 42, 255);
            }
        """)

    def _apply_image_button_styles(self):
        """Apply image-based style for all 3 bottom buttons."""
        self._set_button_image_style(
            self.choose_frame_btn,
            [
                "choose_frame_normal.png",
                "choisis_cadre_normal.png",
                "choisir_cadre_normal.png",
                "frame_normal.png",
                "cadre_normal.png",
                "choose_frame_unpressed.png"
            ],
            [
                "choose_frame_pressed.png",
                "choisis_cadre_pressed.png",
                "choisir_cadre_pressed.png",
                "frame_pressed.png",
                "cadre_pressed.png",
                "choose_frame_down.png"
            ],
            "Choisis ton cadre"
        )

        self._set_button_image_style(
            self.capture_btn,
            [
                "capture_normal.png",
                "photo_normal.png",
                "camera_normal.png",
                "prendre_photo_normal.png",
                "capture_unpressed.png"
            ],
            [
                "capture_pressed.png",
                "photo_pressed.png",
                "camera_pressed.png",
                "prendre_photo_pressed.png",
                "capture_down.png"
            ],
            "📸"
        )

        self._set_button_image_style(
            self.gallery_btn,
            [
                "gallery_normal.png",
                "galerie_normal.png",
                "gallerie_normal.png",
                "gallery_unpressed.png"
            ],
            [
                "gallery_pressed.png",
                "galerie_pressed.png",
                "gallerie_pressed.png",
                "gallery_down.png"
            ],
            "Galerie"
        )

    def update_capture_button_style(self, diameter: int):
        """Update round capture button size and style.

        Args:
            diameter: Button diameter in pixels
        """
        diameter = max(180, min(280, int(diameter)))
        radius = diameter // 2
        border_width = max(5, diameter // 30)
        font_size = max(72, int(diameter * 0.62))

        self.capture_btn.setFixedSize(diameter, diameter)
        self.capture_btn.setFont(QFont("Segoe UI Emoji", font_size, QFont.Weight.Bold))
        self.capture_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 1,
                    stop: 0 #3b82f6,
                    stop: 1 #1d4ed8
                );
                color: #ffffff;
                border: {border_width}px solid #dbeafe;
                border-radius: {radius}px;
                font-size: {font_size}px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 1,
                    stop: 0 #60a5fa,
                    stop: 1 #2563eb
                );
                border: {border_width}px solid #bfdbfe;
            }}
            QPushButton:pressed {{
                background-color: #1e40af;
                border: {border_width}px solid #93c5fd;
            }}
            QPushButton:disabled {{
                background-color: #94a3b8;
                color: #e2e8f0;
                border: {border_width}px solid #cbd5e1;
            }}
        """)
        self._apply_image_button_styles()

    def _adapt_capture_button_size(self):
        """Adapt capture button size to preview area."""
        ref_size = min(self.preview_label.width(), self.preview_label.height())
        if ref_size <= 0:
            return
        target_diameter = int(ref_size * 0.24)
        self.update_capture_button_style(target_diameter)
    
    def set_frame(self, frame_path: str):
        """Set the selected frame.
        
        Args:
            frame_path: Path to frame image
        """
        self.selected_frame = frame_path if frame_path else None
        self.frame_preview_cache = {}
    
    def start_camera(self):
        """Start the camera preview."""
        if not self.camera.is_active:
            if self.camera.start():
                self.timer.start(30)  # Update at ~30 FPS
            else:
                self.capture_btn.setEnabled(False)
                self.preview_label.setText("Impossible d'ouvrir la caméra.\nVérifiez la configuration dans Administration.")
                self.preview_label.setStyleSheet("""
                    background-color: #0f172a;
                    color: #cbd5e1;
                    border: 2px solid #1e293b;
                    border-radius: 14px;
                    padding: 24px;
                """)
    
    def stop_camera(self):
        """Stop the camera preview."""
        self.timer.stop()
        self.camera.stop()
        self.capture_btn.setEnabled(True)
    
    def update_frame(self):
        """Update the camera preview frame."""
        frame = self.camera.get_frame()
        if frame is not None:
            display_frame = frame
            if self.selected_frame:
                try:
                    display_frame = self.photo_controller.apply_frame_to_array(frame, self.selected_frame)
                except Exception:
                    display_frame = frame

            self.preview_label.setStyleSheet("""
                background-color: #0f172a;
                border: 2px solid #1e293b;
                border-radius: 14px;
            """)
            # Convert numpy array to QImage
            height, width, channel = display_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(display_frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Scale to fit preview
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            # Center-crop to fill the whole preview area
            target_width = max(1, self.preview_label.width())
            target_height = max(1, self.preview_label.height())
            if scaled_pixmap.width() > target_width or scaled_pixmap.height() > target_height:
                x = max(0, (scaled_pixmap.width() - target_width) // 2)
                y = max(0, (scaled_pixmap.height() - target_height) // 2)
                scaled_pixmap = scaled_pixmap.copy(x, y, target_width, target_height)

            if self.is_capturing:
                painter = QPainter(scaled_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                if self.countdown > 0:
                    overlay_text = str(self.countdown)
                else:
                    overlay_text = "📷"

                font_size = max(64, min(scaled_pixmap.width(), scaled_pixmap.height()) // 3)
                font = QFont("Segoe UI", font_size, QFont.Weight.Bold)
                painter.setFont(font)

                painter.setPen(QColor(15, 23, 42, 210))
                painter.drawText(
                    scaled_pixmap.rect().adjusted(4, 4, 4, 4),
                    Qt.AlignmentFlag.AlignCenter,
                    overlay_text
                )

                painter.setPen(QColor(249, 115, 22))
                painter.drawText(
                    scaled_pixmap.rect(),
                    Qt.AlignmentFlag.AlignCenter,
                    overlay_text
                )
                painter.end()

            self.preview_label.setPixmap(scaled_pixmap)
    
    def start_countdown(self):
        """Start the countdown before capture."""
        self.countdown = 3
        self.is_capturing = True
        self.capture_btn.setEnabled(False)
        self.countdown_timer.start(1000)  # 1 second interval
    
    def update_countdown(self):
        """Update countdown display."""
        self.countdown -= 1
        
        if self.countdown > 0:
            return
        else:
            self.countdown_timer.stop()
            QTimer.singleShot(500, self.capture_photo)
    
    def capture_photo(self):
        """Capture the photo."""
        photo = self.camera.capture_photo(self.selected_frame)
        
        if photo:
            # Apply frame if selected
            if self.selected_frame:
                photo = self.photo_controller.apply_frame(photo, self.selected_frame)
            
            self.photo_captured.emit(photo)
        else:
            QMessageBox.critical(self, "Erreur", "Échec de la capture de photo")
        
        # Reset UI
        self.capture_btn.setEnabled(True)
        self.is_capturing = False
    
    def showEvent(self, event):
        """Handle show event."""
        super().showEvent(event)
        self._adapt_capture_button_size()
        self.start_camera()
    
    def hideEvent(self, event):
        """Handle hide event."""
        super().hideEvent(event)
        self.stop_camera()

    def resizeEvent(self, event):
        """Handle resize event."""
        super().resizeEvent(event)
        self._adapt_capture_button_size()
