"""Report Adapter - Report-Generierung mit Warnsystem (Woche 4)"""

from typing import Dict, List
from ..ports import ReportPort
from ..reports import InventoryReport, MovementReport


class ConsoleReportAdapter(ReportPort):
    """Report-Adapter für formatierte Konsolenausgabe"""

    def __init__(self, products: Dict = None, movements: List = None):
        self.products = products or {}
        self.movements = movements or []

    def generate_inventory_report(self) -> str:
        """Erstellt einen Lagerbestandsbericht über die reine Report-Klasse."""
        return InventoryReport(self.products).generate()

    def generate_movement_report(self) -> str:
        """Bewegungsprotokoll über die reine Report-Klasse erzeugen."""
        return MovementReport(self.movements).generate()
