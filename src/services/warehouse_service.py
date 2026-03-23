"""Warehouse Service - Geschäftslogik für Lagerverwaltung"""

from datetime import datetime
from typing import Dict, List, Optional

from ..domain.product import Product
from ..domain.warehouse import Movement, Warehouse
from ..ports import RepositoryPort


class WarehouseService:
    """Service für zentrale Lagerverwaltungslogik"""

    def __init__(self, repository: RepositoryPort):
        self.repository = repository
        self.warehouse = Warehouse("Hauptlager")

    def create_product(
        self,
        product_id: str,
        name: str,
        description: str,
        price: float,
        category: str = "",
        initial_quantity: int = 0,
    ) -> Product:
        """Erstellt und speichert ein neues Produkt"""
        product = Product(
            id=product_id,
            name=name,
            description=description,
            price=price,
            quantity=initial_quantity,
            category=category,
        )
        self.repository.save_product(product)
        self.warehouse.add_product(product)
        return product

    def add_to_stock(
        self, product_id: str, quantity: int, reason: str = "", user: str = "system"
    ) -> None:
        """Erhöht den Bestand eines Produkts"""
        product = self.repository.load_product(product_id)
        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden")

        product.update_quantity(quantity)
        self.repository.save_product(product)

        movement = Movement(
            id=f"mov_{datetime.now().timestamp()}",
            product_id=product_id,
            product_name=product.name,
            quantity_change=quantity,
            movement_type="IN",
            reason=reason,
            performed_by=user,
        )
        self.repository.save_movement(movement)

    def remove_from_stock(
        self, product_id: str, quantity: int, reason: str = "", user: str = "system"
    ) -> None:
        """Verringert den Bestand eines Produkts"""
        product = self.repository.load_product(product_id)
        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden")

        if product.quantity < quantity:
            raise ValueError(
                f"Unzureichender Bestand. Verfügbar: {product.quantity}, Angefordert: {quantity}"
            )

        product.update_quantity(-quantity)
        self.repository.save_product(product)

        movement = Movement(
            id=f"mov_{datetime.now().timestamp()}",
            product_id=product_id,
            product_name=product.name,
            quantity_change=-quantity,
            movement_type="OUT",
            reason=reason,
            performed_by=user,
        )
        self.repository.save_movement(movement)

    def get_product(self, product_id: str) -> Optional[Product]:
        """Ruft ein einzelnes Produkt ab"""
        return self.repository.load_product(product_id)

    def get_all_products(self) -> Dict[str, Product]:
        """Ruft alle Produkte ab"""
        return self.repository.load_all_products()

    def get_movements(self) -> List[Movement]:
        """Ruft alle Lagerbewegungen ab"""
        return self.repository.load_movements()

    def get_total_inventory_value(self) -> float:
        """Berechnet den Gesamtwert des Lagerbestands"""
        products = self.repository.load_all_products()
        return sum(p.get_total_value() for p in products.values())

    def delete_product(self, product_id: str) -> None:
        """Löscht ein Produkt"""
        product = self.repository.load_product(product_id)
        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden")
        self.repository.delete_product(product_id)
        if product_id in self.warehouse.products:
            del self.warehouse.products[product_id]

    def filter_movements_by_date(self, start_date, end_date):
        """Filter movements by date range (inclusive)."""
        movements = self.repository.load_movements()
        return [m for m in movements if start_date <= m.timestamp.date() <= end_date]

    def filter_movements_by_type(self, movement_type: str):
        """Filter movements by movement type (IN/OUT/CORRECTION)."""
        movements = self.repository.load_movements()
        return [m for m in movements if m.movement_type == movement_type]

    def get_movements_for_product(self, product_id: str):
        """Return all movements for a given product id."""
        movements = self.repository.load_movements()
        return [m for m in movements if m.product_id == product_id]

    def generate_movement_report(self) -> str:
        """Generate movement report using ConsoleReportAdapter."""
        from ..adapters.report import ConsoleReportAdapter

        products = self.repository.load_all_products()
        movements = self.repository.load_movements()
        adapter = ConsoleReportAdapter(products=products, movements=movements)
        return adapter.generate_movement_report()

    def generate_statistics_report(self) -> str:
        """Generate statistics report using ConsoleReportAdapter."""
        from ..adapters.report import ConsoleReportAdapter

        movements = self.repository.load_movements()
        adapter = ConsoleReportAdapter(movements=movements)
        return adapter.generate_statistics_report()

    def generate_inventory_report(self) -> str:
        """Generate inventory report using ConsoleReportAdapter."""
        from ..adapters.report import ConsoleReportAdapter

        products = self.repository.load_all_products()
        adapter = ConsoleReportAdapter(products=products)
        return adapter.generate_inventory_report()

    def adjust_stock_inventory(self, product_id: str, new_quantity: int, user: str = "system", reason: str = "Inventur-Korrektur") -> None:
        """Setzt den Bestand hart auf `new_quantity` und protokolliert die Differenz als ADJUST."""
        product = self.repository.load_product(product_id)
        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden")

        diff = new_quantity - product.quantity
        product.quantity = new_quantity
        self.repository.save_product(product)

        if diff != 0:
            movement = Movement(
                id=f"mov_{datetime.now().timestamp()}",
                product_id=product_id,
                product_name=product.name,
                quantity_change=diff,
                movement_type="ADJUST",
                reason=reason,
                performed_by=user,
            )
            self.repository.save_movement(movement)

    def get_low_stock_items(self, threshold: int = 10):
        """Return list of products with quantity less or equal to threshold."""
        products = self.repository.load_all_products()
        return [p for p in products.values() if p.quantity <= threshold]

    def update_category_prices(self, category: str, factor: float) -> None:
        """Update prices for all products in given category by a multiplicative factor.

        `factor` is the relative change (e.g. 0.10 increases prices by 10%).
        """
        products = self.repository.load_all_products()
        for p in products.values():
            if p.category == category:
                p.price = p.price * (1 + factor)
                self.repository.save_product(p)
