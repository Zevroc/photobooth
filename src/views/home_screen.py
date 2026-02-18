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
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Choisissez votre cadre préféré")
        subtitle.setFont(QFont("Arial", 20))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        layout.addWidget(subtitle)
        
        # Frames grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")
        
        frames_widget = QWidget()
        self.frames_layout = QGridLayout(frames_widget)
        self.frames_layout.setSpacing(20)
        
        scroll_area.setWidget(frames_widget)
        layout.addWidget(scroll_area, 1)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        
        # Admin button
        admin_btn = QPushButton("⚙ Administration")
        admin_btn.setFont(QFont("Arial", 14))
        admin_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        admin_btn.clicked.connect(self.admin_requested.emit)
        bottom_layout.addWidget(admin_btn)
        
        bottom_layout.addStretch()
        
        # Start button
        self.start_btn = QPushButton("Commencer ➔")
        self.start_btn.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 20px 50px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.on_start_clicked)
        bottom_layout.addWidget(self.start_btn)
        
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
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
        self.frames_layout.addWidget(no_frame_btn, 0, 0)
        
        # Load frames from directory
        if os.path.exists(frames_dir):
            frame_files = [f for f in os.listdir(frames_dir) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            for i, frame_file in enumerate(frame_files, start=1):
                frame_path = os.path.join(frames_dir, frame_file)
                frame_btn = self.create_frame_button(frame_path, os.path.splitext(frame_file)[0])
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
                background-color: white;
                border: 3px solid #bdc3c7;
                border-radius: 10px;
            }
            QPushButton:hover {
                border-color: #3498db;
            }
            QPushButton:checked {
                border-color: #2ecc71;
                border-width: 5px;
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
            placeholder.setFont(QFont("Arial", 64))
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(placeholder)
        
        # Name label
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 12))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        for i in range(self.frames_layout.count()):
            item = self.frames_layout.itemAt(i)
            if item and item.widget() and item.widget() != button:
                item.widget().setChecked(False)
        
        self.selected_frame = frame_path
        self.start_btn.setEnabled(True)
    
    def on_start_clicked(self):
        """Handle start button click."""
        if self.selected_frame is not None:
            self.frame_selected.emit(self.selected_frame if self.selected_frame else "")
