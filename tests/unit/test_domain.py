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
