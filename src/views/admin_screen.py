"""Admin screen for application settings."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QComboBox, QCheckBox,
    QTabWidget, QFormLayout, QFileDialog,
    QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QImage, QPixmap
from src.models import AppConfig
from src.controllers.camera_controller import CameraController
from src.controllers.printer_controller import PrinterController


class AdminScreen(QWidget):
    """Admin screen for settings."""
    
    back_requested = pyqtSignal()  # Signal to go back
    config_saved = pyqtSignal()    # Signal when config is saved
    
    def __init__(self, config: AppConfig):
        super().__init__()
        self.config = config
        self.preview_controller = None
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_camera_preview)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("⚙ Administration")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0f172a;")
        layout.addWidget(title)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #e2e8f0;
                color: #0f172a;
                padding: 10px 18px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
            }
        """)
        
        self.tabs.addTab(self.create_camera_tab(), "📷 Caméra")
        self.tabs.addTab(self.create_home_tab(), "🏠 Accueil")
        self.tabs.addTab(self.create_frames_tab(), "🖼 Cadres")
        self.tabs.addTab(self.create_onedrive_tab(), "☁ OneDrive")
        self.tabs.addTab(self.create_email_tab(), "📧 Email")
        self.tabs.addTab(self.create_printer_tab(), "🖨 Imprimante")
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
        layout.addWidget(self.tabs, 1)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Retour")
        back_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 12px 22px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
        """)
        back_btn.clicked.connect(self.back_requested.emit)
        button_layout.addWidget(back_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton("💾 Sauvegarder")
        save_btn.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 12px 28px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                color: #0f172a;
            }
            QLabel {
                color: #0f172a;
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                background-color: #ffffff;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                padding: 8px 10px;
            }
            QLineEdit:read-only {
                background-color: #f1f5f9;
                color: #334155;
            }
            QCheckBox {
                color: #0f172a;
            }
        """)
    
    def create_camera_tab(self):
        """Create camera settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        layout.setSpacing(15)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 8)
        
        # Camera selection
        self.camera_combo = QComboBox()
        cameras = CameraController.list_available_cameras()
        if cameras:
            for device_id, name in cameras:
                self.camera_combo.addItem(name, device_id)
        else:
            self.camera_combo.addItem("Aucune caméra détectée", 0)
        
        # Set current camera
        current_index = self.camera_combo.findData(self.config.camera.device_id)
        if current_index >= 0:
            self.camera_combo.setCurrentIndex(current_index)
        
        form_layout.addRow("Caméra:", self.camera_combo)
        
        # Resolution
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItem("1920x1080 (Full HD)", (1920, 1080))
        self.resolution_combo.addItem("1280x720 (HD)", (1280, 720))
        self.resolution_combo.addItem("640x480 (VGA)", (640, 480))
        current_resolution = (self.config.camera.resolution_width, self.config.camera.resolution_height)
        resolution_index = self.resolution_combo.findData(current_resolution)
        if resolution_index >= 0:
            self.resolution_combo.setCurrentIndex(resolution_index)
        form_layout.addRow("Résolution:", self.resolution_combo)

        layout.addLayout(form_layout)

        preview_title = QLabel("Aperçu caméra")
        preview_title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        layout.addWidget(preview_title)

        self.camera_preview_label = QLabel("Aperçu indisponible")
        self.camera_preview_label.setMinimumSize(420, 240)
        self.camera_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_preview_label.setStyleSheet("""
            QLabel {
                background-color: #0f172a;
                color: #cbd5e1;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        layout.addWidget(self.camera_preview_label)

        self.camera_combo.currentIndexChanged.connect(self.start_camera_preview)
        self.resolution_combo.currentIndexChanged.connect(self.start_camera_preview)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_frames_tab(self):
        """Create frames settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        info = QLabel("Les cadres doivent être des images PNG avec transparence")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Frames directory
        dir_layout = QHBoxLayout()
        self.frames_dir_edit = QLineEdit("assets/frames")
        self.frames_dir_edit.setReadOnly(True)
        dir_layout.addWidget(QLabel("Dossier:"))
        dir_layout.addWidget(self.frames_dir_edit)
        
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.browse_frames_dir)
        dir_layout.addWidget(browse_btn)
        
        layout.addLayout(dir_layout)

        self.show_no_frame_option_check = QCheckBox("Afficher l'option Sans cadre")
        self.show_no_frame_option_check.setChecked(self.config.show_no_frame_option)
        layout.addWidget(self.show_no_frame_option_check)

        layout.addStretch()
        
        widget.setLayout(layout)
        return widget

    def create_home_tab(self):
        """Create home screen text settings tab."""
        widget = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.home_title_edit = QLineEdit(self.config.home_title)
        layout.addRow("Titre accueil:", self.home_title_edit)

        self.home_subtitle_edit = QLineEdit(self.config.home_subtitle)
        layout.addRow("Sous-titre accueil:", self.home_subtitle_edit)

        self.start_fullscreen_check = QCheckBox("Démarrer en plein écran")
        self.start_fullscreen_check.setChecked(self.config.start_fullscreen)
        layout.addRow("", self.start_fullscreen_check)

        widget.setLayout(layout)
        return widget
    
    def create_onedrive_tab(self):
        """Create OneDrive settings tab."""
        widget = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.onedrive_enabled = QCheckBox("Activer OneDrive")
        self.onedrive_enabled.setChecked(self.config.onedrive.enabled)
        layout.addRow("", self.onedrive_enabled)
        
        self.onedrive_client_id = QLineEdit(self.config.onedrive.client_id)
        layout.addRow("Client ID:", self.onedrive_client_id)
        
        self.onedrive_tenant_id = QLineEdit(self.config.onedrive.tenant_id)
        layout.addRow("Tenant ID:", self.onedrive_tenant_id)
        
        self.onedrive_folder = QLineEdit(self.config.onedrive.folder_path)
        layout.addRow("Dossier:", self.onedrive_folder)
        
        widget.setLayout(layout)
        return widget
    
    def create_email_tab(self):
        """Create email settings tab."""
        widget = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.email_enabled = QCheckBox("Activer Email")
        self.email_enabled.setChecked(self.config.email.enabled)
        layout.addRow("", self.email_enabled)
        
        self.email_server = QLineEdit(self.config.email.smtp_server)
        layout.addRow("Serveur SMTP:", self.email_server)
        
        self.email_port = QLineEdit(str(self.config.email.smtp_port))
        layout.addRow("Port:", self.email_port)
        
        self.email_sender = QLineEdit(self.config.email.sender_email)
        layout.addRow("Email expéditeur:", self.email_sender)
        
        self.email_password = QLineEdit(self.config.email.sender_password)
        self.email_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Mot de passe:", self.email_password)
        
        self.email_tls = QCheckBox("Utiliser TLS")
        self.email_tls.setChecked(self.config.email.use_tls)
        layout.addRow("", self.email_tls)
        
        widget.setLayout(layout)
        return widget
    
    def create_printer_tab(self):
        """Create printer settings tab."""
        widget = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.printer_enabled = QCheckBox("Activer Impression")
        self.printer_enabled.setChecked(self.config.printer.enabled)
        layout.addRow("", self.printer_enabled)
        
        self.printer_combo = QComboBox()
        printers = PrinterController.list_available_printers()
        self.printer_combo.addItem("-- Sélectionner --", "")
        for printer in printers:
            self.printer_combo.addItem(printer, printer)
        
        # Set current printer
        current_index = self.printer_combo.findData(self.config.printer.printer_name)
        if current_index >= 0:
            self.printer_combo.setCurrentIndex(current_index)
        
        layout.addRow("Imprimante:", self.printer_combo)
        
        self.paper_size_combo = QComboBox()
        self.paper_size_combo.addItems(["A4", "Letter", "4x6", "5x7"])
        self.paper_size_combo.setCurrentText(self.config.printer.paper_size)
        layout.addRow("Format papier:", self.paper_size_combo)
        
        widget.setLayout(layout)
        return widget
    
    def browse_frames_dir(self):
        """Browse for frames directory."""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Sélectionner le dossier des cadres",
            self.frames_dir_edit.text()
        )
        if dir_path:
            self.frames_dir_edit.setText(dir_path)
    
    def save_config(self):
        """Save configuration."""
        # Update camera config
        selected_device = self.camera_combo.currentData()
        self.config.camera.device_id = int(selected_device) if selected_device is not None else 0
        self.config.camera.device_name = self.camera_combo.currentText()
        selected_resolution = self.resolution_combo.currentData() or (1920, 1080)
        self.config.camera.resolution_width = int(selected_resolution[0])
        self.config.camera.resolution_height = int(selected_resolution[1])
        
        # Update OneDrive config
        self.config.onedrive.enabled = self.onedrive_enabled.isChecked()
        self.config.onedrive.client_id = self.onedrive_client_id.text()
        self.config.onedrive.tenant_id = self.onedrive_tenant_id.text()
        self.config.onedrive.folder_path = self.onedrive_folder.text()
        
        # Update email config
        self.config.email.enabled = self.email_enabled.isChecked()
        self.config.email.smtp_server = self.email_server.text()
        self.config.email.smtp_port = int(self.email_port.text() or 587)
        self.config.email.sender_email = self.email_sender.text()
        self.config.email.sender_password = self.email_password.text()
        self.config.email.use_tls = self.email_tls.isChecked()
        
        # Update printer config
        self.config.printer.enabled = self.printer_enabled.isChecked()
        self.config.printer.printer_name = self.printer_combo.currentData()
        self.config.printer.paper_size = self.paper_size_combo.currentText()

        # Update home screen text config
        self.config.home_title = self.home_title_edit.text().strip() or "Bienvenue au Photobooth!"
        self.config.home_subtitle = self.home_subtitle_edit.text().strip() or "Choisissez votre cadre préféré"
        self.config.start_fullscreen = self.start_fullscreen_check.isChecked()
        self.config.show_no_frame_option = self.show_no_frame_option_check.isChecked()
        
        # Save to file
        self.config.save()
        
        QMessageBox.information(self, "Succès", "Configuration sauvegardée!")
        self.config_saved.emit()

    def on_tab_changed(self, index: int):
        """Handle tab change events."""
        if index == 0:
            self.start_camera_preview()
        else:
            self.stop_camera_preview()

    def start_camera_preview(self):
        """Start live camera preview in admin camera tab."""
        if self.tabs.currentIndex() != 0:
            return

        self.stop_camera_preview()

        device_id = self.camera_combo.currentData()
        resolution = self.resolution_combo.currentData() or (1280, 720)
        self.preview_controller = CameraController(int(device_id) if device_id is not None else 0, resolution)

        if self.preview_controller.start():
            self.camera_preview_label.setText("")
            self.preview_timer.start(80)
        else:
            self.camera_preview_label.setPixmap(QPixmap())
            self.camera_preview_label.setText("Impossible d'ouvrir la caméra sélectionnée")

    def update_camera_preview(self):
        """Update camera preview frame."""
        if not self.preview_controller:
            return

        frame = self.preview_controller.get_frame()
        if frame is None:
            return

        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        scaled = pixmap.scaled(
            self.camera_preview_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.camera_preview_label.setPixmap(scaled)

    def stop_camera_preview(self):
        """Stop live camera preview."""
        self.preview_timer.stop()
        if self.preview_controller:
            self.preview_controller.stop()
            self.preview_controller = None

    def showEvent(self, event):
        """Handle show event."""
        super().showEvent(event)
        if self.tabs.currentIndex() == 0:
            self.start_camera_preview()

    def hideEvent(self, event):
        """Handle hide event."""
        super().hideEvent(event)
        self.stop_camera_preview()
