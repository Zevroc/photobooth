# Photobooth - Version Exécutable

Bienvenue dans Photobooth ! Cette version compilée ne nécessite pas l'installation de Python.

## 🚀 Démarrage Rapide

1. **Lancez l'application** : Double-cliquez sur `Photobooth.exe`
2. **Configuration initiale** :
   - Accédez à "⚙ Administration"
   - Configurez votre caméra
   - Ajoutez des cadres dans `assets/frames/` (PNG avec transparence)
   - Configurez les options de partage (optionnel)

## 📁 Structure des Fichiers

```
Photobooth/
├── Photobooth.exe          # L'application (à lancer)
├── _internal/               # Dépendances (ne pas modifier)
├── assets/
│   ├── frames/             # Vos cadres photo (PNG)
│   ├── photos/             # Photos enregistrées
│   └── temp/               # Fichiers temporaires
├── config/
│   └── config.json         # Configuration (créé au premier lancement)
└── src/                    # Code source compilé
```

## 🎨 Ajouter des Cadres

1. Créez ou téléchargez des images PNG avec transparence
2. Placez-les dans le dossier `assets/frames/`
3. Redémarrez l'application ou rechargez depuis l'administration

Format recommandé :
- **Format** : PNG avec canal alpha (transparence)
- **Taille** : 1920x1080 ou plus
- **Zone transparente** : Là où la photo doit apparaître

## ⚙️ Configuration

### Caméra
- Sélectionnez votre caméra dans l'administration
- Ajustez la résolution si nécessaire
- Testez la capture avant utilisation

### OneDrive (Optionnel)
- Activez dans l'administration
- Connectez-vous avec votre compte Microsoft
- Les photos seront uploadées automatiquement

### Email (Optionnel)
- Configurez votre serveur SMTP
- Utilisez un mot de passe d'application pour Gmail
- Les photos peuvent être envoyées aux invités

### Impression (Optionnel)
- Sélectionnez votre imprimante
- Choisissez le format papier
- Testez l'impression avant l'événement

## 🔧 Dépannage

### L'application ne démarre pas
- Vérifiez que tous les fichiers sont présents
- Ne déplacez pas l'exécutable hors de son dossier
- Vérifiez les autorisations Windows Defender

### La caméra ne fonctionne pas
- Vérifiez que la caméra est branchée
- Fermez les autres applications utilisant la caméra
- Essayez un autre ID de caméra dans l'administration

### Problèmes d'impression
- Vérifiez que l'imprimante est allumée et connectée
- Vérifiez les pilotes de l'imprimante
- Testez l'impression depuis une autre application

### OneDrive ne se connecte pas
- Vérifiez votre connexion internet
- Vérifiez vos identifiants OneDrive
- Consultez les logs dans config/

## 📝 Licence

MIT License - Cette application est gratuite et open source.

## 🔗 Plus d'Informations

- Code source : https://github.com/Zevroc/photobooth
- Documentation : Voir le dossier `docs/` du repository
- Signaler un bug : GitHub Issues

## ✨ Conseils d'Utilisation

- **Testez avant l'événement** : Vérifiez tous les paramètres
- **Préparez vos cadres** : Ayez plusieurs options
- **Espace de stockage** : Assurez-vous d'avoir assez d'espace
- **Sauvegarde** : Copiez régulièrement le dossier `assets/photos/`
- **Alimentation** : Branchez le PC sur secteur
- **Mode plein écran** : Appuyez sur F11 pour le mode plein écran (si supporté)

Bon événement ! 📷✨
