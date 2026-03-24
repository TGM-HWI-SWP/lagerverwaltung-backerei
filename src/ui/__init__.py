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
    project_root = Path(__file__).resolve().parents[2]
    default_db_path = project_root / "lagerverwaltung.db"

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--repo", choices=["memory", "sqlite"], default="sqlite")
    parser.add_argument("--db", default=str(default_db_path))
    args, _ = parser.parse_known_args()

    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = project_root / db_path

    app = QApplication(sys.argv)

    # QSS-Stylesheet laden
    style_path = Path(__file__).parent / "style.qss"
    if style_path.exists():
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))

    window = WarehouseMainWindow(repository_type=args.repo, db_path=str(db_path))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
