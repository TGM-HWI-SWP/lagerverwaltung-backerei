# Release Notes – v0.2.0 (Walking Skeleton & Architektur)

**Release Date:** 24. Februar 2026

## 🎯 Release-Ziele (erfolgreich abgeschlossen)

✅ **Architektur definieren** – Port-Adapter-Architektur implementiert  
✅ **Walking Skeleton** – Lauffähige Grundstruktur mit allen Schichten  
✅ **GUI-Entwurf** – PyQt6 UI mit Dialog-System und grundlegenden Funktionen  
✅ **Dokumentation** – Umfassende Architektur-Dokumentation

---

## 📦 Komponenten in v0.2

### 1. **Domain Layer** (`src/domain/`)
- `Product` Klasse mit Validierung
- `Warehouse` Klasse für Lagerverwaltung
- `Movement` Klasse für Lagerbewegungen
- Geschäftslogik unabhängig von UI/DB

### 2. **Service Layer** (`src/services/`)
- `WarehouseService` - orchestriert Geschäftslogik
- Methoden für Produkt-CRUD und Bestandsverwaltung
- Validierung und Error-Handling

### 3. **Adapter Layer** (`src/adapters/`)
- `RepositoryPort` - abstrakte Schnittstelle
- `InMemoryRepository` - Basis-Implementierung
- `ReportAdapter` - Report-Grundgerüst

### 4. **UI Layer** (`src/ui/`)
- `WarehouseMainWindow` - Hauptfenster mit PyQt6
- `ProductDialogWindow` - Dialog für Produkt-Verwaltung
- Tabel-Widget für Produktliste
- Funktionsfähig zum Hinzufügen/Bearbeiten von Produkten

### 5. **Dokumentation** (`docs/`)
- `architecture.md` - detaillierte Architektur-Beschreibung
- `contracts.md` - Schnittstellen-Dokumentation
- `DATACLASS_ERKLAERT.md` - Python Dataclass Erklärung

---

## 🚀 Wie ihr die App testet

```bash
# 1. Dependencies installieren
pip install -e .

# 2. App starten
python -m src.ui

# 3. GUI-Test
- Produkt hinzufügen Button klicken
- Dialog ausfüllen und speichern
- Produkt sollte in Tabelle erscheinen
```

---

## ✅ Checkliste - Fertig für v0.2

- [x] Architektur-Dokumentation komplett
- [x] Domain-Modelle implementiert & validiert
- [x] Service-Layer mit Business Logic
- [x] PyQt6 GUI lauffähig
- [x] Port-Adapter-Pattern aktiv
- [x] Test-Struktur vorhanden
- [x] pyproject.toml konfiguriert
- [x] README mit Setup-Anleitung
- [x] Alle Python-Dateien mit Docstrings

---

## 🔜 Was kommt in v0.3?

- **Kernlogik & GUI-Minimum** Expansion
- Bestandsverwaltung erweitern (Ein-/Ausgang)
- Persistierung mit TinyDB
- Erweiterte GUI-Features
- Unit-Tests schreiben

---

## 📊 Projekt-Status

```
v0.1 ✅ Projektstart & Rollen
v0.2 ✅ Architektur & Walking Skeleton  ← AKTUELL
v0.3 ⏳ Kernlogik & GUI-Minimum
v0.4 ⏳ Reports
v0.5 ⏳ Tests & Stabilisierung
v1.0 ⏳ Finale, stabile Version
```

---

## 🏗️ Architektur-Übersicht

```
┌──────────────────────────────────┐
│    UI Layer (PyQt6)              │
│  WarehouseMainWindow, Dialoge    │
└────────────┬─────────────────────┘
             │
┌────────────▼─────────────────────┐
│    Service Layer                 │
│  WarehouseService                │
└────────────┬─────────────────────┘
             │
┌────────────▼─────────────────────┐
│    Domain Layer                  │
│  Product, Warehouse, Movement    │
└────────────┬─────────────────────┘
             │
      ┌──────┴──────┐
      │             │
 ┌────▼──────┐ ┌───▼──────────┐
 │  Ports    │ │  Adapters    │
 │(Abstract) │ │(Implemen.)   │
 └───────────┘ └──────────────┘
```

---

## 📝 Nächste Schritte für v0.3

1. **Persistierung** - TinyDB Integration
2. **Erweiterte GUI**:
   - Bestandsein-/ausgang Dialog
   - Suchfunktion
   - Produktdetails-View
3. **Service-Erweiterung**:
   - Bewegungshistorie
   - Bestandsabfragen
4. **Tests schreiben** für Domain & Service

---

## 👥 Team-Hinweise

- **Architektur folgen**: Neue Code-Features in die richtige Schicht (Domain/Service/Adapter/UI)
- **Port-Adapter nutzen**: Neue Adapter (z.B. neue DB) über RepositoryPort abstrahieren
- **Testen**: Vor dem commit Tests ausführen
- **Dokumentieren**: Neue Features in architecture.md dokumentieren

---

**Version:** 0.2.0  
**Release Date:** 24. Februar 2026  
**Status:** ✅ Stable - Ready for v0.3 development
