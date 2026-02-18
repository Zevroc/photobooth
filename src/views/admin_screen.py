"""Admin screen for application settings."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QComboBox, QCheckBox,
    QTabWidget, QFormLayout, QFileDialog, QScrollArea,
    QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
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
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("⚙ Administration")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title)
        
        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: white;
            }
        """)
        
        tabs.addTab(self.create_camera_tab(), "📷 Caméra")
        tabs.addTab(self.create_frames_tab(), "🖼 Cadres")
        tabs.addTab(self.create_onedrive_tab(), "☁ OneDrive")
        tabs.addTab(self.create_email_tab(), "📧 Email")
        tabs.addTab(self.create_printer_tab(), "🖨 Imprimante")
        
        layout.addWidget(tabs, 1)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Retour")
        back_btn.setFont(QFont("Arial", 14))
        back_btn.setStyleSheet("""
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
        back_btn.clicked.connect(self.back_requested.emit)
        button_layout.addWidget(back_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton("💾 Sauvegarder")
        save_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 40px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def create_camera_tab(self):
        """Create camera settings tab."""
        widget = QWidget()
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Camera selection
        self.camera_combo = QComboBox()
        cameras = CameraController.list_available_cameras()
        for device_id, name in cameras:
            self.camera_combo.addItem(name, device_id)
        
        # Set current camera
        current_index = self.camera_combo.findData(self.config.camera.device_id)
        if current_index >= 0:
            self.camera_combo.setCurrentIndex(current_index)
        
        layout.addRow("Caméra:", self.camera_combo)
        
        # Resolution
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItem("1920x1080 (Full HD)", (1920, 1080))
        self.resolution_combo.addItem("1280x720 (HD)", (1280, 720))
        self.resolution_combo.addItem("640x480 (VGA)", (640, 480))
        layout.addRow("Résolution:", self.resolution_combo)
        
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
        layout.addStretch()
        
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
        self.config.camera.device_id = self.camera_combo.currentData()
        self.config.camera.device_name = self.camera_combo.currentText()
        
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
        
        # Save to file
        self.config.save()
        
        QMessageBox.information(self, "Succès", "Configuration sauvegardée!")
        self.config_saved.emit()
