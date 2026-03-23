"""Test Fixtures - Dummy-Daten für Tests"""

import pytest
from datetime import datetime, timedelta
from typing import List

from src.domain.product import Product
from src.domain.warehouse import Movement
from src.adapters.repository import InMemoryRepository
from src.services import WarehouseService


@pytest.fixture
def empty_repository():
    """Leeres Repository für Basis-Tests"""
    return InMemoryRepository()


@pytest.fixture
def basic_products():
    """Grundlegende Testprodukte"""
    return [
        Product(
            id="P001",
            name="Laptop",
            description="Gaming Laptop",
            price=999.99,
            quantity=10,
            category="Elektronik",
        ),
        Product(
            id="P002",
            name="Maus",
            description="Gaming Maus",
            price=49.99,
            quantity=50,
            category="Zubehör",
        ),
        Product(
            id="P003",
            name="Tastatur",
            description="Mechanische Tastatur",
            price=129.99,
            quantity=25,
            category="Zubehör",
        ),
    ]


@pytest.fixture
def repository_with_basic_products(empty_repository, basic_products):
    """Repository mit grundlegenden Testprodukten"""
    for product in basic_products:
        empty_repository.save_product(product)
    return empty_repository


@pytest.fixture
def service_with_basic_products(repository_with_basic_products):
    """WarehouseService mit grundlegenden Testprodukten"""
    return WarehouseService(repository_with_basic_products)


@pytest.fixture
def movements_sample():
    """Beispiel-Lagerbewegungen für verschiedene Szenarien"""
    base_time = datetime(2024, 1, 1, 9, 0, 0)

    return [
        Movement(
            id="mov_001",
            product_id="P001",
            product_name="Laptop",
            quantity_change=10,
            movement_type="IN",
            reason="Initialer Einkauf",
            timestamp=base_time,
            performed_by="admin",
        ),
        Movement(
            id="mov_002",
            product_id="P001",
            product_name="Laptop",
            quantity_change=-2,
            movement_type="OUT",
            reason="Verkauf",
            timestamp=base_time + timedelta(hours=1),
            performed_by="user1",
        ),
        Movement(
            id="mov_003",
            product_id="P002",
            product_name="Maus",
            quantity_change=50,
            movement_type="IN",
            reason="Restocking",
            timestamp=base_time + timedelta(hours=2),
            performed_by="admin",
        ),
        Movement(
            id="mov_004",
            product_id="P002",
            product_name="Maus",
            quantity_change=-5,
            movement_type="OUT",
            reason="Verkauf",
            timestamp=base_time + timedelta(hours=3),
            performed_by="user2",
        ),
        Movement(
            id="mov_005",
            product_id="P003",
            product_name="Tastatur",
            quantity_change=25,
            movement_type="IN",
            reason="Neuer Lieferant",
            timestamp=base_time + timedelta(hours=4),
            performed_by="admin",
        ),
    ]


@pytest.fixture
def repository_with_movements(repository_with_basic_products, movements_sample):
    """Repository mit Produkten und Bewegungen"""
    for movement in movements_sample:
        repository_with_basic_products.save_movement(movement)
    return repository_with_basic_products


@pytest.fixture
def service_with_movements(repository_with_movements):
    """WarehouseService mit Produkten und Bewegungen"""
    return WarehouseService(repository_with_movements)


@pytest.fixture
def large_dataset():
    """Großer Datensatz für Performance-Tests"""
    products = []
    movements = []

    # Erstelle 100 Produkte
    for i in range(1, 101):
        product = Product(
            id=f"P{i:03d}",
            name=f"Produkt {i}",
            description=f"Beschreibung für Produkt {i}",
            price=float(i * 10),
            quantity=i * 5,
            category=f"Kategorie {(i % 5) + 1}",
        )
        products.append(product)

    # Erstelle 500 Bewegungen
    base_time = datetime(2024, 1, 1, 9, 0, 0)
    movement_types = ["IN", "OUT", "CORRECTION"]
    reasons = ["Einkauf", "Verkauf", "Korrektur", "Retour", "Umverteilung"]

    for i in range(1, 501):
        product_idx = (i % len(products))
        product = products[product_idx]

        # Abwechselnd Ein- und Ausgänge
        quantity_change = (i % 10) + 1
        if i % 2 == 0:
            quantity_change = -quantity_change

        movement = Movement(
            id=f"mov_{i:03d}",
            product_id=product.id,
            product_name=product.name,
            quantity_change=quantity_change,
            movement_type=movement_types[i % len(movement_types)],
            reason=reasons[i % len(reasons)],
            timestamp=base_time + timedelta(minutes=i),
            performed_by=f"user{i % 5}",
        )
        movements.append(movement)

    return {
        "products": products,
        "movements": movements,
    }


@pytest.fixture
def repository_with_large_dataset(empty_repository, large_dataset):
    """Repository mit großem Datensatz"""
    for product in large_dataset["products"]:
        empty_repository.save_product(product)
    for movement in large_dataset["movements"]:
        empty_repository.save_movement(movement)
    return empty_repository


@pytest.fixture
def edge_case_products():
    """Produkte für Edge Cases"""
    return [
        Product(
            id="P_EDGE_001",
            name="Sehr teures Produkt",
            description="Test für hohe Preise",
            price=999999.99,
            quantity=1,
            category="Luxus",
        ),
        Product(
            id="P_EDGE_002",
            name="Billiges Produkt",
            description="Test für niedrige Preise",
            price=0.01,
            quantity=1000000,
            category="Budget",
        ),
        Product(
            id="P_EDGE_003",
            name="Produkt mit langer Beschreibung",
            description="A" * 1000,  # 1000 Zeichen lange Beschreibung
            price=100.00,
            quantity=10,
            category="Test",
        ),
        Product(
            id="P_EDGE_004",
            name="Unicode Produkt ñáéíóú",
            description="Test für Unicode-Zeichen: αβγδε 中文 🚀",
            price=50.00,
            quantity=5,
            category="International",
        ),
    ]


@pytest.fixture
def empty_movements_repository(empty_repository, basic_products):
    """Repository mit Produkten aber ohne Bewegungen (für Report-Tests)"""
    for product in basic_products:
        empty_repository.save_product(product)
    return empty_repository


@pytest.fixture
def single_product_repository(empty_repository):
    """Repository mit nur einem Produkt"""
    product = Product(
        id="P_SINGLE",
        name="Einzelprodukt",
        description="Für Tests mit einem Produkt",
        price=100.00,
        quantity=10,
        category="Test",
    )
    empty_repository.save_product(product)
    return empty_repository


@pytest.fixture
def mixed_movement_types():
    """Bewegungen mit verschiedenen Typen für Statistik-Tests"""
    base_time = datetime(2024, 1, 1, 9, 0, 0)

    return [
        Movement(
            id="mix_001",
            product_id="P001",
            product_name="Testprodukt",
            quantity_change=100,
            movement_type="IN",
            reason="Großeinkauf",
            timestamp=base_time,
            performed_by="admin",
        ),
        Movement(
            id="mix_002",
            product_id="P001",
            product_name="Testprodukt",
            quantity_change=-20,
            movement_type="OUT",
            reason="Verkauf",
            timestamp=base_time + timedelta(hours=1),
            performed_by="user1",
        ),
        Movement(
            id="mix_003",
            product_id="P001",
            product_name="Testprodukt",
            quantity_change=5,
            movement_type="CORRECTION",
            reason="Bestandskorrektur",
            timestamp=base_time + timedelta(hours=2),
            performed_by="admin",
        ),
        Movement(
            id="mix_004",
            product_id="P001",
            product_name="Testprodukt",
            quantity_change=-3,
            movement_type="OUT",
            reason="Retour",
            timestamp=base_time + timedelta(hours=3),
            performed_by="user2",
        ),
    ]


@pytest.fixture
def service_with_large_dataset(repository_with_large_dataset):
    """WarehouseService für den großen Datensatz"""
    return WarehouseService(repository_with_large_dataset)


@pytest.fixture
def service(empty_repository):
    """Allgemeiner WarehouseService mit leerem Repository"""
    return WarehouseService(empty_repository)