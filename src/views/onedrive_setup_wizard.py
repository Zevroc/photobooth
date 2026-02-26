"""OneDrive setup with device code flow."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox, QApplication, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from src.controllers.onedrive_controller import OneDriveController


class OneDriveSetupWizard(QDialog):
    """Dialog for setting up OneDrive with device code authentication."""
    
    config_updated = pyqtSignal(str, str)  # Emits (client_id, tenant_id)
    
    def __init__(self, parent=None, initial_client_id="", initial_tenant_id=""):
        super().__init__(parent)
        self.client_id = initial_client_id or "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # Default public client
        self.tenant_id = initial_tenant_id or "common"
        self.auth_success = False
        self.controller = None
        self.device_flow = None
        self.poll_timer = None
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Connexion OneDrive")
        self.setMinimumWidth(600)
        self.setMinimumHeight(600)
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
            "Cliquez sur 'Démarrer la connexion' pour obtenir votre code.\n"
            "Ou utilisez la connexion avec email puis validation téléphone."
        )
        desc.setWordWrap(True)
        desc.setFont(QFont("Segoe UI", 12))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Device code display (initially hidden)
        self.code_container = QWidget()
        code_layout = QVBoxLayout(self.code_container)
        code_layout.setContentsMargins(20, 20, 20, 20)
        code_layout.setSpacing(15)
        
        code_label = QLabel("Votre code:")
        code_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        code_layout.addWidget(code_label)
        
        self.device_code_label = QLabel("")
        self.device_code_label.setFont(QFont("Courier New", 48, QFont.Weight.Bold))
        self.device_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.device_code_label.setStyleSheet("""
            background-color: #eff6ff;
            color: #1e40af;
            border: 3px solid #3b82f6;
            border-radius: 15px;
            padding: 30px;
            letter-spacing: 8px;
        """)
        code_layout.addWidget(self.device_code_label)
        
        self.copy_code_btn = QPushButton("📋 Copier le code")
        self.copy_code_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.copy_code_btn.setMinimumHeight(50)
        self.copy_code_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.copy_code_btn.clicked.connect(self.copy_code)
        code_layout.addWidget(self.copy_code_btn)
        
        self.url_label = QLabel("")
        self.url_label.setFont(QFont("Segoe UI", 11))
        self.url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.url_label.setWordWrap(True)
        self.url_label.setOpenExternalLinks(True)
        self.url_label.setStyleSheet("color: #475569; margin-top: 10px;")
        code_layout.addWidget(self.url_label)
        
        wait_label = QLabel("⏳ En attente de votre validation sur téléphone...")
        wait_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        wait_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wait_label.setStyleSheet("color: #f97316; margin-top: 10px;")
        code_layout.addWidget(wait_label)
        
        self.code_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 15px;
                border: 2px solid #e2e8f0;
            }
        """)
        self.code_container.hide()
        layout.addWidget(self.code_container)
        
        layout.addSpacing(20)
        
        # Status display
        self.status_label = QLabel("Prêt à se connecter")
        self.status_label.setStyleSheet("color: #0f172a; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Connect button
        self.connect_btn = QPushButton("🔓 Démarrer la connexion")
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

        self.interactive_btn = QPushButton("🔐 Connexion avec email")
        self.interactive_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.interactive_btn.setMinimumHeight(52)
        self.interactive_btn.setStyleSheet("""
            QPushButton {
                background-color: #0ea5e9;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #0284c7;
            }
            QPushButton:pressed {
                background-color: #0369a1;
            }
            QPushButton:disabled {
                background-color: #cbd5e1;
                color: #64748b;
            }
        """)
        self.interactive_btn.clicked.connect(self.do_connect_interactive)
        layout.addWidget(self.interactive_btn)
        
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
        """)
    
    def copy_code(self):
        """Copy device code to clipboard."""
        code = self.device_code_label.text()
        if code:
            clipboard = QApplication.clipboard()
            clipboard.setText(code)
            self.copy_code_btn.setText("✅ Code copié!")
            QTimer.singleShot(2000, lambda: self.copy_code_btn.setText("📋 Copier le code"))
    
    def do_connect(self):
        """Start OneDrive connection with device code flow."""
        self.status_label.setText("Génération du code...")
        self.connect_btn.setEnabled(False)
        self.interactive_btn.setEnabled(False)
        
        # Create controller with default client ID
        self.controller = OneDriveController(
            client_id=self.client_id,
            tenant_id=self.tenant_id,
            enabled=True
        )
        
        # Start device flow
        self.device_flow, error_msg = self.controller.start_device_flow()
        
        if not self.device_flow or error_msg:
            self.status_label.setText("❌ Erreur de génération du code")
            self.status_label.setStyleSheet("color: #dc2626; font-weight: bold;")
            self.connect_btn.setEnabled(True)
            self.interactive_btn.setEnabled(True)
            
            error_detail = error_msg or "Impossible de générer le code de connexion."
            QMessageBox.critical(
                self,
                "Erreur de connexion OneDrive",
                error_detail
            )
            return
        
        # Display the code
        user_code = self.device_flow.get("user_code", "")
        verification_uri = self.device_flow.get("verification_uri", "https://microsoft.com/devicelogin")
        
        self.device_code_label.setText(user_code)
        self.url_label.setText(
            f'1. Ouvrez <a href="{verification_uri}" style="color: #2563eb;">{verification_uri}</a><br>'
            f'2. Entrez le code ci-dessus<br>'
            f'3. Cliquez sur le nombre sur votre téléphone'
        )
        
        self.code_container.show()
        self.connect_btn.hide()
        self.interactive_btn.hide()
        self.status_label.setText("En attente de votre validation...")
        self.status_label.setStyleSheet("color: #f97316; font-weight: bold;")
        
        # Start polling for completion
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.check_auth_completion)
        self.poll_timer.start(3000)  # Check every 3 seconds
    
    def check_auth_completion(self):
        """Check if user has completed device authentication."""
        if not self.device_flow or not self.controller:
            if self.poll_timer:
                self.poll_timer.stop()
            return
        
        # Try to complete the flow
        success = self.controller.complete_device_flow(self.device_flow)
        
        if success:
            # Stop polling
            if self.poll_timer:
                self.poll_timer.stop()
            
            self.auth_success = True
            self.status_label.setText("✅ Connexion réussie!")
            self.status_label.setStyleSheet("color: #22c55e; font-weight: bold;")
            self.save_btn.setEnabled(True)
            self.code_container.hide()
            
            QMessageBox.information(
                self,
                "Succès",
                "Votre compte OneDrive est maintenant connecté!\n"
                "Cliquez sur 'Sauvegarder' pour terminer."
            )

    def do_connect_interactive(self):
        """Start OneDrive connection using interactive browser login."""
        self.status_label.setText("Ouverture du navigateur...")
        self.status_label.setStyleSheet("color: #0f172a; font-weight: bold;")
        self.connect_btn.setEnabled(False)
        self.interactive_btn.setEnabled(False)

        self.controller = OneDriveController(
            client_id=self.client_id,
            tenant_id=self.tenant_id,
            enabled=True
        )

        success = self.controller.authenticate_interactive()
        if success:
            self.auth_success = True
            self.status_label.setText("✅ Connexion réussie!")
            self.status_label.setStyleSheet("color: #22c55e; font-weight: bold;")
            self.save_btn.setEnabled(True)
            self.code_container.hide()
            self.connect_btn.hide()
            self.interactive_btn.hide()

            QMessageBox.information(
                self,
                "Succès",
                "Connexion OneDrive réussie via email.\n"
                "Cliquez sur 'Sauvegarder' pour terminer."
            )
        else:
            self.status_label.setText("❌ Connexion échouée")
            self.status_label.setStyleSheet("color: #dc2626; font-weight: bold;")
            self.connect_btn.setEnabled(True)
            self.interactive_btn.setEnabled(True)
            QMessageBox.warning(
                self,
                "Erreur",
                "Connexion OneDrive impossible. Vérifiez votre connexion."
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
    
    def closeEvent(self, event):
        """Handle dialog close event."""
        if self.poll_timer:
            self.poll_timer.stop()
        super().closeEvent(event)
