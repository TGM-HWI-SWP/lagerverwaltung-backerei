"""UI Layer - Graphical User Interface

Re-exportiert die Klassen aus den UI-Modulen, damit
`from src.ui import main` und `from src.ui.main_window import WarehouseMainWindow`
konsistent funktionieren.
"""

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from .main_window import WarehouseMainWindow
from .dialogs import ProductDialogWindow, StockDialog

__all__ = ["WarehouseMainWindow", "ProductDialogWindow", "StockDialog", "main"]


def main():
    """Starte die Lagerverwaltungsanwendung"""
    app = QApplication(sys.argv)

    # QSS-Stylesheet laden
    style_path = Path(__file__).parent / "style.qss"
    if style_path.exists():
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))

    window = WarehouseMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
