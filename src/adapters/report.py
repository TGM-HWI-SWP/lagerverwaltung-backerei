"""Report Adapter - Report-Generierung mit Warnsystem (Woche 4)"""

from typing import Dict, List
from ..ports import ReportPort


class ConsoleReportAdapter(ReportPort):
    """Report-Adapter für formatierte Konsolenausgabe"""

    def __init__(self, products: Dict = None, movements: List = None):
        self.products = products or {}
        self.movements = movements or []

    def generate_inventory_report(self) -> str:
        """
        Lagerbestandsbericht (Report A) mit Warnsystem für Woche 4.
        Markiert Produkte mit geringem Bestand (< 10 Stück) automatisch.
        """
        if not self.products:
            return "Lager ist leer.\n"

        report = "=" * 70 + "\n"
        report += "LAGERBESTANDSBERICHT (BÄCKEREI-VERWALTUNG)\n"
        report += "=" * 70 + "\n\n"
        
        # Header für die Tabelle
        report += f"{'ID':<10} | {'Name':<20} | {'Bestand':<8} | {'Status':<15}\n"
        report += "-" * 70 + "\n"

        total_value = 0
        low_stock_count = 0

        for product_id, product in self.products.items():
            value = product.get_total_value()
            total_value += value
            
            # Warn-Logik für Woche 4
            if product.quantity < 10:
                status = "!!! KNAPP !!!"
                low_stock_count += 1
            elif product.quantity == 0:
                status = "LEER"
                low_stock_count += 1
            else:
                status = "OK"

            # Zeile 1: Basisdaten
            report += f"{product_id:<10} | {product.name:<20} | {product.quantity:<8} | {status:<15}\n"
            # Zeile 2: Details (leicht eingerückt)
            report += f"           > Kategorie: {product.category:<12} | Preis: {product.price:>6.2f} € | Wert: {value:>7.2f} €\n"
            report += " " * 70 + "\n"

        report += "-" * 70 + "\n"
        report += f"Gesamtwert Lager:    {total_value:>10.2f} €\n"
        report += f"Kritische Bestände:  {low_stock_count:>10} Artikel\n"
        report += "=" * 70 + "\n"

        return report

    def generate_movement_report(self) -> str:
        """
        Bewegungsprotokoll als Text generieren.
        Sortiert Bewegungen chronologisch.
        """
        if not self.movements:
            return "Keine Lagerbewegungen vorhanden.\n"

        report = "=" * 85 + "\n"
        report += "BEWEGUNGSPROTOKOLL\n"
        report += "=" * 85 + "\n\n"
        
        report += f"{'Zeitpunkt':<20} | {'Produkt':<20} | {'Typ':<10} | {'Änderung':<10} | {'User':<15}\n"
        report += "-" * 85 + "\n"

        # Sortierung nach Timestamp
        sorted_movements = sorted(self.movements, key=lambda m: m.timestamp)

        for movement in sorted_movements:
            time_str = movement.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            
            report += f"{time_str:<20} | {movement.product_name:<20} | {movement.movement_type:<10} | {movement.quantity_change:>+9} | {movement.performed_by:<15}\n"
            if movement.reason:
                report += f"   Grund: {movement.reason}\n"

        report += "=" * 85 + "\n"
        report += f"Gesamtbewegungen: {len(self.movements)}\n"
        report += "=" * 85 + "\n"

        return report