# Retrospektive

## Projektübersicht

**Projekttitel:** Lagerverwaltungssystem  
**Projektdauer:** 8 Wochen  
**Gruppengröße:** 4 Personen  
**Projektverantwortung:** Pia Endlich (Rolle 1)

---

## Versionsmilestones

### v0.1 - Projektstart & Grundarchitektur
**Abschluss:** 2026-02-03

#### Was lief gut?
- Klare Rollenverteilung und Verantwortlichkeiten
- Erste Port-/Adapter-Struktur stand früh
- Teamkommunikation über Branches und kurze Abstimmungen
- Früher Start mit Repository-Konventionen

#### Was konnte verbessert werden?
- Frühere Abstimmung über Dateibereiche, um Konflikte zu reduzieren
- Genauere Definition der Persistenzstrategie von Anfang an
- Früheres Einführen fixer Review-Routinen

#### Learnings
- Ein sauberer Projektstart reduziert spätere Integrationskosten deutlich.

---

### v0.2 - Walking Skeleton
**Abschluss:** 2026-02-24

#### Was lief gut?
- Schnittstellen zentral in `contracts.md` dokumentiert
- Walking Skeleton über alle Schichten funktionsfähig
- Grundlegender Git-Workflow im Team etabliert
- Struktur-Refactoring (`__init__` bereinigt, Module getrennt)

#### Was konnte verbessert werden?
- Dokumente konsequenter synchron zu Code-Änderungen halten
- Merge-Strategie früher üben statt erst bei Konfliktfällen

#### Learnings
- Eine dokumentierte Schnittstelle ist die zentrale Integrationsgrundlage.

---

### v0.3 - Kernlogik & GUI
**Abschluss:** 2026-03-03

#### Was lief gut?
- Kernlogik für Produktverwaltung und Lagerbewegungen stabilisiert
- GUI-Skeleton inkl. Produktverwaltung funktional
- Service-Layer klar strukturiert
- Erste End-to-End-Workflows über UI möglich

#### Was konnte verbessert werden?
- Paralleländerungen an zentralen Dateien besser koordinieren
- Mehr Integrationsprüfungen während der Woche

#### Learnings
- Kleine, häufige Integrationen sind wichtiger als große Sammelmerges.

---

### v0.4 - Reports
**Abschluss:** 2026-03-17

#### Was lief gut?
- Report A und Report B als eigene Komponenten umgesetzt
- Reports testbar und deterministisch ausgeführt
- Testumfang deutlich erhöht (inkl. GUI- und Report-Tests)
- Struktur für Export/Anzeige in UI verbessert

#### Was konnte verbessert werden?
- Metriken in Tests und Doku (Coverage/Performance) einheitlicher führen
- Changelogs früher laufend pflegen statt gesammelt nachzutragen

#### Learnings
- Reporting funktioniert am besten als entkoppelte, reine Logikkomponente.

---

### v0.5 - Tests & Stabilisierung
**Abschluss:** 2026-03-24

#### Was lief gut?
- Testsuite stabilisiert, alle Tests grün
- Mehrere Inkonsistenzen zwischen Tests und Implementierung behoben
- Build-/Start-Komfort über `pyproject.toml` verbessert
- Mergekonflikte nachvollziehbar dokumentiert

#### Was konnte verbessert werden?
- Versions- und Tag-Strategie früher konsequent umsetzen
- Verbleibende Dokument-Templates früher schließen

#### Learnings
- Stabilisierung ist ein eigener Arbeitsschritt und braucht feste Zeit im Plan.

---

### v1.0 - Finale & Präsentation
**Abschluss:** Offen (in Arbeit)

#### Was lief gut?
- Finalisierungsplan ist klar definiert
- Offene Punkte sind identifiziert und priorisiert

#### Was konnte verbessert werden?
- Frühere Vorbereitung der finalen Abgabedokumente (PDFs)
- Endabnahme-Checkliste schon zu Beginn der letzten Iteration verwenden

#### Learnings
- Eine klare Done-Definition pro Artefakt verhindert Last-Minute-Fehler.

---

## Überblick: Stärken & Schwächen

### Team-Stärken
- Kommunikation
- Code-Qualität
- Zusammenarbeit
- Problem-Solving
- Dokumentation

### Verbesserungspotenzial
- Dokumentation durchgehend aktuell halten
- Branch-/Merge-Disziplin bei parallel bearbeiteten Dateien
- Einheitliche Versionierungsroutine über alle Milestones

### Einzelne Learnings pro Rolle

#### Rolle 1 (Contract Owner)
- Gelernt: Schnittstellen zentral zu führen, Konflikte strukturiert aufzulösen
- Verbessern: Noch frühere Eskalation bei parallelen Dateikonflikten

#### Rolle 2 (Businesslogik & Report A)
- Gelernt: Deterministische Businesslogik vereinfacht Testing und UI-Integration
- Verbessern: Contracts bei Methodenerweiterungen sofort mitziehen

#### Rolle 3 (Report B & Tests)
- Gelernt: Randfalltests decken Integrationsprobleme früh auf
- Verbessern: Testmetriken und Doku enger synchronisieren

#### Rolle 4 (GUI & Interaktion)
- Gelernt: UI-Entwicklung profitiert stark von klaren Service-Contracts
- Verbessern: Frühere Abstimmung bei Änderungen in zentralen UI-Dateien

---

## Technische Erkenntnisse

### Was funktioniert gut?
- Port-Adapter-Architektur: gut testbar, Adapter austauschbar
- Testing-Ansatz: breite Abdeckung von Domain, Service, Reports, GUI
- Git-Workflow: grundsätzlich etabliert und nachvollziehbar
- Modulstruktur: gute Trennung von UI, Services, Domain und Adapters

### Technische Schulden
- Dokumente mit Template-Resten vollständig schließen
- Contracts fortlaufend an neue Service-Methoden anpassen
- Persistenz-Default und UI-Startverhalten klar dokumentieren

### Empfehlungen für Folge-Projekte
1. Pro Woche fixer Integrationsslot mit gemeinsamem Merge & Testlauf
2. Definition of Done inkl. Doku-/Tag-/Konfliktnachweis pro Milestone
3. Einheitliche Commit-Konvention und Review-Checkliste verbindlich nutzen

---

## Mergekonflikte & Lösungen

| Datei | Konflikt-Typ | Lösung | Gelerntes |
|-------|-------------|--------|----------|
| `docs/contracts.md` | Content-Konflikt | Beide Änderungen manuell integriert, Marker entfernt, erneut getestet | Konflikte nicht mit `--ours/--theirs` blind lösen |
| `src/ui/__init__.py` | Content-Konflikt | Alte/duplizierte Logik verworfen, modulare Re-Export-Struktur beibehalten | Verantwortlichkeiten pro Modul strikt trennen |

---

## Abschließende Bewertung

### Projektqualität (1-10)
- Code-Qualität: 8
- Dokumentation: 7
- Tests: 9
- Zusammenarbeit: 8
- **Durchschnitt:** 8.0

### Was würde ich anders machen?
1. Bereits ab v0.2 verbindliche Merge- und Doku-Checkliste nutzen
2. Changelogs wöchentlich abschließen statt blockweise
3. Contracts als Pflicht-Reviewpunkt vor jedem Merge behandeln

### Feedback an die Lehrperson
- Die Rollenstruktur war praxisnah und hilfreich für Teamverantwortung.
- Mergekonflikte als Lernziel waren sinnvoll und realitätsnah.

---

**Retrospektive erstellt:** 2026-03-24  
**Geschrieben von:** Projektteam (koordiniert durch Rolle 1)
