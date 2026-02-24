"""Reports Module - Report-Generierung

Die eigentlichen Report-Klassen liegen in eigenen Modulen, damit
sie unabhängig von der Konsolenausgabe verwendet werden können.
"""

from .inventory_report import InventoryReport
from .movement_report import MovementReport

__all__ = ["InventoryReport", "MovementReport"]

