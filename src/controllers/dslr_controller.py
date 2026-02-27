"""DSLR camera controller using gphoto2 subprocess."""
import os
import platform
import subprocess
import tempfile
from datetime import datetime
from typing import List, Optional, Tuple

import numpy as np
from PIL import Image

from src.models.photo import Photo

# Suppress console window on Windows when spawning gphoto2
_CREATION_FLAGS = getattr(subprocess, "CREATE_NO_WINDOW", 0)


class DSLRController:
    """Controls a DSLR camera via the gphoto2 command-line tool.

    Supports any camera recognised by gphoto2 (including Olympus E-500).
    Requires gphoto2 to be installed and on PATH, or a full path provided.
    """

    def __init__(self, gphoto2_path: str = "gphoto2"):
        self.gphoto2_path = gphoto2_path or "gphoto2"
        self.is_active = False
        self.last_error: str = ""

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                     #
    # ------------------------------------------------------------------ #

    def _run(self, args: list, timeout: int = 15) -> subprocess.CompletedProcess:
        cmd = [self.gphoto2_path] + args
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=_CREATION_FLAGS,
        )

    # ------------------------------------------------------------------ #
    #  Controller interface (mirrors CameraController)                      #
    # ------------------------------------------------------------------ #

    def start(self) -> bool:
        """Verify gphoto2 is accessible and at least one camera is detected."""
        try:
            result = self._run(["--auto-detect"], timeout=10)
            cameras = self._parse_camera_list(result.stdout)
            self.is_active = len(cameras) > 0
            if not self.is_active:
                self.last_error = "Aucun appareil détecté par gphoto2"
            return self.is_active
        except FileNotFoundError:
            self.last_error = f"gphoto2 introuvable : {self.gphoto2_path}"
            return False
        except subprocess.TimeoutExpired:
            self.last_error = "gphoto2 n'a pas répondu (timeout)"
            return False
        except Exception as e:
            self.last_error = str(e)
            return False

    def stop(self) -> None:
        self.is_active = False

    def get_frame(self) -> Optional[np.ndarray]:
        """Capture a live-view preview frame from the camera."""
        tmp = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                tmp = f.name
            self._run(
                ["--capture-preview", f"--filename={tmp}", "--force-overwrite"],
                timeout=10,
            )
            if tmp and os.path.exists(tmp) and os.path.getsize(tmp) > 0:
                img = Image.open(tmp).convert("RGB")
                return np.array(img)
        except Exception as e:
            print(f"[DSLRController] preview error: {e}")
        finally:
            if tmp and os.path.exists(tmp):
                os.unlink(tmp)
        return None

    def capture_photo(self, frame_path: Optional[str] = None) -> Optional[Photo]:
        """Trigger the shutter, download the full-resolution image."""
        tmp = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                tmp = f.name
            result = self._run(
                ["--capture-image-and-download", f"--filename={tmp}", "--force-overwrite"],
                timeout=30,
            )
            if tmp and os.path.exists(tmp) and os.path.getsize(tmp) > 0:
                img = Image.open(tmp).convert("RGB")
                return Photo(
                    image_data=np.array(img),
                    timestamp=datetime.now(),
                    frame_path=frame_path,
                )
            self.last_error = result.stderr.strip() or "Aucun fichier reçu"
        except subprocess.TimeoutExpired:
            self.last_error = "Délai dépassé lors de la capture"
        except Exception as e:
            self.last_error = str(e)
            print(f"[DSLRController] capture error: {e}")
        finally:
            if tmp and os.path.exists(tmp):
                os.unlink(tmp)
        return None

    # ------------------------------------------------------------------ #
    #  Utilities                                                            #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_camera_list(stdout: str) -> List[str]:
        """Extract camera entries from gphoto2 --auto-detect output."""
        lines = stdout.strip().splitlines()
        # Skip header lines (Model / Port / -----)
        cameras = []
        for line in lines:
            stripped = line.strip()
            if stripped and "-----" not in stripped and "Model" not in stripped and "Port" not in stripped:
                cameras.append(stripped)
        return cameras

    @classmethod
    def detect_cameras(cls, gphoto2_path: str = "gphoto2") -> List[str]:
        """Return list of detected camera model strings."""
        try:
            result = subprocess.run(
                [gphoto2_path, "--auto-detect"],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=_CREATION_FLAGS,
            )
            return cls._parse_camera_list(result.stdout)
        except Exception:
            return []

    def __del__(self):
        self.stop()
