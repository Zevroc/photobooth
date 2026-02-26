"""Printer controller for printing photos."""
import os
import sys


# Windows paper size constants (DMPAPER_*)
_PAPER_CONSTANTS = {
    "A4":      9,    # 210 x 297 mm
    "Letter":  1,    # 8.5 x 11 in
    "4x6":    256,   # 101.6 x 152.4 mm  (custom)
    "10x15":  256,   # 100 x 150 mm      (custom)
    "5x7":    256,   # 127 x 178 mm      (custom)
    "100x148": 256,  # 100 x 148 mm      (custom – postcard)
}

# Custom paper dimensions in units of 0.1 mm  (width, height)
_PAPER_DIMENSIONS_01MM = {
    "4x6":     (1016, 1524),
    "10x15":   (1000, 1500),
    "5x7":     (1270, 1778),
    "100x148": (1000, 1480),
}


class PrinterController:
    """Manages photo printing."""

    def __init__(self, printer_name: str = "", enabled: bool = False, paper_size: str = "A4"):
        """Initialize printer controller.

        Args:
            printer_name: Name of the printer
            enabled: Whether printing is enabled
            paper_size: Paper size identifier (A4, Letter, 4x6, 10x15, 5x7, 100x148)
        """
        self.printer_name = printer_name
        self.enabled = enabled
        self.paper_size = paper_size

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def print_photo(self, photo_path: str) -> bool:
        """Print a photo.

        Args:
            photo_path: Path to photo file

        Returns:
            True if print successful, False otherwise
        """
        if not self.enabled or not os.path.exists(photo_path):
            return False

        try:
            if sys.platform == "win32":
                return self._print_windows(photo_path)
            else:
                print(f"Printing not supported on {sys.platform}")
                return False
        except Exception as e:
            print(f"Error printing photo: {e}")
            return False

    @staticmethod
    def list_available_printers():
        """List all available printers.

        Returns:
            List of printer names
        """
        try:
            if sys.platform == "win32":
                import win32print
                return [p[2] for p in win32print.EnumPrinters(2)]
            return []
        except ImportError:
            return []
        except Exception as e:
            print(f"Error listing printers: {e}")
            return []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_paper_size_constant(self) -> int:
        """Return the DMPAPER_* constant for the configured paper size."""
        return _PAPER_CONSTANTS.get(self.paper_size, 9)

    def _apply_paper_size_to_devmode(self, devmode) -> None:
        """Adjust a DEVMODE structure for the configured paper size (in-place)."""
        try:
            devmode.PaperSize = self._get_paper_size_constant()
            dims = _PAPER_DIMENSIONS_01MM.get(self.paper_size)
            if dims:
                devmode.PaperWidth = dims[0]
                devmode.PaperLength = dims[1]
        except Exception as e:
            print(f"Could not set DevMode paper size: {e}")

    def _print_windows(self, photo_path: str) -> bool:
        """Print a photo on Windows using GDI (win32ui + win32print + PIL).

        The image is scaled to fill the printable area while preserving the
        aspect ratio and centred on the page.

        Args:
            photo_path: Absolute path to the photo file.

        Returns:
            True if the print job was submitted successfully.
        """
        try:
            import win32print
            import win32ui
            import win32con
            from PIL import Image, ImageWin
        except ImportError as exc:
            print(f"Printing dependencies not available: {exc}")
            return False

        try:
            printer_name = self.printer_name or win32print.GetDefaultPrinter()

            # --- Retrieve and adjust DEVMODE ---
            hprinter = win32print.OpenPrinter(printer_name)
            try:
                printer_info = win32print.GetPrinter(hprinter, 2)
                devmode = printer_info.get("pDevMode")
            finally:
                win32print.ClosePrinter(hprinter)

            if devmode is not None:
                self._apply_paper_size_to_devmode(devmode)

            # --- Create a printer DC ---
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_name)

            if devmode is not None:
                try:
                    hdc.ResetDC(devmode)
                except Exception as e:
                    print(f"ResetDC warning (non-fatal): {e}")

            # --- Get printable area ---
            printable_w = hdc.GetDeviceCaps(win32con.HORZRES)
            printable_h = hdc.GetDeviceCaps(win32con.VERTRES)

            # --- Load and scale image ---
            img = Image.open(photo_path).convert("RGB")
            img_w, img_h = img.size

            ratio = min(printable_w / img_w, printable_h / img_h)
            new_w = int(img_w * ratio)
            new_h = int(img_h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)

            # --- Centre on page ---
            x = (printable_w - new_w) // 2
            y = (printable_h - new_h) // 2

            # --- Submit print job ---
            hdc.StartDoc(os.path.basename(photo_path))
            hdc.StartPage()

            dib = ImageWin.Dib(img)
            dib.draw(hdc.GetHandleOutput(), (x, y, x + new_w, y + new_h))

            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()
            return True

        except Exception as e:
            print(f"Windows printing error: {e}")
            return False
