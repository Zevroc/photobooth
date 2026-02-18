# Guide de Développement

## 🛠️ Configuration de l'environnement de développement

### Prérequis
- Python 3.8+
- Git
- Visual Studio Code (recommandé) ou autre IDE

### Installation pour le développement
```bash
# Cloner le repository
git clone https://github.com/Zevroc/photobooth.git
cd photobooth

# Créer et activer l'environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Installer les outils de développement (optionnel)
pip install pylint black pytest
```

## 📁 Structure du code

### Models (`src/models/`)
Contient les classes de données et la configuration.

**Fichiers principaux:**
- `__init__.py`: Classes de configuration (AppConfig, CameraConfig, etc.)
- `photo.py`: Classe Photo

**Responsabilités:**
- Définir la structure des données
- Sérialisation/désérialisation JSON
- Validation des données

### Controllers (`src/controllers/`)
Contient la logique métier de l'application.

**Fichiers:**
- `camera_controller.py`: Gestion de la caméra
- `photo_controller.py`: Traitement des photos
- `onedrive_controller.py`: Upload OneDrive
- `email_controller.py`: Envoi d'emails
- `printer_controller.py`: Impression

**Responsabilités:**
- Interaction avec le matériel
- Logique métier
- API externes

### Views (`src/views/`)
Contient les interfaces utilisateur PyQt6.

**Fichiers:**
- `home_screen.py`: Écran d'accueil
- `capture_screen.py`: Capture photo
- `preview_screen.py`: Prévisualisation
- `admin_screen.py`: Administration

**Responsabilités:**
- Affichage de l'interface
- Gestion des événements utilisateur
- Mise à jour de l'UI

## 🔄 Flux de données

```
User Input
    ↓
View (emit signal)
    ↓
Main App (slot)
    ↓
Controller (business logic)
    ↓
Model (data)
    ↓
Controller (process)
    ↓
View (update UI)
```

## 🎨 Conventions de code

### Style Python
- Suivre PEP 8
- Utiliser des docstrings pour toutes les fonctions/classes
- Type hints quand possible

```python
def capture_photo(self, frame_path: Optional[str] = None) -> Optional[Photo]:
    """Capture a photo from the camera.
    
    Args:
        frame_path: Optional path to a frame image to overlay
        
    Returns:
        Photo object or None if capture failed
    """
    # Implementation
```

### Nommage
- **Classes**: PascalCase (ex: `CameraController`)
- **Fonctions/méthodes**: snake_case (ex: `capture_photo`)
- **Constantes**: UPPER_CASE (ex: `DEFAULT_RESOLUTION`)
- **Fichiers**: snake_case (ex: `camera_controller.py`)

### Signals PyQt6
```python
# Déclarer les signals en haut de la classe
frame_selected = pyqtSignal(str)
photo_captured = pyqtSignal(Photo)

# Émettre un signal
self.frame_selected.emit(frame_path)

# Connecter un signal
self.home_screen.frame_selected.connect(self.on_frame_selected)
```

## 🧪 Tests

### Structure des tests
```
tests/
├── test_models.py
├── test_controllers.py
└── test_integration.py
```

### Exemple de test
```python
import pytest
from src.models.photo import Photo
import numpy as np
from datetime import datetime

def test_photo_creation():
    img_data = np.zeros((100, 100, 3), dtype=np.uint8)
    photo = Photo(
        image_data=img_data,
        timestamp=datetime.now()
    )
    assert photo.width == 100
    assert photo.height == 100
```

### Lancer les tests
```bash
pytest tests/
```

## 📝 Ajouter une nouvelle fonctionnalité

### 1. Créer le modèle (si nécessaire)
```python
# src/models/new_model.py
@dataclass
class NewModel:
    field1: str
    field2: int
```

### 2. Créer le controller
```python
# src/controllers/new_controller.py
class NewController:
    def __init__(self):
        pass
    
    def do_something(self):
        pass
```

### 3. Créer la vue
```python
# src/views/new_screen.py
from PyQt6.QtWidgets import QWidget

class NewScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Create UI
        pass
```

### 4. Intégrer dans main.py
```python
# main.py
from src.views.new_screen import NewScreen

class PhotoboothApp(QMainWindow):
    def __init__(self):
        # ...
        self.new_screen = NewScreen()
        self.stacked_widget.addWidget(self.new_screen)
```

## 🐛 Debugging

### Activer les logs
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Debug PyQt6
```python
# Afficher les widgets
print(self.stacked_widget.currentWidget())

# Lister tous les widgets
for i in range(self.stacked_widget.count()):
    print(self.stacked_widget.widget(i))
```

### Debug OpenCV
```python
# Afficher les propriétés de la caméra
cap = cv2.VideoCapture(0)
print(f"Width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
print(f"Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
print(f"FPS: {cap.get(cv2.CAP_PROP_FPS)}")
```

## 🔧 Outils utiles

### Formatage du code
```bash
# Formater avec black
black src/

# Vérifier avec pylint
pylint src/
```

### Git workflow
```bash
# Créer une branche
git checkout -b feature/nouvelle-fonctionnalite

# Commit
git add .
git commit -m "feat: ajouter nouvelle fonctionnalité"

# Push
git push origin feature/nouvelle-fonctionnalite
```

### Convention de commits
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage
- `refactor:` Refactoring
- `test:` Tests
- `chore:` Maintenance

## 📚 Ressources

### PyQt6
- [Documentation officielle](https://doc.qt.io/qtforpython/)
- [Tutoriels PyQt6](https://www.pythonguis.com/pyqt6-tutorial/)

### OpenCV
- [Documentation OpenCV](https://docs.opencv.org/)
- [Tutoriels OpenCV Python](https://opencv-python-tutroals.readthedocs.io/)

### Python
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Documentation](https://docs.python.org/3/)

## 🤝 Contribution

### Processus
1. Fork le repository
2. Créer une branche pour votre fonctionnalité
3. Faire vos modifications
4. Ajouter des tests
5. Soumettre une Pull Request

### Checklist PR
- [ ] Code formaté avec black
- [ ] Docstrings ajoutées
- [ ] Tests passent
- [ ] Documentation mise à jour
- [ ] Pas de warnings pylint

## 📞 Contact

Pour toute question technique:
- Ouvrir une issue GitHub
- Consulter la documentation
