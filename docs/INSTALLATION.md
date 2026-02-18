# Guide d'Installation et d'Utilisation

## 📋 Prérequis

### Système
- Windows 10/11 (recommandé pour support tactile complet)
- Python 3.8 ou supérieur
- Webcam intégrée ou externe (USB/WiFi)

### Matériel optionnel
- Écran tactile pour une meilleure expérience
- Imprimante pour impression directe
- Appareil photo externe pour meilleure qualité

## 🔧 Installation

### 1. Cloner le repository
```bash
git clone https://github.com/Zevroc/photobooth.git
cd photobooth
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 5. Lancer l'application
```bash
python main.py
```

## 🎯 Configuration

### Première utilisation

1. **Lancer l'application**
   ```bash
   python main.py
   ```

2. **Accéder au panel d'administration**
   - Cliquer sur le bouton "⚙ Administration" en bas à gauche

3. **Configurer la caméra**
   - Onglet "📷 Caméra"
   - Sélectionner la caméra à utiliser
   - Choisir la résolution (1920x1080 recommandé)

4. **Ajouter des cadres**
   - Placer vos images de cadres (PNG avec transparence) dans le dossier `assets/frames/`
   - Les cadres apparaîtront automatiquement dans l'écran d'accueil

5. **Configurer OneDrive (optionnel)**
   - Onglet "☁ OneDrive"
   - Activer OneDrive
   - Entrer le Client ID et Tenant ID de votre application Azure AD
   - Spécifier le dossier de destination

6. **Configurer l'email (optionnel)**
   - Onglet "📧 Email"
   - Activer Email
   - Entrer les paramètres SMTP
   - Pour Gmail, utiliser un mot de passe d'application

7. **Configurer l'imprimante (optionnel)**
   - Onglet "🖨 Imprimante"
   - Activer Impression
   - Sélectionner l'imprimante
   - Choisir le format papier

8. **Sauvegarder**
   - Cliquer sur "💾 Sauvegarder"

## 📸 Utilisation

### Prendre une photo

1. **Écran d'accueil**
   - Choisir un cadre parmi les options disponibles
   - Ou sélectionner "Sans Cadre"
   - Cliquer sur "Commencer ➔"

2. **Capture**
   - Se positionner devant la caméra
   - Cliquer sur "📷 Prendre la Photo"
   - Un compte à rebours de 3 secondes démarre
   - La photo est capturée automatiquement

3. **Prévisualisation**
   - Voir la photo avec le cadre appliqué
   - Options disponibles:
     - 📧 **Email**: Envoyer par email
     - ☁ **OneDrive**: Upload vers OneDrive
     - 🖨 **Imprimer**: Imprimer la photo
   - Cliquer sur "← Reprendre" pour refaire la photo
   - Cliquer sur "Terminé ✓" pour revenir à l'accueil

### Navigation

- **← Retour**: Revenir à l'écran précédent
- **⚙ Administration**: Accéder aux paramètres
- **Terminé ✓**: Terminer et revenir à l'accueil

## 🎨 Personnalisation

### Créer des cadres personnalisés

1. **Format d'image**
   - Format: PNG
   - Transparence: Oui (canal alpha)
   - Taille recommandée: 1920x1080 pixels

2. **Design**
   - Créer le cadre avec votre logiciel préféré (Photoshop, GIMP, etc.)
   - Laisser la zone centrale transparente pour la photo
   - Sauvegarder en PNG avec transparence

3. **Installation**
   - Copier le fichier dans `assets/frames/`
   - Redémarrer l'application ou recharger depuis Admin

### Exemple de structure de cadre
```
┌─────────────────────────┐
│   ┌─────────────┐      │  <- Bordure opaque
│   │             │      │
│   │ Transparent │      │  <- Zone pour la photo
│   │             │      │
│   └─────────────┘      │
│  Photobooth 2024       │  <- Texte/décorations
└─────────────────────────┘
```

## 🔐 Configuration OneDrive

### Créer une application Azure AD

1. Aller sur [Azure Portal](https://portal.azure.com)
2. Azure Active Directory > App registrations > New registration
3. Nom: "Photobooth"
4. Supported account types: Accounts in this organizational directory only
5. Redirect URI: Public client/native > http://localhost
6. Copier:
   - Application (client) ID
   - Directory (tenant) ID
7. API permissions > Add permission > Microsoft Graph > Delegated > Files.ReadWrite

### Configuration dans l'app
1. Administration > OneDrive
2. Coller Client ID et Tenant ID
3. Spécifier le chemin du dossier (ex: /Photos/Photobooth)
4. Sauvegarder

## 📧 Configuration Email

### Gmail
1. Activer l'authentification à 2 facteurs
2. Créer un mot de passe d'application:
   - Mon compte Google > Sécurité > Mots de passe d'application
3. Utiliser ce mot de passe dans la configuration

### Autres fournisseurs
- **Outlook**: smtp-mail.outlook.com:587
- **Yahoo**: smtp.mail.yahoo.com:587
- **Custom SMTP**: Utiliser les paramètres de votre fournisseur

## 🖨️ Configuration Imprimante

### Windows
1. Installer les pilotes de l'imprimante
2. Configurer l'imprimante dans Windows
3. Dans l'app, sélectionner l'imprimante dans la liste
4. Choisir le format papier approprié

### Formats supportés
- **A4**: Standard (210x297mm)
- **Letter**: US (216x279mm)
- **4x6**: Format photo (10x15cm)
- **5x7**: Format photo (13x18cm)

## 🚨 Dépannage

### La caméra ne fonctionne pas
- Vérifier que la caméra est connectée
- Vérifier les permissions dans Windows
- Essayer de changer l'ID de la caméra dans Admin

### Les cadres n'apparaissent pas
- Vérifier que les fichiers sont bien en PNG
- Vérifier qu'ils sont dans `assets/frames/`
- Relancer l'application

### L'email ne s'envoie pas
- Vérifier les paramètres SMTP
- Pour Gmail, utiliser un mot de passe d'application
- Vérifier la connexion Internet

### L'impression ne fonctionne pas
- Vérifier que pywin32 est installé
- Vérifier que l'imprimante est configurée dans Windows
- Vérifier que l'imprimante est en ligne

## 📝 Fichiers de log

Les erreurs sont affichées dans la console. Pour sauvegarder les logs:
```bash
python main.py > logs.txt 2>&1
```

## 🆘 Support

Pour obtenir de l'aide:
1. Consulter la documentation dans `docs/`
2. Vérifier les issues GitHub
3. Créer une nouvelle issue avec:
   - Description du problème
   - Système d'exploitation
   - Version de Python
   - Messages d'erreur

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
