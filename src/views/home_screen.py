"""Home screen for selecting photo frame."""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont


class HomeScreen(QWidget):
    """Home screen for frame selection."""
    
    frame_selected = pyqtSignal(str)  # Signal when a frame is selected
    admin_requested = pyqtSignal()    # Signal when admin button is clicked
    
    def __init__(self):
        super().__init__()
        self.selected_frame = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Title
        title = QLabel("Bienvenue au Photobooth!")
        title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0f172a; margin-bottom: 8px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Choisissez votre cadre préféré")
        subtitle.setFont(QFont("Segoe UI", 18, QFont.Weight.Medium))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #475569; margin-bottom: 12px;")
        layout.addWidget(subtitle)
        
        # Frames grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background: transparent;")
        
        frames_widget = QWidget()
        self.frames_layout = QGridLayout(frames_widget)
        self.frames_layout.setSpacing(20)
        self.frame_buttons = []
        
        scroll_area.setWidget(frames_widget)
        layout.addWidget(scroll_area, 1)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        
        # Admin button
        admin_btn = QPushButton("⚙ Administration")
        admin_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        admin_btn.setStyleSheet("""
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
        admin_btn.clicked.connect(self.admin_requested.emit)
        bottom_layout.addWidget(admin_btn)
        
        bottom_layout.addStretch()
        
        # Start button
        self.start_btn = QPushButton("Commencer ➔")
        self.start_btn.setFont(QFont("Segoe UI", 17, QFont.Weight.Bold))
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 16px 36px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #94a3b8;
            }
        """)
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.on_start_clicked)
        bottom_layout.addWidget(self.start_btn)
        
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #f8fafc;")
    
    def load_frames(self, frames_dir: str):
        """Load available frames from directory.
        
        Args:
            frames_dir: Directory containing frame images
        """
        # Clear existing frames
        while self.frames_layout.count():
            item = self.frames_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add "No Frame" option
        no_frame_btn = self.create_frame_button(None, "Sans Cadre")
        self.frame_buttons = [no_frame_btn]
        self.frames_layout.addWidget(no_frame_btn, 0, 0)
        
        # Load frames from directory
        if os.path.exists(frames_dir):
            frame_files = [f for f in os.listdir(frames_dir) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            for i, frame_file in enumerate(frame_files, start=1):
                frame_path = os.path.join(frames_dir, frame_file)
                frame_btn = self.create_frame_button(frame_path, os.path.splitext(frame_file)[0])
                self.frame_buttons.append(frame_btn)
                row = i // 3
                col = i % 3
                self.frames_layout.addWidget(frame_btn, row, col)
    
    def create_frame_button(self, frame_path, name):
        """Create a button for a frame.
        
        Args:
            frame_path: Path to frame image (None for no frame)
            name: Display name
            
        Returns:
            QPushButton for the frame
        """
        btn = QPushButton()
        btn.setFixedSize(250, 250)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #cbd5e1;
                border-radius: 14px;
            }
            QPushButton:hover {
                border-color: #3b82f6;
                background-color: #f8fafc;
            }
            QPushButton:checked {
                border-color: #2563eb;
                border-width: 3px;
                background-color: #eff6ff;
            }
        """)
        btn.setCheckable(True)
        
        layout = QVBoxLayout()
        
        # Image preview
        if frame_path and os.path.exists(frame_path):
            pixmap = QPixmap(frame_path)
            pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, 
                                  Qt.TransformationMode.SmoothTransformation)
            img_label = QLabel()
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(img_label)
        else:
            placeholder = QLabel("📷")
            placeholder.setFont(QFont("Segoe UI", 56, QFont.Weight.Bold))
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("color: #2563eb;")
            layout.addWidget(placeholder)
        
        # Name label
        name_label = QLabel(name)
        name_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: #0f172a;")
        layout.addWidget(name_label)
        
        btn.setLayout(layout)
        btn.clicked.connect(lambda: self.on_frame_selected(frame_path, btn))
        
        return btn
    
    def on_frame_selected(self, frame_path, button):
        """Handle frame selection.
        
        Args:
            frame_path: Path to selected frame
            button: The button that was clicked
        """
        # Uncheck all other buttons
        for frame_button in self.frame_buttons:
            if frame_button != button:
                frame_button.setChecked(False)
        
        self.selected_frame = frame_path if frame_path else ""
        self.start_btn.setEnabled(True)
    
    def on_start_clicked(self):
        """Handle start button click."""
        if self.start_btn.isEnabled():
            self.frame_selected.emit(self.selected_frame)
