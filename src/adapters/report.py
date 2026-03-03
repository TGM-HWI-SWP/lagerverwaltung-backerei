"""Report Adapter - Report-Generierung"""

from typing import Dict

from ..ports import ReportPort


class ConsoleReportAdapter(ReportPort):
    """Report-Adapter für Konsolenausgabe"""

    def __init__(self, products: Dict = None, movements: list = None):
        self.products = products or {}
        self.movements = movements or []

    def generate_inventory_report(self) -> str:
        """
        Lagerbestandsbericht als Text generieren

        Returns:
            Formatierter Bericht
        """
        if not self.products:
            return "Lager ist leer.\n"

        report = "=" * 60 + "\n"
        report += "LAGERBESTANDSBERICHT\n"
        report += "=" * 60 + "\n\n"

        total_value = 0
        for product_id, product in self.products.items():
            value = product.get_total_value()
            total_value += value
            report += f"ID: {product_id}\n"
            report += f"  Name: {product.name}\n"
            report += f"  Kategorie: {product.category}\n"
            report += f"  Bestand: {product.quantity}\n"
            report += f"  Preis: {product.price:.2f} €\n"
            report += f"  Gesamtwert: {value:.2f} €\n\n"

        report += "-" * 60 + "\n"
        report += f"Gesamtwert Lager: {total_value:.2f} €\n"
        report += "=" * 60 + "\n"

        return report

    def generate_movement_report(self) -> str:
        """
        Bewegungsprotokoll als Text generieren

        Returns:
            Formatierter Bericht
        """
        if not self.movements:
            return "Keine Lagerbewegungen vorhanden.\n"

        report = "=" * 80 + "\n"
        report += "BEWEGUNGSPROTOKOLL\n"
        report += "=" * 80 + "\n\n"

        for movement in sorted(self.movements, key=lambda m: m.timestamp):
            report += f"[{movement.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]\n"
            report += f"  Produkt: {movement.product_name} (ID: {movement.product_id})\n"
            report += f"  Typ: {movement.movement_type}\n"
            report += f"  Menge: {movement.quantity_change:+d}\n"
            if movement.reason:
                report += f"  Grund: {movement.reason}\n"
            report += f"  Durchgeführt von: {movement.performed_by}\n\n"

        report += "=" * 80 + "\n"
        report += f"Gesamtbewegungen: {len(self.movements)}\n"
        report += "=" * 80 + "\n"

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
