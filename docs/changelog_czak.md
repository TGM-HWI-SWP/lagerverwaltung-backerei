# Changelog - [Name]

Persönliches Changelog für Przemyslaw Czak, Rolle 2 Businesslogik & Report A 

---

## [v0.2] - 10.02.2026

### Implementiert
Domänen-Modelle für Bäckerei-Produkte und Lagerbewegungen initialisiert
WarehouseService mit grundlegenden CRUD-Operationen erstellt
Validierungslogik für Preise und Bestände in der Domäne integriert

### Tests geschrieben
keine

### Commits
```
Keine in Woche 2
```

### Mergekonflikt(e)
Keine

---

## [v0.3] - 17.02.2026

### Implementiert
delete_product im Service implementiert zur vollständigen Port-Compliance
Walking Skeleton: Technischer Durchstich von Service zu In-Memory-Repository

### Tests geschrieben
Keine

### Commits
```
- feat(service): implement delete_product to comply with repository port
- docs(docs): update week 3 changelog with feature commits
```

### Mergekonflikt(e)
noch keine

---

## [v0.4] – 24.02.2026

### Implementiert
- ✅ Reports modularisiert: `InventoryReport` und `MovementReport` als
  eigenständige Logik‑Klassen unter `src/reports`
- ✅ `ConsoleReportAdapter` delegiert an die neuen Report‑Klassen,
  doppelte Code‑Logik entfernt
- ✅ GUI erweitert
  - Produkt löschen implementiert
  - Anzeige von Lager‑ und Bewegungsberichten per `QMessageBox`
  - README um Startanweisung für GUI ergänzt
- ✅ Business‑Service: neuer Testfall `update_category_prices`
- ✅ Unit‑Tests für Report‑Klassen hinzugefügt
- ✅ Integrationstest verschärft (strenge Assertions, direkte
  Nutzung der Report‑Klassen)
- ✅ Dokumentation aktualisiert:
  - `docs/architecture.md` um Hinweis auf reine Report‑Klassen ergänzt
  - `docs/contracts.md` um Beschreibung/Versionen der Report‑Komponenten
  - `docs/tests.md` um `test_reports.py` und Testpfade erweitert
  - `README.md` ergänzt (GUI, Reports, …)
- ✅ Versionsangaben und Hinweise in den Docs aktualisiert
- ✅ Versionsnummer in `src/__init__.py` bestätigt

### Tests geschrieben
- `tests/unit/test_reports.py` (Leerer/inhaltlich korrekter Lager‑ &
  Bewegungsbericht)
- Erweiterung von `tests/unit/test_warehouse_service.py`
  um `test_update_category_prices`
- Integrationstest angepasst (`tests/integration/test_integration.py`)

### Commits
- `feat: add modular report classes and adapter delegation`
- `test: add report unit tests and extend warehouse service tests`
- `ui: implement delete button and report dialogs`
- `docs: update architecture, contracts, tests, README`
- `chore: bump version, update changelog`

### Mergekonflikt(e)
- Konflikte zwischen Branches `develop` und `rolle2` in `services` und
  `contracts` gelöst

---

**Changelog erstellt von:** Przemyslaw (Rolle 2)  
**Letzte Aktualisierung:** 24.02.2026  


## [v0.5] - [Datum]

### Implementiert
- [Feature/Fix]

### Tests geschrieben
- [Tests]

### Commits
```
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte]

---

## [v1.0] - [Datum]

### Implementiert
- [Feature/Fix]

### Tests geschrieben
- [Tests]

### Commits
```
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte]

---

## Zusammenfassung

**Gesamt implementierte Features:** [Anzahl]  
**Gesamt geschriebene Tests:** [Anzahl]  
**Gesamt Commits:** [Anzahl]  
**Größte Herausforderung:** [Beschreibung]  
**Schönste Code-Zeile:** [Code-Snippet]

---

**Changelog erstellt von:** [Name]  
**Letzte Aktualisierung:** [Datum]
