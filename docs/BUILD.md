# Guide de Compilation en Exécutable

Ce guide explique comment compiler l'application Photobooth en un fichier exécutable Windows (.exe).

## 📋 Prérequis

- Python 3.8 ou supérieur installé
- Toutes les dépendances de l'application installées
- PyInstaller (installé automatiquement avec les requirements)

## 🚀 Compilation Rapide

### Méthode 1 : Script de Build Automatique (Recommandé)

Le moyen le plus simple de compiler l'application est d'utiliser le script de build fourni :

```bash
# 1. Installer les dépendances de build
pip install -r requirements.txt

# 2. Exécuter le script de build
python build.py
```

Le script va :
- ✓ Vérifier que PyInstaller est installé
- ✓ Nettoyer les builds précédents
- ✓ Compiler l'application
- ✓ Vérifier que l'exécutable a été créé avec succès

### Méthode 2 : Compilation Manuelle avec PyInstaller

Si vous préférez contrôler manuellement le processus :

```bash
# 1. Installer PyInstaller
pip install pyinstaller

# 2. Compiler avec le fichier spec
pyinstaller photobooth.spec --clean
```

## 📦 Résultat de la Compilation

Après la compilation, vous trouverez :

```
dist/
└── Photobooth/
    ├── Photobooth.exe          # L'exécutable principal
    ├── _internal/               # Dépendances et bibliothèques
    ├── assets/                  # Assets de l'application
    ├── config/                  # Configuration
    └── src/                     # Code source Python compilé
```

## 🎯 Distribution de l'Application

Pour distribuer l'application compilée :

1. **Copier le dossier complet** `dist/Photobooth/` vers un autre emplacement ou créer une archive
2. **Tous les fichiers sont nécessaires** - ne copiez pas seulement l'exécutable
3. **Ajoutez vos cadres** dans `assets/frames/` si nécessaire

### Création d'une Archive de Distribution

```bash
# Windows PowerShell
Compress-Archive -Path dist\Photobooth -DestinationPath Photobooth-v1.0.0.zip

# Ou avec 7-Zip (si installé)
7z a Photobooth-v1.0.0.zip dist\Photobooth\
```

## ⚙️ Configuration du Build

### Fichier photobooth.spec

Le fichier `photobooth.spec` contrôle le processus de compilation. Vous pouvez le personnaliser :

```python
# Pour ajouter un icône :
exe = EXE(
    ...
    icon='assets/icon.ico',  # Décommentez et ajoutez votre icône
)

# Pour créer un exécutable unique (sans dossier) :
# Changez exclude_binaries=True à exclude_binaries=False
# et déplacez la configuration dans exe au lieu de coll
```

### Options Avancées

**Mode Console** : Pour activer la console de debug :
```python
exe = EXE(
    ...
    console=True,  # Affiche une console pour le debug
)
```

**Optimisation UPX** : Pour réduire la taille (UPX doit être installé) :
```python
exe = EXE(
    ...
    upx=True,  # Déjà activé par défaut
)
```

## 🔍 Dépannage

### Problème : "PyInstaller n'est pas installé"

```bash
pip install pyinstaller
```

### Problème : "Module not found" lors de l'exécution

Si l'exécutable ne trouve pas certains modules :

1. Ajoutez le module à `hiddenimports` dans `photobooth.spec` :
```python
hiddenimports=[
    ...
    'votre_module_manquant',
],
```

2. Recompilez :
```bash
pyinstaller photobooth.spec --clean
```

### Problème : Fichiers manquants (assets, config)

Vérifiez que les dossiers sont inclus dans la section `datas` du spec :
```python
datas=[
    ('assets', 'assets'),
    ('config', 'config'),
    ('src', 'src'),
],
```

### Problème : L'exécutable est trop volumineux

Options pour réduire la taille :

1. **Installer UPX** pour la compression :
   - Télécharger depuis https://upx.github.io/
   - Ajouter au PATH système

2. **Exclure des modules inutiles** dans le spec :
```python
excludes=['tkinter', 'matplotlib'],  # Exemple
```

3. **Utiliser un exécutable unique** (peut être plus petit mais plus lent) :
```bash
pyinstaller --onefile main.py
```

## 📊 Taille Attendue

- **Version standard (dossier)** : ~150-250 MB
- **Version onefile** : ~100-180 MB
- Dépend des bibliothèques incluses (PyQt6, OpenCV, etc.)

## 🔒 Sécurité

L'exécutable compilé :
- ✓ Ne contient pas de code source lisible
- ✓ Inclut toutes les dépendances nécessaires
- ✓ Peut être distribué sans nécessiter Python
- ⚠️ Peut être détecté par certains antivirus (faux positif) - voir ci-dessous

### Note sur les Antivirus

Les exécutables PyInstaller peuvent parfois déclencher des faux positifs avec les antivirus. Pour minimiser ce risque :

1. **Signer l'exécutable** avec un certificat de code
2. **Soumettre à VirusTotal** pour analyse
3. **Contacter les fournisseurs d'antivirus** pour signaler le faux positif

## 🎨 Personnalisation

### Ajouter un Icône

1. Créez un fichier `.ico` (ou convertissez une image PNG)
2. Placez-le dans le projet (ex: `assets/icon.ico`)
3. Modifiez `photobooth.spec` :
```python
exe = EXE(
    ...
    icon='assets/icon.ico',
)
```

### Ajouter des Métadonnées de Version (Windows)

Créez un fichier `version.txt` et ajoutez-le à la compilation avec l'option `--version-file`.

## 📝 Checklist Avant Distribution

- [ ] Testez l'exécutable sur une machine Windows propre (sans Python)
- [ ] Vérifiez que tous les assets sont présents (frames, config)
- [ ] Testez toutes les fonctionnalités principales
- [ ] Vérifiez la caméra, l'impression, OneDrive, email
- [ ] Créez une documentation utilisateur
- [ ] Créez une archive de distribution
- [ ] Testez l'installation depuis l'archive

## 📚 Ressources Supplémentaires

- [Documentation PyInstaller](https://pyinstaller.org/)
- [Guide des Spec Files](https://pyinstaller.readthedocs.io/en/stable/spec-files.html)
- [Optimisation et Dépannage](https://pyinstaller.readthedocs.io/en/stable/when-things-go-wrong.html)

## 💡 Conseils de Production

1. **Versionnez vos builds** : Utilisez un numéro de version dans le nom du fichier
2. **Testez sur différentes versions de Windows** : Windows 10, 11, etc.
3. **Documentez les dépendances système** : Caméra, imprimante, connexion internet
4. **Créez un installateur** : Utilisez Inno Setup ou NSIS pour un installateur professionnel
5. **Automatisez avec CI/CD** : GitHub Actions peut compiler automatiquement les releases

## 🤝 Support

En cas de problème :
- Consultez les logs de PyInstaller dans le dossier `build/`
- Activez le mode console pour voir les erreurs
- Vérifiez les issues GitHub du projet
- Consultez la documentation PyInstaller
