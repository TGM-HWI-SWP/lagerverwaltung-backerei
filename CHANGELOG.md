# Changelog

Alle wichtigen Änderungen in diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/).

## [0.4.0] – 2026-03-24

### ✅ Added
- **GUI-Fix:** `__init__.py` verwendet jetzt `main_window.py` statt veraltete Kopie
- **`__main__.py`** hinzugefügt – `python -m src.ui` funktioniert jetzt korrekt
- **Versionsnummer** im Fenstertitel auf v0.4.0 aktualisiert

### 🔧 Fixed
- Doppelte `WarehouseMainWindow`-Klasse entfernt (alte v0.1-Kopie in `__init__.py`)
- Doppelter `QApplication`-Import entfernt
- Unused `QComboBox`-Import in `dialogs.py` entfernt

---

## [0.3.0] – 2026-03-03

### ✅ Added
- **Komplette GUI** (Rolle 4): Suchfunktion, Bestandsfarben, Statusleiste, Export
- **Dialoge:** ProductDialogWindow (Add/Edit), StockDialog (Ein-/Auslagern)
- **Bäckerei-Theme:** QSS-Stylesheet mit warmen Farben
- **39 GUI-Tests** in `tests/unit/test_gui.py`
- **Manueller Testplan** in `docs/gui_testplan.md`
- **SQLite-Repository** als persistente Speicheroption (Rolle 2)
- **Modulare Reports:** `InventoryReport` und `MovementReport` als eigenständige Klassen (Rolle 2)
- **Report B:** Statistikreport mit Bewegungstypen und Top-Produkte (Rolle 3)
- **Erweiterte Tests:** `test_reports.py`, `test_warehouse_service.py`, `test_sqlite_repository.py` (Rolle 3)
- **Test-Fixtures:** `tests/fixtures.py` mit Dummy-Daten und Edge Cases

### 📋 Features
- Bestandsfarben: Rot (kritisch <=5), Orange (knapp 6-15), Grün (>15)
- Farbige Bewegungstypen (IN=grün, OUT=rot)
- Farbige Buttons (Löschen=rot, Einlagern=grün, Auslagern=orange)
- Report-Export als .txt-Datei
- Echtzeit-Suchfilter (Name, ID, Kategorie, case-insensitive)
- WarehouseService erweitert: `delete_product`, `filter_movements_by_date/type`, `adjust_stock_inventory`, `get_low_stock_items`, `update_category_prices`

---

## [0.2.0] – 2026-02-24

### ✅ Added
- **Architektur** vollständig implementiert (Port-Adapter / Hexagonal Architecture)
- **Walking Skeleton** mit lauffähiger Grundstruktur
- **GUI mit PyQt6** - Benutzeroberfläche mit Dialog-System für Produktmanagement
- **Domain-Layer** mit Product und Warehouse Entities
- **Service-Layer** mit WarehouseService und Business Logic
- **Adapter-Pattern** für flexible Datenspeicherung (Repository)
- **Umfangreiche Dokumentation** in `docs/architecture.md`
- **Test-Grundgerüst** für Unit- und Integration Tests
- **Projektstruktur** nach professionellen Standards

### 📋 Features
- Produkte hinzufügen, bearbeiten, löschen
- Bestandsverwaltung mit Validierung
- Dialog-System für Dateneingabe
- Port-Adapter-Architektur für Erweiterbarkeit
- Grundgerüst für Lagerbewegungen

### 🔧 Technologie Stack
- Python 3.10+
- PyQt6 6.6.0+ (GUI)
- TinyDB 4.8.0+ (Persistierung)
- pytest 7.4.0+ (Testing)

---

## [0.1.0] – 2026-02-20

### ✅ Added
- **Projektstart** und initiale Rollen-Definition
- **Contracts** und Schnittstellen-Dokumentation
- **Projektvorlage** mit Grundstruktur
- **Dokumentation** für Projektmanagement

---

## Release-Richtlinien

### Versions-Schema
- **Patch (0.0.x)**: Bugfixes und kleine Verbesserungen
- **Minor (0.x.0)**: Neue Features, keine Breaking Changes
- **Major (x.0.0)**: Breaking Changes, große Umbrüche

### Beim Release durchführen
1. CHANGELOG.md aktualisieren
2. Version in `pyproject.toml` erhöhen
3. Git commit: `chore: release v0.x.0`
4. Git tag: `v0.x.0`
5. Alle Tests müssen grün sein
