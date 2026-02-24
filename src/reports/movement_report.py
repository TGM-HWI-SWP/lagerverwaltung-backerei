"""Bewegungsprotokoll (Report B) als eigenständige Komponente"""

from typing import List

from ..domain.warehouse import Movement


class MovementReport:
    """Erzeugt einen Bericht aller Lagerbewegungen."""

    def __init__(self, movements: List[Movement] = None):
        self.movements = movements or []

    def generate(self) -> str:
        """Formatiert das Bewegungsprotokoll als String."""
        if not self.movements:
            return "Keine Lagerbewegungen vorhanden.\n"

        report = "=" * 85 + "\n"
        report += "BEWEGUNGSPROTOKOLL\n"
        report += "=" * 85 + "\n\n"

        report += (
            f"{'Zeitpunkt':<20} | {'Produkt':<20} | {'Typ':<10} | {'Änderung':<10} | {'User':<15}\n"
        )
        report += "-" * 85 + "\n"

        sorted_movements = sorted(self.movements, key=lambda m: m.timestamp)

        for movement in sorted_movements:
            time_str = movement.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            report += (
                f"{time_str:<20} | {movement.product_name:<20} | {movement.movement_type:<10} | {movement.quantity_change:>+9} | {movement.performed_by:<15}\n"
            )
            if movement.reason:
                report += f"   Grund: {movement.reason}\n"

        report += "=" * 85 + "\n"
        report += f"Gesamtbewegungen: {len(self.movements)}\n"
        report += "=" * 85 + "\n"

        return report
