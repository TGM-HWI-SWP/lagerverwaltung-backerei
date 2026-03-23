# Changelog

Alle wichtigen Änderungen in diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/).

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
