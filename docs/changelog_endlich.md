# Changelog - Rolle 1

Persönliches Changelog für Rolle 1 (Contract Owner & Projektverantwortung)

---

## [v0.2] - 2026-02-24

### Implementiert

#### Phase 1: Dokumentation & Planung (2026-02-10)
- ✅ **Projektcharta & PSP überprüft** - Projektmanagement-Dokumentation validiert
- ✅ **contracts.md erweitert** - GUIPort Schnittstelle hinzugefügt
- ✅ **Exception Handling definiert** - 4 Custom Exceptions spezifiziert (ProductNotFoundError, InsufficientStockError, InvalidProductDataError, RepositoryError)
- ✅ **Adapter-Implementierungen dokumentiert** - InMemory, SQLite, JSON, Console, File konkretisiert
- ✅ **Report-Formate spezifiziert** - Text & JSON Formate mit Beispielen festgelegt
- ✅ **Validierungsregeln definiert** - Detaillierte Feldvalidierung für Product & Movement (Mindest-/Maximalwerte)
- ✅ **Bäckerei-Kategorien festgelegt** - 5 vordefinierte Kategorien: Brot, Backware, Kuchen, Süßes, Sonstiges
- ✅ **Architektur-Diagramm erstellt** - Visual Übersicht aller Schnittstellen
- ✅ **Rollen-Abhängigkeiten dokumentiert** - Klare Definition was Rolle 2, 3, 4 braucht

#### Phase 2: Code Refactoring & Release (2026-02-24)
- ✅ **Codestruktur aufgeräumt** - Code aus __init__.py in separate Module verschoben
  - `src/services/warehouse_service.py` (separate Datei)
  - `src/ui/main_window.py` (separate Datei)
  - `src/ui/dialogs.py` (separate Datei)
- ✅ **Separation of Concerns** - __init__.py nur noch Imports, kein Code
- ✅ **Contracts komplett überarbeitet** - Tabellen, Beispiele, Import-Patterns, Version-Matrix
- ✅ **CHANGELOG.md erstellt** - Release-History dokumentiert
- ✅ **RELEASE_NOTES_v0.2.md erstellt** - Ausführliche v0.2 Dokumentation
- ✅ **pyproject.toml aktualisiert** - Version auf 0.2.0
- ✅ **Feature-Branch Struktur initiiert** - feature/rolle1/contracts-v0.3, feature/rolle2/domain-models, etc.
- ✅ **Team-Aufgabenliste erstellt** - ROLLE1_AUFGABEN_v0.3.md für Koordination

### Tests geschrieben
- Keine (Dokumentation/Release)

### Commits
```
git tag -a v0.2.0 "Release v0.2.0: Walking Skeleton & Architektur"
chore: release v0.2.0 - Walking Skeleton & Architektur
refactor(structure): bereinige Code in __init__ Files und verbessere Ordnerstruktur
```

### Mergekonflikt(e)
- Keine (Solo Development auf main)

### Notizen
- ✔️ v0.2 Release abgeschlossen
- ✔️ Codequalität verbessert durch Modul-Separation
- ✔️ Contracts für v0.3 Development vorbereitet
- ✅ Feature-Branches auf develop bereit für Team-Arbeit
- ⏳ Nächste Aufgaben: v0.3 Integration koordinieren, Merge-Konflikte handling trainieren

---

## [v0.3] - 2026-03-17

### Implementiert
- Peer-Feedback-Runde im Team vorbereitet und durchgeführt
- Feedback aus den Rollen gesammelt (Schnittstellenklarheit, Doku-Stand, Merge-Vorgehen)
- Offene Punkte in Contracts und Doku priorisiert

### Tests geschrieben
- Keine eigenen neuen Tests (Rolle 1 Fokus: Koordination & Qualitätssicherung)

### Commits
```
- docs: peer feedback erfasst und Follow-ups für Team vorbereitet
```

### Mergekonflikt(e)
- Konfliktanalyse unterstützt und Lösungsstrategie mit Team abgestimmt

---

## [v0.4] - 2026-03-24

### Implementiert
- Mergekonflikt-Dokumentation erstellt und nachvollziehbar strukturiert
- Abgleich Projektstand gegen Aufgabenkriterien durchgeführt
- PM-/Retro-/KI-Dokumentation vervollständigt und aktualisiert
- Versionierungsstand (Tags) geprüft und ergänzt
- SQLite-Persistenz im Startpfad abgesichert (stabiler absoluter DB-Pfad im Projektordner)
- GUI-Start verbessert: Produkt- und Bewegungsdaten werden beim Öffnen automatisch geladen

### Tests geschrieben
- Keine neuen Unit-Tests, aber Teststatus validiert (Suite grün)

### Commits
```
- docs: mergekonflikt dokumentation
- docs: retrospective und KI-Einsatz ergänzt
- chore: version tags für Meilensteine ergänzt
- fix(ui): sqlite default path stabilisiert und auto-refresh beim Start aktiviert
```

### Mergekonflikt(e)
- Konflikte in UI-/Dokubereich analysiert, bereinigt und dokumentiert

---

## [v0.5] - Offen

### Implementiert
- Stabilisierungsschritte vorbereitet (offene Doku-/Contract-Punkte)

### Tests geschrieben
- Laufende Regressionstests bei Änderungen

### Commits
```
- folgt mit v0.5-Abschluss
```

### Mergekonflikt(e)
- Keine neuen

---

## [v1.0] - Offen

### Implementiert
- Finalisierung ausständig

### Tests geschrieben
- Finale Abnahmetests ausständig

### Commits
```
- folgt zu v1.0
```

### Mergekonflikt(e)
- Offen

---

## Zusammenfassung

**Gesamt implementierte Features:** Fokus auf Koordination, Contracts, Konfliktlösung und Projektdokumentation  
**Gesamt geschriebene Tests:** Keine direkten neuen Tests (Rolle 1 Schwerpunkt)  
**Gesamt Commits:** Siehe Git-Historie Rolle 1 Branch/Integration  
**Größte Herausforderung:** Mergekonflikte mit parallel veränderten Team-Dateien sauber und nachvollziehbar lösen  
**Schönste Code-Zeile:** `parser.add_argument("--repo", choices=["memory", "sqlite"], default="sqlite")`

---

**Changelog erstellt von:** Pia Endlich (Rolle 1)  
**Letzte Aktualisierung:** 2026-03-24
