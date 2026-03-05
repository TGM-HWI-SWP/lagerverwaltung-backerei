"""GUI-Tests für Rolle 4 - GUI & Interaktion

Testet die UI-Komponenten der Lagerverwaltung mit PyQt6.
Benötigt eine QApplication-Instanz (wird als Fixture bereitgestellt).
"""

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.ui.main_window import WarehouseMainWindow
from src.ui.dialogs import ProductDialogWindow, StockDialog


@pytest.fixture(scope="session")
def qapp():
    """QApplication-Instanz für alle GUI-Tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def main_window(qapp):
    """Frisches Hauptfenster für jeden Test"""
    window = WarehouseMainWindow()
    return window


@pytest.fixture
def window_with_product(main_window):
    """Hauptfenster mit einem vorinstallierten Produkt"""
    main_window.service.create_product(
        product_id="BRT-001",
        name="Vollkornbrot",
        description="Frisches Vollkornbrot",
        price=3.50,
        category="Brot",
        initial_quantity=20,
    )
    main_window._refresh_products()
    return main_window


# ── Hauptfenster-Tests ────────────────────────────────────────────


class TestMainWindow:
    """Tests für das Hauptfenster"""

    def test_window_title(self, main_window):
        """Fenstertitel enthält Versionsnummer"""
        assert "Lagerverwaltungssystem" in main_window.windowTitle()

    def test_has_three_tabs(self, main_window):
        """Hauptfenster hat genau 3 Tabs"""
        assert main_window.tabs.count() == 3

    def test_tab_names(self, main_window):
        """Tabs haben die korrekten Bezeichnungen"""
        assert main_window.tabs.tabText(0) == "Produkte"
        assert main_window.tabs.tabText(1) == "Lagerbewegungen"
        assert main_window.tabs.tabText(2) == "Berichte"

    def test_products_table_columns(self, main_window):
        """Produkttabelle hat 6 Spalten"""
        assert main_window.products_table.columnCount() == 6

    def test_movements_table_columns(self, main_window):
        """Bewegungstabelle hat 6 Spalten"""
        assert main_window.movements_table.columnCount() == 6

    def test_empty_products_table(self, main_window):
        """Leere Produkttabelle bei Start"""
        assert main_window.products_table.rowCount() == 0

    def test_search_field_exists(self, main_window):
        """Suchfeld existiert"""
        assert main_window.search_field is not None
        assert main_window.search_field.placeholderText() != ""


# ── Produktverwaltung-Tests ───────────────────────────────────────


class TestProductManagement:
    """Tests für Produktverwaltung über die GUI"""

    def test_refresh_shows_products(self, window_with_product):
        """Refresh zeigt Produkte in der Tabelle"""
        assert window_with_product.products_table.rowCount() == 1
        assert window_with_product.products_table.item(0, 0).text() == "BRT-001"
        assert window_with_product.products_table.item(0, 1).text() == "Vollkornbrot"

    def test_refresh_shows_correct_values(self, window_with_product):
        """Refresh zeigt korrekte Werte"""
        assert window_with_product.products_table.item(0, 2).text() == "Brot"
        assert window_with_product.products_table.item(0, 3).text() == "20"
        assert window_with_product.products_table.item(0, 4).text() == "3.50"
        assert window_with_product.products_table.item(0, 5).text() == "70.00"

    def test_delete_updates_table(self, window_with_product):
        """Nach dem Löschen wird die Tabelle aktualisiert"""
        window_with_product.service.delete_product("BRT-001")
        window_with_product._refresh_products()
        assert window_with_product.products_table.rowCount() == 0

    def test_multiple_products(self, window_with_product):
        """Mehrere Produkte werden korrekt angezeigt"""
        window_with_product.service.create_product(
            "SEM-001", "Semmel", "Frische Semmel", 0.50, "Gebäck", 100
        )
        window_with_product._refresh_products()
        assert window_with_product.products_table.rowCount() == 2


# ── Suchfunktion-Tests ───────────────────────────────────────────


class TestSearchFilter:
    """Tests für die Suchfunktion"""

    def test_filter_by_name(self, window_with_product):
        """Filtern nach Produktname"""
        window_with_product.service.create_product(
            "SEM-001", "Semmel", "Frische Semmel", 0.50, "Gebäck", 100
        )
        window_with_product._refresh_products()

        window_with_product._filter_products("Vollkorn")

        visible = [
            row
            for row in range(window_with_product.products_table.rowCount())
            if not window_with_product.products_table.isRowHidden(row)
        ]
        assert len(visible) == 1
        assert window_with_product.products_table.item(visible[0], 1).text() == "Vollkornbrot"

    def test_filter_by_category(self, window_with_product):
        """Filtern nach Kategorie"""
        window_with_product.service.create_product(
            "SEM-001", "Semmel", "Frische Semmel", 0.50, "Gebäck", 100
        )
        window_with_product._refresh_products()

        window_with_product._filter_products("Gebäck")

        visible = [
            row
            for row in range(window_with_product.products_table.rowCount())
            if not window_with_product.products_table.isRowHidden(row)
        ]
        assert len(visible) == 1

    def test_filter_by_id(self, window_with_product):
        """Filtern nach Produkt-ID"""
        window_with_product._filter_products("BRT")

        visible = [
            row
            for row in range(window_with_product.products_table.rowCount())
            if not window_with_product.products_table.isRowHidden(row)
        ]
        assert len(visible) == 1

    def test_empty_filter_shows_all(self, window_with_product):
        """Leerer Suchbegriff zeigt alle Produkte"""
        window_with_product.service.create_product(
            "SEM-001", "Semmel", "Frische Semmel", 0.50, "Gebäck", 100
        )
        window_with_product._refresh_products()

        window_with_product._filter_products("")

        visible = [
            row
            for row in range(window_with_product.products_table.rowCount())
            if not window_with_product.products_table.isRowHidden(row)
        ]
        assert len(visible) == 2

    def test_filter_case_insensitive(self, window_with_product):
        """Suche ist nicht case-sensitiv"""
        window_with_product._filter_products("vollkorn")

        visible = [
            row
            for row in range(window_with_product.products_table.rowCount())
            if not window_with_product.products_table.isRowHidden(row)
        ]
        assert len(visible) == 1


# ── Lagerbewegungen-Tests ────────────────────────────────────────


class TestMovements:
    """Tests für die Lagerbewegungen-Anzeige"""

    def test_movements_empty_on_start(self, main_window):
        """Keine Bewegungen bei Start"""
        main_window._refresh_movements()
        assert main_window.movements_table.rowCount() == 0

    def test_movements_after_stock_change(self, window_with_product):
        """Bewegungen werden nach Bestandsänderung angezeigt"""
        window_with_product.service.add_to_stock("BRT-001", 5, "Lieferung", "Max")
        window_with_product._refresh_movements()
        assert window_with_product.movements_table.rowCount() == 1
        assert window_with_product.movements_table.item(0, 2).text() == "IN"

    def test_movements_sorted_newest_first(self, window_with_product):
        """Bewegungen sind nach Zeitstempel sortiert (neueste zuerst)"""
        window_with_product.service.add_to_stock("BRT-001", 5, "Lieferung 1", "Max")
        window_with_product.service.remove_from_stock("BRT-001", 2, "Verkauf", "Anna")
        window_with_product._refresh_movements()

        assert window_with_product.movements_table.rowCount() == 2
        # Neueste Bewegung (OUT) sollte oben stehen
        assert window_with_product.movements_table.item(0, 2).text() == "OUT"
        assert window_with_product.movements_table.item(1, 2).text() == "IN"


# ── Berichte-Tests ───────────────────────────────────────────────


class TestReports:
    """Tests für die Berichterstellung"""

    def test_inventory_report_empty(self, main_window):
        """Leerer Bericht bei leerem Lager"""
        main_window._show_inventory_report()
        assert "leer" in main_window.report_text.toPlainText().lower()

    def test_inventory_report_with_data(self, window_with_product):
        """Bericht enthält Produktdaten"""
        window_with_product._show_inventory_report()
        report = window_with_product.report_text.toPlainText()
        assert "Vollkornbrot" in report
        assert "LAGERBESTANDSBERICHT" in report

    def test_movement_report_empty(self, main_window):
        """Leerer Bewegungsbericht"""
        main_window._show_movement_report()
        assert "keine" in main_window.report_text.toPlainText().lower()

    def test_movement_report_with_data(self, window_with_product):
        """Bewegungsbericht enthält Bewegungsdaten"""
        window_with_product.service.add_to_stock("BRT-001", 10, "Lieferung", "Max")
        window_with_product._show_movement_report()
        report = window_with_product.report_text.toPlainText()
        assert "BEWEGUNGSPROTOKOLL" in report
        assert "Vollkornbrot" in report


# ── Dialog-Tests ─────────────────────────────────────────────────


class TestDialogs:
    """Tests für die Dialogfenster"""

    def test_product_dialog_add_mode(self, qapp):
        """Produkt-Dialog im Hinzufügen-Modus"""
        dialog = ProductDialogWindow()
        assert "hinzufügen" in dialog.windowTitle().lower()
        assert dialog.product_id_field.isReadOnly() is False

    def test_product_dialog_edit_mode(self, qapp):
        """Produkt-Dialog im Bearbeiten-Modus"""
        data = {
            "product_id": "TEST-001",
            "name": "Testbrot",
            "description": "Beschreibung",
            "price": 2.50,
            "quantity": 10,
            "category": "Brot",
        }
        dialog = ProductDialogWindow(product_data=data)
        assert "bearbeiten" in dialog.windowTitle().lower()
        assert dialog.product_id_field.isReadOnly() is True
        assert dialog.product_id_field.text() == "TEST-001"
        assert dialog.name_field.text() == "Testbrot"
        assert dialog.price_field.value() == 2.50

    def test_product_dialog_get_data(self, qapp):
        """get_data gibt korrekte Daten zurück"""
        dialog = ProductDialogWindow()
        dialog.product_id_field.setText("X-001")
        dialog.name_field.setText("Test")
        dialog.description_field.setText("Beschreibung")
        dialog.price_field.setValue(5.0)
        dialog.quantity_field.setValue(10)
        dialog.category_field.setText("Kategorie")

        data = dialog.get_data()
        assert data["product_id"] == "X-001"
        assert data["name"] == "Test"
        assert data["price"] == 5.0
        assert data["quantity"] == 10

    def test_stock_dialog_in_mode(self, qapp):
        """Stock-Dialog im Einlagern-Modus"""
        dialog = StockDialog(product_name="Brot", mode="in")
        assert "Einlagern" in dialog.windowTitle()

    def test_stock_dialog_out_mode(self, qapp):
        """Stock-Dialog im Auslagern-Modus"""
        dialog = StockDialog(product_name="Brot", mode="out")
        assert "Auslagern" in dialog.windowTitle()

    def test_stock_dialog_get_data(self, qapp):
        """StockDialog gibt korrekte Daten zurück"""
        dialog = StockDialog(product_name="Brot", mode="in")
        dialog.quantity_field.setValue(5)
        dialog.reason_field.setText("Lieferung")
        dialog.user_field.setText("Max")

        data = dialog.get_data()
        assert data["quantity"] == 5
        assert data["reason"] == "Lieferung"
        assert data["user"] == "Max"

    def test_stock_dialog_default_user(self, qapp):
        """StockDialog verwendet 'system' als Standard-Benutzer"""
        dialog = StockDialog(product_name="Brot", mode="in")
        data = dialog.get_data()
        assert data["user"] == "system"


# ── Statusleiste-Tests ───────────────────────────────────────────


class TestStatusBar:
    """Tests für die Statusleiste"""

    def test_status_bar_exists(self, main_window):
        """Statusleiste existiert"""
        assert main_window.statusBar() is not None

    def test_status_bar_empty_on_start(self, main_window):
        """Statusleiste zeigt 0 Produkte bei Start"""
        assert "0" in main_window.status_product_count.text()

    def test_status_bar_updates_after_add(self, window_with_product):
        """Statusleiste aktualisiert sich nach Produkthinzufügen"""
        assert "1" in window_with_product.status_product_count.text()
        assert "70.00" in window_with_product.status_total_value.text()

    def test_status_bar_updates_after_delete(self, window_with_product):
        """Statusleiste aktualisiert sich nach Löschen"""
        window_with_product.service.delete_product("BRT-001")
        window_with_product._refresh_products()
        assert "0" in window_with_product.status_product_count.text()
        assert "0.00" in window_with_product.status_total_value.text()


# ── Farbcodierung-Tests ──────────────────────────────────────────


class TestStockColorCoding:
    """Tests für die Bestandsfarben"""

    def test_green_for_sufficient_stock(self, window_with_product):
        """Grün für ausreichenden Bestand (>15)"""
        qty_item = window_with_product.products_table.item(0, 3)
        bg = qty_item.background().color().name()
        assert bg == "#27ae60"

    def test_red_for_critical_stock(self, main_window):
        """Rot für kritischen Bestand (<=5)"""
        main_window.service.create_product(
            "LOW-001", "Wenig Brot", "Fast leer", 2.0, "Brot", 3
        )
        main_window._refresh_products()
        qty_item = main_window.products_table.item(0, 3)
        bg = qty_item.background().color().name()
        assert bg == "#e74c3c"

    def test_orange_for_warning_stock(self, main_window):
        """Orange für knappen Bestand (6-15)"""
        main_window.service.create_product(
            "MED-001", "Mittel Brot", "Knapp", 2.0, "Brot", 10
        )
        main_window._refresh_products()
        qty_item = main_window.products_table.item(0, 3)
        bg = qty_item.background().color().name()
        assert bg == "#f39c12"


# ── Export-Tests ─────────────────────────────────────────────────


class TestExport:
    """Tests für die Export-Funktion"""

    def test_export_button_disabled_on_start(self, main_window):
        """Export-Button ist initial deaktiviert"""
        assert main_window.export_btn.isEnabled() is False

    def test_export_button_enabled_after_report(self, window_with_product):
        """Export-Button wird nach Berichtserstellung aktiviert"""
        window_with_product._show_inventory_report()
        assert window_with_product.export_btn.isEnabled() is True
