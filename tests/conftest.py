"""Shared fixtures for all test modules."""
import numpy as np
import pytest
from datetime import datetime
from PIL import Image, ImageDraw

from src.models.photo import Photo
from src.controllers.photo_controller import PhotoController


@pytest.fixture
def sample_image():
    """640x480 solid-blue RGB array."""
    return np.full((480, 640, 3), [0, 0, 200], dtype=np.uint8)


@pytest.fixture
def sample_photo(sample_image):
    return Photo(image_data=sample_image, timestamp=datetime(2024, 1, 1, 12, 0, 0))


@pytest.fixture
def frame_png(tmp_path):
    """640x480 RGBA frame: 20 px opaque red border, transparent centre."""
    w, h = 640, 480
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w - 1, h - 1], fill=(255, 0, 0, 255))   # red fill
    draw.rectangle([20, 20, w - 21, h - 21], fill=(0, 0, 0, 0))   # punch transparent hole
    path = str(tmp_path / "frame.png")
    img.save(path)
    return path


@pytest.fixture
def photo_controller(tmp_path):
    return PhotoController(photos_directory=str(tmp_path / "photos"))
