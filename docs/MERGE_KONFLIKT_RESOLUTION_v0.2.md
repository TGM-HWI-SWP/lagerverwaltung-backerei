# Merge-Konflikt Resolution - v0.2 Integration

**Datum:** 24. Februar 2026  
**Beteiligung:** Rolle 1 (Contract Owner) + Rolle 2 (Services)  
**Konfliktstatus:** ✅ **GELÖST**

---

## 📋 Konflikt-Übersicht

| Aspekt | Details |
|--------|---------|
| **Betroffene Branches** | `develop` ↔ `feature/rolle2/domain-models` |
| **Betroffene Dateien** | `src/services/__init__.py`, `docs/contracts.md` |
| **Konflikt-Typ** | Content-Konflikt (Überlappende Änderungen) |
| **Schweregrad** | Mittel (Lösbar ohne Code-Verlust) |
| **Gelöst von** | Rolle 1 (Contract Owner) |

---

## 🔴 Konfliktursache

### Was ist passiert?

Beide Branches haben **zur gleichen Zeit** die **gleichen Dateien** geändert:

```
Feature-Branch (Rolle 2)          Main-Branch (develop)
        ↓                               ↓
    Ändert Zeile 437              Ändert Zeile 437
    in contracts.md               in contracts.md
        ↓                               ↓
    ❌ KONFLIKT!
    Git kann nicht automatisch
    zusammenführen
```

### Betroffene Bereiche

| Datei | Was geändert wurde | Von wem | Konflikt? |
|-------|-------------------|--------|-----------|
| `docs/contracts.md` | Zeile 437 (Zukünftige Änderungen) | Beide | ✅ JA |
| `src/services/__init__.py` | Imports | Nur entwickelt | ❌ NEIN |

---

## 🔍 Konflikt-Details

### Konflikt-Marker in contracts.md

```markdown
<<<<<<< HEAD
## Zukünftige Änderungen

- [ ] SQLite-Adapter implementieren
- [ ] GraphML-Report-Generierung
- [ ] Benutzer-Management erweitern
- [ ] Batch-Operationen unterstützen
- [ ] **Delete Product mit Bestätigungsdialog hinzufügen** (v0.3)

=======
## Zukünftige Änderungen

- [ ] SQLite-Adapter implementieren
- [ ] GraphML-Report-Generierung
- [ ] Benutzer-Management erweitern
- [ ] Batch-Operationen unterstützen
- [ ] **v0.5 Support mit erweiterten Features** (v0.5)

>>>>>>> feature/rolle2/merge-test-v2
```

### Was bedeutet das?

- **`<<<<<<< HEAD`**: Das ist die Version in `develop` (Person A)
- **`=======`**: Trennlinie zwischen den zwei Versionen
- **`>>>>>>> feature/rolle2/merge-test-v2`**: Das ist die Version in feature/rolle2 (Person B)

---

## ✅ Lösungsschritte

### Schritt 1: Konflikt erkennen

```bash
# Git meldet Konflikt
git merge feature/rolle2/merge-test-v2

# Output:
# CONFLICT (content): Merge conflict in docs/contracts.md
# Automatic merge failed; fix conflicts and then commit the result.

git status
# On branch develop
# You have unmerged paths.
#   both modified: docs/contracts.md
```

### Schritt 2: Datei analysieren

**Öffne `docs/contracts.md` und suche:**

```
<<<<<<< HEAD
(Konfikt-Anfang)
...
=======
(Konflikt-Mitte)
...
>>>>>>> feature/rolle2/merge-test-v2
(Konflikt-Ende)
```

**Analyse:**
- Person A (develop): Möchte Delete Dialog Feature hinzufügen
- Person B (feature/rolle2): Möchte v0.5 Features hinzufügen
- **Beide sind wichtig!** → Beide behalten

### Schritt 3: Manuell zusammenführen

**VORHER (mit Konflikt-Markern):**
```markdown
<<<<<<< HEAD
- [ ] **Delete Product mit Bestätigungsdialog hinzufügen** (v0.3)
=======
- [ ] **v0.5 Support mit erweiterten Features** (v0.5)
>>>>>>> feature/rolle2/merge-test-v2
```

**NACHHER (BEIDEN behalten):**
```markdown
- [ ] **Delete Product mit Bestätigungsdialog hinzufügen** (v0.3)
- [ ] **v0.5 Support mit erweiterten Features** (v0.5)
```

**Wichtige Regel:**
- ❌ **NICHT** einfach einen Teil löschen
- ✅ **SONDERN:** BEIDE Features sind wertvoll → beide behalten
- ❌ **NICHT** die Konflikt-Marker (`<<<<`, `====`, `>>>>`) vergessen zu löschen!

### Schritt 4: Merge abschließen

```bash
# 1. Änderungen adden
git add docs/contracts.md

# 2. Status prüfen
git status
# All conflicts fixed but you are still merging.

# 3. Merge mit Commit abschließen
git commit -m "merge: Rolle 1 + Rolle 2 Contracts zusammenführen

- Delete Product Dialog (v0.3) von Rolle 1
- v0.5 Features von Rolle 2
- Beide Features sind orthogonal (unabhängig)"

# Output:
# [develop abc1234] merge: Rolle 1 + Rolle 2 Contracts zusammenführen

# 4. Zu GitHub pushen
git push origin develop
```

### Schritt 5: Validierung

```bash
# Verifikation dass Merge erfolgreich war
git log --oneline -3
# abc1234 merge: Rolle 1 + Rolle 2 Contracts zusammenführen
# xyz9999 refactor(structure): ...
# f34bd47 chore: release v0.2.0

# Keine Konflikt-Marker mehr?
git grep "<<<<<<< HEAD" || echo "✅ Clean - Keine Konflikt-Marker!"

# Beide Features sichtbar?
grep -E "Delete Product|v0.5 Support" docs/contracts.md
# → Sollte BEIDE Features zeigen
```

---

## 📊 Konflikt-Statistiken

| Metrik | Wert |
|--------|------|
| **Dauer zur Lösung** | ~5 Minuten |
| **Betroffene Dateien** | 1 |
| **Konflikt-Blöcke** | 1 |
| **Zeilen mit Konflikt** | 7 |
| **Tests bestanden** | ✅ JA |
| **Merge erfolgreich** | ✅ JA |

---

## 💡 Was wir gelernt haben

### ✅ Best Practices

1. **Kommunikation früh**
   - Wer ändert was diese Woche?
   - Überlappende Änderungen vorbeugen

2. **Kleine, häufige Merges**
   - Nicht zwei Wochen warten
   - Early & Often mergen → kleinere Konflikte

3. **Beide Seiten verstehen**
   - Nicht einfach einen Part löschen
   - Beide Features können wertvoll sein
   - Zusammenführen statt Überschreiben

4. **Tests nach Merge**
   - Nach Konflikt-Auflösung immer testen
   - Stellt sicher dass Code funktioniert

### ⚠️ Was zu vermeiden ist

| ❌ FALSCH | ✅ RICHTIG |
|----------|----------|
| `git checkout --ours` (einfach löschen) | Datei öffnen & manuell zusammenführen |
| `git merge --abort` (ganz abbrechen) | Konflikt-Marker verstehen & lösen |
| Ohne Tests mergen | Immer nach Merge testen |
| Nicht kommunizieren | Früh mit Team absprechen |

---

## 🔗 Zukunfts-Empfehlungen

### Für nächste Merges

- ✅ Rolle 2 & Rolle 3 sollten **täglich** zu develop mergen (nicht erst am Ende)
- ✅ Role 4 sollte mit Rolle 2 kommunizieren bevor UI änderungen gemacht werden
- ✅ **Daily Stand-Up:** "Wer ändert welche Dateien diese Woche?"

### Merge-Strategie

```
develop (Main Integration Branch)
    ↑
    │ (Täglich mergen, kleine Konflikte)
    │
feature/rolle2/... ─┐
feature/rolle3/... ─┤
feature/rolle4/... ─┘

STATT:

feature/rolle2/... ─┐
                    ├─→ (Großer Konflikt am Ende!)
feature/rolle3/... ─┤
feature/rolle4/... ─┘
```

---

## 📝 Zusammenfassung

| Phase | Schritt | Status |
|-------|---------|--------|
| 1️⃣ | Konflikt erkennen | ✅ Done |
| 2️⃣ | Analyse durchführen | ✅ Done |
| 3️⃣ | Manuell zusammenführen | ✅ Done |
| 4️⃣ | Merge abschließen | ✅ Done |
| 5️⃣ | Testen & Validieren | ✅ Done |
| 6️⃣ | Zu GitHub pushen | ✅ Done |

**Ergebnis:** ✅ **Erfolgreich gelöst** - Beide Features sind jetzt in develop vorhanden!

---

## 📞 Weitere Fragen?

- **Wie erkenne ich Konflikte?** → `git status` zeigt "both modified"
- **Wie sehen Konflikt-Marker aus?** → `<<<<<<<`, `=======`, `>>>>>>>`
- **Wie löse ich sie?** → Datei öffnen, zusammenführen, Marker löschen
- **Wie weiß ich ob es funktioniert?** → Tests! `pytest`

---

**Dokumentation:** Konflikt-Resolution v0.2  
**Letztes Update:** 24. Februar 2026  
**Status:** ✅ Stabil - Ready für nächste Integrations-Phase
