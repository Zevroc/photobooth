# Photobooth - Architecture Documentation

## 📁 Structure du Projet

```
photobooth/
├── main.py                 # Point d'entrée de l'application
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation principale
├── .gitignore            # Fichiers à ignorer par Git
│
├── src/                   # Code source
│   ├── __init__.py
│   ├── models/           # Modèles de données
│   │   ├── __init__.py   # Configuration de l'application
│   │   └── photo.py      # Modèle Photo
│   │
│   ├── controllers/      # Logique métier
│   │   ├── __init__.py
│   │   ├── camera_controller.py      # Gestion caméra
│   │   ├── photo_controller.py       # Traitement photos
│   │   ├── onedrive_controller.py    # Upload OneDrive
│   │   ├── email_controller.py       # Envoi email
│   │   └── printer_controller.py     # Impression
│   │
│   ├── views/            # Interface utilisateur (PyQt6)
│   │   ├── __init__.py
│   │   ├── home_screen.py      # Écran d'accueil
│   │   ├── capture_screen.py   # Écran capture photo
│   │   ├── preview_screen.py   # Prévisualisation
│   │   └── admin_screen.py     # Panel admin
│   │
│   ├── utils/            # Utilitaires
│   │   └── __init__.py
│   │
│   └── config/           # Configuration
│       └── __init__.py
│
├── assets/               # Ressources
│   ├── frames/          # Cadres/fonds pour photos
│   ├── photos/          # Photos sauvegardées
│   └── temp/            # Fichiers temporaires
│
├── config/              # Fichiers de configuration
│   └── config.json     # Configuration de l'app (généré)
│
└── docs/                # Documentation
    └── ARCHITECTURE.md  # Ce fichier
```

## 🏗️ Architecture

### Pattern MVC (Model-View-Controller)

L'application utilise le pattern MVC pour séparer les responsabilités:

#### Models (`src/models/`)
- **AppConfig**: Configuration complète de l'application (caméra, OneDrive, email, imprimante)
- **Photo**: Représentation d'une photo capturée avec ses métadonnées

#### Controllers (`src/controllers/`)
- **CameraController**: Gestion de la caméra (démarrage, arrêt, capture)
- **PhotoController**: Traitement des photos (application de cadres, sauvegarde)
- **OneDriveController**: Upload vers OneDrive
- **EmailController**: Envoi par email
- **PrinterController**: Impression

#### Views (`src/views/`)
- **HomeScreen**: Sélection du cadre photo
- **CaptureScreen**: Capture photo avec compte à rebours
- **PreviewScreen**: Prévisualisation et partage
- **AdminScreen**: Configuration de l'application

### Flux de l'Application

```
1. Démarrage
   └─> HomeScreen (Choix du cadre)

2. Sélection du cadre
   └─> CaptureScreen (Prise de photo)
       ├─> Aperçu caméra en temps réel
       ├─> Compte à rebours (3, 2, 1)
       └─> Capture

3. Photo capturée
   └─> PreviewScreen (Prévisualisation)
       ├─> Sauvegarde automatique
       ├─> Options de partage
       │   ├─> Email
       │   ├─> OneDrive
       │   └─> Impression
       └─> Retour ou Nouveau

4. Administration
   └─> AdminScreen (Configuration)
       ├─> Caméra
       ├─> Cadres
       ├─> OneDrive
       ├─> Email
       └─> Imprimante
```

## 🔧 Technologies

### Frontend
- **PyQt6**: Framework UI moderne et tactile
- **Qt Widgets**: Composants d'interface

### Backend
- **OpenCV**: Capture et traitement vidéo/image
- **Pillow**: Manipulation d'images (cadres, redimensionnement)
- **MSAL**: Authentification Microsoft pour OneDrive
- **smtplib**: Envoi d'emails
- **win32print**: Impression Windows

### Stockage
- **JSON**: Configuration de l'application
- **Système de fichiers**: Sauvegarde des photos

## 📊 Modèles de Données

### AppConfig
```python
{
    "camera": {
        "device_id": 0,
        "device_name": "Camera 0",
        "resolution_width": 1920,
        "resolution_height": 1080,
        "fps": 30
    },
    "onedrive": {
        "client_id": "",
        "tenant_id": "",
        "enabled": false,
        "folder_path": "/Photos/Photobooth"
    },
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "",
        "sender_password": "",
        "use_tls": true,
        "enabled": false
    },
    "printer": {
        "printer_name": "",
        "enabled": false,
        "paper_size": "A4"
    },
    "available_frames": [],
    "save_to_disk": true,
    "photos_directory": "assets/photos"
}
```

### Photo
```python
@dataclass
class Photo:
    image_data: np.ndarray  # Image en RGB
    timestamp: datetime
    frame_path: Optional[str]
    width: int
    height: int
```

## 🔐 Sécurité

- Les mots de passe sont stockés localement (à améliorer avec chiffrement)
- Authentification OAuth2 pour OneDrive
- TLS/SSL pour les emails

## 🚀 Déploiement

### Prérequis
- Python 3.8+
- Windows 10/11 (pour support tactile complet)
- Webcam ou caméra externe

### Installation
```bash
# Cloner le repository
git clone https://github.com/Zevroc/photobooth.git
cd photobooth

# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

### Configuration initiale
1. Lancer l'application
2. Cliquer sur "Administration"
3. Configurer:
   - Caméra
   - Cadres (ajouter des images PNG dans `assets/frames/`)
   - OneDrive (optionnel)
   - Email (optionnel)
   - Imprimante (optionnel)
4. Sauvegarder

## 🎨 Personnalisation

### Ajouter des cadres
1. Créer une image PNG avec transparence
2. Placer dans `assets/frames/`
3. Les cadres apparaîtront automatiquement dans l'écran d'accueil

### Thème
Le thème clair est défini dans les fichiers de vue avec des styles inline.
Pour modifier, éditer les styles CSS dans chaque fichier `*_screen.py`.

## 📝 Développement Futur

### Améliorations possibles
- [ ] Support multi-langues
- [ ] Thème sombre
- [ ] Filtres photo en temps réel
- [ ] GIF/Boomerang
- [ ] Partage réseaux sociaux
- [ ] Mode galerie
- [ ] Statistiques d'utilisation
- [ ] Support Linux/macOS
- [ ] Chiffrement des credentials
- [ ] Base de données pour l'historique
