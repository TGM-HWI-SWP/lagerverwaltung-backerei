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
        self.repository.delete_product(product_id)
        self.warehouse.remove_product(product_id)
