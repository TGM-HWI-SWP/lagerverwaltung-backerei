# Repository-Setup Anleitung

**Status:** ✅ Konfiguriert für v0.1  
**Datum:** 10.02.2025  
**Verantwortlich:** Rolle 1 (Contract Owner)

---

## 1. Initiale Git-Konfiguration

### 1.1 Lokale Konfiguration

```bash
# Überprüfe aktuelle Konfiguration
git config --list | grep user

# Setze deinen Namen & E-Mail
git config --local user.name "Dein Name"
git config --local user.email "deine.email@schule.at"

# Überprüfe Konfiguration
git config user.name
git config user.email
```

### 1.2 Branch-Setup

```bash
# Stelle sicher, dass du auf main bist
git checkout main

# Aktualisiere main
git pull origin main

# Erstelle develop Branch (falls noch nicht vorhanden)
git checkout -b develop
git push -u origin develop

# Setze develop als Standard-Branch für lokale Entwicklung
git config --local develop.default true
```

---

## 2. Branch-Strategie (Git Flow)

### 2.1 Branch-Struktur

```
main (stable releases v1.0, v0.5, etc.)
  │
  └─ develop (integration & nächste Version)
      │
      ├─ feature/rolle1/project-management
      ├─ feature/rolle2/domain-models
      ├─ feature/rolle3/testing
      └─ feature/rolle4/gui
```

### 2.2 Branch-Naming Konvention

**Format:** `feature/rolle<N>/<kurze-beschreibung>`

**Beispiele:**
```bash
feature/rolle1/project-charter
feature/rolle2/product-class
feature/rolle3/unit-tests
feature/rolle4/main-window
bugfix/rolle2/validation-error
hotfix/database-crash
```

### 2.3 Neue Feature Branches erstellen

```bash
# Wechsel zu develop
git checkout develop
git pull origin develop

# Erstelle Feature-Branch (jede Rolle für sich)
git checkout -b feature/rolle2/product-class

# Entwickle & committe regelmäßig
git add .
git commit -m "feat(domain): create Product class with validation"
git push -u origin feature/rolle2/product-class
```

---

## 3. Commit-Nachricht Konvention

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (Pflicht)
- **`feat`** - Neue Funktion
- **`fix`** - Bug-Fix
- **`docs`** - Dokumentation
- **`test`** - Tests (Testcode nur)
- **`refactor`** - Code-Umstrukturierung
- **`ci`** - CI/CD-Konfiguration
- **`chore`** - Dependencies, Config, etc.

### Scope (Optional, empfohlen)
- `domain` - Domain-Modelle (Product, Warehouse)
- `service` - Business Logic (WarehouseService)
- `repo` - Persistierung (Repository-Adapter)
- `ui` - GUI (PyQt6)
- `test` - Test-Framework
- `docs` - Dokumentation
- `config` - Projekt-Konfiguration

### Subject (Pflicht)
- Max 50 Zeichen
- Imperative form ("add" nicht "added")
- Kleinbuchstaben
- Kein Punkt am Ende

### Body (Optional, für komplexe Changes)
- Erkläre **WAS** und **WARUM**, nicht HOW
- Max 72 Zeichen pro Zeile
- Getrennt von Subject durch Leerzeile

### Footer (Optional)
- Schließe Issues: `Closes #123`
- Breaking Changes: `BREAKING CHANGE: description`

### Beispiele

```bash
# Einfaches Feature
git commit -m "feat(domain): add Product.update_quantity method"

# Mit Body
git commit -m "feat(service): implement warehouse stock calculation

- Calculate total value based on quantity and price
- Handle negative quantities gracefully
- Add logging for audit trail"

# Mit Issue-Reference
git commit -m "fix(ui): resolve table sorting issue

Closes #42"

# Breaking Change
git commit -m "refactor(repo): change Repository interface

BREAKING CHANGE: load_all_products now returns List instead of Dict"
```

---

## 4. Pull Request & Code Review

### 4.1 PR erstellen (GitHub)

1. **Push deinen Branch**
   ```bash
   git push origin feature/rolle2/product-class
   ```

2. **Gehe zu GitHub → Pull requests → New PR**

3. **Ausfüllen:**
   - **Base:** `develop`
   - **Compare:** dein `feature/rolle2/...` Branch
   - **Title:** Kurze Beschreibung (z.B. "Add Product class with validation")
   - **Description:** 
     ```markdown
     ## Änderungen
     - Neue Product-Klasse
     - Preisvalidierung
     - Unit-Tests
     
     ## Testing
     - ✅ pytest läuft
     - ✅ Coverage 85%
     
     ## Abhängigkeiten
     - Braucht RepositoryPort Definition (von Rolle 1)
     ```

4. **Request Review von Rolle 1 & 3**

### 4.2 Code Review Checkliste

Reviewer überprüft:
- ✅ Entspricht contracts.md?
- ✅ Tests vorhanden? (mind. 80% Coverage)
- ✅ Docstrings dokumentiert?
- ✅ Keine redundanten Imports?
- ✅ Folgt Naming-Konventionen?
- ✅ Performance-Probleme?
- ✅ Security-Issues?

### 4.3 Feedback & Fixes

```bash
# Feedback erhalten
# → Fixes durchführen
git add .
git commit -m "refactor(domain): address review feedback in Product class"
git push

# Automatisch updated PR
# → Reviewer approved
# → Merge!
```

---

## 5. Merging & Integration

### 5.1 Merge in develop (Friday Integration)

```bash
# 1. Stelle sicher, dass Feature komplett ist
git checkout feature/rolle2/product-class
git pull origin develop  # Aktualisiere mit neuesten develop Changes

# 2. Merge lokal testen
git merge develop  # Eventuell Konflikte auflösen

# 3. Tests durchführen
pytest

# 4. Push & PR approval abholen
git push

# 5. Merge auf GitHub (über PR oder CLI)
# GitHub: "Squash and merge" empfohlen
# Oder CLI:
git checkout develop
git pull origin develop
git merge --squash feature/rolle2/product-class
git commit -m "feat(domain): add Product class with validation"
git push origin develop

# 6. Feature-Branch löschen
git branch -d feature/rolle2/product-class
git push origin --delete feature/rolle2/product-class
```

### 5.2 Mergekonflikt Handling

```bash
# Konflikt erkennen
git status
# >> conflict in src/domain/product.py

# Konflikt anschauen
cat src/domain/product.py
# >>> <<<<<<< HEAD
# >>> Deine Version
# >>> =======
# >>> Ihre Version
# >>> >>>>>>> feature/rolle3/...

# Auflösen:
# 1. Entscheide welche Version besser ist
# 2. Oder kombiniere beide intelligently
# 3. Entferne Konflikt-Marker

# Git sagen, dass gelöst
git add src/domain/product.py
git commit -m "fix: resolve merge conflict in product.py"
git push
```

---

## 6. Wöchentliches Workflow

### Montag (Plannung)
```bash
# 1. Aktuelle develop ziehen
git checkout develop
git pull origin develop

# 2. Neuen Feature-Branch für die Woche
git checkout -b feature/rolle2/week1-implementation

# 3. Arbeiten!
```

### Freitag (Integration)
```bash
# 1. Alle lokalen Commits pushen
git push origin feature/rolle2/week1-implementation

# 2. PR auf develop öffnen

# 3. Code Review durchführen (Rolle 1 + 3)

# 4. Nach Review: Merge in develop

# 5. Entwicklungs-Tag erstellen
git checkout develop
git pull origin develop
git tag -a v0.1 -m "Weekly release - Week 1"
git push origin v0.1

# 6. Branch aufräumen
git branch -d feature/rolle2/week1-implementation
git push origin --delete feature/rolle2/week1-implementation
```

---

## 7. .gitignore Überblick

✅ **Bereits konfiguriert für:**
- `__pycache__/` - Python Bytecode
- `.pytest_cache/` - Pytest Cache
- `.coverage` - Coverage-Reports
- `.env` - Umgebungsvariablen
- `.venv/` - Virtual Environments
- `*.pyc` - Compiled Python
- `*.log` - Logdateien
- `.vscode/` - IDE Settings (optional hinzufügen)

**Bei Bedarf ergänzen:**
```bash
# .gitignore hinzufügen (falls gewünscht)
echo ".vscode/" >> .gitignore
echo ".idea/" >> .gitignore
echo "data/*.db" >> .gitignore
echo "data/*.json" >> .gitignore
git add .gitignore
git commit -m "chore: expand gitignore for IDE and data files"
```

---

## 8. Hilfreiche Git Commands

```bash
# Status überprüfen
git status
git log --oneline -5

# Branches anschauen
git branch -a

# Unterschiede sehen
git diff
git diff origin/develop

# Letzten Commit ändern
git commit --amend

# Commit rückgängig machen (lokal)
git reset HEAD~1

# Alle Changes discarden
git reset --hard

# Tags anschauen
git tag -l
git show v0.1
```

---

## 9. CI/CD Vorbereitung

### GitHub Actions (optional für später)
Für v0.3 geplant:
- [ ] Automatic `pytest` auf Push
- [ ] Coverage Reports
- [ ] Linting (pylint, black)
- [ ] Auto-Tag erstellen bei Release

---

## 10. Rollen & Verantwortlichkeiten

| Rolle | Hauptaufgabe | Branch-Pattern |
|-------|-----------|--------|
| Rolle 1 | Koordination, Dokumentation | `feature/rolle1/*` |
| Rolle 2 | Domain & Service | `feature/rolle2/*` |
| Rolle 3 | Reports & Tests | `feature/rolle3/*` |
| Rolle 4 | GUI | `feature/rolle4/*` |

**Rolle 1 ist auch für:**
- Develop Branch Verwaltung
- PR-Review Koordination
- Merge-Konflikt Support
- Tag/Release Management

---

## ✅ Setup Checklist

- [ ] Lokale Git-Konfiguration gesetzt
- [ ] Develop Branch existiert & ist aktuell
- [ ] Jede Rolle hat ihren Feature-Branch erstellt
- [ ] .gitignore ist konfiguriert
- [ ] Git Workflow Dokumentation gelesen (dieses Dokument)
- [ ] GIT_WORKFLOW.md gelesen
- [ ] Erste Commits mit richtiger Konvention durchgeführt
- [ ] PR-Template (optional) erstellt

---

**Repo-Setup abgeschlossen!** 🎉  
**Nächster Schritt:** Rolle 2 startet mit Domain-Modellen (feature/rolle2/domain-models)
