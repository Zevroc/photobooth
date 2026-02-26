"""Preview screen for reviewing and sharing captured photo."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMessageBox, QDialog, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QFont
from src.models.photo import Photo


class VirtualKeyboardDialog(QDialog):
    """Full-screen virtual keyboard dialog for touchscreen email input."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Entrez votre adresse email")
        self.setModal(True)
        self.setMinimumSize(900, 620)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(14)

        # Title
        title = QLabel("📧 Entrez votre adresse email")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0f172a;")
        layout.addWidget(title)

        # Email input display
        self.email_input = QLineEdit()
        self.email_input.setReadOnly(True)
        self.email_input.setPlaceholderText("exemple@gmail.com")
        self.email_input.setFont(QFont("Segoe UI", 22))
        self.email_input.setMinimumHeight(60)
        self.email_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #0f172a;
                border: 3px solid #3b82f6;
                border-radius: 12px;
                padding: 10px 18px;
            }
        """)
        layout.addWidget(self.email_input)

        layout.addSpacing(6)

        # Keyboard rows
        KEY_STYLE = """
            QPushButton {
                background-color: #ffffff;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                font-size: 18px;
                font-weight: 600;
                min-width: 52px;
                min-height: 52px;
            }
            QPushButton:pressed {
                background-color: #3b82f6;
                color: #ffffff;
                border-color: #2563eb;
            }
        """
        SPECIAL_STYLE = """
            QPushButton {
                background-color: #e2e8f0;
                color: #0f172a;
                border: 1px solid #94a3b8;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 700;
                min-width: 72px;
                min-height: 52px;
            }
            QPushButton:pressed {
                background-color: #64748b;
                color: #ffffff;
            }
        """

        rows = [
            ["1","2","3","4","5","6","7","8","9","0","-","_"],
            ["q","w","e","r","t","y","u","i","o","p","@"],
            ["a","s","d","f","g","h","j","k","l",".",],
            ["z","x","c","v","b","n","m","⌫"],
        ]

        for row in rows:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(6)
            row_layout.addStretch()
            for key in row:
                btn = QPushButton(key)
                if key == "⌫":
                    btn.setStyleSheet(SPECIAL_STYLE)
                    btn.setMinimumWidth(80)
                    btn.clicked.connect(self._backspace)
                else:
                    btn.setStyleSheet(KEY_STYLE)
                    btn.clicked.connect(lambda checked, k=key: self._type_key(k))
                row_layout.addWidget(btn)
            row_layout.addStretch()
            layout.addLayout(row_layout)

        # Space + bottom row
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(10)
        bottom_row.addStretch()

        space_btn = QPushButton("espace")
        space_btn.setStyleSheet(SPECIAL_STYLE)
        space_btn.setMinimumWidth(220)
        space_btn.setMinimumHeight(52)
        space_btn.clicked.connect(lambda: self._type_key(" "))
        bottom_row.addWidget(space_btn)

        clear_btn = QPushButton("🗑 Effacer")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #fee2e2;
                color: #dc2626;
                border: 1px solid #fca5a5;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 700;
                min-width: 110px;
                min-height: 52px;
            }
            QPushButton:pressed { background-color: #fca5a5; }
        """)
        clear_btn.clicked.connect(lambda: self.email_input.setText(""))
        bottom_row.addWidget(clear_btn)

        bottom_row.addStretch()
        layout.addLayout(bottom_row)

        layout.addSpacing(6)

        # Cancel / Send buttons
        action_row = QHBoxLayout()
        action_row.setSpacing(16)

        cancel_btn = QPushButton("✕ Annuler")
        cancel_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        cancel_btn.setMinimumHeight(58)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 14px 30px;
            }
            QPushButton:pressed { background-color: #4b5563; }
        """)
        cancel_btn.clicked.connect(self.reject)
        action_row.addWidget(cancel_btn)

        send_btn = QPushButton("📧 Envoyer")
        send_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        send_btn.setMinimumHeight(58)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 14px 40px;
            }
            QPushButton:pressed { background-color: #1d4ed8; }
        """)
        send_btn.clicked.connect(self._on_send)
        action_row.addWidget(send_btn)

        layout.addLayout(action_row)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f8fafc;")

    def _type_key(self, key: str):
        self.email_input.setText(self.email_input.text() + key)

    def _backspace(self):
        self.email_input.setText(self.email_input.text()[:-1])

    def _on_send(self):
        email = self.email_input.text().strip()
        if not email or "@" not in email:
            QMessageBox.warning(self, "Email invalide", "Veuillez entrer une adresse email valide.")
            return
        self.accept()

    def get_email(self) -> str:
        return self.email_input.text().strip()


class PreviewScreen(QWidget):
    """Screen for previewing and sharing captured photo."""
    
    retake_requested = pyqtSignal()  # Signal to retake photo
    done = pyqtSignal()              # Signal when done
    onedrive_upload_requested = pyqtSignal(str)  # Signal to upload saved path to OneDrive
    email_send_requested = pyqtSignal(str, str)  # Signal to send (recipient, saved_path)
    print_requested = pyqtSignal(str)  # Signal to print saved path
    
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
        title.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0f172a;")
        layout.addWidget(title)
        
        # Photo preview
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #1e293b;
            border-radius: 14px;
        """)
        self.photo_label.setMinimumSize(600, 450)
        layout.addWidget(self.photo_label, 1)
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        actions_layout.addStretch()
        
        # Email button
        self.email_btn = QPushButton("📧 Envoyer par email")
        self.email_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        self.email_btn.setStyleSheet(self._button_style("#3498db"))
        self.email_btn.clicked.connect(self.on_email_clicked)
        actions_layout.addWidget(self.email_btn)
        
        # OneDrive button
        self.onedrive_btn = QPushButton("☁ Envoyer sur OneDrive")
        self.onedrive_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        self.onedrive_btn.setStyleSheet(self._button_style("#0078d4"))
        self.onedrive_btn.clicked.connect(self.on_onedrive_clicked)
        actions_layout.addWidget(self.onedrive_btn)
        
        # Print button
        self.print_btn = QPushButton("🖨 Imprimer la photo")
        self.print_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        self.print_btn.setStyleSheet(self._button_style("#9b59b6"))
        self.print_btn.clicked.connect(self.on_print_clicked)
        actions_layout.addWidget(self.print_btn)
        actions_layout.addStretch()
        
        layout.addLayout(actions_layout)
        self.actions_layout = actions_layout
        
        # Bottom buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        
        # Retake button
        retake_btn = QPushButton("↺ Reprendre la photo")
        retake_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        retake_btn.setStyleSheet("""
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
        retake_btn.clicked.connect(self.retake_requested.emit)
        bottom_layout.addWidget(retake_btn)
        
        bottom_layout.addStretch()
        
        # Done button
        done_btn = QPushButton("✅ Valider")
        done_btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        done_btn.setStyleSheet("""
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
        """)
        done_btn.clicked.connect(self.done.emit)
        bottom_layout.addWidget(done_btn)
        
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #f8fafc;")

    def set_enabled_actions(self, email_enabled: bool, onedrive_enabled: bool, print_enabled: bool):
        """Show/hide sharing actions based on enabled options.

        Args:
            email_enabled: Whether email action is enabled
            onedrive_enabled: Whether OneDrive action is enabled
            print_enabled: Whether print action is enabled
        """
        self.email_btn.setVisible(email_enabled)
        self.onedrive_btn.setVisible(onedrive_enabled)
        self.print_btn.setVisible(print_enabled)
    
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
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
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
        if not self.saved_path:
            QMessageBox.warning(self, "Email", "Aucune photo sauvegardée à envoyer.")
            return

        dialog = VirtualKeyboardDialog(self)
        if dialog.exec() == VirtualKeyboardDialog.DialogCode.Accepted:
            email = dialog.get_email()
            if email:
                self.email_send_requested.emit(email, self.saved_path)
    
    def on_onedrive_clicked(self):
        """Handle OneDrive button click."""
        if not self.saved_path:
            QMessageBox.warning(
                self,
                "OneDrive",
                "Aucune photo sauvegardée à envoyer."
            )
            return

        self.onedrive_upload_requested.emit(self.saved_path)
    
    def on_print_clicked(self):
        """Handle print button click."""
        if not self.saved_path:
            QMessageBox.warning(
                self,
                "Impression",
                "Aucune photo sauvegardée à imprimer."
            )
            return

        self.print_requested.emit(self.saved_path)
