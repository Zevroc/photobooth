"""Admin screen for application settings."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QLineEdit, QComboBox, QCheckBox,
    QTabWidget, QFormLayout, QFileDialog,
    QGroupBox, QMessageBox, QTextEdit, QDialog, QApplication,
    QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, QUrl
from PyQt6.QtGui import QFont, QImage, QPixmap, QCursor, QDesktopServices
from src.models import AppConfig
from src.controllers.camera_controller import CameraController
from src.controllers.printer_controller import PrinterController
from src.controllers.email_controller import EmailController
from src.views.onedrive_setup_wizard import OneDriveSetupWizard


class _OneDriveAuthWorker(QThread):
    """Background thread for OneDrive device flow completion."""
    success = pyqtSignal()
    failure = pyqtSignal(str)

    def __init__(self, controller, flow):
        super().__init__()
        self.controller = controller
        self.flow = flow

    def run(self):
        try:
            ok = self.controller.complete_device_flow(self.flow)
            if ok:
                self.success.emit()
            else:
                self.failure.emit("Authentification échouée ou délai expiré.")
        except Exception as e:
            self.failure.emit(str(e))


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
        self.tabs.addTab(self.create_buttons_tab(), "🔘 Boutons")
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

    def create_buttons_tab(self):
        """Create custom button images settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        info = QLabel("Laissez vide pour utiliser les images par défaut. Formats: PNG, JPG, etc.")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Capture button (with generated style toggle)
        self._create_capture_button_selector(layout)
        
        # Choose frame button
        self._create_button_selector(
            layout, "🖼 Changer de cadre",
            "choose_frame_normal", "choose_frame_pressed"
        )
        
        # Gallery button
        self._create_button_selector(
            layout, "📷 Galerie",
            "gallery_normal", "gallery_pressed"
        )
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def _create_capture_button_selector(self, parent_layout: QVBoxLayout):
        """Create capture button selector with generated-style toggle."""
        group = QGroupBox("📸 Prendre une photo")
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.capture_generated_check = QCheckBox(
            "Utiliser le bouton Photobooth Miss (généré)"
        )
        self.capture_generated_check.setChecked(
            getattr(self.config.buttons, "capture_mode", "image") == "miss"
        )
        self.capture_generated_check.stateChanged.connect(self._toggle_capture_selectors)
        layout.addWidget(self.capture_generated_check)

        # Normal image selector
        normal_layout = QHBoxLayout()
        normal_layout.addWidget(QLabel("État normal:"))
        self.capture_normal_edit = QLineEdit(self.config.buttons.capture_normal)
        self.capture_normal_edit.setReadOnly(True)
        self.capture_normal_edit.setPlaceholderText("Aucune image sélectionnée")
        normal_layout.addWidget(self.capture_normal_edit)
        self.capture_normal_btn = QPushButton("Parcourir...")
        self.capture_normal_btn.clicked.connect(
            lambda checked=False: self._browse_button_image(self.capture_normal_edit, "capture_normal")
        )
        normal_layout.addWidget(self.capture_normal_btn)
        self.capture_normal_clear = QPushButton("✕")
        self.capture_normal_clear.setMaximumWidth(40)
        self.capture_normal_clear.clicked.connect(
            lambda checked=False: self._clear_button_image(self.capture_normal_edit, "capture_normal")
        )
        normal_layout.addWidget(self.capture_normal_clear)
        layout.addLayout(normal_layout)

        # Pressed image selector
        pressed_layout = QHBoxLayout()
        pressed_layout.addWidget(QLabel("État pressé:"))
        self.capture_pressed_edit = QLineEdit(self.config.buttons.capture_pressed)
        self.capture_pressed_edit.setReadOnly(True)
        self.capture_pressed_edit.setPlaceholderText("Aucune image sélectionnée")
        pressed_layout.addWidget(self.capture_pressed_edit)
        self.capture_pressed_btn = QPushButton("Parcourir...")
        self.capture_pressed_btn.clicked.connect(
            lambda checked=False: self._browse_button_image(self.capture_pressed_edit, "capture_pressed")
        )
        pressed_layout.addWidget(self.capture_pressed_btn)
        self.capture_pressed_clear = QPushButton("✕")
        self.capture_pressed_clear.setMaximumWidth(40)
        self.capture_pressed_clear.clicked.connect(
            lambda checked=False: self._clear_button_image(self.capture_pressed_edit, "capture_pressed")
        )
        pressed_layout.addWidget(self.capture_pressed_clear)
        layout.addLayout(pressed_layout)

        group.setLayout(layout)
        parent_layout.addWidget(group)
        self._toggle_capture_selectors()

    def _toggle_capture_selectors(self):
        """Enable/disable capture image selectors based on generated toggle."""
        use_generated = self.capture_generated_check.isChecked()
        for widget in (
            self.capture_normal_edit,
            self.capture_pressed_edit,
            self.capture_normal_btn,
            self.capture_pressed_btn,
            self.capture_normal_clear,
            self.capture_pressed_clear,
        ):
            widget.setEnabled(not use_generated)
    
    def _create_button_selector(self, parent_layout: QVBoxLayout, label: str, normal_attr: str, pressed_attr: str):
        """Create a button image selector pair (normal + pressed).
        
        Args:
            parent_layout: Parent layout to add selector to
            label: Display label for the button
            normal_attr: Config attribute for normal state
            pressed_attr: Config attribute for pressed state
        """
        group = QGroupBox(label)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Normal image selector
        normal_layout = QHBoxLayout()
        normal_layout.addWidget(QLabel("État normal:"))
        normal_edit = QLineEdit(getattr(self.config.buttons, normal_attr, ""))
        normal_edit.setReadOnly(True)
        normal_edit.setPlaceholderText("Aucune image sélectionnée")
        normal_layout.addWidget(normal_edit)
        normal_btn = QPushButton("Parcourir...")
        normal_btn.clicked.connect(
            lambda checked=False, le=normal_edit, attr=normal_attr: self._browse_button_image(le, attr)
        )
        normal_layout.addWidget(normal_btn)
        clear_normal = QPushButton("✕")
        clear_normal.setMaximumWidth(40)
        clear_normal.clicked.connect(
            lambda checked=False, le=normal_edit, attr=normal_attr: self._clear_button_image(le, attr)
        )
        normal_layout.addWidget(clear_normal)
        layout.addLayout(normal_layout)
        
        # Pressed image selector
        pressed_layout = QHBoxLayout()
        pressed_layout.addWidget(QLabel("État pressé:"))
        pressed_edit = QLineEdit(getattr(self.config.buttons, pressed_attr, ""))
        pressed_edit.setReadOnly(True)
        pressed_edit.setPlaceholderText("Aucune image sélectionnée")
        pressed_layout.addWidget(pressed_edit)
        pressed_btn = QPushButton("Parcourir...")
        pressed_btn.clicked.connect(
            lambda checked=False, le=pressed_edit, attr=pressed_attr: self._browse_button_image(le, attr)
        )
        pressed_layout.addWidget(pressed_btn)
        clear_pressed = QPushButton("✕")
        clear_pressed.setMaximumWidth(40)
        clear_pressed.clicked.connect(
            lambda checked=False, le=pressed_edit, attr=pressed_attr: self._clear_button_image(le, attr)
        )
        pressed_layout.addWidget(clear_pressed)
        layout.addLayout(pressed_layout)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
        # Store references for later use
        setattr(self, f"{normal_attr}_edit", normal_edit)
        setattr(self, f"{pressed_attr}_edit", pressed_edit)
    
    def _browse_button_image(self, line_edit: QLineEdit, config_attr: str):
        """Browse and select a button image file.
        
        Args:
            line_edit: QLineEdit to update with file path
            config_attr: Config attribute to update
        """
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Sélectionner une image pour le bouton",
                "",
                "Images (*.png *.jpg *.jpeg *.bmp *.gif);;Tous les fichiers (*)"
            )
            if file_path:
                line_edit.setText(file_path)
                # Ensure buttons config exists
                if hasattr(self.config, 'buttons'):
                    setattr(self.config.buttons, config_attr, file_path)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors de la sélection de l'image:\n\n{str(e)}"
            )
    
    def _clear_button_image(self, line_edit: QLineEdit, config_attr: str):
        """Clear button image selection.
        
        Args:
            line_edit: QLineEdit to clear
            config_attr: Config attribute to clear
        """
        try:
            line_edit.setText("")
            if hasattr(self.config, 'buttons'):
                setattr(self.config.buttons, config_attr, "")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors de la suppression de l'image:\n\n{str(e)}"
            )

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
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        self.onedrive_enabled = QCheckBox("Activer OneDrive")
        self.onedrive_enabled.setChecked(self.config.onedrive.enabled)
        form_layout.addRow("", self.onedrive_enabled)
        
        self.onedrive_client_id = QLineEdit(self.config.onedrive.client_id)
        form_layout.addRow("Client ID:", self.onedrive_client_id)
        
        self.onedrive_tenant_id = QLineEdit(self.config.onedrive.tenant_id)
        form_layout.addRow("Tenant ID:", self.onedrive_tenant_id)
        
        self.onedrive_folder = QLineEdit(self.config.onedrive.folder_path)
        form_layout.addRow("Dossier:", self.onedrive_folder)
        
        layout.addLayout(form_layout)
        
        # Setup wizard button
        wizard_btn = QPushButton("🧙 Assistant de configuration")
        wizard_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        wizard_btn.setStyleSheet("""
            QPushButton {
                background-color: #7c3aed;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 10px 18px;
            }
            QPushButton:hover {
                background-color: #6d28d9;
            }
        """)
        wizard_btn.clicked.connect(self.open_onedrive_wizard)
        layout.addWidget(wizard_btn)

        # Test / authenticate button
        test_onedrive_btn = QPushButton("🔑 Générer le code de connexion")
        test_onedrive_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        test_onedrive_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 10px 18px;
            }
            QPushButton:hover {
                background-color: #006cbd;
            }
        """)
        test_onedrive_btn.clicked.connect(self._test_onedrive_connection)
        layout.addWidget(test_onedrive_btn)

        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def _test_onedrive_connection(self):
        """Generate an OneDrive device flow code and show authentication dialog."""
        client_id = self.onedrive_client_id.text().strip()
        tenant_id = self.onedrive_tenant_id.text().strip() or "common"

        if not client_id:
            QMessageBox.warning(
                self, "Configuration manquante",
                "Veuillez saisir le Client ID avant de générer le code de connexion."
            )
            return

        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))
        try:
            from src.controllers.onedrive_controller import OneDriveController
            self._onedrive_controller = OneDriveController(
                client_id=client_id,
                tenant_id=tenant_id,
                enabled=True
            )
            flow = self._onedrive_controller.start_device_flow()
        except Exception as e:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            QMessageBox.critical(
                self, "Erreur de connexion",
                f"Impossible de générer le code de connexion.\n"
                f"Vérifiez votre Client ID et votre connexion Internet.\n\n"
                f"Détail\u00a0: {e}"
            )
            return

        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        if not flow:
            QMessageBox.critical(
                self, "Erreur de connexion",
                "Impossible de générer le code de connexion.\n"
                "Vérifiez votre Client ID et votre connexion Internet."
            )
            return

        self._onedrive_flow = flow
        user_code = flow.get("user_code", "")
        verification_uri = flow.get("verification_uri", "https://microsoft.com/devicelogin")
        self._show_device_flow_dialog(user_code, verification_uri)

    def _show_device_flow_dialog(self, user_code: str, verification_uri: str):
        """Show the OneDrive device flow authentication dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Connexion OneDrive — Code d'authentification")
        dialog.setMinimumWidth(520)
        dialog.setModal(True)
        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.setContentsMargins(25, 25, 25, 25)
        dlg_layout.setSpacing(15)

        dialog.setStyleSheet("""
            QDialog { background-color: #f8fafc; color: #0f172a; }
            QLabel  { color: #0f172a; font-size: 13px; }
        """)

        title_lbl = QLabel("Authentification OneDrive")
        title_lbl.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        dlg_layout.addWidget(title_lbl)

        dlg_layout.addWidget(QLabel("Suivez ces étapes pour autoriser l'accès à OneDrive\u00a0:"))

        # Step 1
        step1 = QLabel(f"1\u00b7 Ouvrez votre navigateur et allez sur\u00a0:")
        dlg_layout.addWidget(step1)
        url_lbl = QLabel(f"<a href='{verification_uri}'>{verification_uri}</a>")
        url_lbl.setOpenExternalLinks(True)
        url_lbl.setFont(QFont("Segoe UI", 11))
        dlg_layout.addWidget(url_lbl)

        # Code display
        dlg_layout.addWidget(QLabel("2\u00b7 Entrez ce code sur la page\u00a0:"))
        code_widget = QWidget()
        code_widget.setStyleSheet(
            "background-color: #e0f2fe; border-radius: 8px; padding: 6px;"
        )
        code_row = QHBoxLayout(code_widget)
        code_row.setContentsMargins(10, 8, 10, 8)
        code_lbl = QLabel(user_code)
        code_lbl.setFont(QFont("Courier New", 26, QFont.Weight.Bold))
        code_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        code_lbl.setStyleSheet("color: #0369a1; letter-spacing: 4px;")
        code_row.addWidget(code_lbl)
        copy_btn = QPushButton("📋 Copier")
        copy_btn.setFixedWidth(80)
        copy_btn.setStyleSheet(
            "QPushButton{background:#0369a1;color:#fff;border-radius:6px;padding:4px 8px;}"
            "QPushButton:hover{background:#0284c7;}"
        )
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(user_code))
        code_row.addWidget(copy_btn)
        dlg_layout.addWidget(code_widget)

        dlg_layout.addWidget(QLabel("3\u00b7 Connectez-vous avec votre compte Microsoft."))
        dlg_layout.addWidget(QLabel("4\u00b7 Une fois authentifié, cliquez sur \"Vérifier\"."))

        # Open browser button
        open_btn = QPushButton("🌐 Ouvrir le navigateur")
        open_btn.setStyleSheet(
            "QPushButton{background:#64748b;color:#fff;border-radius:8px;padding:8px 14px;}"
            "QPushButton:hover{background:#475569;}"
        )
        open_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(verification_uri))
        )
        dlg_layout.addWidget(open_btn)

        # Status area
        self._dlg_status_lbl = QLabel("")
        self._dlg_status_lbl.setWordWrap(True)
        dlg_layout.addWidget(self._dlg_status_lbl)

        self._dlg_progress = QProgressBar()
        self._dlg_progress.setRange(0, 0)  # indeterminate
        self._dlg_progress.setVisible(False)
        dlg_layout.addWidget(self._dlg_progress)

        # Bottom buttons
        bottom_row = QHBoxLayout()
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(dialog.reject)
        bottom_row.addWidget(close_btn)
        bottom_row.addStretch()

        self._verify_btn = QPushButton("✓ Vérifier l'authentification")
        self._verify_btn.setStyleSheet(
            "QPushButton{background:#2563eb;color:#fff;border-radius:8px;padding:9px 16px;}"
            "QPushButton:hover{background:#1d4ed8;}"
        )
        self._verify_btn.clicked.connect(
            lambda: self._start_verify_auth(dialog)
        )
        bottom_row.addWidget(self._verify_btn)
        dlg_layout.addLayout(bottom_row)

        dialog.exec()

    def _start_verify_auth(self, dialog: QDialog):
        """Start background thread to verify OneDrive authentication."""
        self._verify_btn.setEnabled(False)
        self._dlg_progress.setVisible(True)
        self._dlg_status_lbl.setText("En attente de confirmation…")
        self._dlg_status_lbl.setStyleSheet("color: #64748b;")

        self._auth_worker = _OneDriveAuthWorker(
            self._onedrive_controller, self._onedrive_flow
        )
        self._auth_worker.success.connect(
            lambda: self._on_auth_success(dialog)
        )
        self._auth_worker.failure.connect(
            lambda msg: self._on_auth_failure(msg)
        )
        self._auth_worker.start()

    def _on_auth_success(self, dialog: QDialog):
        """Handle successful OneDrive authentication."""
        self._dlg_progress.setVisible(False)
        self._dlg_status_lbl.setText("✓ Authentification réussie\u00a0! OneDrive est connecté.")
        self._dlg_status_lbl.setStyleSheet("color: #16a34a; font-weight: bold;")
        self._verify_btn.setEnabled(True)
        self._verify_btn.setText("Fermer")
        self._verify_btn.clicked.disconnect()
        self._verify_btn.clicked.connect(dialog.accept)

    def _on_auth_failure(self, message: str):
        """Handle failed OneDrive authentication."""
        self._dlg_progress.setVisible(False)
        self._dlg_status_lbl.setText(f"✗ {message}")
        self._dlg_status_lbl.setStyleSheet("color: #dc2626;")
        self._verify_btn.setEnabled(True)

    def open_onedrive_wizard(self):
        """Open OneDrive setup wizard."""
        wizard = OneDriveSetupWizard(
            self,
            self.onedrive_client_id.text(),
            self.onedrive_tenant_id.text()
        )
        wizard.config_updated.connect(self.on_onedrive_config_updated)
        wizard.exec()
    
    def on_onedrive_config_updated(self, client_id: str, tenant_id: str):
        """Handle OneDrive configuration update from wizard."""
        self.onedrive_client_id.setText(client_id)
        self.onedrive_tenant_id.setText(tenant_id)
        QMessageBox.information(
            self,
            "✓ Configuration mise à jour",
            "La configuration OneDrive a été mise à jour.\n"
            "N'oubliez pas de cliquer sur 'Sauvegarder'."
        )

    
    def create_email_tab(self):
        """Create email settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        self.email_enabled = QCheckBox("Activer Email")
        self.email_enabled.setChecked(self.config.email.enabled)
        form_layout.addRow("", self.email_enabled)
        
        self.email_server = QLineEdit(self.config.email.smtp_server)
        form_layout.addRow("Serveur SMTP:", self.email_server)
        
        self.email_port = QLineEdit(str(self.config.email.smtp_port))
        form_layout.addRow("Port:", self.email_port)
        
        self.email_sender = QLineEdit(self.config.email.sender_email)
        form_layout.addRow("Email expéditeur:", self.email_sender)
        
        self.email_password = QLineEdit(self.config.email.sender_password)
        self.email_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Mot de passe:", self.email_password)
        
        self.email_tls = QCheckBox("Utiliser TLS")
        self.email_tls.setChecked(self.config.email.use_tls)
        form_layout.addRow("", self.email_tls)
        
        layout.addLayout(form_layout)
        
        # Test button
        test_btn = QPushButton("🧪 Tester la connexion")
        test_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 10px 18px;
            }
            QPushButton:hover {
                background-color: #d97706;
            }
        """)
        test_btn.clicked.connect(self.test_email_connection)
        layout.addWidget(test_btn)
        
        layout.addStretch()
        
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
        self.paper_size_combo.addItems(["A4", "Letter", "4x6", "5x7", "100x148"])
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
    
    def test_email_connection(self):
        """Test email connection with current settings."""
        # Show waiting cursor
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))
        
        try:
            # Create temporary email controller with current settings
            email_controller = EmailController(
                smtp_server=self.email_server.text(),
                smtp_port=int(self.email_port.text() or 587),
                sender_email=self.email_sender.text(),
                sender_password=self.email_password.text(),
                use_tls=self.email_tls.isChecked(),
                enabled=True
            )
            
            # Test connection
            success, message = email_controller.test_connection()
            
            # Restore normal cursor
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            
            # Show detailed message in a custom dialog
            self._show_test_result_dialog(success, message)
            
        except Exception as e:
            # Restore normal cursor
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            
            error_msg = f"❌ Erreur lors du test:\n\n{str(e)}"
            self._show_test_result_dialog(False, error_msg)
    
    def _show_test_result_dialog(self, success: bool, message: str):
        """Show test result in a dialog with proper formatting.
        
        Args:
            success: Whether the test succeeded
            message: Message to display
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Test de Connexion Email")
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(300)
        
        layout = QVBoxLayout()
        
        # Title label
        title = QLabel("✅ Test Réussi" if success else "❌ Test Échoué")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Message text (read-only, selectable)
        text_edit = QTextEdit()
        text_edit.setPlainText(message)
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont("Consolas", 10))
        layout.addWidget(text_edit)
        
        # OK button
        ok_btn = QPushButton("OK")
        ok_btn.setMinimumWidth(100)
        ok_btn.clicked.connect(dialog.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        
        # Style based on success/failure
        if success:
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #f0fdf4;
                }
                QLabel {
                    color: #15803d;
                }
            """)
        else:
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #fef2f2;
                }
                QLabel {
                    color: #991b1b;
                }
            """)
        
        dialog.exec()
    
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

        # Update buttons config
        self.config.buttons.capture_mode = (
            "miss" if self.capture_generated_check.isChecked() else "image"
        )
        self.config.buttons.capture_normal = self.capture_normal_edit.text()
        self.config.buttons.capture_pressed = self.capture_pressed_edit.text()
        self.config.buttons.choose_frame_normal = self.choose_frame_normal_edit.text()
        self.config.buttons.choose_frame_pressed = self.choose_frame_pressed_edit.text()
        self.config.buttons.gallery_normal = self.gallery_normal_edit.text()
        self.config.buttons.gallery_pressed = self.gallery_pressed_edit.text()
        
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
