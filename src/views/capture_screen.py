"""Capture screen for taking photos with countdown."""
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
    back_requested = pyqtSignal()       # Signal to go back
    
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
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        self.title = QLabel("Préparez-vous!")
        self.title.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: #0f172a; margin-bottom: 12px;")
        layout.addWidget(self.title)
        
        # Camera preview
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("""
            background-color: #0f172a;
            border: 2px solid #1e293b;
            border-radius: 14px;
        """)
        self.preview_label.setMinimumSize(800, 600)
        layout.addWidget(self.preview_label, 1)
        
        # Countdown label
        self.countdown_label = QLabel("")
        self.countdown_label.setFont(QFont("Segoe UI", 108, QFont.Weight.Bold))
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("color: #f97316;")
        self.countdown_label.hide()

        # Capture button (bottom-center overlay)
        self.capture_btn = QPushButton("📸")
        self.capture_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.capture_btn.clicked.connect(self.start_countdown)
        self.update_capture_button_style(185)
        
        # Place countdown on top of preview
        overlay_layout = QVBoxLayout()
        overlay_layout.setContentsMargins(20, 20, 20, 20)
        overlay_layout.addWidget(self.countdown_label, 0, Qt.AlignmentFlag.AlignCenter)
        overlay_layout.addStretch()

        capture_layout = QHBoxLayout()
        capture_layout.addStretch()
        capture_layout.addWidget(self.capture_btn)
        capture_layout.addStretch()
        overlay_layout.addLayout(capture_layout)

        self.preview_label.setLayout(overlay_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        # Back button
        back_btn = QPushButton("← Retour")
        back_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #f8fafc;
                border: none;
                border-radius: 12px;
                padding: 14px 24px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
        """)
        back_btn.clicked.connect(self.on_back_clicked)
        button_layout.addWidget(back_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #f8fafc;")

    def update_capture_button_style(self, diameter: int):
        """Update round capture button size and style.

        Args:
            diameter: Button diameter in pixels
        """
        diameter = max(150, min(240, int(diameter)))
        radius = diameter // 2
        border_width = max(5, diameter // 30)
        font_size = max(54, diameter // 2)

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

    def _adapt_capture_button_size(self):
        """Adapt capture button size to preview area."""
        ref_size = min(self.preview_label.width(), self.preview_label.height())
        if ref_size <= 0:
            return
        target_diameter = int(ref_size * 0.23)
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
                self.title.setText("Préparez-vous!")
                self.timer.start(30)  # Update at ~30 FPS
            else:
                self.capture_btn.setEnabled(False)
                self.title.setText("Caméra indisponible")
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
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

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
    
    def on_back_clicked(self):
        """Handle back button click."""
        self.stop_camera()
        self.back_requested.emit()
    
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
