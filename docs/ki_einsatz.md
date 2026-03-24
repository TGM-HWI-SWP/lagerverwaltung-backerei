# KI-Einsatz-Dokumentation

## Ziel
Diese Datei dokumentiert transparent, wie KI im Projekt eingesetzt wurde.

## Grundsatz
KI wurde als Assistenz genutzt. Architektur-, Schnittstellen- und Integrationsentscheidungen wurden durch das Team getroffen und manuell geprüft.

## Einsatzbereiche

### 1. Code-Unterstützung
- Vorschläge für Testfälle und Refactorings
- Hilfe bei Fehlersuche (z. B. Assertion-/Report-Differenzen)
- Unterstützung bei Start-/Setup-Themen (`pyproject.toml`, Entry-Points)

### 2. Dokumentation
- Strukturhilfe für Mergekonflikt-Dokumentation
- Formulierungshilfe für Changelog-/Retro-Texte

### 3. Qualitätssicherung
- Gegenprüfung von erwarteten und tatsächlichen Testergebnissen
- Hinweise zu Inkonsistenzen zwischen Code und Doku

## Manuelle Prüfungen durch das Team
- Alle übernommenen Änderungen wurden inhaltlich gegengeprüft
- Kritische Änderungen wurden über Tests validiert (`pytest`)
- Mergekonflikte wurden nicht automatisch, sondern manuell aufgelöst und dokumentiert

## Nicht an KI delegiert
- Finale Architekturentscheidungen
- Festlegung von Contracts
- Abgabeentscheidung und Priorisierung im Projektmanagement

## Nachweiszeitraum
- v0.4 bis v0.5 (Stabilisierung, Tests, Doku)

## Stand
- Letzte Aktualisierung: 2026-03-24
- Verantwortlich: Rolle 1 (Koordination), Teamreview durch alle Rollen
