# 📷 Photobooth

Application desktop moderne pour transformer votre PC en photobooth interactif avec support tactile.

## 🎯 Objectif

Créer une application desktop pour Windows permettant de faire d'un PC portable tactile en photobooth simple et esthétique permettant de mettre un cadre par-dessus les photos. Avec les photos, on doit pouvoir :
- ✅ Enregistrer la photo sur le disque
- ☁️ Enregistrer sur OneDrive
- 📧 Envoyer par email
- 🖨️ Imprimer

Les photos peuvent être prises soit par la webcam du PC soit par un appareil photo connecté en USB ou WiFi.

## 🧰 Stack technique

- **Python 3.8+** - Langage principal
- **PyQt6** - Interface graphique moderne et tactile
- **OpenCV** - Capture vidéo et traitement d'images
- **Pillow** - Manipulation d'images et application de cadres
- **MSAL** - Intégration OneDrive via Microsoft Graph API
- **SMTP** - Envoi d'emails
- **win32print** - Support d'impression Windows
- **CUPS (lp)** - Support d'impression macOS

## 📱 Fonctionnalités principales

### 1. 🏠 Accueil
- Choix du cadre photo parmi les options disponibles
- Option "Sans cadre" disponible
- Interface tactile et intuitive
- Accès rapide à l'administration

### 2. 📸 Prise de vue
- Aperçu en temps réel de la caméra
- Compte à rebours avant capture (3, 2, 1)
- Application automatique du cadre sélectionné
- Option de reprendre la photo

### 3. 👁️ Prévisualisation
- Affichage de la photo avec cadre appliqué
- Sauvegarde automatique sur le disque
- Options de partage :
  - 📧 Envoi par email
  - ☁️ Upload OneDrive
  - 🖨️ Impression directe
- Navigation simple (reprendre ou terminer)

### 4. ⚙️ Administration
- **Caméra** : Sélection et configuration
- **Cadres** : Gestion des cadres disponibles
- **OneDrive** : Configuration de l'intégration
- **Email** : Paramètres SMTP
- **Imprimante** : Sélection et format papier

## 🎨 UI/UX

- Interface moderne et épurée
- Thème clair professionnel
- Support tactile complet
- Navigation intuitive
- Boutons larges adaptés au tactile
- Animations et transitions fluides

## 📁 Structure du projet

```
photobooth/
├── main.py                    # Point d'entrée
├── requirements.txt           # Dépendances
├── photobooth.spec            # Config build Windows/Linux
├── photobooth_macos.spec      # Config build macOS (.app bundle)
├── src/
│   ├── models/               # Modèles de données
│   ├── controllers/          # Logique métier
│   └── views/                # Interface utilisateur
├── assets/
│   ├── frames/              # Cadres photo
│   ├── photos/              # Photos sauvegardées
│   └── temp/                # Fichiers temporaires
├── config/
│   └── config.json          # Configuration
└── docs/                    # Documentation
```

## 🚀 Démarrage rapide

### Installation

```bash
# Cloner le repository
git clone https://github.com/Zevroc/photobooth.git
cd photobooth

# Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS / Linux

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

### Configuration initiale

1. Lancer l'application
2. Cliquer sur "⚙ Administration"
3. Configurer la caméra
4. Ajouter des cadres dans `assets/frames/` (format PNG avec transparence)
5. Configurer les options de partage (optionnel)
6. Sauvegarder

### 📦 Compilation en Exécutable

Pour créer un fichier exécutable :

```bash
# Installer les dépendances de l'application
pip install -r requirements.txt

# Installer les dépendances de build
pip install -r requirements-build.txt

# Compiler l'application (détecte automatiquement la plateforme)
python build.py
```

- **Windows** → `dist/Photobooth/Photobooth.exe`
- **macOS** → `dist/Photobooth.app` (bundle cliquable)
- **Linux** → `dist/Photobooth/Photobooth`

Pour plus de détails, consultez le **[Guide de Compilation](docs/BUILD.md)**

## 🖥️ Dépendances système

### macOS (10.13+)

Aucune dépendance système supplémentaire n'est requise. L'application utilise CUPS (intégré à macOS) pour l'impression.

Sur la première ouverture du `.app` compilé, macOS peut afficher un avertissement Gatekeeper :

```bash
# Contourner Gatekeeper (si l'app n'est pas signée)
xattr -cr dist/Photobooth.app
```

Ou faire un clic droit > Ouvrir la première fois.

### Linux (Ubuntu/Debian)

Pour exécuter l'application (ou le binaire compilé) sur Linux, installez d'abord les bibliothèques système Qt/OpenGL :

```bash
sudo apt-get install -y \
  libgl1 \
  libegl1 \
  libxkbcommon0 \
  libxcb-cursor0
```

Si vous êtes en environnement sans écran (container/serveur), vous pouvez tester le démarrage en mode offscreen :

```bash
QT_QPA_PLATFORM=offscreen ./dist/Photobooth/Photobooth
```

### Windows

Sur Windows 10/11, installez les prérequis suivants avant d'exécuter `Photobooth.exe` :

1. **Microsoft Visual C++ Redistributable 2015-2022 (x64)**
2. **Pilotes caméra** (webcam USB ou caméra intégrée)
3. **Pilotes imprimante** (si impression activée)

Puis lancez l'application :

```powershell
dist\Photobooth\Photobooth.exe
```

Si vous construisez depuis les sources sous Windows :

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-build.txt
python build.py
```

## 📖 Documentation

- **[Guide d'installation](docs/INSTALLATION.md)** - Installation détaillée et configuration
- **[Guide de compilation](docs/BUILD.md)** - Compilation en exécutable
- **[Architecture](docs/ARCHITECTURE.md)** - Structure et design de l'application
- **[Guide de développement](docs/DEVELOPMENT.md)** - Contribution et développement
- **[Guide des cadres](docs/FRAMES.md)** - Création et gestion des cadres photo

## 🎯 Cas d'usage

- Événements (mariages, anniversaires, fêtes)
- Salons professionnels et stands
- Centres commerciaux
- Espaces de coworking
- Installations artistiques interactives

## 🔐 Sécurité

- Configuration stockée localement
- Support OAuth2 pour OneDrive
- TLS/SSL pour les emails
- Pas de collecte de données externes

## 📝 Licence

MIT License - voir le fichier LICENSE pour plus de détails

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez le [guide de développement](docs/DEVELOPMENT.md) pour commencer.

## 📞 Support

- 📫 Issues GitHub pour les bugs et demandes de fonctionnalités
- 📖 Documentation dans le dossier `docs/`

## ✨ Roadmap

- [ ] Support multi-langues
- [ ] Thème sombre
- [ ] Filtres photo en temps réel
- [ ] Mode GIF/Boomerang
- [ ] Partage réseaux sociaux
- [ ] Mode galerie
- [x] Support macOS
