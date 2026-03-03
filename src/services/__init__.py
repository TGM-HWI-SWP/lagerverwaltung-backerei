"""Services - Business Logic Layer"""

from datetime import datetime, date
from typing import Dict, List, Optional

from ..domain.product import Product
from ..domain.warehouse import Movement, Warehouse
from ..ports import RepositoryPort


class WarehouseService:
    """Service für Lagerverwaltung"""

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
        """Neues Produkt erstellen und speichern"""
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
        """Bestand erhöhen"""
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
        """Bestand verringern"""
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
        """Produkt abrufen"""
        return self.repository.load_product(product_id)

    def get_all_products(self) -> Dict[str, Product]:
        """Alle Produkte abrufen"""
        return self.repository.load_all_products()

    def get_movements(self) -> List[Movement]:
        """Alle Lagerbewegungen abrufen"""
        return self.repository.load_movements()

    def get_total_inventory_value(self) -> float:
        """Gesamtwert des Lagerbestands berechnen"""
        products = self.repository.load_all_products()
        return sum(p.get_total_value() for p in products.values())

    def filter_movements_by_date(
        self, start_date: date, end_date: date
    ) -> List[Movement]:
        """
        Lagerbewegungen nach Datumsbereich filtern

        Args:
            start_date: Starttag (inklusive)
            end_date: Enddatum (inklusive)

        Returns:
            Liste gefilterte Lagerbewegungen
        """
        movements = self.repository.load_movements()
        filtered = [
            m
            for m in movements
            if start_date <= m.timestamp.date() <= end_date
        ]
        return filtered

    def filter_movements_by_type(self, movement_type: str) -> List[Movement]:
        """
        Lagerbewegungen nach Typ filtern

        Args:
            movement_type: z.B. "IN", "OUT", "CORRECTION"

        Returns:
            Liste gefilterte Lagerbewegungen
        """
        movements = self.repository.load_movements()
        return [m for m in movements if m.movement_type == movement_type]

    def get_movements_for_product(self, product_id: str) -> List[Movement]:
        """
        Alle Lagerbewegungen für ein bestimmtes Produkt abrufen

        Args:
            product_id: ID des Produkts

        Returns:
            Liste von Lagerbewegungen
        """
        movements = self.repository.load_movements()
        return [m for m in movements if m.product_id == product_id]

    def generate_movement_report(self) -> str:
        """
        Bewegungsprotokoll generieren (Report B Teil 1)

        Returns:
            Formatiertes Bewegungsprotokoll als String
        """
        from ..adapters.report import ConsoleReportAdapter

        products = self.repository.load_all_products()
        movements = self.repository.load_movements()
        adapter = ConsoleReportAdapter(products=products, movements=movements)
        return adapter.generate_movement_report()

    def generate_statistics_report(self) -> str:
        """
        Statistikreport über Lagerbewegungen generieren (Report B Teil 2)

        Returns:
            Formatierter Statistikreport als String
        """
        from ..adapters.report import ConsoleReportAdapter

        movements = self.repository.load_movements()
        adapter = ConsoleReportAdapter(movements=movements)
        return adapter.generate_statistics_report()

    def generate_inventory_report(self) -> str:
        """
        Lagerbestandsbericht generieren (Report A)

        Returns:
            Formatierter Lagerbestandsbericht als String
        """
        from ..adapters.report import ConsoleReportAdapter

        products = self.repository.load_all_products()
        adapter = ConsoleReportAdapter(products=products)
        return adapter.generate_inventory_report()
