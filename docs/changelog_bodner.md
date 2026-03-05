# Changelog - Noah Bodner

Persönliches Changelog für Noah Bodner, Rolle: Rolle 4 - GUI & Interaktion

---

## [v0.2] - 2026-02-24

### Implementiert
- GUI-Skeleton mit 3 Tabs (Produkte, Lagerbewegungen, Berichte)
- ProductDialogWindow für Produkteingabe
- Produkttabelle mit 6 Spalten
- Grundlegende Button-Struktur (Hinzufügen, Aktualisieren, Löschen)

### Tests geschrieben
- Keine (Skeleton-Phase)

### Commits
```
- (siehe git log für v0.2 commits)
```

### Mergekonflikt(e)
- Keine

---

## [v0.3] - 2026-03-03

### Implementiert
- Delete-Funktion mit Bestätigungsdialog
- Lagerbestandsbericht-Anzeige im Reports-Tab (ConsoleReportAdapter)
- Bewegungsprotokoll-Anzeige im Reports-Tab
- Produkt-Bearbeitung (Edit-Dialog mit vorausgefüllten Daten, ID gesperrt)
- Einlagern-Dialog (Menge, Grund, Benutzer)
- Auslagern-Dialog (Menge, Grund, Benutzer)
- Echtzeit-Suchfilter (Name, ID, Kategorie, case-insensitive)
- Lagerbewegungen-Tab mit echten Daten (neueste zuerst)
- Responsive Tabellen mit dynamischer Spaltenbreite
- Bäckerei-Theme (QSS-Stylesheet mit warmen Farben)
- Bestandsfarben: Rot (kritisch <=5), Orange (knapp 6-15), Grün (>15)
- Statusleiste mit Produktanzahl und Gesamtwert
- Export-Funktion (Berichte als .txt speichern)
- Farbige Bewegungstypen (IN=grün, OUT=rot)
- Farbige Buttons (Löschen=rot, Einlagern=grün, Auslagern=orange)
- contracts.md mit GUI-Schnittstellen erweitert
- Manuelle Testcheckliste (docs/gui_testplan.md)

### Tests geschrieben
- TestMainWindow (7 Tests): Fenster, Tabs, Tabellen, Suchfeld
- TestProductManagement (4 Tests): Refresh, Werte, Löschen, Mehrere Produkte
- TestSearchFilter (5 Tests): Name, Kategorie, ID, Leer, Case-insensitive
- TestMovements (3 Tests): Leer, Nach Änderung, Sortierung
- TestReports (4 Tests): Leer/Voll Inventar, Leer/Voll Bewegungen
- TestDialogs (7 Tests): Add/Edit-Modus, Daten, StockDialog Modi
- TestStatusBar (4 Tests): Existenz, Leer, Nach Add, Nach Delete
- TestStockColorCoding (3 Tests): Grün, Orange, Rot
- TestExport (2 Tests): Button deaktiviert/aktiviert

### Commits
```
- feat(ui): implement complete GUI for Rolle 4
- feat(ui): add styling, color coding, status bar, export, docs
```

### Mergekonflikt(e)
- `src/services/__init__.py`: Konflikt zwischen HEAD (Re-Export) und feature/rolle2/merge-test-v2 (Inline-Klasse). Aufgelöst zugunsten HEAD, da warehouse_service.py separat existiert.

---

## [v0.4] - [Datum]

### Implementiert
- [Ausstehend: Report B von Rolle 3 in GUI einbinden]

### Tests geschrieben
- [Tests]

### Commits
```
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte]

---

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

**Gesamt implementierte Features:** 17
**Gesamt geschriebene Tests:** 39
**Gesamt Commits:** [wird aktualisiert]
**Größte Herausforderung:** Merge-Konflikt in services/__init__.py auflösen ohne Code von Rolle 2 zu verlieren
**Schönste Code-Zeile:** `self.search_field.textChanged.connect(self._filter_products)`

---

**Changelog erstellt von:** Noah Bodner
**Letzte Aktualisierung:** 2026-03-03
