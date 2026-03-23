"""Services - Business Logic Layer"""

from .warehouse_service import WarehouseService

<<<<<<< HEAD
__all__ = ["WarehouseService"]
=======
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
        """Neues Produkt erstellen mit Validierung"""
        # Woche 4: Validierung
        if price < 0:
            raise ValueError("Der Preis eines Produkts kann nicht negativ sein.")
        if not name or len(name.strip()) < 2:
            raise ValueError("Der Produktname muss mindestens 2 Zeichen lang sein.")
        if initial_quantity < 0:
            raise ValueError("Der Anfangsbestand kann nicht negativ sein.")

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
        if quantity <= 0:
            raise ValueError("Die Menge zum Hinzufügen muss positiv sein.")
            
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
        if quantity <= 0:
            raise ValueError("Die Menge zum Entnehmen muss positiv sein.")

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

    def adjust_stock_inventory(self, product_id: str, actual_quantity: int, user: str = "inventur_admin") -> None:
        """
        Woche 4: Inventur-Logik
        Setzt den Bestand exakt auf den gezählten Wert und loggt die Differenz automatisch.
        """
        if actual_quantity < 0:
            raise ValueError("Der gezählte Bestand kann nicht negativ sein.")

        product = self.repository.load_product(product_id)
        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden")

        difference = actual_quantity - product.quantity
        if difference == 0:
            return

        product.quantity = actual_quantity
        self.repository.save_product(product)

        movement = Movement(
            id=f"adj_{datetime.now().timestamp()}",
            product_id=product_id,
            product_name=product.name,
            quantity_change=difference,
            movement_type="ADJUST",
            reason=f"Inventur-Korrektur (Differenz: {difference})",
            performed_by=user,
        )
        self.repository.save_movement(movement)

    def update_category_prices(self, category: str, percentage: float) -> None:
        """Erhöht oder senkt alle Preise einer Kategorie um einen Prozentsatz (z.B. 0.10 für +10%)"""
        all_products = self.repository.load_all_products()
        updated_count = 0
        
        for product in all_products.values():
            if product.category == category:
                product.price = round(product.price * (1 + percentage), 2)
                self.repository.save_product(product)
                updated_count += 1
        
        print(f"Preise für {updated_count} Produkte in '{category}' wurden angepasst.")

    def get_low_stock_items(self, threshold: int = 10) -> List[Product]:
        """Gibt eine Liste aller Produkte unter dem Schwellenwert zurück"""
        all_products = self.repository.load_all_products()
        return [p for p in all_products.values() if p.quantity < threshold]

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
    
    def delete_product(self, product_id: str) -> None:
        """Produkt vollständig löschen"""
        product = self.repository.load_product(product_id)
        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden.")
        
        self.repository.delete_product(product_id)
>>>>>>> feature/rolle2/merge-test-v2
