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

    def generate_statistics_report(self) -> str:
        """
        Statistikreport über Lagerbewegungen generieren

        Returns:
            Formatierter Statistik-Bericht
        """
        if not self.movements:
            return "Keine Lagerbewegungen für Statistik vorhanden.\n"

        # Berechne Statistiken
        total_movements = len(self.movements)
        movement_types = {}
        product_movements = {}
        total_inbound = 0  # Waren rein
        total_outbound = 0  # Waren raus

        for movement in self.movements:
            # Zähle Bewegungstypen
            movement_types[movement.movement_type] = (
                movement_types.get(movement.movement_type, 0) + 1
            )

            # Zähle Bewegungen pro Produkt
            if movement.product_id not in product_movements:
                product_movements[movement.product_id] = {
                    "name": movement.product_name,
                    "count": 0,
                    "total_quantity": 0,
                }
            product_movements[movement.product_id]["count"] += 1
            product_movements[movement.product_id]["total_quantity"] += (
                movement.quantity_change
            )

            # Berechne Ein-/Ausgang
            if movement.quantity_change > 0:
                total_inbound += movement.quantity_change
            else:
                total_outbound += abs(movement.quantity_change)

        # Generiere Report
        report = "=" * 80 + "\n"
        report += "STATISTIKREPORT - LAGERBEWEGUNGEN\n"
        report += "=" * 80 + "\n\n"

        report += f"Gesamtzahl Bewegungen: {total_movements}\n"
        report += f"Gesamt Waren eingegangen: {total_inbound} Einheiten\n"
        report += f"Gesamt Waren ausgegeben: {total_outbound} Einheiten\n"
        report += f"Netto-Bestandsveränderung: {total_inbound - total_outbound:+d} Einheiten\n\n"

        report += "-" * 80 + "\n"
        report += "BEWEGUNGSTYPEN:\n"
        report += "-" * 80 + "\n"
        for mov_type, count in sorted(movement_types.items()):
            report += f"  {mov_type}: {count} Bewegungen\n"

        report += "\n"
        report += "-" * 80 + "\n"
        report += "TOP PRODUKTE (nach Bewegungsanzahl):\n"
        report += "-" * 80 + "\n"
        sorted_products = sorted(
            product_movements.items(),
            key=lambda x: x[1]["count"],
            reverse=True,
        )
        for product_id, data in sorted_products[:10]:  # Top 10
            report += (
                f"  {data['name']} (ID: {product_id})\n"
                f"    Bewegungen: {data['count']}\n"
                f"    Gesamtmenge: {data['total_quantity']:+d}\n\n"
            )

        report += "=" * 80 + "\n"
        return report
