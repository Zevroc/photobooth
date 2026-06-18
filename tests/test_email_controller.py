"""Tests for EmailController with a mocked SMTP server."""
import smtplib
from unittest.mock import patch, MagicMock
import pytest

from src.controllers.email_controller import EmailController


@pytest.fixture
def ctrl():
    return EmailController(
        smtp_server="smtp.example.com",
        smtp_port=587,
        sender_email="sender@example.com",
        sender_password="secret",
        use_tls=True,
        enabled=True,
    )


def _mock_smtp():
    """Return a context-manager mock for smtplib.SMTP."""
    server = MagicMock()
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=server)
    cm.__exit__ = MagicMock(return_value=False)
    return cm, server


# --- send_photo ---

def test_send_photo_disabled(tmp_path):
    ctrl = EmailController(enabled=False)
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"fake")
    assert ctrl.send_photo("x@x.com", str(photo)) is False


def test_send_photo_missing_file(ctrl):
    assert ctrl.send_photo("x@x.com", "/nonexistent/photo.jpg") is False


def test_send_photo_success(ctrl, tmp_path):
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"\xff\xd8\xff" + b"\x00" * 100)
    cm, server = _mock_smtp()

    with patch("src.controllers.email_controller.smtplib.SMTP", return_value=cm):
        result = ctrl.send_photo("dest@example.com", str(photo))

    assert result is True
    server.starttls.assert_called_once()
    server.login.assert_called_once_with("sender@example.com", "secret")
    server.send_message.assert_called_once()


def test_send_photo_no_tls(tmp_path):
    ctrl = EmailController(
        smtp_server="smtp.example.com", smtp_port=25,
        sender_email="s@x.com", sender_password="pw",
        use_tls=False, enabled=True,
    )
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"fake")
    cm, server = _mock_smtp()

    with patch("src.controllers.email_controller.smtplib.SMTP", return_value=cm):
        ctrl.send_photo("dest@x.com", str(photo))

    server.starttls.assert_not_called()


def test_send_photo_smtp_error_returns_false(ctrl, tmp_path):
    photo = tmp_path / "p.jpg"
    photo.write_bytes(b"fake")
    with patch("src.controllers.email_controller.smtplib.SMTP",
               side_effect=smtplib.SMTPException("boom")):
        assert ctrl.send_photo("dest@x.com", str(photo)) is False


# --- test_connection ---

def test_connection_no_credentials():
    ctrl = EmailController(smtp_server="smtp.x.com", smtp_port=587)
    ok, msg = ctrl.test_connection()
    assert ok is False
    assert "non configurés" in msg


def test_connection_success():
    ctrl = EmailController(
        smtp_server="smtp.example.com", smtp_port=587,
        sender_email="s@x.com", sender_password="pw",
        use_tls=True, enabled=True,
    )
    cm, server = _mock_smtp()
    with patch("src.controllers.email_controller.smtplib.SMTP", return_value=cm):
        ok, msg = ctrl.test_connection()
    assert ok is True
    assert "succès" in msg
