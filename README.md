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

Pour créer un fichier exécutable Windows (.exe) :

```bash
# Installer les dépendances de build
pip install -r requirements.txt

# Compiler l'application
python build.py
```

L'exécutable sera créé dans `dist/Photobooth/Photobooth.exe`

Pour plus de détails, consultez le **[Guide de Compilation](docs/BUILD.md)**

## 📖 Documentation

- **[Guide d'installation](docs/INSTALLATION.md)** - Installation détaillée et configuration
- **[Architecture](docs/ARCHITECTURE.md)** - Structure et design de l'application
- **[Guide de développement](docs/DEVELOPMENT.md)** - Contribution et développement

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
- [ ] Support Linux/macOS
