# Aufgabenliste – Rolle 1 (Contract Owner) – v0.3 Vorbereitung

**Deine Rolle:** Projektverantwortung & Schnittstellen (Contract Owner)

---

## 📋 DEINE AUFGABEN FÜR v0.3

### Phase 1: Vorbereitung (JETZT!)
- [ ] **Contracts aktualisieren** → `docs/contracts.md`
  - [ ] Alle neuen Services/Adapter dokumentieren
  - [ ] Versionseinträge hinzufügen (v0.3 Scope)
  - [ ] Änderungen: Was ist neu? Was ist gebrochen?
  
- [ ] **Feature-Übersicht erstellen** → `docs/v0.3-features.md`
  - [ ] Welche Features kommen in v0.3?
  - [ ] Abhängigkeiten zwischen Rollen klären
  - [ ] Integrationspunkte definieren

- [ ] **Team-Kick-off durchführen**
  - [ ] Jede Rolle hat ihre Feature-Branch
  - [ ] Schnittstellen erklären
  - [ ] Timeline abstimmen

### Phase 2: Integration (Während v0.3 Entwicklung)
- [ ] **Täglich Integrationschecks**
  - [ ] Welche Features sind fertig?
  - [ ] Arbeiten die Schnittstellen?
  - [ ] Merge-Konflikte lösen?

- [ ] **Code-Reviews**
  - [ ] Prüfe contracts.md Compliance
  - [ ] Validiere neuen Code gegen Architektur
  - [ ] Genehmige Feature-Branches zum Merge

- [ ] **Dokumentation aktualisieren**
  - [ ] architecture.md updaten (neue Services)
  - [ ] contracts.md erweitern
  - [ ] Integration Notes hinzufügen

### Phase 3: Release v0.3 (End of Cycle)
- [ ] **Alle Feature-Branches mergen** zu develop
- [ ] **Final-Check**: Alles funktioniert?
- [ ] **CHANGELOG & RELEASE_NOTES schreiben**
- [ ] **Git Tag v0.3.0 erstellen**
- [ ] **Release Notes auf GitHub pushen**
- [ ] **Develop → Main mergen** (nur stabile Version!)
- [ ] **Team informieren** ✅

---

## 🔗 INTEGRATIONSPOINTS FÜR v0.3

Aktuell haben wir diese Rollen/Branches:

```
👤 Rolle 1 (DEINE ROLLE)
   feature/rolle1/project-management
   └─ Contracts & Integration
   └─ Versionsverantwortung

👤 Rolle 2 – Businesslogik & Repository
   feature/rolle2/domain-models
   └─ WarehouseService erweitern
   └─ TinyDB Repository implementieren

👤 Rolle 3 – Reports & Tests
   feature/rolle3/testing-setup
   └─ Unit-Tests schreiben
   └─ Report-Generierung

👤 Rolle 4 – GUI Erwiterung
   feature/rolle4/gui-skeleton
   └─ Erweiterte UI-Features
   └─ Dialoge für Bewegungen
```

---

## 📝 WAS DU JETZT MACHEN SOLLST (KONKRETE NÄCHSTE SCHRITTE)

### 1️⃣ **JETZT – Contracts aktualisieren**

```bash
cd c:\Users\piaen\github-classroom\TGM-HWI-SWP\lagerverwaltung-backerei
git checkout develop
git pull origin develop
git checkout -b feature/rolle1/contracts-v0.3
```

**Dann in `docs/contracts.md` hinzufügen:**
- [ ] Welche neuen Methoden kommen in v0.3?
  - TinyDB-Repository als neue Implementierung?
  - Bewegungs-Schnittstellen erweitern?
  - Report-Schnittstellen clarify?

- [ ] Versionierung: v0.3 Scope definieren
- [ ] Breaking Changes? Rückwärts-Kompatibilität?

### 2️⃣ **Diese Woche – Feature-Planung**

Erstelle `docs/v0.3-PLAN.md`:
```
## v0.3: Kernlogik & GUI-Minimum

### Services die fertig sein müssen:
- [ ] WarehouseService mit Bewegungen
- [ ] Persistierungs-Service (TinyDB)
- [ ] Report-Service erweitert

### Abhängigkeiten:
- Rolle 2 (WarehouseService) → Rolle 1 (Service-Interfaces)
- Rolle 4 (GUI) → Rolle 2 (Services verfügbar)
- Rolle 3 (Tests) → Alle (um zu testen)

### Integrations-Checkpoints:
- Tag 1-2: Features in Feature-Branches
- Tag 3-4: Daily Integration Tests
- Tag 5: Finales Merging
```

### 3️⃣ **Diese Woche – Team-Kick-off**

Sag deinem Team:

> "Wir starten v0.3-Entwicklung auf develop Branch.  
> Jede Rolle arbeitet auf ihrem feature/ Branch.  
> Ich (Rolle 1) kümmere mich um Schnittstellen & Integration.  
> Contracts sind in docs/contracts.md – folgt den Interfaces!"

---

## 🚀 WORKFLOW FÜR DEINE FEATURE-BRANCHES

Wenn du die Contracts aktualisierst:

```bash
# 1. Neue Branch erstellen
git checkout -b feature/rolle1/contracts-v0.3

# 2. Änderungen machen (z.B. docs/contracts.md)
# ... bearbeite Dateien ...

# 3. Committen mit richtiger Nachricht
git add .
git commit -m "docs(contracts): v0.3 Schnittstellen definieren

- TinyDB Repository erweitern
- Bewegungs-API definieren
- Report-Schnittstelle clarify"

# 4. Pushen & Pull Request erstellen
git push origin feature/rolle1/contracts-v0.3

# 5. Pull Request auf GitHub erstellen
#    -> base: develop
#    -> compare: feature/rolle1/contracts-v0.3
```

Dann: **Wartet auf approval von anderen Rollen** ✅

---

## 📊 GIT STRUKTUR NACH v0.3

```
main (v0.2.0 stable)
  ↓
develop (v0.3 integration)
  ├─ feature/rolle1/contracts-v0.3 ← MERGED
  ├─ feature/rolle2/... ← MERGED
  ├─ feature/rolle3/... ← MERGED
  └─ feature/rolle4/... ← MERGED
  ↓ (nach Release)
main (v0.3.0 stable) ← Tag erstellen
```

---

## ⚠️ WICHTIG: WORAUF DU ACHTEN MUSST

1. **Andere Rollen nicht blockieren** – Schnittstellen early & clear definieren
2. **Täglich auf Konflikte checken** – Merge oft um Probleme früh zu finden
3. **Dokumentation = Source of Truth** – contracts.md ist verbindlich!
4. **Alle Reviews vor Merge** – Keine Überraschungen

---

## 📞 COMMUNICATION CHECKLIST

- [ ] Team informiert über v0.3-Plan
- [ ] Contracts Review durchgeführt
- [ ] Feature-Dependencies geklärt
- [ ] Daily Standup etabliert (wo sind wir?)
- [ ] Merge-Strategie abgesprochen

---

**Status:** 🟡 BEREIT FÜR START  
**Nächster Schritt:** Feature-Branch `feature/rolle1/contracts-v0.3` erstellen und los geht's! 🚀
