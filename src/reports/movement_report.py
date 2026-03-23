"""Bewegungsprotokoll (Report B) als eigenständige Komponente"""

from typing import List

from ..domain.warehouse import Movement


class MovementReport:
    """Erzeugt einen Bericht aller Lagerbewegungen."""

    def __init__(self, movements: List[Movement] = None):
        self.movements = movements or []

    def generate(self) -> str:
        """Gibt das formatierte Bewegungsprotokoll als String zurück.

        Der Bericht enthält immer eine Kopfzeile; bei fehlenden Bewegungen
        wird ein Hinweis und die Gesamtanzahl 0 ausgegeben.
        """
        report = "=" * 85 + "\n"
        report += "BEWEGUNGSPROTOKOLL\n"
        report += "=" * 85 + "\n\n"

        report += (
            f"{'Zeitpunkt':<20} | {'ID':<8} | {'Produkt':<20} | {'Typ':<10} | {'Änderung':<10} | {'User':<15}\n"
        )
        report += "-" * 85 + "\n"

        if not self.movements:
            report += "Keine Lagerbewegungen vorhanden.\n"
            report += "=" * 85 + "\n"
            report += f"Gesamtbewegungen: 0\n"
            report += "=" * 85 + "\n"
            return report

        sorted_movements = sorted(self.movements, key=lambda m: m.timestamp)

        for movement in sorted_movements:
            time_str = movement.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            # include movement.id so tests can assert ID positions
            report += (
                f"{time_str:<20} | {movement.id:<8} | {movement.product_name:<20} | {movement.movement_type:<10} | "
                f"{movement.quantity_change:>+9} | {movement.performed_by:<15}\n"
            )
            if movement.reason:
                report += f"   Grund: {movement.reason}\n"

        report += "=" * 85 + "\n"
        report += f"Gesamtbewegungen: {len(self.movements)}\n"
        report += "=" * 85 + "\n"

        return report
