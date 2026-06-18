"""Tests for AppConfig load / save / roundtrip."""
import json
import os
import pytest

from src.models import AppConfig


def test_default_config_no_file(tmp_path):
    """Loading from a non-existent path returns sensible defaults."""
    cfg = AppConfig.load(str(tmp_path / "nonexistent.json"))
    assert cfg.save_to_disk is True
    assert cfg.camera.resolution_width == 1920
    assert cfg.email.enabled is False
    assert cfg.printer.paper_size == "A4"
    assert cfg.available_frames == []


def test_save_and_load_roundtrip(tmp_path):
    path = str(tmp_path / "config.json")
    cfg = AppConfig.load(path)
    cfg.home_title = "Mon Photobooth"
    cfg.camera.device_id = 2
    cfg.email.smtp_server = "smtp.test.com"
    cfg.printer.paper_size = "4x6"
    cfg.save(path)

    reloaded = AppConfig.load(path)
    assert reloaded.home_title == "Mon Photobooth"
    assert reloaded.camera.device_id == 2
    assert reloaded.email.smtp_server == "smtp.test.com"
    assert reloaded.printer.paper_size == "4x6"


def test_load_ignores_unknown_keys(tmp_path):
    """Extra keys in the JSON file are silently ignored."""
    path = str(tmp_path / "config.json")
    with open(path, "w") as f:
        json.dump({
            "camera": {"device_id": 3, "future_key": "ignored"},
            "email": {},
            "printer": {},
            "buttons": {},
            "available_frames": [],
        }, f)

    cfg = AppConfig.load(path)
    assert cfg.camera.device_id == 3


def test_config_creates_parent_directory(tmp_path):
    path = str(tmp_path / "subdir" / "config.json")
    AppConfig.load().save(path)
    assert os.path.exists(path)


def test_last_selected_frame_default(tmp_path):
    cfg = AppConfig.load(str(tmp_path / "x.json"))
    assert cfg.last_selected_frame == ""
