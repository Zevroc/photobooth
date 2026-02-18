# 🚀 Quick Start Guide

Get your photobooth up and running in minutes!

## ⚡ Fast Setup (3 steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Configure (Optional)
Click "⚙ Administration" in the app to configure camera, frames, and sharing options.

## 📸 First Photo

1. **Select a Frame** (or "Sans Cadre" for no frame)
2. Click **"Commencer ➔"**
3. Click **"📷 Prendre la Photo"**
4. Smile! 😊 (3 second countdown)
5. **Preview** your photo
6. Choose to save, email, upload, or print!

## 🎨 Add Custom Frames

1. Create a PNG image with transparency (1920x1080 recommended)
2. Save it in `assets/frames/`
3. Restart the app or reload from Admin panel

See [docs/FRAMES.md](docs/FRAMES.md) for detailed frame creation guide.

## ⚙️ Configuration Options

### Camera Settings
- Select camera device
- Set resolution (1920x1080, 1280x720, or 640x480)

### OneDrive Integration
1. Create an Azure AD application
2. Get Client ID and Tenant ID
3. Enter in Admin > OneDrive tab
4. Enable OneDrive uploads

### Email Settings
1. Enter SMTP server details
2. For Gmail: use App Password (not your regular password)
3. Enable email in Admin panel

### Printer Settings
1. Install printer drivers
2. Select printer in Admin panel
3. Choose paper size

## 🐛 Troubleshooting

### Camera doesn't work
- Check camera is connected
- Try different camera ID in Admin settings
- Make sure no other app is using the camera

### Dependencies installation fails
```bash
# Update pip first
python -m pip install --upgrade pip

# Install dependencies one by one if needed
pip install PyQt6
pip install opencv-python
pip install Pillow
```

### Application won't start
- Verify Python 3.8+ is installed: `python --version`
- Check all dependencies are installed
- Run setup script: `python setup.py`

## 📚 More Information

- **Full Installation Guide**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Architecture & Design**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Development Guide**: [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
- **Frame Creation**: [docs/FRAMES.md](docs/FRAMES.md)

## 💡 Tips

- Use **touchscreen** for best experience
- Create multiple frames for variety
- Test camera before your event
- Save photos are in `assets/photos/`
- Configuration is saved in `config/config.json`

## 🎉 Ready to Go!

Your photobooth is ready for:
- ✅ Weddings & Parties
- ✅ Corporate Events
- ✅ Trade Shows
- ✅ Marketing Activations
- ✅ Fun with Friends!

**Have fun! 📷✨**
