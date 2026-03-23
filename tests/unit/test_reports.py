"""Tests für Report B - Bewegungsprotokoll und Statistiken"""

import pytest
from datetime import date, datetime, timedelta


class TestReportGeneration:
    """Tests für Report-Generierung"""

    def test_generate_movement_report_with_data(self, service_with_movements):
        """Test: Bewegungsprotokoll mit Daten"""
        report = service_with_movements.generate_movement_report()

        # Prüfe grundlegende Struktur
        assert "BEWEGUNGSPROTOKOLL" in report
        assert "Gesamtbewegungen: 5" in report

        # Prüfe Inhalte
        assert "Laptop" in report
        assert "Maus" in report
        assert "Tastatur" in report
        assert "IN" in report
        assert "OUT" in report

    def test_generate_movement_report_empty(self, empty_repository):
        """Test: Bewegungsprotokoll ohne Daten"""
        from src.services import WarehouseService
        service = WarehouseService(empty_repository)

        report = service.generate_movement_report()
        assert "Keine Lagerbewegungen vorhanden" in report

    def test_generate_statistics_report_with_data(self, service_with_movements):
        """Test: Statistikreport mit Daten"""
        report = service_with_movements.generate_statistics_report()

        # Prüfe grundlegende Struktur
        assert "STATISTIKREPORT - LAGERBEWEGUNGEN" in report
        assert "Gesamtzahl Bewegungen: 5" in report

        # Prüfe Berechnungen
        assert "Gesamt Waren eingegangen: 85 Einheiten" in report
        assert "Gesamt Waren ausgegeben: 7 Einheiten" in report
        assert "Netto-Bestandsveränderung: +78 Einheiten" in report

        # Prüfe Bewegungstypen
        assert "IN: 3 Bewegungen" in report
        assert "OUT: 2 Bewegungen" in report

        # Prüfe Top-Produkte
        assert "Laptop" in report
        assert "Maus" in report
        assert "Tastatur" in report

    def test_generate_statistics_report_empty(self, empty_repository):
        """Test: Statistikreport ohne Daten"""
        from src.services import WarehouseService
        service = WarehouseService(empty_repository)

        report = service.generate_statistics_report()
        assert "Keine Lagerbewegungen für Statistik vorhanden" in report

    def test_generate_inventory_report_still_works(self, service_with_basic_products):
        """Test: Dass der ursprüngliche Inventory-Report noch funktioniert"""
        report = service_with_basic_products.generate_inventory_report()

        assert "LAGERBESTANDSBERICHT" in report
        assert "Laptop" in report
        assert "Maus" in report
        assert "Tastatur" in report
        assert "Gesamtwert Lager:" in report


class TestStatisticsCalculations:
    """Tests für Statistik-Berechnungen"""

    def test_statistics_with_mixed_movement_types(self, repository_with_basic_products, mixed_movement_types):
        """Test: Statistik mit verschiedenen Bewegungstypen"""
        for movement in mixed_movement_types:
            repository_with_basic_products.save_movement(movement)

        from src.services import WarehouseService
        service = WarehouseService(repository_with_basic_products)

        report = service.generate_statistics_report()

        # Prüfe Bewegungstypen-Zählung
        assert "IN: 1 Bewegungen" in report
        assert "OUT: 2 Bewegungen" in report
        assert "CORRECTION: 1 Bewegungen" in report

        # Prüfe Mengenberechnung
        assert "Gesamt Waren eingegangen: 105 Einheiten" in report  # 100 + 5
        assert "Gesamt Waren ausgegeben: 23 Einheiten" in report    # 20 + 3

    def test_statistics_with_large_dataset(self, repository_with_large_dataset):
        """Test: Statistik mit großem Datensatz"""
        from src.services import WarehouseService
        service = WarehouseService(repository_with_large_dataset)

        report = service.generate_statistics_report()

        # Prüfe Gesamtzahlen
        assert "Gesamtzahl Bewegungen: 500" in report

        # Prüfe dass Top-Produkte angezeigt werden
        assert "TOP PRODUKTE" in report

        # Performance-Test: Report sollte schnell generiert werden
        import time
        start_time = time.time()
        report = service.generate_statistics_report()
        end_time = time.time()

        assert end_time - start_time < 1.0  # Sollte unter 1 Sekunde dauern


class TestReportEdgeCases:
    """Tests für Edge Cases in Reports"""

    def test_movement_report_with_special_characters(self, repository_with_basic_products):
        """Test: Bewegungsprotokoll mit Unicode-Zeichen"""
        from src.domain.warehouse import Movement
        from datetime import datetime

        # Erstelle Bewegung mit Unicode-Zeichen
        movement = Movement(
            id="test_unicode",
            product_id="P001",
            product_name="Produkt ñáéíóú 🚀",
            quantity_change=5,
            movement_type="IN",
            reason="Test mit Unicode: αβγδε 中文",
            timestamp=datetime.now(),
            performed_by="user_tëst"
        )

        repository_with_basic_products.save_movement(movement)

        from src.services import WarehouseService
        service = WarehouseService(repository_with_basic_products)

        report = service.generate_movement_report()
        # Report sollte keine Exceptions werfen und Unicode-Zeichen enthalten
        assert len(report) > 0
        assert "Produkt" in report

    def test_statistics_with_zero_movements(self, repository_with_basic_products):
        """Test: Statistik mit Produkten aber ohne Bewegungen"""
        from src.services import WarehouseService
        service = WarehouseService(repository_with_basic_products)

        report = service.generate_statistics_report()
        assert "Keine Lagerbewegungen für Statistik vorhanden" in report

    def test_movement_report_with_large_numbers(self, repository_with_basic_products):
        """Test: Bewegungsprotokoll mit großen Zahlen"""
        from src.domain.warehouse import Movement
        from datetime import datetime

        # Erstelle Bewegung mit großer Zahl
        movement = Movement(
            id="test_large",
            product_id="P001",
            product_name="Testprodukt",
            quantity_change=999999,
            movement_type="IN",
            reason="Große Bestellung",
            timestamp=datetime.now(),
            performed_by="admin"
        )

        repository_with_basic_products.save_movement(movement)

        from src.services import WarehouseService
        service = WarehouseService(repository_with_basic_products)

        report = service.generate_movement_report()
        assert "+999999" in report

    def test_statistics_with_single_product_multiple_movements(self, single_product_repository):
        """Test: Statistik mit einem Produkt und vielen Bewegungen"""
        from src.services import WarehouseService
        from src.domain.warehouse import Movement
        from datetime import datetime

        service = WarehouseService(single_product_repository)

        # Erstelle mehrere Bewegungen für dasselbe Produkt
        movements = [
            Movement(f"mov_{i}", "P_SINGLE", "Einzelprodukt", 10 if i % 2 == 0 else -5,
                    "IN" if i % 2 == 0 else "OUT", f"Grund {i}",
                    datetime.now() + timedelta(hours=i), f"user{i%3}")
            for i in range(10)
        ]

        for movement in movements:
            single_product_repository.save_movement(movement)

        report = service.generate_statistics_report()

        # Prüfe dass nur ein Produkt in Top-Produkte erscheint
        assert report.count("Einzelprodukt") >= 2  # Im Header und in Top-Produkte


class TestReportFiltering:
    """Tests für Report-Filterfunktionen"""

    def test_filter_movements_by_date(self, service_with_movements):
        """Test: Bewegungen nach Datum filtern"""
        from datetime import date

        # Filter für einen bestimmten Tag
        filter_date = date(2024, 1, 1)
        end_date = date(2024, 1, 2)

        filtered = service_with_movements.filter_movements_by_date(filter_date, end_date)
        assert len(filtered) == 5  # Alle Bewegungen sind an diesem Tag

        # Filter für nicht existierenden Tag
        future_date = date(2025, 1, 1)
        future_end = date(2025, 1, 2)
        filtered_future = service_with_movements.filter_movements_by_date(future_date, future_end)
        assert len(filtered_future) == 0

    def test_filter_movements_by_type(self, service_with_movements):
        """Test: Bewegungen nach Typ filtern"""
        in_movements = service_with_movements.filter_movements_by_type("IN")
        out_movements = service_with_movements.filter_movements_by_type("OUT")

        assert len(in_movements) == 3
        assert len(out_movements) == 2

        # Prüfe dass alle IN-Bewegungen positive quantity_change haben
        assert all(m.quantity_change > 0 for m in in_movements)
        assert all(m.quantity_change < 0 for m in out_movements)

    def test_get_movements_for_product(self, service_with_movements):
        """Test: Bewegungen für spezifisches Produkt"""
        laptop_movements = service_with_movements.get_movements_for_product("P001")
        mouse_movements = service_with_movements.get_movements_for_product("P002")
        keyboard_movements = service_with_movements.get_movements_for_product("P003")

        assert len(laptop_movements) == 2  # Laptop: IN und OUT
        assert len(mouse_movements) == 2   # Maus: IN und OUT
        assert len(keyboard_movements) == 1  # Tastatur: nur IN

        # Prüfe Produkt-IDs
        assert all(m.product_id == "P001" for m in laptop_movements)
        assert all(m.product_id == "P002" for m in mouse_movements)
        assert all(m.product_id == "P003" for m in keyboard_movements)

    def test_get_movements_for_nonexistent_product(self, service_with_movements):
        """Test: Bewegungen für nicht existierendes Produkt"""
        nonexistent_movements = service_with_movements.get_movements_for_product("NONEXISTENT")
        assert len(nonexistent_movements) == 0


class TestReportIntegration:
    """Integrationstests für Reports"""

    def test_full_workflow_with_reports(self, empty_repository):
        """Test: Vollständiger Workflow mit Report-Generierung"""
        from src.services import WarehouseService

        service = WarehouseService(empty_repository)

        # 1. Produkte erstellen
        service.create_product("PROD001", "Testprodukt 1", "Beschreibung 1", 100.0, initial_quantity=10)
        service.create_product("PROD002", "Testprodukt 2", "Beschreibung 2", 200.0, initial_quantity=5)

        # 2. Bewegungen durchführen
        service.add_to_stock("PROD001", 15, reason="Einkauf", user="testuser")
        service.remove_from_stock("PROD001", 5, reason="Verkauf", user="testuser")
        service.add_to_stock("PROD002", 10, reason="Restocking", user="testuser")

        # 3. Reports generieren
        inventory_report = service.generate_inventory_report()
        movement_report = service.generate_movement_report()
        statistics_report = service.generate_statistics_report()

        # 4. Reports validieren
        assert "Testprodukt 1" in inventory_report
        assert "Testprodukt 2" in inventory_report

        assert "Einkauf" in movement_report
        assert "Verkauf" in movement_report
        assert "Restocking" in movement_report

        assert "Gesamtzahl Bewegungen: 3" in statistics_report
        assert "Gesamt Waren eingegangen: 25 Einheiten" in statistics_report
        assert "Gesamt Waren ausgegeben: 5 Einheiten" in statistics_report

    def test_report_consistency(self, service_with_movements):
        """Test: Konsistenz zwischen verschiedenen Reports"""
        movements = service_with_movements.get_movements()
        movement_report = service_with_movements.generate_movement_report()
        statistics_report = service_with_movements.generate_statistics_report()

        # Anzahl der Bewegungen sollte in beiden Reports übereinstimmen
        expected_count = len(movements)
        assert f"Gesamtbewegungen: {expected_count}" in movement_report
        assert f"Gesamtzahl Bewegungen: {expected_count}" in statistics_report

        # Summen sollten übereinstimmen
        total_in = sum(m.quantity_change for m in movements if m.quantity_change > 0)
        total_out = abs(sum(m.quantity_change for m in movements if m.quantity_change < 0))

        assert f"Gesamt Waren eingegangen: {total_in} Einheiten" in statistics_report
        assert f"Gesamt Waren ausgegeben: {total_out} Einheiten" in statistics_report


    """Unit tests für die Report‑Klassen"""

from src.domain.product import Product
from src.domain.warehouse import Movement
from src.reports import InventoryReport, MovementReport


def make_sample_products():
    return {
        "P1": Product(id="P1", name="A", description="", price=1.0, quantity=5, category="x"),
        "P2": Product(id="P2", name="B", description="", price=2.0, quantity=0, category="y"),
        "P3": Product(id="P3", name="C", description="", price=3.0, quantity=2, category="x"),
    }


def make_sample_movements():
    return [
        Movement(id="m1", product_id="P1", product_name="A", quantity_change=5, movement_type="IN"),
        Movement(id="m2", product_id="P1", product_name="A", quantity_change=-2, movement_type="OUT"),
    ]


class TestInventoryReport:
    def test_empty(self):
        r = InventoryReport({})
        assert "Lager ist leer" in r.generate()

    def test_content_and_flags(self):
        products = make_sample_products()
        r = InventoryReport(products)
        out = r.generate()
        assert "P1" in out and "A" in out
        assert "!!! KNAPP !!!" in out  # weil P3 < 10
        assert "LEER" in out  # P2
        assert "Gesamtwert Lager" in out


class TestMovementReport:
    def test_empty(self):
        r = MovementReport([])
        assert "Keine Lagerbewegungen" in r.generate()

    def test_chronology_and_format(self):
        movs = make_sample_movements()
        r = MovementReport(movs)
        out = r.generate()
        assert "BEWEGUNGSPROTOKOLL" in out
        # erster Eintrag vor zweitem
        assert out.index("m1") < out.index("m2")
