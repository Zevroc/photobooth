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
        self.show_no_frame_option = True
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Top-right admin icon button
        top_layout = QHBoxLayout()
        top_layout.addStretch()

        admin_btn = QPushButton("")
        admin_btn.setFixedSize(90, 90)
        admin_btn.setToolTip("Administration")
        admin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        admin_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: rgba(15, 23, 42, 22);
            }
        """)
        admin_btn.clicked.connect(self.admin_requested.emit)
        top_layout.addWidget(admin_btn)

        layout.addLayout(top_layout)
        
        # Title
        self.title_label = QLabel("Bienvenue au Photobooth!")
        self.title_label.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: #0f172a; margin-bottom: 8px;")
        layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Choisissez votre cadre préféré")
        self.subtitle_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Medium))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("color: #475569; margin-bottom: 12px;")
        layout.addWidget(self.subtitle_label)
        
        # Frames grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #e2e8f0;
                width: 16px;
                margin: 8px 2px 8px 2px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical {
                background: #2563eb;
                min-height: 40px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical:hover {
                background: #1d4ed8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
            QScrollBar:horizontal {
                background: #e2e8f0;
                height: 16px;
                margin: 2px 8px 2px 8px;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal {
                background: #2563eb;
                min-width: 40px;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #1d4ed8;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                background: transparent;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: transparent;
            }
        """)
        
        frames_widget = QWidget()
        self.frames_layout = QGridLayout(frames_widget)
        self.frames_layout.setSpacing(20)
        self.frame_buttons = []
        
        scroll_area.setWidget(frames_widget)
        layout.addWidget(scroll_area, 1)
        
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
        
        self.frame_buttons = []

        # Build frame option list
        frame_options = []
        if self.show_no_frame_option:
            frame_options.append(None)
        
        # Load frames from directory
        if os.path.exists(frames_dir):
            frame_files = [f for f in os.listdir(frames_dir) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            frame_files.sort()

            for frame_file in frame_files:
                frame_path = os.path.join(frames_dir, frame_file)
                frame_options.append(frame_path)

        # Render options in grid
        for i, frame_path in enumerate(frame_options):
                frame_btn = self.create_frame_button(frame_path)
                self.frame_buttons.append(frame_btn)
                row = i // 3
                col = i % 3
                self.frames_layout.addWidget(frame_btn, row, col)
    
    def create_frame_button(self, frame_path):
        """Create a button for a frame.
        
        Args:
            frame_path: Path to frame image (None for no frame)
        Returns:
            QPushButton for the frame
        """
        btn = QPushButton()
        btn.setFixedSize(300, 300)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #cbd5e1;
                border-radius: 18px;
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
            pixmap = pixmap.scaled(260, 260, Qt.AspectRatioMode.KeepAspectRatio, 
                                  Qt.TransformationMode.SmoothTransformation)
            img_label = QLabel()
            img_label.setFixedSize(260, 260)
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(img_label)
        else:
            placeholder = QLabel("🚫")
            placeholder.setFont(QFont("Segoe UI", 72, QFont.Weight.Bold))
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("color: #2563eb;")
            layout.addWidget(placeholder)
        
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
        self.frame_selected.emit(self.selected_frame)

    def set_home_texts(self, title: str, subtitle: str, start_button_text: str = ""):
        """Set configurable home texts.

        Args:
            title: Main title text
            subtitle: Subtitle text
            start_button_text: Unused legacy argument kept for compatibility
        """
        self.title_label.setText(title or "Bienvenue au Photobooth!")
        self.subtitle_label.setText(subtitle or "Choisissez votre cadre préféré")

    def set_frames_options(self, show_no_frame_option: bool):
        """Set frame-list display options.

        Args:
            show_no_frame_option: Whether to display the no-frame option
        """
        self.show_no_frame_option = bool(show_no_frame_option)
