# Projektvorlage für Softwareentwicklung und Projektmanagement

Dies ist eine **vollständige, produktionsreife Projektvorlage** für die 8-Wöchige Schulprojekt im Fach Softwareentwicklung & Projektmanagement (4. Jahrgang).

## 🎯 Was ist enthalten?

### ✅ Programmiergerüst
- **Basis-Klassen:** `Product`, `Warehouse`, `Movement`
- **Port-Adapter-Architektur** für Maximum-Testbarkeit
- **Service-Layer** für Geschäftslogik
- **In-Memory Repository** für schnelle Prototypen
- **PyQt6 GUI-Skeleton** mit Tabs und Dialogen
- **Unit & Integration Tests** (pytest)

### ✅ Dokumentations-Vorlagen
- README.md - Komplette Projektübersicht
- docs/contracts.md - Schnittstellen-Dokumentation (Rolle 1)
- docs/architecture.md - Architektur-Erklärung
- docs/tests.md - Test-Strategie und Übersicht
- docs/projektmanagement.md - PM-Dokumente (Projektcharta, PSP, Gantt)
- docs/retrospective.md - Retrospektive pro Milestone
- docs/changelog_template.md - Persönliche Changelog-Vorlage
- docs/known_issues.md - Issues und Limitations
- GIT_WORKFLOW.md - Git Best Practices

### ✅ Vorkonfiguration
- pyproject.toml mit allen Dependencies
- pytest-Konfiguration
- Code-Style-Einstellungen (.pylintrc, .flake8)
- .gitignore für Python-Projekte

## 🚀 Quick Start

### Installation
```bash
# 1. Dependencies installieren
pip install -e .
pip install -e ".[dev]"

# 2. Tests ausführen (verifiziert Setup)
pytest tests/ -v

# 3. GUI starten (optional)
python -m src.ui
```

### Erste Schritte
```python
from src.adapters.repository import RepositoryFactory
from src.services import WarehouseService

# Initialisierung
repository = RepositoryFactory.create_repository("memory")
service = WarehouseService(repository)

# Produkt erstellen
product = service.create_product(
    product_id="LAPTOP-001",
    name="ProBook Laptop",
    description="Hochwertiger Laptop",
    price=1200.0,
    category="Elektronik",
    initial_quantity=5
)

# Bestand ändern
service.add_to_stock("LAPTOP-001", 3, reason="Neuer Einkauf", user="Max Mustermann")
```

## 📋 Rollenverteilung

| Rolle | Aufgaben |
|-------|----------|
| **1: Contract Owner** | Projektleitung, Schnittstellen-Docs, Releases |
| **2: Businesslogik** | Domain-Modelle, Service-Layer, Report A |
| **3: Tests & Reports** | Advanced Tests, Report B, Qualitätssicherung |
| **4: GUI** | PyQt6-Interface, User Experience, Integration |

## 📅 8-Wochen Roadmap

```
Woche 1: Projektstart, Roles, Basis-Architektur (v0.1)
Woche 2: Schnittstellen-Docs, Walking Skeleton (v0.2)
Woche 3: Kernlogik, GUI-Minimum (v0.3)
Woche 4: Coding Sprint 1 + Report A (v0.4)
Woche 5: Coding Sprint 2 + Report A Final (v0.4)
Woche 6: Report B, Advanced Tests (v0.4)
Woche 7: Stabilisierung, Dokumentation (v0.5)
Woche 8: v1.0 Final, Präsentation & Abgabe
```

## 🏗️ Projektstruktur

```
projekt/
├── src/
│   ├── domain/          # Business-Entities
│   ├── ports/           # Interfaces (abstrakt)
│   ├── adapters/        # Implementierungen
│   ├── services/        # Geschäftslogik
│   ├── ui/              # PyQt6 GUI
│   └── reports/         # Report-Module
├── tests/
│   ├── unit/            # Unit-Tests
│   └── integration/      # Integration-Tests
├── docs/
│   ├── contracts.md
│   ├── architecture.md
│   ├── tests.md
│   ├── projektmanagement.md
│   ├── retrospective.md
│   └── changelog_template.md
├── pyproject.toml       # Dependencies & Config
├── README.md            # Projekt-Übersicht
└── GIT_WORKFLOW.md      # Git Best Practices
```

## 📚 Wichtige Dokumentationen

### Für Schüler/innen
- **Start:** README.md lesen
- **Verstehen:** docs/architecture.md studieren
- **Entwickeln:** GIT_WORKFLOW.md befolgen
- **Dokumentieren:** docs/changelog_<name>.md führen

### Für Lehrperson
- **Kontrolle:** docs/projektmanagement.md
- **Qualität:** docs/tests.md & docs/contracts.md
- **Progress:** Persönliche Changelogs pro Woche checken

## 🧪 Testing

```bash
# Alle Tests
pytest tests/ -v

# Unit Tests nur
pytest tests/unit/ -v

# Mit Coverage
pytest --cov=src tests/
```

**Ziel:** 90%+ Test-Coverage bis v1.0

## 🔗 Architektur-Highlights

### Port-Adapter Pattern
```
UI ↔ Service ↔ Domain ↔ Ports ↔ Adapters (Repository, Reports)
```

**Vorteile:**
- ✅ Testbarkeit: Mock-Repositories für Tests
- ✅ Wartbarkeit: Klare Separation of Concerns
- ✅ Erweiterbarkeit: Neue Adapter ohne Code-Änderung

### Versionierung
```
Tags: v0.1, v0.2, v0.3, v0.4, v0.5, v1.0
Pro Milestone: Neues Tag + Persönliche Changelogs
```

## 🎓 Lernziele

1. **Professionelle Versionsverwaltung** (Git, Mergekonflikte)
2. **Objektorientierte Architektur** (Port-Adapter, SOLID)
3. **Automatisiertes Testing** (Unit, Integration, Coverage)
4. **Agile Vorgehensweise** (Iterative Entwicklung, Retrospektiven)
5. **Dokumentation als Code** (Markdown, API-Docs)
6. **GUI-Entwicklung** (PyQt6, User Experience)
7. **Teamfähigkeit** (Rollen, Kommunikation, Mergekonflikte)

## ⚙️ Technologie-Stack

- **Language:** Python 3.10+
- **GUI:** PyQt6
- **Testing:** pytest
- **Storage:** In-Memory (default), SQL (optional), JSON (optional)
- **Version Control:** Git
- **Documentation:** Markdown

## 🤝 Git-Workflow (Kurzversion)

```bash
# Feature Branch
git checkout -b feature/rolle2/product-validation
git commit -m "feat(domain): add price validation"
git push origin feature/rolle2/product-validation

# Pull Request → Code Review → Merge to develop
git checkout develop && git pull origin develop
```

**Mergekonflikte?** → Dokumentieren in `docs/changelog_<name>.md`

## 📞 Support & Fragen

### Fehler beim Setup?
1. Python 3.10+ installiert? `python --version`
2. Alle Dependencies installiert? `pip install -e ".[dev]"`
3. Tests funktionieren? `pytest tests/ -v`

### Architektur-Fragen?
→ Siehe `docs/architecture.md` und `docs/contracts.md`

### Testing-Fragen?
→ Siehe `docs/tests.md` und `tests/unit/test_domain.py` (Beispiele)

## 📄 Lizenz

Schulprojekt - TGM (Die Schule der Technik)

---

**Version:** 0.4.0
**Erstellt:** 2025-01-20
**Für:** Softwareentwicklung & Projektmanagement, 5. Jahrgang, 7-8 Wochen
