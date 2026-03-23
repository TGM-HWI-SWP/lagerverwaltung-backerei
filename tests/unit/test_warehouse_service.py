"""Tests - Unit & Integration Tests für Woche 4"""

import pytest
from src.adapters.repository import InMemoryRepository
from src.services import WarehouseService
from src.adapters.report import ConsoleReportAdapter

class TestWarehouseServiceWoche4:
    """Tests für die erweiterten Funktionen in Woche 4"""

    @pytest.fixture
    def service(self):
        """Setup: Erstellt einen frischen Service mit In-Memory Repo"""
        repo = InMemoryRepository()
        return WarehouseService(repo)

    def test_adjust_stock_inventory_records_correct_difference(self, service):
        """Testet die neue Inventur-Logik: Setzt Bestand hart und loggt Differenz"""
        # 1. Setup: Produkt mit 10 Stück erstellen
        service.create_product("B-001", "Semmel", "Frisch", 0.50, initial_quantity=10)
        
        # 2. Action: Inventur ergibt nur 7 Stück (Schwund von 3)
        service.adjust_stock_inventory("B-001", 7, user="Przemyslaw")
        
        # 3. Assert
        product = service.get_product("B-001")
        assert product.quantity == 7
        
        movements = service.get_movements()
        # Die letzte Bewegung sollte die Korrektur sein
        last_mov = movements[-1]
        assert last_mov.quantity_change == -3
        assert last_mov.movement_type == "ADJUST"
        assert "Inventur-Korrektur" in last_mov.reason

    def test_low_stock_detection_logic(self, service):
        """Testet, ob der Service Produkte mit wenig Bestand korrekt erkennt"""
        service.create_product("P1", "Viel Lager", "Test", 1.0, initial_quantity=20)
        service.create_product("P2", "Wenig Lager", "Test", 1.0, initial_quantity=5)
        
        low_stock_items = service.get_low_stock_items(threshold=10)
        
        assert len(low_stock_items) == 1
        assert low_stock_items[0].id == "P2"

    def test_report_warning_indicator(self, service):
        """Integrationstest: Erscheint die Warnung !!! KNAPP !!! im Report?"""
        # Setup: Ein Produkt das knapp ist
        service.create_product("P-WARN", "Mehl", "Basis", 0.80, initial_quantity=3)
        
        products = service.get_all_products()
        movements = service.get_movements()
        adapter = ConsoleReportAdapter(products, movements)
        
        report = adapter.generate_inventory_report()
        
        # Assert: Die Warnung muss im Text vorkommen
        assert "!!! KNAPP !!!" in report
        assert "Kritische Bestände:           1" in report

    def test_remove_from_stock_insufficient_error(self, service):
        """Sicherheitstest: Verhindert der Service negativen Bestand?"""
        service.create_product("B-002", "Brot", "Test", 2.50, initial_quantity=5)
        
        with pytest.raises(ValueError, match="Unzureichender Bestand"):
            service.remove_from_stock("B-002", 10)

    def test_update_category_prices(self, service):
        """Preisanpassung für eine Kategorie"""
        service.create_product("C1", "Artikel 1", "", 10.0, category="food")
        service.create_product("C2", "Artikel 2", "", 20.0, category="tool")
        service.create_product("C3", "Artikel 3", "", 5.0, category="food")

        service.update_category_prices("food", 0.10)
        p1 = service.get_product("C1")
        p3 = service.get_product("C3")

        assert p1.price == pytest.approx(11.0)
        assert p3.price == pytest.approx(5.5)
        # Artikel aus anderer Kategorie darf sich nicht ändern
        p2 = service.get_product("C2")
        assert p2.price == 20.0
