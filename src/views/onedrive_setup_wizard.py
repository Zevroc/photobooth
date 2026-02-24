"""OneDrive setup wizard for guided configuration."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QStackedWidget, QProgressBar, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QFont, QDesktopServices


class OneDriveSetupWizard(QDialog):
    """Wizard dialog for setting up OneDrive integration."""
    
    config_updated = pyqtSignal(str, str)  # Emits (client_id, tenant_id)
    
    def __init__(self, parent=None, initial_client_id="", initial_tenant_id=""):
        super().__init__(parent)
        self.client_id = initial_client_id
        self.tenant_id = initial_tenant_id
        self.current_step = 0
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Assistant de configuration OneDrive")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🔧 Assistant de Configuration OneDrive")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(3)
        self.progress.setValue(1)
        layout.addWidget(self.progress)
        
        # Stacked widget for steps
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_intro_page())
        self.stacked_widget.addWidget(self.create_client_id_page())
        self.stacked_widget.addWidget(self.create_tenant_id_page())
        self.stacked_widget.addWidget(self.create_summary_page())
        
        layout.addWidget(self.stacked_widget, 1)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.back_btn = QPushButton("← Précédent")
        self.back_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.back_btn.setMinimumWidth(120)
        self.back_btn.setEnabled(False)
        self.back_btn.clicked.connect(self.go_previous)
        button_layout.addWidget(self.back_btn)
        
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.cancel_btn.setMinimumWidth(120)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        self.next_btn = QPushButton("Suivant →")
        self.next_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.next_btn.setMinimumWidth(120)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        button_layout.addWidget(self.next_btn)
        
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
            QLineEdit, QTextEdit {
                background-color: #ffffff;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        
        # Initialize display state
        self.update_display()
    
    def create_intro_page(self):
        """Create introduction page."""
        widget = self.create_page_widget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        intro_label = QLabel(
            "Bienvenue!\n\n"
            "Cet assistant vous guidera pour configurer l'intégration OneDrive "
            "avec votre Photobooth.\n\n"
            "Vous devrez:\n"
            "1. Créer une application Azure AD\n"
            "2. Obtenir le Client ID\n"
            "3. Obtenir le Tenant ID\n\n"
            "Le processus prend environ 5-10 minutes."
        )
        intro_label.setWordWrap(True)
        intro_label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(intro_label)
        
        link_label = QLabel(
            '<a href="https://portal.azure.com">Ouvrir le portail Azure →</a>'
        )
        link_label.setOpenExternalLinks(True)
        link_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(link_label)
        
        layout.addStretch()
        return widget
    
    def create_client_id_page(self):
        """Create Client ID page."""
        widget = self.create_page_widget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = QLabel("Étape 1: Client ID")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        instructions = QLabel(
            "1. Allez sur https://portal.azure.com\n"
            "2. Cliquez sur 'Azure Active Directory'\n"
            "3. Cliquez sur 'Inscriptions d'applications'\n"
            "4. Cliquez sur 'Nouvelle inscription'\n"
            "5. Entrez un nom (ex: 'Photobooth')\n"
            "6. Pour 'Types de comptes pris en charge', sélectionnez\n"
            "   'Comptes dans cet annuaire d'organisation (locataire unique)'\n"
            "7. Cliquez sur 'Inscrire'\n"
            "8. Copiez l'ID d'application (Client ID) ci-dessous"
        )
        instructions.setWordWrap(True)
        instructions.setFont(QFont("Segoe UI", 11))
        layout.addWidget(instructions)
        
        layout.addWidget(QLabel("Client ID:"))
        self.client_id_input = QLineEdit()
        self.client_id_input.setText(self.client_id)
        self.client_id_input.setPlaceholderText("Collez votre Client ID ici...")
        layout.addWidget(self.client_id_input)
        
        layout.addStretch()
        return widget
    
    def create_tenant_id_page(self):
        """Create Tenant ID page."""
        widget = self.create_page_widget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = QLabel("Étape 2: Tenant ID")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        instructions = QLabel(
            "1. Retournez sur https://portal.azure.com\n"
            "2. Cliquez sur 'Azure Active Directory'\n"
            "3. Cliquez sur 'Propriétés'\n"
            "4. Copiez 'ID du répertoire (Tenant)' ci-dessous\n\n"
            "Vous pouvez également:\n"
            "- Utiliser l'ID du locataire de votre application inscrite\n"
            "- Ou utiliser 'common' pour permettre plusieurs comptes"
        )
        instructions.setWordWrap(True)
        instructions.setFont(QFont("Segoe UI", 11))
        layout.addWidget(instructions)
        
        layout.addWidget(QLabel("Tenant ID:"))
        self.tenant_id_input = QLineEdit()
        self.tenant_id_input.setText(self.tenant_id)
        self.tenant_id_input.setPlaceholderText("Collez votre Tenant ID ici...")
        layout.addWidget(self.tenant_id_input)
        
        layout.addStretch()
        return widget
    
    def create_summary_page(self):
        """Create summary page."""
        widget = self.create_page_widget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        title = QLabel("Configuration Complète")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        summary_label = QLabel(
            "Voici un résumé de votre configuration OneDrive:\n"
        )
        summary_label.setWordWrap(True)
        layout.addWidget(summary_label)
        
        # Client ID display
        layout.addWidget(QLabel("Client ID:"))
        self.summary_client_id = QLineEdit()
        self.summary_client_id.setReadOnly(True)
        layout.addWidget(self.summary_client_id)
        
        # Tenant ID display
        layout.addWidget(QLabel("Tenant ID:"))
        self.summary_tenant_id = QLineEdit()
        self.summary_tenant_id.setReadOnly(True)
        layout.addWidget(self.summary_tenant_id)
        
        notes_label = QLabel(
            "✓ Configuration prête!\n\n"
            "Cliquez sur 'Terminer' pour sauvegarder ou 'Précédent' "
            "pour modifier."
        )
        notes_label.setWordWrap(True)
        notes_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(notes_label)
        
        layout.addStretch()
        return widget
    
    def create_page_widget(self):
        """Create a page widget for the stacked widget."""
        widget = QVBoxLayout()
        container = QWidget()
        container.setLayout(widget)
        return container
    
    def go_next(self):
        """Go to next step."""
        if self.current_step == 1:
            self.client_id = self.client_id_input.text().strip()
        elif self.current_step == 2:
            self.tenant_id = self.tenant_id_input.text().strip()
        
        if self.current_step < 3:
            self.current_step += 1
            self.update_display()
    
    def go_previous(self):
        """Go to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_display()
    
    def update_display(self):
        """Update the display for current step."""
        self.stacked_widget.setCurrentIndex(self.current_step)
        self.progress.setValue(self.current_step + 1)
        
        # Update button states
        self.back_btn.setEnabled(self.current_step > 0)
        
        # Always disconnect from previous handlers and reconnect properly
        try:
            self.next_btn.clicked.disconnect(self.go_next)
        except TypeError:
            pass
        try:
            self.next_btn.clicked.disconnect(self.finish_wizard)
        except TypeError:
            pass
        
        if self.current_step == 3:
            # Summary page - show final review
            self.summary_client_id.setText(self.client_id)
            self.summary_tenant_id.setText(self.tenant_id)
            self.next_btn.setText("✓ Terminer")
            self.next_btn.clicked.connect(self.finish_wizard)
        else:
            self.next_btn.setText("Suivant →")
            self.next_btn.clicked.connect(self.go_next)
    
    def finish_wizard(self):
        """Finish the wizard and emit signal with collected data."""
        # Update from current page if on step 1 or 2
        if self.current_step == 1:
            self.client_id = self.client_id_input.text().strip()
        elif self.current_step == 2:
            self.tenant_id = self.tenant_id_input.text().strip()
        
        # Emit the collected data
        self.config_updated.emit(self.client_id, self.tenant_id)
        self.accept()

