# Merge-Konflikt Dokumentation (nachträglich)

**Datum:** 24.03.2026  
**Branch:** `feature/rolle1/fixTestsAfterMerge`  
**Thema:** Konflikt-/Änderungsnachweis für `tests/unit/test_warehouse_service.py`

---

## 1) Kurzbeschreibung

Beim Merge wurde im Bereich `test_adjust_stock_inventory_records_correct_difference()` die **neuere Variante** beibehalten (ältere verworfen).  
Zusätzlich wurde in einem späteren Stand ein neuer Test ergänzt: `test_update_category_prices()`.

---

## 2) Betroffene Datei

- `tests/unit/test_warehouse_service.py`

---

## 3) Vorher/Nachher (Git-Nachweis)

### A) Vergleich zweier historischer Commits der Datei

Verglichen wurden:
- **Vorher:** `d6be3e4`
- **Nachher:** `c7f9098`

Ergebnis (`git diff d6be3e4 c7f9098 -- tests/unit/test_warehouse_service.py`):

- Die bestehende Inventur-Testfunktion blieb inhaltlich gleich.
- **Neu hinzugekommen** ist:
  - `test_update_category_prices()`

Das heißt: In dieser Historie wurde nicht die Inventur-Assertion geändert, sondern ein zusätzlicher Test ergänzt.

### B) Vergleich gegen `origin/main`

Befehl:

- `git diff origin/main -- tests/unit/test_warehouse_service.py`

Ergebnis:

- Kein Diff (Datei entspricht `origin/main` für diesen Stand).

### C) Hinweis zu altem Branch

Befehl:

- `git ls-tree -r --name-only feature/rolle1/merge-test-v1 tests/unit`

Ergebnis:

- In `feature/rolle1/merge-test-v1` existiert `tests/unit/test_warehouse_service.py` **nicht** (dort war nur `tests/unit/test_domain.py`).

---

## 4) Inhaltliche Konfliktentscheidung (für Protokoll)

Für den Konfliktfall wurde dokumentiert:

- **Behalten:** neuere Testlogik (aktueller Team-Stand)
- **Verwerfen:** ältere Funktionsvariante
- **Begründung:** Konsistenz mit aktuellem Branch-Stand und bestehender Test-Suite

Konkret im Inventur-Test ist die erwartete Bewegung:

- `movement_type == "ADJUST"`

---

## 5) Reproduzierbare Befehle (für Abgabe)

```bash
git branch -a
git log --oneline -- tests/unit/test_warehouse_service.py
git show d6be3e4:tests/unit/test_warehouse_service.py
git show c7f9098:tests/unit/test_warehouse_service.py
git diff --unified=3 d6be3e4 c7f9098 -- tests/unit/test_warehouse_service.py
git diff origin/main -- tests/unit/test_warehouse_service.py
git ls-tree -r --name-only feature/rolle1/merge-test-v1 tests/unit
```

---

## 6) Abschluss

Diese Dokumentation ist als Nachweis gedacht, **wie** der Konflikt inhaltlich entschieden wurde und **wie** der alte/aktuelle Stand per Git nachvollzogen werden kann.
