"""UI Layer - Graphical User Interface

Re-exportiert die Klassen aus den UI-Modulen, damit
`from src.ui import main` und `from src.ui.main_window import WarehouseMainWindow`
konsistent funktionieren.
"""

import sys
import argparse
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from .main_window import WarehouseMainWindow
from .dialogs import ProductDialogWindow, StockDialog

__all__ = ["WarehouseMainWindow", "ProductDialogWindow", "StockDialog", "main"]


def main():
    """Starte die Lagerverwaltungsanwendung"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--repo", choices=["memory", "sqlite"], default="sqlite")
    parser.add_argument("--db", default="lagerverwaltung.db")
    args, _ = parser.parse_known_args()

    app = QApplication(sys.argv)

    # QSS-Stylesheet laden
    style_path = Path(__file__).parent / "style.qss"
    if style_path.exists():
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))

    window = WarehouseMainWindow(repository_type=args.repo, db_path=args.db)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
