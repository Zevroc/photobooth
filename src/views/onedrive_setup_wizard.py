"""Simple OneDrive setup with email and password."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.controllers.onedrive_controller import OneDriveController


class OneDriveSetupWizard(QDialog):
    """Simple dialog for setting up OneDrive with email/password."""
    
    config_updated = pyqtSignal(str, str)  # Emits (client_id, tenant_id)
    
    def __init__(self, parent=None, initial_client_id="", initial_tenant_id=""):
        super().__init__(parent)
        self.client_id = initial_client_id or "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # Default public client
        self.tenant_id = initial_tenant_id or "common"
        self.email = ""
        self.password = ""
        self.auth_success = False
        self.controller = None
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Connexion OneDrive")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("☁ Connecter OneDrive")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Entrez vos identifiants Microsoft pour connecter votre compte OneDrive.\n"
            "Vos photos seront uploadées automatiquement."
        )
        desc.setWordWrap(True)
        desc.setFont(QFont("Segoe UI", 12))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Email field
        layout.addWidget(QLabel("Adresse email Microsoft:"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("exemple@outlook.com")
        self.email_input.setMinimumHeight(45)
        self.email_input.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.email_input)
        
        layout.addSpacing(15)
        
        # Password field
        layout.addWidget(QLabel("Mot de passe Microsoft:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Votre mot de passe")
        self.password_input.setMinimumHeight(45)
        self.password_input.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.password_input)
        
        warn_label = QLabel("⚠️ Votre mot de passe n'est jamais stocké, seulement le token de connexion.")
        warn_label.setStyleSheet("color: #666; font-size: 10px;")
        warn_label.setWordWrap(True)
        layout.addWidget(warn_label)
        
        layout.addSpacing(20)
        
        # Status display
        self.status_label = QLabel("Prêt à se connecter")
        self.status_label.setStyleSheet("color: #0f172a; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Connect button
        self.connect_btn = QPushButton("🔓 Se connecter")
        self.connect_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.connect_btn.setMinimumHeight(60)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
            QPushButton:disabled {
                background-color: #cbd5e1;
                color: #64748b;
            }
        """)
        self.connect_btn.clicked.connect(self.do_connect)
        layout.addWidget(self.connect_btn)
        
        layout.addSpacing(15)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setMinimumWidth(120)
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.save_btn = QPushButton("✅ Sauvegarder")
        self.save_btn.setMinimumWidth(120)
        self.save_btn.setMinimumHeight(45)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
        """)
        self.save_btn.clicked.connect(self.save_config)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8fafc;
                color: #0f172a;
            }
            QLabel {
                color: #0f172a;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #0f172a;
                border: 2px solid #cbd5e1;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
            }
        """)
    
    def do_connect(self):
        """Perform OneDrive connection with email and password."""
        self.email = self.email_input.text().strip()
        self.password = self.password_input.text().strip()
        
        if not self.email:
            QMessageBox.warning(self, "Email requis", "Veuillez renseigner votre adresse email.")
            return
        
        if not self.password:
            QMessageBox.warning(self, "Mot de passe requis", "Veuillez renseigner votre mot de passe.")
            return
        
        self.status_label.setText("Connexion en cours...")
        self.connect_btn.setEnabled(False)
        self.email_input.setEnabled(False)
        self.password_input.setEnabled(False)
        
        # Create controller with default client ID
        self.controller = OneDriveController(
            client_id=self.client_id,
            tenant_id=self.tenant_id,
            enabled=True
        )
        
        # Try to authenticate with email/password
        success = self.controller.authenticate_with_credentials(self.email, self.password)
        
        if success:
            self.auth_success = True
            self.status_label.setText("✅ Connexion réussie!")
            self.status_label.setStyleSheet("color: #22c55e; font-weight: bold;")
            self.save_btn.setEnabled(True)
            QMessageBox.information(
                self,
                "Succès",
                "Votre compte OneDrive est maintenant connecté.\n"
                "Cliquez sur 'Sauvegarder' pour terminer."
            )
        else:
            self.status_label.setText("❌ Connexion échouée")
            self.status_label.setStyleSheet("color: #dc2626; font-weight: bold;")
            self.connect_btn.setEnabled(True)
            self.email_input.setEnabled(True)
            self.password_input.setEnabled(True)
            QMessageBox.critical(
                self,
                "Erreur de connexion",
                "Impossible de se connecter avec ces identifiants.\n\n"
                "Vérifiez:\n"
                "• Votre email est correct\n"
                "• Votre mot de passe est correct\n"
                "• Votre compte Microsoft existe\n"
                "• Votre connexion Internet fonctionne\n\n"
                "Si le problème persiste, contactez votre administrateur."
            )
    
    def save_config(self):
        """Save configuration and close dialog."""
        self.config_updated.emit(self.client_id, self.tenant_id)
        QMessageBox.information(
            self,
            "Configuration sauvegardée",
            "Votre connexion OneDrive a été configurée avec succès!\n"
            "Les photos seront uploadées automatiquement."
        )
        self.accept()
