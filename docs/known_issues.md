# Known Issues

## Aktuelle Probleme

### Kritisch
- Keine kritischen Issues momentan

### Hoch
- Keine

### Mittel
- [ ] `CHANGELOG.md` und Release Notes für v0.3/v0.4 nachträglich ergänzt – ggf. unvollständig
- [ ] `retrospective.md` ist noch unausgefüllt (Template)

### Niedrig
- [ ] Beim Starten mit SQLite (`--repo sqlite`) wird die `.db`-Datei im aktuellen Verzeichnis erstellt, kein konfigurierbarer Standardpfad
- [ ] Report-Export nur als `.txt` möglich, kein PDF/CSV

---

## Gelöste Issues (Archiv)

### v0.4
- ✓ `src/ui/__init__.py` enthielt eine veraltete GUI-Kopie (v0.1) statt der aktuellen `main_window.py` – behoben durch Re-Export
- ✓ `python -m src.ui` schlug fehl wegen fehlender `__main__.py` – behoben
- ✓ Versionsnummer im Fenstertitel war "v0.3.0" statt "v0.4.0" – behoben
- ✓ Unused `QComboBox`-Import in `dialogs.py` – entfernt

### v0.3
- ✓ Merge-Konflikt in `src/services/__init__.py` zwischen Re-Export und Inline-Klasse – zugunsten Re-Export gelöst

### v0.2
- ✓ Merge-Konflikt in `docs/contracts.md` zwischen Rolle 1 und Rolle 2 – beide Features behalten

### v0.1
- ✓ Anfangsproblem bei Repository-Erstellung

---

## Bekannte Limitationen

### Features, die absichtlich nicht implementiert sind
- Benutzer-Authentifizierung
- Grafische Reports mit Matplotlib (geplant für v1.0)
- Mehrsprachigkeit
- Batch-Import/Export von Produkten

### Performance-Limitationen
- In-Memory Repository: max. ~100.000 Produkte pro Session
- Keine Pagination implementiert
- SQLite-Repository lädt alle Daten beim Start in den Speicher

---

**Letzte Aktualisierung:** 2026-03-24
**Version:** 0.4.0
