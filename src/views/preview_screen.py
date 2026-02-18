"""Preview screen for reviewing and sharing captured photo."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QMessageBox, QInputDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QFont
from src.models.photo import Photo


class PreviewScreen(QWidget):
    """Screen for previewing and sharing captured photo."""
    
    retake_requested = pyqtSignal()  # Signal to retake photo
    done = pyqtSignal()              # Signal when done
    
    def __init__(self):
        super().__init__()
        self.current_photo = None
        self.saved_path = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Votre Photo!")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        # Photo preview
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setStyleSheet("""
            background-color: white;
            border: 5px solid #2c3e50;
            border-radius: 10px;
        """)
        self.photo_label.setMinimumSize(600, 450)
        layout.addWidget(self.photo_label, 1)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        # Email button
        email_btn = QPushButton("📧 Email")
        email_btn.setFont(QFont("Arial", 14))
        email_btn.setStyleSheet(self._button_style("#3498db"))
        email_btn.clicked.connect(self.on_email_clicked)
        actions_layout.addWidget(email_btn)
        
        # OneDrive button
        onedrive_btn = QPushButton("☁ OneDrive")
        onedrive_btn.setFont(QFont("Arial", 14))
        onedrive_btn.setStyleSheet(self._button_style("#0078d4"))
        onedrive_btn.clicked.connect(self.on_onedrive_clicked)
        actions_layout.addWidget(onedrive_btn)
        
        # Print button
        print_btn = QPushButton("🖨 Imprimer")
        print_btn.setFont(QFont("Arial", 14))
        print_btn.setStyleSheet(self._button_style("#9b59b6"))
        print_btn.clicked.connect(self.on_print_clicked)
        actions_layout.addWidget(print_btn)
        
        layout.addLayout(actions_layout)
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        
        # Retake button
        retake_btn = QPushButton("← Reprendre")
        retake_btn.setFont(QFont("Arial", 14))
        retake_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        retake_btn.clicked.connect(self.retake_requested.emit)
        bottom_layout.addWidget(retake_btn)
        
        bottom_layout.addStretch()
        
        # Done button
        done_btn = QPushButton("Terminé ✓")
        done_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        done_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 20px 50px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        done_btn.clicked.connect(self.done.emit)
        bottom_layout.addWidget(done_btn)
        
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def _button_style(self, color):
        """Generate button style with given color.
        
        Args:
            color: Background color
            
        Returns:
            Style string
        """
        darker = self._darken_color(color)
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
            }}
            QPushButton:hover {{
                background-color: {darker};
            }}
        """
    
    def _darken_color(self, color):
        """Darken a hex color.
        
        Args:
            color: Hex color string
            
        Returns:
            Darkened hex color
        """
        # Simple darkening - reduce each component
        if color.startswith('#'):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r, g, b = max(0, r - 30), max(0, g - 30), max(0, b - 30)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def set_photo(self, photo: Photo, saved_path: str):
        """Set the photo to display.
        
        Args:
            photo: Photo object
            saved_path: Path where photo was saved
        """
        self.current_photo = photo
        self.saved_path = saved_path
        
        # Display photo
        height, width, channel = photo.image_data.shape
        bytes_per_line = 3 * width
        q_image = QImage(photo.image_data.data, width, height, bytes_per_line, 
                        QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            self.photo_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.photo_label.setPixmap(scaled_pixmap)
    
    def on_email_clicked(self):
        """Handle email button click."""
        email, ok = QInputDialog.getText(
            self, 
            "Envoyer par Email", 
            "Entrez l'adresse email:"
        )
        
        if ok and email:
            # Placeholder for email sending
            QMessageBox.information(
                self, 
                "Email", 
                f"La photo serait envoyée à: {email}\n(Fonctionnalité à configurer dans Admin)"
            )
    
    def on_onedrive_clicked(self):
        """Handle OneDrive button click."""
        # Placeholder for OneDrive upload
        QMessageBox.information(
            self, 
            "OneDrive", 
            "La photo serait uploadée sur OneDrive\n(Fonctionnalité à configurer dans Admin)"
        )
    
    def on_print_clicked(self):
        """Handle print button click."""
        # Placeholder for printing
        QMessageBox.information(
            self, 
            "Impression", 
            "La photo serait imprimée\n(Fonctionnalité à configurer dans Admin)"
        )
