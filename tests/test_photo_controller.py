"""Tests for PhotoController: save, apply_frame, thumbnail."""
import os
import numpy as np
import pytest
from PIL import Image


def test_save_photo_creates_file(photo_controller, sample_photo):
    path = photo_controller.save_photo(sample_photo, "test.jpg")
    assert os.path.exists(path)
    assert path.endswith(".jpg")


def test_save_photo_correct_dimensions(photo_controller, sample_photo):
    path = photo_controller.save_photo(sample_photo, "dim.jpg")
    img = Image.open(path)
    assert img.size == (640, 480)


def test_save_photo_auto_filename(photo_controller, sample_photo):
    path = photo_controller.save_photo(sample_photo)
    assert os.path.exists(path)
    assert "photo_" in os.path.basename(path)


def test_apply_frame_missing_path(photo_controller, sample_photo):
    result = photo_controller.apply_frame(sample_photo, "/nonexistent/frame.png")
    assert result.frame_applied is False


def test_apply_frame_empty_path(photo_controller, sample_photo):
    result = photo_controller.apply_frame(sample_photo, "")
    assert result.frame_applied is False


def test_apply_frame_sets_flag(photo_controller, sample_photo, frame_png):
    result = photo_controller.apply_frame(sample_photo, frame_png)
    assert result.frame_applied is True
    assert result.frame_path == frame_png


def test_apply_frame_preserves_shape(photo_controller, sample_photo, frame_png):
    """Output must have the same (h, w) as the frame, in RGB."""
    result = photo_controller.apply_frame(sample_photo, frame_png)
    assert result.image_data.shape == (480, 640, 3)


def test_apply_frame_composites_correctly(photo_controller, frame_png):
    """Border pixels show frame colour; transparent centre shows photo colour."""
    blue = np.full((480, 640, 3), [0, 0, 255], dtype=np.uint8)
    result = photo_controller.apply_frame_to_array(blue, frame_png)
    # Centre pixel (transparent frame) → stays blue
    assert result[240, 320, 2] > 200
    # Corner pixel (opaque red frame) → becomes red
    assert result[5, 5, 0] > 200


def test_apply_frame_to_array_none_image(photo_controller, frame_png):
    result = photo_controller.apply_frame_to_array(None, frame_png)
    assert result is None


def test_apply_frame_preview_keeps_camera_resolution(photo_controller, sample_image, frame_png):
    """Preview overlay must not change the camera feed dimensions."""
    result = photo_controller.apply_frame_to_array_preview(sample_image, frame_png)
    assert result.shape == sample_image.shape


def test_get_thumbnail_fits_target(photo_controller, sample_photo):
    thumb = photo_controller.get_photo_thumbnail(sample_photo, size=(150, 100))
    h, w = thumb.shape[:2]
    assert w <= 150
    assert h <= 100
