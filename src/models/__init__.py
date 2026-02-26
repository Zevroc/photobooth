"""Configuration models and management."""
import json
import os
from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class CameraConfig:
    """Camera configuration."""
    device_id: int = 0
    device_name: str = "Default Camera"
    resolution_width: int = 1920
    resolution_height: int = 1080
    fps: int = 30


@dataclass
class EmailConfig:
    """Email configuration."""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = ""
    sender_password: str = ""
    use_tls: bool = True
    enabled: bool = False


@dataclass
class PrinterConfig:
    """Printer configuration."""
    printer_name: str = ""
    enabled: bool = False
    paper_size: str = "A4"


@dataclass
class ButtonsConfig:
    """Button image configuration."""
    capture_normal: str = ""
    capture_pressed: str = ""
    choose_frame_normal: str = ""
    choose_frame_pressed: str = ""
    gallery_normal: str = ""
    gallery_pressed: str = ""
    capture_mode: str = "image"


@dataclass
class AppConfig:
    """Application configuration."""
    camera: CameraConfig
    email: EmailConfig
    printer: PrinterConfig
    buttons: ButtonsConfig
    available_frames: List[str]
    save_to_disk: bool = True
    photos_directory: str = "assets/photos"
    shutter_sound_path: str = "assets/sounds/shutter.wav"
    countdown_sound_path: str = "assets/sounds/beep.wav"
    home_title: str = "Bienvenue au Photobooth!"
    home_subtitle: str = "Choisissez votre cadre préféré"
    preview_title: str = "Votre Photo!"
    home_start_button_text: str = "Commencer ➔"
    start_fullscreen: bool = True
    show_no_frame_option: bool = True
    last_selected_frame: str = ""
    
    @classmethod
    def load(cls, config_path: str = "config/config.json") -> "AppConfig":
        """Load configuration from file."""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
                return cls(
                    camera=CameraConfig(**data.get('camera', {})),
                    email=EmailConfig(**data.get('email', {})),
                    printer=PrinterConfig(**data.get('printer', {})),
                    buttons=ButtonsConfig(**data.get('buttons', {})),
                    available_frames=data.get('available_frames', []),
                    save_to_disk=data.get('save_to_disk', True),
                    photos_directory=data.get('photos_directory', 'assets/photos'),
                    shutter_sound_path=data.get('shutter_sound_path', 'assets/sounds/shutter.wav'),
                    countdown_sound_path=data.get('countdown_sound_path', 'assets/sounds/beep.wav'),
                    home_title=data.get('home_title', 'Bienvenue au Photobooth!'),
                    home_subtitle=data.get('home_subtitle', 'Choisissez votre cadre préféré'),
                    preview_title=data.get('preview_title', 'Votre Photo!'),
                    home_start_button_text=data.get('home_start_button_text', 'Commencer ➔'),
                    start_fullscreen=data.get('start_fullscreen', True),
                    show_no_frame_option=data.get('show_no_frame_option', True),
                    last_selected_frame=data.get('last_selected_frame', '')
                )
        else:
            # Return default configuration
            return cls(
                camera=CameraConfig(),
                email=EmailConfig(),
                printer=PrinterConfig(),
                buttons=ButtonsConfig(),
                available_frames=[],
                save_to_disk=True,
                photos_directory='assets/photos',
                shutter_sound_path='assets/sounds/shutter.wav',
                countdown_sound_path='assets/sounds/beep.wav',
                home_title='Bienvenue au Photobooth!',
                home_subtitle='Choisissez votre cadre préféré',
                preview_title='Votre Photo!',
                home_start_button_text='Commencer ➔',
                start_fullscreen=True,
                show_no_frame_option=True,
                last_selected_frame=''
            )
    
    def save(self, config_path: str = "config/config.json") -> None:
        """Save configuration to file."""
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump({
                'camera': asdict(self.camera),
                'email': asdict(self.email),
                'printer': asdict(self.printer),
                'buttons': asdict(self.buttons),
                'available_frames': self.available_frames,
                'save_to_disk': self.save_to_disk,
                'photos_directory': self.photos_directory,
                'shutter_sound_path': self.shutter_sound_path,
                'countdown_sound_path': self.countdown_sound_path,
                'home_title': self.home_title,
                'home_subtitle': self.home_subtitle,
                'preview_title': self.preview_title,
                'home_start_button_text': self.home_start_button_text,
                'start_fullscreen': self.start_fullscreen,
                'show_no_frame_option': self.show_no_frame_option,
                'last_selected_frame': self.last_selected_frame
            }, f, indent=4)
