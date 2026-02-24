"""Inventarbericht (Report A) als eigenständige Komponente"""

from typing import Dict

from ..domain.product import Product


class InventoryReport:
    """Erzeugt einen Bericht über den aktuellen Lagerbestand."""

    def __init__(self, products: Dict[str, Product] = None):
        self.products = products or {}

    def generate(self) -> str:
        """Erzeugt einen formatierten String.

        Die Logik entspricht weitgehend dem bisherigen
        `ConsoleReportAdapter.generate_inventory_report`, jedoch
        ist der Code hier unabhängig von einer konkreten Ausgabe.
        """
        if not self.products:
            return "Lager ist leer.\n"

        report = "=" * 70 + "\n"
        report += "LAGERBESTANDSBERICHT (BÄCKEREI-VERWALTUNG)\n"
        report += "=" * 70 + "\n\n"

        report += f"{'ID':<10} | {'Name':<20} | {'Bestand':<8} | {'Status':<15}\n"
        report += "-" * 70 + "\n"

        total_value = 0
        low_stock_count = 0

        for product_id, product in self.products.items():
            value = product.get_total_value()
            total_value += value

            if product.quantity < 10:
                status = "!!! KNAPP !!!"
                low_stock_count += 1
            elif product.quantity == 0:
                status = "LEER"
                low_stock_count += 1
            else:
                status = "OK"

            report += f"{product_id:<10} | {product.name:<20} | {product.quantity:<8} | {status:<15}\n"
            report += (
                f"           > Kategorie: {product.category:<12} | Preis: {product.price:>6.2f} € | Wert: {value:>7.2f} €\n"
            )
            report += " " * 70 + "\n"

        report += "-" * 70 + "\n"
        report += f"Gesamtwert Lager:    {total_value:>10.2f} €\n"
        report += f"Kritische Bestände:  {low_stock_count:>10} Artikel\n"
        report += "=" * 70 + "\n"

        return report
