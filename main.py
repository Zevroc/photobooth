"""Main application file."""
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox, QLabel
from PyQt6.QtCore import Qt, QTimer

from src.models import AppConfig
from src.controllers.camera_controller import CameraController
from src.controllers.photo_controller import PhotoController
from src.controllers.onedrive_controller import OneDriveController
from src.controllers.email_controller import EmailController
from src.controllers.printer_controller import PrinterController

from src.views.home_screen import HomeScreen
from src.views.capture_screen import CaptureScreen
from src.views.gallery_screen import GalleryScreen
from src.views.preview_screen import PreviewScreen
from src.views.admin_screen import AdminScreen


APP_STYLE = """
QMainWindow {
    background: #f8fafc;
}

QLabel {
    color: #0f172a;
}

QPushButton {
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton:focus {
    border: 2px solid #93c5fd;
}

QLineEdit, QComboBox, QTextEdit, QSpinBox {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 8px 10px;
    color: #0f172a;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QSpinBox:focus {
    border: 2px solid #60a5fa;
}

QGroupBox {
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    margin-top: 10px;
    padding-top: 12px;
    font-weight: 700;
    color: #0f172a;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 4px;
}
"""


class PhotoboothApp(QMainWindow):
    """Main photobooth application."""
    
    def __init__(self):
        super().__init__()
        
        # Load configuration
        self.config = AppConfig.load()
        
        # Initialize controllers
        self.camera_controller = CameraController(
            self.config.camera.device_id,
            (self.config.camera.resolution_width, self.config.camera.resolution_height)
        )
        self.photo_controller = PhotoController(self.config.photos_directory)
        self.onedrive_controller = OneDriveController(
            self.config.onedrive.client_id,
            self.config.onedrive.tenant_id,
            self.config.onedrive.enabled
        )
        self.email_controller = EmailController(
            self.config.email.smtp_server,
            self.config.email.smtp_port,
            self.config.email.sender_email,
            self.config.email.sender_password,
            self.config.email.use_tls,
            self.config.email.enabled
        )
        self.printer_controller = PrinterController(
            self.config.printer.printer_name,
            self.config.printer.enabled,
            self.config.printer.paper_size
        )
        
        # Initialize UI
        self.init_ui()
        
        # Current photo
        self.current_photo = None
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Photobooth")
        self.setMinimumSize(1024, 768)
        
        # Enable touch events for touch screens
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents)
        
        # Create stacked widget for screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create screens
        self.home_screen = HomeScreen()
        self.capture_screen = CaptureScreen(self.camera_controller, self.photo_controller)
        self.capture_screen.set_buttons_config(self.config.buttons)
        self.gallery_screen = GalleryScreen()
        self.preview_screen = PreviewScreen()
        self.admin_screen = AdminScreen(self.config)
        
        # Add screens to stack
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.capture_screen)
        self.stacked_widget.addWidget(self.gallery_screen)
        self.stacked_widget.addWidget(self.preview_screen)
        self.stacked_widget.addWidget(self.admin_screen)
        
        # Connect signals
        self.home_screen.frame_selected.connect(self.on_frame_selected)
        self.home_screen.admin_requested.connect(self.show_admin)
        
        self.capture_screen.photo_captured.connect(self.on_photo_captured)
        self.capture_screen.frame_picker_requested.connect(self.show_home)
        self.capture_screen.gallery_requested.connect(self.show_gallery)
        self.capture_screen.admin_requested.connect(self.show_admin)

        self.gallery_screen.back_requested.connect(self.show_capture)
        
        self.preview_screen.retake_requested.connect(self.show_capture)
        self.preview_screen.done.connect(self.show_capture)
        self.preview_screen.onedrive_upload_requested.connect(self.on_preview_onedrive_upload)
        self.preview_screen.email_send_requested.connect(self.on_preview_email_send)
        self.preview_screen.print_requested.connect(self.on_preview_print)
        
        self.admin_screen.back_requested.connect(self.show_capture)
        self.admin_screen.config_saved.connect(self.on_config_saved)
        
        # Load frames in home screen
        self.home_screen.set_frames_options(self.config.show_no_frame_option)
        self.home_screen.load_frames("assets/frames")
        self.home_screen.set_home_texts(
            self.config.home_title,
            self.config.home_subtitle,
            self.config.home_start_button_text
        )

        # Restore last selected frame
        frame_path = self.config.last_selected_frame
        if frame_path and not os.path.exists(frame_path):
            frame_path = ""
        self.capture_screen.set_frame(frame_path)

        self.preview_screen.set_enabled_actions(
            self.config.email.enabled,
            self.config.onedrive.enabled,
            self.config.printer.enabled
        )
        self.preview_screen.set_preview_title(getattr(self.config, 'preview_title', 'Votre Photo!'))

        # Reload frames
        self.home_screen.load_frames("assets/frames")
        
        # Show capture screen directly
        self.show_capture()

        # Start window mode from configuration
        if self.config.start_fullscreen:
            self.showFullScreen()
    
    def show_home(self):
        """Show home screen."""
        self.stacked_widget.setCurrentWidget(self.home_screen)
    
    def show_capture(self):
        """Show capture screen."""
        self.stacked_widget.setCurrentWidget(self.capture_screen)

    def show_gallery(self):
        """Show gallery screen."""
        self.gallery_screen.load_photos(self.config.photos_directory)
        self.stacked_widget.setCurrentWidget(self.gallery_screen)
    
    def show_preview(self):
        """Show preview screen."""
        self.stacked_widget.setCurrentWidget(self.preview_screen)
    
    def show_admin(self):
        """Show admin screen."""
        self.stacked_widget.setCurrentWidget(self.admin_screen)
    
    def on_frame_selected(self, frame_path: str):
        """Handle frame selection.
        
        Args:
            frame_path: Path to selected frame
        """
        self.capture_screen.set_frame(frame_path)
        self.config.last_selected_frame = frame_path or ""
        self.config.save()
        self.show_capture()
    
    def on_photo_captured(self, photo):
        """Handle photo capture.
        
        Args:
            photo: Captured Photo object
        """
        self.current_photo = photo

        if photo and photo.frame_path and not photo.frame_applied:
            photo = self.photo_controller.apply_frame(photo, photo.frame_path)
            self.current_photo = photo
        
        # Save photo to disk
        saved_path = self.photo_controller.save_photo(photo)
        
        # Upload to OneDrive if enabled
        if self.config.onedrive.enabled:
            self.onedrive_controller.upload_photo(saved_path, self.config.onedrive.folder_path)
        
        # Show preview
        self.preview_screen.set_photo(photo, saved_path)
        self.show_preview()
    
    def on_config_saved(self):
        """Handle configuration save."""
        # Reload configuration
        self.config = AppConfig.load()
        
        # Update camera controller
        self.camera_controller = CameraController(
            self.config.camera.device_id,
            (self.config.camera.resolution_width, self.config.camera.resolution_height)
        )
        self.capture_screen.camera = self.camera_controller
        
        # Update button configuration
        self.capture_screen.set_buttons_config(self.config.buttons)

        # Update service controllers
        self.onedrive_controller = OneDriveController(
            self.config.onedrive.client_id,
            self.config.onedrive.tenant_id,
            self.config.onedrive.enabled
        )
        self.email_controller = EmailController(
            self.config.email.smtp_server,
            self.config.email.smtp_port,
            self.config.email.sender_email,
            self.config.email.sender_password,
            self.config.email.use_tls,
            self.config.email.enabled
        )
        self.printer_controller = PrinterController(
            self.config.printer.printer_name,
            self.config.printer.enabled,
            self.config.printer.paper_size
        )

        # Update home and preview UI options from config
        self.home_screen.set_home_texts(
            self.config.home_title,
            self.config.home_subtitle,
            self.config.home_start_button_text
        )
        self.home_screen.set_frames_options(self.config.show_no_frame_option)
        self.preview_screen.set_preview_title(getattr(self.config, 'preview_title', 'Votre Photo!'))

        frame_path = self.config.last_selected_frame
        if frame_path and not os.path.exists(frame_path):
            frame_path = ""
        self.capture_screen.set_frame(frame_path)

        self.preview_screen.set_enabled_actions(
            self.config.email.enabled,
            self.config.onedrive.enabled,
            self.config.printer.enabled
        )

    def show_toast(self, message: str, duration_ms: int = 5000):
        """Show a temporary notification that auto-dismisses.

        Args:
            message: Text to display
            duration_ms: Duration in milliseconds before disappearing
        """
        toast = QLabel(message, self)
        toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        toast.setStyleSheet("""
            QLabel {
                background-color: #1e293b;
                color: #f8fafc;
                border: 2px solid #3b82f6;
                border-radius: 16px;
                padding: 18px 36px;
                font-size: 20px;
                font-weight: 700;
            }
        """)
        toast.adjustSize()
        # Center horizontally, place near bottom
        w = max(toast.width(), 500)
        toast.setFixedWidth(w)
        toast.adjustSize()
        x = (self.width() - toast.width()) // 2
        y = self.height() - toast.height() - 60
        toast.move(x, y)
        toast.show()
        toast.raise_()
        QTimer.singleShot(duration_ms, toast.deleteLater)

    def on_preview_onedrive_upload(self, saved_path: str):
        """Upload preview photo to OneDrive on demand.

        Args:
            saved_path: Local path of saved photo
        """
        if not self.config.onedrive.enabled:
            QMessageBox.warning(
                self,
                "OneDrive désactivé",
                "OneDrive est désactivé dans l'administration."
            )
            return

        if not saved_path or not os.path.exists(saved_path):
            QMessageBox.warning(
                self,
                "Fichier introuvable",
                "La photo à envoyer est introuvable."
            )
            return

        success = self.onedrive_controller.upload_photo(
            saved_path,
            self.config.onedrive.folder_path
        )

        if success:
            QMessageBox.information(
                self,
                "OneDrive",
                "Photo envoyée sur OneDrive avec succès."
            )
        else:
            QMessageBox.warning(
                self,
                "OneDrive",
                "Échec de l'envoi sur OneDrive. Vérifiez la configuration et réessayez."
            )

    def on_preview_email_send(self, recipient_email: str, saved_path: str):
        """Send preview photo by email on demand.

        Args:
            recipient_email: Target email address
            saved_path: Local path of saved photo
        """
        if not self.config.email.enabled:
            QMessageBox.warning(
                self,
                "Email désactivé",
                "L'envoi email est désactivé dans l'administration."
            )
            return

        if not recipient_email:
            QMessageBox.warning(
                self,
                "Email invalide",
                "Veuillez renseigner une adresse email valide."
            )
            return

        if not saved_path or not os.path.exists(saved_path):
            QMessageBox.warning(
                self,
                "Fichier introuvable",
                "La photo à envoyer est introuvable."
            )
            return

        success = self.email_controller.send_photo(recipient_email, saved_path)
        if success:
            self.show_toast(f"✅ Photo envoyée à {recipient_email}")
        else:
            QMessageBox.warning(
                self,
                "Email",
                "Échec de l'envoi email. Vérifiez la configuration SMTP."
            )

    def on_preview_print(self, saved_path: str):
        """Print preview photo on demand.

        Args:
            saved_path: Local path of saved photo
        """
        if not self.config.printer.enabled:
            QMessageBox.warning(
                self,
                "Impression désactivée",
                "L'impression est désactivée dans l'administration."
            )
            return

        if not saved_path or not os.path.exists(saved_path):
            QMessageBox.warning(
                self,
                "Fichier introuvable",
                "La photo à imprimer est introuvable."
            )
            return

        success = self.printer_controller.print_photo(saved_path)
        if success:
            QMessageBox.information(
                self,
                "Impression",
                "Photo envoyée à l'imprimante."
            )
        else:
            QMessageBox.warning(
                self,
                "Impression",
                "Échec de l'impression. Vérifiez la configuration imprimante."
            )
    
    def closeEvent(self, event):
        """Handle application close.
        
        Args:
            event: Close event
        """
        # Clean up camera
        self.camera_controller.stop()
        event.accept()

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts for fullscreen mode."""
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
            event.accept()
            return

        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.showNormal()
            event.accept()
            return

        super().keyPressEvent(event)


def main():
    """Main entry point."""
    # Create necessary directories
    os.makedirs("assets/frames", exist_ok=True)
    os.makedirs("assets/photos", exist_ok=True)
    os.makedirs("assets/temp", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Photobooth")
    
    # Set application style
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLE)
    
    # Create and show main window
    window = PhotoboothApp()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
