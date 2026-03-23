"""Repository Adapter - In-Memory und persistente Implementierungen"""

from typing import Dict, List, Optional
from datetime import datetime

from ..domain.product import Product
from ..domain.warehouse import Movement
from ..ports import RepositoryPort


class InMemoryRepository(RepositoryPort):
    """In-Memory Repository - schnell für Tests und schnelle Prototypen"""

    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.movements: List[Movement] = []

    def save_product(self, product: Product) -> None:
        """Produkt im Memory speichern"""
        self.products[product.id] = product

    def load_product(self, product_id: str) -> Optional[Product]:
        """Produkt aus Memory laden"""
        return self.products.get(product_id)

    def load_all_products(self) -> Dict[str, Product]:
        """Alle Produkte aus Memory laden"""
        return self.products.copy()

    def delete_product(self, product_id: str) -> None:
        """Produkt aus Memory löschen"""
        if product_id in self.products:
            del self.products[product_id]

    def save_movement(self, movement: Movement) -> None:
        """Bewegung im Memory speichern"""
        self.movements.append(movement)

    def load_movements(self) -> List[Movement]:
        """Alle Bewegungen aus Memory laden"""
        return self.movements.copy()


import sqlite3
from pathlib import Path


class RepositoryFactory:
    """Factory für Repository-Instanzen"""

    @staticmethod
    def create_repository(repository_type: str = "memory", *args, **kwargs) -> RepositoryPort:
        """
        Repository basierend auf Typ erstellen

        Args:
            repository_type: "memory", "sqlite" oder andere (z.B. "json")
            *args, **kwargs: Zusatzargumente, z.B. Pfad für sqlite

        Returns:
            RepositoryPort Instanz
        """
        if repository_type == "memory":
            return InMemoryRepository()
        elif repository_type == "sqlite":
            db_path = kwargs.get("db_path") or (args[0] if args else "data.db")
            return SQLiteRepository(db_path)
        else:
            raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")


class SQLiteRepository(InMemoryRepository):
    """SQLite-basiertes Repository.

    Erbt zunächst von InMemoryRepository für API-Kompatibilität;
    speichert zusätzlich in einer SQLite-Datenbank.
    """

    def __init__(self, db_path: str = "data.db"):
        super().__init__()
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        # load existing data into memory structures
        self._load_from_db()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                price REAL,
                quantity INTEGER,
                sku TEXT,
                category TEXT,
                created_at TEXT,
                updated_at TEXT,
                notes TEXT
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS movements (
                id TEXT PRIMARY KEY,
                product_id TEXT,
                product_name TEXT,
                quantity_change INTEGER,
                movement_type TEXT,
                reason TEXT,
                timestamp TEXT,
                performed_by TEXT
            )
            """
        )
        self.conn.commit()

    def _load_from_db(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM products")
        rows = c.fetchall()
        for row in rows:
            prod = Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                quantity=row[4],
                sku=row[5],
                category=row[6],
                created_at=datetime.fromisoformat(row[7]),
                updated_at=datetime.fromisoformat(row[8]),
                notes=row[9],
            )
            self.products[prod.id] = prod
        c.execute("SELECT * FROM movements")
        rows = c.fetchall()
        for row in rows:
            mov = Movement(
                id=row[0],
                product_id=row[1],
                product_name=row[2],
                quantity_change=row[3],
                movement_type=row[4],
                reason=row[5],
                timestamp=datetime.fromisoformat(row[6]),
                performed_by=row[7],
            )
            self.movements.append(mov)

    def save_product(self, product: Product) -> None:
        super().save_product(product)
        c = self.conn.cursor()
        c.execute(
            """
            INSERT OR REPLACE INTO products VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                product.id,
                product.name,
                product.description,
                product.price,
                product.quantity,
                product.sku,
                product.category,
                product.created_at.isoformat(),
                product.updated_at.isoformat(),
                product.notes,
            ),
        )
        self.conn.commit()

    def delete_product(self, product_id: str) -> None:
        super().delete_product(product_id)
        c = self.conn.cursor()
        c.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()

    def save_movement(self, movement: Movement) -> None:
        super().save_movement(movement)
        c = self.conn.cursor()
        c.execute(
            """
            INSERT OR REPLACE INTO movements VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                movement.id,
                movement.product_id,
                movement.product_name,
                movement.quantity_change,
                movement.movement_type,
                movement.reason,
                movement.timestamp.isoformat(),
                movement.performed_by,
            ),
        )
        self.conn.commit()
