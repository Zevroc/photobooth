"""Tests for PrinterController: macOS CUPS path and Windows/disabled paths."""
from unittest.mock import patch, MagicMock
import pytest

from src.controllers.printer_controller import PrinterController


# --- print_photo disabled / missing file ---

def test_print_disabled(tmp_path):
    ctrl = PrinterController(enabled=False)
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"fake")
    assert ctrl.print_photo(str(photo)) is False


def test_print_missing_file():
    ctrl = PrinterController(enabled=True)
    assert ctrl.print_photo("/nonexistent/photo.jpg") is False


def test_print_unsupported_platform_returns_false(tmp_path):
    ctrl = PrinterController(enabled=True)
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"fake")
    with patch("sys.platform", "linux"):
        assert ctrl.print_photo(str(photo)) is False


# --- macOS (lp command) ---

def test_print_macos_calls_lp(tmp_path):
    ctrl = PrinterController(printer_name="TestPrinter", enabled=True, paper_size="A4")
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"fake")

    with patch("sys.platform", "darwin"), \
         patch("src.controllers.printer_controller.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = ctrl.print_photo(str(photo))

    assert result is True
    cmd = mock_run.call_args[0][0]
    assert cmd[0] == "lp"
    assert "-d" in cmd
    assert "TestPrinter" in cmd


def test_print_macos_default_printer(tmp_path):
    """When printer_name is empty, -d flag must not appear."""
    ctrl = PrinterController(printer_name="", enabled=True, paper_size="A4")
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"fake")

    with patch("sys.platform", "darwin"), \
         patch("src.controllers.printer_controller.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        ctrl.print_photo(str(photo))

    cmd = mock_run.call_args[0][0]
    assert "-d" not in cmd


def test_print_macos_paper_size_media(tmp_path):
    """Paper size must be translated to a CUPS media= option."""
    ctrl = PrinterController(printer_name="", enabled=True, paper_size="4x6")
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"fake")

    with patch("sys.platform", "darwin"), \
         patch("src.controllers.printer_controller.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        ctrl.print_photo(str(photo))

    cmd = mock_run.call_args[0][0]
    assert any("media=" in arg for arg in cmd)


def test_print_macos_lp_error_returns_false(tmp_path):
    ctrl = PrinterController(printer_name="", enabled=True)
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"fake")

    with patch("sys.platform", "darwin"), \
         patch("src.controllers.printer_controller.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stderr="error")
        result = ctrl.print_photo(str(photo))

    assert result is False


# --- list_available_printers ---

def test_list_printers_macos_parses_lpstat():
    output = "printer HP_LaserJet is idle.\nprinter Canon_Selphy is idle.\n"
    with patch("sys.platform", "darwin"), \
         patch("src.controllers.printer_controller.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=output, returncode=0)
        printers = PrinterController.list_available_printers()

    assert "HP_LaserJet" in printers
    assert "Canon_Selphy" in printers


def test_list_printers_unsupported_platform():
    with patch("sys.platform", "linux"):
        assert PrinterController.list_available_printers() == []
