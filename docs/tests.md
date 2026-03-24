# Test-Dokumentation

## Übersicht

Dieses Dokument beschreibt die Test-Strategie und Test-Struktur des Projekts.

**Aktueller Stand:** 110 Tests, alle bestanden (Stand v0.4.0)

## Test-Dateien

| Datei | Anzahl | Beschreibung |
|-------|--------|-------------|
| `tests/unit/test_domain.py` | 40 | Product-Klasse, Validierung, Warehouse |
| `tests/unit/test_gui.py` | 39 | GUI-Komponenten (Fenster, Dialoge, Suche, Farben) |
| `tests/unit/test_reports.py` | 21 | InventoryReport, MovementReport, Statistik |
| `tests/unit/test_warehouse_service.py` | 5 | Service-Methoden |
| `tests/unit/test_sqlite_repository.py` | 3 | SQLite-Persistenz |
| `tests/integration/test_integration.py` | 2 | Kompletter Workflow, Report-Generierung |
| **Gesamt** | **110** | |

## Test-Fixtures

Zentrale Fixtures in `tests/fixtures.py`:

| Fixture | Beschreibung |
|---------|-------------|
| `empty_repository` | Leeres InMemoryRepository |
| `basic_products` | 3 Testprodukte (Laptop, Maus, Tastatur) |
| `repository_with_basic_products` | Repository mit 3 Produkten |
| `service_with_basic_products` | WarehouseService mit 3 Produkten |
| `movements_sample` | 5 Beispiel-Bewegungen (IN/OUT) |
| `large_dataset` | 100 Produkte + 500 Bewegungen (Performance) |
| `edge_case_products` | Extremwerte, Unicode, lange Beschreibungen |
| `mixed_movement_types` | IN, OUT, CORRECTION Bewegungen |

GUI-Fixtures in `tests/unit/test_gui.py`:

| Fixture | Beschreibung |
|---------|-------------|
| `qapp` | QApplication-Instanz (session-scoped) |
| `main_window` | Frisches Hauptfenster |
| `window_with_product` | Hauptfenster mit Produkt "Vollkornbrot" |

## Unit Tests

### TestProduct (`test_domain.py`)
- `test_product_creation` – Grundlegende Erstellung
- `test_product_validation_negative_price` – Validierung negativ Preis
- `test_update_quantity` – Bestandsänderung
- `test_update_quantity_insufficient` – Fehlerfall: zu wenig Bestand
- `test_get_total_value` – Wertberechnung

### TestWarehouseService (`test_domain.py` + `test_warehouse_service.py`)
- `test_create_product` – Produkt erstellen
- `test_add_to_stock` – Bestand erhöhen
- `test_remove_from_stock` – Bestand verringern
- `test_remove_from_stock_insufficient` – Fehlerfall
- `test_get_all_products` – Alle Produkte abrufen
- `test_get_total_inventory_value` – Gesamtwert
- `test_get_movements` – Lagerbewegungen abrufen
- `test_update_category_prices` – Kategoriepreise anpassen

### GUI-Tests (`test_gui.py`)
- **TestMainWindow** (7): Fensterstruktur, Tabs, Tabellen, Suchfeld
- **TestProductManagement** (4): CRUD-Operationen über GUI
- **TestSearchFilter** (5): Filtern nach Name, Kategorie, ID, Case-insensitive
- **TestMovements** (3): Leere/gefüllte Bewegungstabelle, Sortierung
- **TestReports** (4): Leere/gefüllte Berichte im Textfeld
- **TestDialogs** (7): Add/Edit-Modus, StockDialog, Datenrückgabe
- **TestStatusBar** (4): Existenz, Leer, Nach Add, Nach Delete
- **TestStockColorCoding** (3): Grün (>15), Orange (6-15), Rot (<=5)
- **TestExport** (2): Button initial deaktiviert / nach Report aktiviert

### Report-Tests (`test_reports.py`)
- InventoryReport: Leerer Bericht, Bericht mit Daten, Werte korrekt
- MovementReport: Leerer Bericht, Bericht mit Daten, Sortierung
- Statistikreport: Bewegungstypen, Top-Produkte, Netto-Bestandsveränderung

### SQLite-Tests (`test_sqlite_repository.py`)
- Produkt speichern und laden
- Bewegung speichern und laden
- Produkt löschen

## Integration Tests

### TestIntegration (`test_integration.py`)
- `test_full_workflow` – Kompletter Workflow (erstellen → ändern → berechnen)
- `test_report_generation` – Berichte generieren über ConsoleReportAdapter

## Test-Ausführung

### Alle Tests
```bash
pytest tests/ -v
```

### Nur Unit Tests
```bash
pytest tests/unit/ -v
```

### Nur GUI Tests
```bash
pytest tests/unit/test_gui.py -v
```

### Nur Integration Tests
```bash
pytest tests/integration/ -v
```

### Mit Coverage
```bash
pytest --cov=src tests/ --cov-report=html
```

### Einzelnen Test ausführen
```bash
pytest tests/unit/test_domain.py::TestProduct::test_product_creation -v
```

## Coverage-Ziele

- **Domain Layer:** 100% Abdeckung
- **Services:** 95%+ Abdeckung
- **Adapters:** 90%+ Abdeckung
- **UI:** 39 automatisierte Tests + manueller Testplan (`docs/gui_testplan.md`)

## Test-Naming-Konvention

```
test_<component>_<action>_<expected_result>

Beispiele:
- test_product_creation()                        ✓
- test_product_validation_negative_price()       ✓
- test_filter_by_name()                          ✓
- test_green_for_sufficient_stock()              ✓
- test_full_workflow()                           ✓
```

## Test-Metriken

| Milestone | Unit-Tests | Integration | Coverage | Status |
|-----------|-----------|-------------|----------|--------|
| v0.2      | 5+        | 1           | 80%+     | ✅ |
| v0.3      | 10+       | 3           | 85%+     | ✅ |
| v0.4      | 100+      | 2           | 90%+     | ✅ |
| v0.5      | 110+      | 5           | 90%+     | ⏳ |
| v1.0      | 120+      | 8           | 95%+     | ⏳ |

---

**Letzte Aktualisierung:** 2026-03-24
**Version:** 0.4.0
