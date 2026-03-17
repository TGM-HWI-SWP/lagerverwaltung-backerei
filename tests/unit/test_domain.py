"""Tests - Unit Tests für die Geschäftslogik"""

import pytest
from src.domain.product import Product
from src.adapters.repository import InMemoryRepository
from src.services import WarehouseService


class TestProduct:
    """Tests für die Product-Klasse"""

    def test_product_creation(self):
        """Test: Produkt erstellen"""
        product = Product(
            id="P001",
            name="Test Produkt",
            description="Ein Test",
            price=10.0,
            quantity=5,
        )
        assert product.id == "P001"
        assert product.name == "Test Produkt"
        assert product.quantity == 5

    def test_product_validation_negative_price(self):
        """Test: Produkt mit negativem Preis sollte fehlschlagen"""
        with pytest.raises(ValueError):
            Product(
                id="P001",
                name="Test",
                description="Test",
                price=-10.0,
            )

    def test_update_quantity(self):
        """Test: Bestand aktualisieren"""
        product = Product(
            id="P001",
            name="Test",
            description="Test",
            price=10.0,
            quantity=10,
        )
        product.update_quantity(5)
        assert product.quantity == 15

        product.update_quantity(-5)
        assert product.quantity == 10

    def test_update_quantity_insufficient(self):
        """Test: Bestand kann nicht negativ werden"""
        product = Product(
            id="P001",
            name="Test",
            description="Test",
            price=10.0,
            quantity=5,
        )
        with pytest.raises(ValueError):
            product.update_quantity(-10)

    def test_get_total_value(self):
        """Test: Gesamtwert berechnen"""
        product = Product(
            id="P001",
            name="Test",
            description="Test",
            price=10.0,
            quantity=5,
        )
        assert product.get_total_value() == 50.0


class TestWarehouseService:
    """Tests für WarehouseService"""

    @pytest.fixture
    def service(self):
        """Fixture für WarehouseService mit In-Memory Repository"""
        repository = InMemoryRepository()
        return WarehouseService(repository)

    def test_create_product(self, service):
        """Test: Produkt über Service erstellen"""
        product = service.create_product(
            product_id="P001",
            name="Test Produkt",
            description="Ein Test",
            price=15.0,
            category="Test",
            initial_quantity=10,
        )
        assert product.id == "P001"
        assert product.quantity == 10

    def test_add_to_stock(self, service):
        """Test: Bestand erhöhen"""
        service.create_product("P001", "Test", "Test", 10.0, initial_quantity=5)
        service.add_to_stock("P001", 3, reason="Neuer Einkauf")

        product = service.get_product("P001")
        assert product.quantity == 8

    def test_remove_from_stock(self, service):
        """Test: Bestand verringern"""
        service.create_product("P001", "Test", "Test", 10.0, initial_quantity=10)
        service.remove_from_stock("P001", 3, reason="Verkauf")

        product = service.get_product("P001")
        assert product.quantity == 7

    def test_remove_from_stock_insufficient(self, service):
        """Test: Nicht genug Bestand zum Entnehmen"""
        service.create_product("P001", "Test", "Test", 10.0, initial_quantity=5)

        with pytest.raises(ValueError):
            service.remove_from_stock("P001", 10)

    def test_get_all_products(self, service):
        """Test: Alle Produkte abrufen"""
        service.create_product("P001", "Produkt 1", "Test", 10.0)
        service.create_product("P002", "Produkt 2", "Test", 20.0)

        products = service.get_all_products()
        assert len(products) == 2

    def test_get_total_inventory_value(self, service):
        """Test: Gesamtwert des Lagers berechnen"""
        service.create_product("P001", "Test 1", "Test", 10.0, initial_quantity=5)
        service.create_product("P002", "Test 2", "Test", 20.0, initial_quantity=3)

        total = service.get_total_inventory_value()
        assert total == 110.0  # (10*5) + (20*3)

    def test_get_movements(self, service):
        """Test: Lagerbewegungen abrufen"""
        service.create_product("P001", "Test", "Test", 10.0, initial_quantity=5)
        service.add_to_stock("P001", 3)
        service.remove_from_stock("P001", 2)

        movements = service.get_movements()
        assert len(movements) == 2


class TestReportFixtures:
    """Tests für die neuen Dummy-Daten Fixtures"""

    def test_basic_products_fixture(self, basic_products):
        """Test: basic_products Fixture funktioniert"""
        assert len(basic_products) == 3
        assert basic_products[0].id == "P001"
        assert basic_products[0].name == "Laptop"
        assert basic_products[0].price == 999.99

    def test_movements_sample_fixture(self, movements_sample):
        """Test: movements_sample Fixture funktioniert"""
        assert len(movements_sample) == 5
        total_in = sum(m.quantity_change for m in movements_sample if m.quantity_change > 0)
        total_out = abs(sum(m.quantity_change for m in movements_sample if m.quantity_change < 0))
        assert total_in == 85  # 10 + 50 + 25
        assert total_out == 7  # 2 + 5

    def test_service_with_movements_fixture(self, service_with_movements):
        """Test: service_with_movements Fixture funktioniert"""
        products = service_with_movements.get_all_products()
        movements = service_with_movements.get_movements()

        assert len(products) == 3
        assert len(movements) == 5

        # Teste Reports
        inventory_report = service_with_movements.generate_inventory_report()
        movement_report = service_with_movements.generate_movement_report()
        statistics_report = service_with_movements.generate_statistics_report()

        assert "LAGERBESTANDSBERICHT" in inventory_report
        assert "BEWEGUNGSPROTOKOLL" in movement_report
        assert "STATISTIKREPORT" in statistics_report


class TestWarehouseServiceReports:
    """Erweiterte Tests für WarehouseService Report-Methoden"""

    def test_generate_reports_with_edge_case_products(self, repository_with_basic_products, edge_case_products):
        """Test: Reports mit Edge-Case-Produkten"""
        for product in edge_case_products:
            repository_with_basic_products.save_product(product)

        from src.services import WarehouseService
        service = WarehouseService(repository_with_basic_products)

        # Reports sollten keine Exceptions werfen
        inventory_report = service.generate_inventory_report()
        assert len(inventory_report) > 0
        assert "Sehr teures Produkt" in inventory_report
        assert "Unicode Produkt" in inventory_report

    def test_movement_report_with_many_movements(self, repository_with_large_dataset):
        """Test: Bewegungsprotokoll mit vielen Bewegungen"""
        from src.services import WarehouseService
        service = WarehouseService(repository_with_large_dataset)

        import time
        start_time = time.time()
        report = service.generate_movement_report()
        end_time = time.time()

        # Sollte schnell sein (< 0.5 Sekunden für 500 Bewegungen)
        assert end_time - start_time < 0.5
        assert "Gesamtbewegungen: 500" in report

    def test_statistics_report_with_many_movements(self, repository_with_large_dataset):
        """Test: Statistikreport mit vielen Bewegungen"""
        from src.services import WarehouseService
        service = WarehouseService(repository_with_large_dataset)

        report = service.generate_statistics_report()

        # Prüfe dass alle Bewegungstypen erfasst werden
        assert "IN:" in report
        assert "OUT:" in report
        assert "CORRECTION:" in report

        # Prüfe dass Top-Produkte angezeigt werden
        assert "TOP PRODUKTE" in report

    def test_filter_methods_with_large_dataset(self, service_with_large_dataset):
        """Test: Filter-Methoden mit großem Datensatz"""
        # Teste Datumsfilter
        from datetime import date
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 2)
        filtered = service_with_large_dataset.filter_movements_by_date(start_date, end_date)
        assert len(filtered) == 500  # Alle Bewegungen sind an diesem Tag

        # Teste Typ-Filter
        in_movements = service_with_large_dataset.filter_movements_by_type("IN")
        out_movements = service_with_large_dataset.filter_movements_by_type("OUT")
        assert len(in_movements) > 0
        assert len(out_movements) > 0
        assert len(in_movements) + len(out_movements) <= 500  # Einige sind CORRECTION

    def test_product_specific_movements_with_large_dataset(self, service_with_large_dataset):
        """Test: Produkt-spezifische Bewegungen mit großem Datensatz"""
        # Teste mit einem bekannten Produkt
        product_movements = service_with_large_dataset.get_movements_for_product("P001")
        assert len(product_movements) > 0

        # Alle Bewegungen sollten das richtige Produkt haben
        assert all(m.product_id == "P001" for m in product_movements)

    def test_report_generation_with_unicode_and_special_chars(self, repository_with_basic_products):
        """Test: Reports mit Unicode und Sonderzeichen"""
        from src.domain.warehouse import Movement
        from datetime import datetime

        # Erstelle Bewegung mit vielen Sonderzeichen
        special_movement = Movement(
            id="special_test",
            product_id="P001",
            product_name="Tëst Prödüct 🚀 中文 αβγ",
            quantity_change=42,
            movement_type="IN",
            reason="Tëst Rëäsön with spëciäl chärs: ñáéíóú @#$%^&*()",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            performed_by="üsër_tëst_🚀"
        )

        repository_with_basic_products.save_movement(special_movement)

        from src.services import WarehouseService
        service = WarehouseService(repository_with_basic_products)

        # Reports sollten keine Exceptions werfen
        movement_report = service.generate_movement_report()
        statistics_report = service.generate_statistics_report()

        assert len(movement_report) > 0
        assert len(statistics_report) > 0
        assert "Tëst Prödüct" in movement_report

    def test_empty_reports_with_products_but_no_movements(self, repository_with_basic_products):
        """Test: Leere Reports bei Produkten ohne Bewegungen"""
        from src.services import WarehouseService
        service = WarehouseService(repository_with_basic_products)

        movement_report = service.generate_movement_report()
        statistics_report = service.generate_statistics_report()

        assert "Keine Lagerbewegungen vorhanden" in movement_report
        assert "Keine Lagerbewegungen für Statistik vorhanden" in statistics_report


class TestRepositoryFactory:
    """Tests für RepositoryFactory"""

    def test_create_memory_repository(self):
        """Test: Memory Repository erstellen"""
        from src.adapters.repository import RepositoryFactory, InMemoryRepository

        repo = RepositoryFactory.create_repository("memory")
        assert isinstance(repo, InMemoryRepository)

    def test_create_repository_invalid_type(self):
        """Test: Ungültiger Repository-Typ"""
        from src.adapters.repository import RepositoryFactory

        with pytest.raises(ValueError, match="Unbekannter Repository-Typ"):
            RepositoryFactory.create_repository("invalid_type")

    def test_create_repository_default(self):
        """Test: Default Repository-Typ (memory)"""
        from src.adapters.repository import RepositoryFactory, InMemoryRepository

        repo = RepositoryFactory.create_repository()
        assert isinstance(repo, InMemoryRepository)


class TestRepositoryEdgeCases:
    """Tests für Repository Edge Cases"""

    def test_delete_nonexistent_product(self, repository_with_basic_products):
        """Test: Nicht existierendes Produkt löschen"""
        initial_count = len(repository_with_basic_products.products)

        # Sollte keine Exception werfen
        repository_with_basic_products.delete_product("NONEXISTENT")

        # Anzahl sollte gleich bleiben
        assert len(repository_with_basic_products.products) == initial_count

    def test_load_nonexistent_product(self, repository_with_basic_products):
        """Test: Nicht existierendes Produkt laden"""
        product = repository_with_basic_products.load_product("NONEXISTENT")
        assert product is None

    def test_repository_isolation(self):
        """Test: Repository-Isolation zwischen Instanzen"""
        from src.adapters.repository import InMemoryRepository

        repo1 = InMemoryRepository()
        repo2 = InMemoryRepository()

        # Produkte in repo1 hinzufügen
        from src.domain.product import Product
        product = Product("TEST", "Test", "Test", 100.0, quantity=10)
        repo1.save_product(product)

        # repo2 sollte leer sein
        assert len(repo1.products) == 1
        assert len(repo2.products) == 0

        # load_all_products sollte Kopien zurückgeben
        products1 = repo1.load_all_products()
        products1["NEW"] = Product("NEW", "New", "New", 50.0)

        # Original sollte unverändert sein
        assert "NEW" not in repo1.products


class TestWarehouseServiceEdgeCases:
    """Tests für WarehouseService Edge Cases"""

    def test_create_product_duplicate_id(self, service):
        """Test: Produkt mit doppelter ID erstellen"""
        service.create_product("TEST", "Test", "Test", 100.0)

        with pytest.raises(ValueError, match="existiert bereits"):
            service.create_product("TEST", "Test2", "Test2", 200.0)

    def test_add_to_stock_nonexistent_product(self, service):
        """Test: Bestand für nicht existierendes Produkt erhöhen"""
        with pytest.raises(ValueError, match="nicht gefunden"):
            service.add_to_stock("NONEXISTENT", 5)

    def test_remove_from_stock_nonexistent_product(self, service):
        """Test: Bestand für nicht existierendes Produkt verringern"""
        with pytest.raises(ValueError, match="nicht gefunden"):
            service.remove_from_stock("NONEXISTENT", 5)

    def test_remove_more_than_available(self, service):
        """Test: Mehr entfernen als verfügbar"""
        service.create_product("TEST", "Test", "Test", 100.0, initial_quantity=5)

        with pytest.raises(ValueError, match="Unzureichender Bestand"):
            service.remove_from_stock("TEST", 10)

    def test_get_nonexistent_product(self, service):
        """Test: Nicht existierendes Produkt abrufen"""
        product = service.get_product("NONEXISTENT")
        assert product is None

    def test_product_creation_edge_cases(self):
        """Test: Produkt-Erstellung Edge Cases"""
        from src.domain.product import Product

        # Produkt mit minimalen Daten
        product = Product("MIN", "Min", "Min", 0.01, quantity=0)
        assert product.price == 0.01
        assert product.quantity == 0

        # Produkt mit maximalen Daten
        product_max = Product(
            id="MAX",
            name="A" * 100,  # Langer Name
            description="B" * 500,  # Lange Beschreibung
            price=999999.99,
            quantity=999999,
            category="C" * 50,  # Lange Kategorie
            sku="SKU123",
            notes="N" * 200  # Lange Notizen
        )
        assert len(product_max.name) == 100
        assert len(product_max.description) == 500

    def test_product_validation(self):
        """Test: Produkt-Validierung"""
        from src.domain.product import Product

        # Negativer Preis sollte fehlschlagen
        with pytest.raises(ValueError, match="Preis kann nicht negativ sein"):
            Product("TEST", "Test", "Test", -10.0)

        # Negative Menge sollte fehlschlagen
        with pytest.raises(ValueError, match="Bestand kann nicht negativ sein"):
            Product("TEST", "Test", "Test", 100.0, quantity=-5)

        # Leere ID sollte fehlschlagen
        with pytest.raises(ValueError, match="Product ID kann nicht leer sein"):
            Product("", "Test", "Test", 100.0)

    def test_product_quantity_operations_edge_cases(self):
        """Test: Bestandsoperationen Edge Cases"""
        from src.domain.product import Product

        product = Product("TEST", "Test", "Test", 100.0, quantity=10)

        # Sehr große Menge hinzufügen
        product.update_quantity(999999)
        assert product.quantity == 1000009

        # Große Menge entfernen
        product.update_quantity(-500000)
        assert product.quantity == 500009

        # Auf 0 reduzieren
        product.update_quantity(-500009)
        assert product.quantity == 0

        # Versuch, unter 0 zu gehen
        with pytest.raises(ValueError, match="Ungültige Bestandsmenge"):
            product.update_quantity(-1)

    def test_product_total_value_calculation(self):
        """Test: Gesamtwert-Berechnung"""
        from src.domain.product import Product

        # Normaler Fall
        product = Product("TEST", "Test", "Test", 100.0, quantity=5)
        assert product.get_total_value() == 500.0

        # Mit 0 Menge
        product_zero = Product("ZERO", "Zero", "Zero", 50.0, quantity=0)
        assert product_zero.get_total_value() == 0.0

        # Mit großen Zahlen
        product_big = Product("BIG", "Big", "Big", 999.99, quantity=10000)
        assert product_big.get_total_value() == 9999900.0

    def test_movement_creation_and_validation(self):
        """Test: Movement-Erstellung und Validierung"""
        from src.domain.warehouse import Movement
        from datetime import datetime

        # Normales Movement
        movement = Movement(
            id="TEST_MOV",
            product_id="PROD001",
            product_name="Test Product",
            quantity_change=5,
            movement_type="IN",
            reason="Test reason",
            timestamp=datetime.now(),
            performed_by="test_user"
        )

        assert movement.quantity_change == 5
        assert movement.movement_type == "IN"

        # Movement mit negativer Menge (OUT)
        out_movement = Movement(
            id="TEST_OUT",
            product_id="PROD001",
            product_name="Test Product",
            quantity_change=-3,
            movement_type="OUT",
            reason="Sale",
            performed_by="user"
        )

        assert out_movement.quantity_change == -3

        # Movement ohne optionale Felder
        minimal_movement = Movement(
            id="MINIMAL",
            product_id="PROD001",
            product_name="Test",
            quantity_change=1,
            movement_type="CORRECTION"
        )

        assert minimal_movement.reason is None
        assert minimal_movement.performed_by == "system"  # Default

    def test_warehouse_operations_edge_cases(self):
        """Test: Warehouse Edge Cases"""
        from src.domain.warehouse import Warehouse

        warehouse = Warehouse("Test Warehouse")

        # Leeres Warehouse
        assert len(warehouse.products) == 0
        assert len(warehouse.movements) == 0
        assert warehouse.get_total_inventory_value() == 0.0

        # Inventory report für leeres Warehouse
        report = warehouse.get_inventory_report()
        assert len(report) == 0

        # Produkt hinzufügen
        from src.domain.product import Product
        product = Product("TEST", "Test", "Test", 100.0, quantity=5)
        warehouse.add_product(product)

        assert len(warehouse.products) == 1
        assert warehouse.get_total_inventory_value() == 500.0

        # Dasselbe Produkt nochmal hinzufügen sollte fehlschlagen
        with pytest.raises(ValueError, match="existiert bereits"):
            warehouse.add_product(product)

        # Movement für nicht existierendes Produkt sollte fehlschlagen
        from src.domain.warehouse import Movement
        from datetime import datetime

        invalid_movement = Movement(
            id="INVALID",
            product_id="NONEXISTENT",
            product_name="Nonexistent",
            quantity_change=1,
            movement_type="IN"
        )

        with pytest.raises(ValueError, match="existiert nicht"):
            warehouse.record_movement(invalid_movement)

    def test_warehouse_inventory_report(self):
        """Test: Lagerbestandsbericht"""
        from src.domain.warehouse import Warehouse
        from src.domain.product import Product

        warehouse = Warehouse("Test")

        # Mehrere Produkte hinzufügen
        products = [
            Product("P1", "Product 1", "Desc 1", 10.0, quantity=5),
            Product("P2", "Product 2", "Desc 2", 20.0, quantity=3),
            Product("P3", "Product 3", "Desc 3", 15.0, quantity=0),  # Kein Bestand
        ]

        for product in products:
            warehouse.add_product(product)

        report = warehouse.get_inventory_report()

        # Prüfe Struktur
        assert len(report) == 3
        assert "P1" in report
        assert "P2" in report
        assert "P3" in report

        # Prüfe Werte
        assert report["P1"]["quantity"] == 5
        assert report["P1"]["price"] == 10.0
        assert report["P1"]["total_value"] == 50.0

        assert report["P2"]["quantity"] == 3
        assert report["P2"]["price"] == 20.0
        assert report["P2"]["total_value"] == 60.0

        assert report["P3"]["quantity"] == 0
        assert report["P3"]["total_value"] == 0.0
