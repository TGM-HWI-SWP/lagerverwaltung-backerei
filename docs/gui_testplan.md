# GUI Testplan - Manuelle Testcheckliste

**Verantwortlich:** Rolle 4 (GUI & Interaktion)
**Version:** v0.3.0
**Datum:** 2026-03-03

Ergänzung zu den 39 automatisierten Tests in `tests/unit/test_gui.py`.

---

## 1. Anwendungsstart

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 1.1 | App starten mit `python -c "from src.ui import main; main()"` | Fenster öffnet sich, Titel enthält Versionsnummer | |
| 1.2 | Fenstergröße prüfen | Mindestens 800x500, Standard 1100x700 | |
| 1.3 | Fenster verkleinern | Minimum wird eingehalten, kein UI-Bruch | |
| 1.4 | 3 Tabs sichtbar | "Produkte", "Lagerbewegungen", "Berichte" | |
| 1.5 | Statusleiste sichtbar | Zeigt "Produkte: 0" und "Gesamtwert: 0.00 €" | |
| 1.6 | Bäckerei-Theme geladen | Warme Farben, braune Buttons, gestylte Tabs | |

---

## 2. Produktverwaltung

### 2.1 Produkt hinzufügen

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 2.1.1 | Button "Produkt hinzufügen" klicken | Dialog öffnet sich mit Titel "Produkt hinzufügen" | |
| 2.1.2 | Alle Felder ausfüllen und OK klicken | Erfolgs-Meldung, Produkt in Tabelle sichtbar | |
| 2.1.3 | Leere ID eingeben | Fehlermeldung | |
| 2.1.4 | Negativen Preis eingeben | Nicht möglich (SpinBox verhindert es) | |
| 2.1.5 | Abbrechen klicken | Dialog schließt, kein Produkt hinzugefügt | |
| 2.1.6 | Statusleiste nach Hinzufügen | Produktanzahl und Gesamtwert aktualisiert | |

### 2.2 Produkt bearbeiten

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 2.2.1 | Produkt auswählen, "Bearbeiten" klicken | Dialog mit vorausgefüllten Daten | |
| 2.2.2 | ID-Feld im Edit-Modus | Schreibgeschützt (grau hinterlegt) | |
| 2.2.3 | Menge-Feld im Edit-Modus | Schreibgeschützt (Änderung nur über Ein-/Auslagern) | |
| 2.2.4 | Name ändern und speichern | Name in Tabelle aktualisiert | |
| 2.2.5 | Kein Produkt ausgewählt, "Bearbeiten" klicken | Warnmeldung "Bitte wähle zuerst ein Produkt" | |

### 2.3 Produkt löschen

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 2.3.1 | Produkt auswählen, "Löschen" klicken | Bestätigungsdialog mit Produktname | |
| 2.3.2 | Bestätigung mit "Ja" | Produkt aus Tabelle entfernt, Erfolgs-Meldung | |
| 2.3.3 | Bestätigung mit "Nein" | Nichts passiert | |
| 2.3.4 | Kein Produkt ausgewählt | Warnmeldung | |

---

## 3. Bestandsverwaltung

### 3.1 Einlagern

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 3.1.1 | Produkt auswählen, "Einlagern" klicken | Dialog mit Produktname, Titel "Einlagern" | |
| 3.1.2 | Menge 10, Grund "Lieferung", Benutzer "Max" eingeben | Bestand erhöht, Bewegung geloggt | |
| 3.1.3 | Bewegungen-Tab prüfen | Neue IN-Bewegung sichtbar (grüner Text) | |
| 3.1.4 | Bestandsfarbe prüfen | Farbe ändert sich entsprechend neuem Wert | |

### 3.2 Auslagern

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 3.2.1 | Produkt auswählen, "Auslagern" klicken | Dialog mit Produktname, Titel "Auslagern" | |
| 3.2.2 | Gültige Menge auslagern | Bestand verringert, Bewegung geloggt | |
| 3.2.3 | Mehr als verfügbar auslagern | Fehlermeldung "Unzureichender Bestand" | |
| 3.2.4 | Bewegungen-Tab prüfen | Neue OUT-Bewegung sichtbar (roter Text) | |

---

## 4. Suchfunktion

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 4.1 | "Brot" in Suchfeld eingeben | Nur Brot-Produkte sichtbar | |
| 4.2 | Nach Kategorie suchen | Nur passende Kategorie sichtbar | |
| 4.3 | Nach Produkt-ID suchen | Nur passendes Produkt sichtbar | |
| 4.4 | Suchfeld leeren | Alle Produkte wieder sichtbar | |
| 4.5 | Groß-/Kleinschreibung testen | Suche ist case-insensitive | |

---

## 5. Berichte

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 5.1 | "Lagerbestandsbericht" klicken (leer) | Text "Lager ist leer" im Textfeld | |
| 5.2 | "Lagerbestandsbericht" klicken (mit Daten) | Formatierter Bericht mit Produktdetails | |
| 5.3 | "Bewegungsprotokoll" klicken (leer) | Text "Keine Lagerbewegungen vorhanden" | |
| 5.4 | "Bewegungsprotokoll" klicken (mit Daten) | Formatierter Bericht mit Bewegungsdetails | |
| 5.5 | Export-Button initial | Deaktiviert (grau) | |
| 5.6 | Export-Button nach Bericht | Aktiviert | |
| 5.7 | Bericht exportieren | Datei-Dialog öffnet, .txt wird gespeichert | |
| 5.8 | Exportierte Datei öffnen | Inhalt identisch mit Textfeld | |

---

## 6. Bestandsfarben (Produkte-Tab)

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 6.1 | Produkt mit Bestand 0-5 | Rote Bestandszelle (#e74c3c) | |
| 6.2 | Produkt mit Bestand 6-15 | Orange Bestandszelle (#f39c12) | |
| 6.3 | Produkt mit Bestand > 15 | Grüne Bestandszelle (#27ae60) | |
| 6.4 | Bestand durch Auslagern unter 5 senken | Farbe wechselt zu Rot | |

---

## 7. Styling & Responsive Design

| # | Testfall | Erwartetes Ergebnis | OK? |
|---|---------|---------------------|-----|
| 7.1 | Bäckerei-Theme sichtbar | Warme Brauntöne, gestylte Buttons | |
| 7.2 | Löschen-Button | Rot gefärbt | |
| 7.3 | Einlagern-Button | Grün gefärbt | |
| 7.4 | Auslagern-Button | Orange gefärbt | |
| 7.5 | Tabelle: Zeilen abwechselnd | Alternating Row Colors aktiv | |
| 7.6 | Tabelle: Spalten verschiebbar | Spaltenbreite per Drag änderbar | |
| 7.7 | Reports-Textfeld | Dunkler Hintergrund, Monospace-Schrift | |
| 7.8 | Fenster maximieren | Layout passt sich an | |

---

## Automatisierte Tests (39 Tests)

Alle automatisierten Tests mit `python -m pytest tests/unit/test_gui.py -v` ausführen.

| Testklasse | Anzahl | Beschreibung |
|-----------|--------|-------------|
| TestMainWindow | 7 | Fensterstruktur, Tabs, Tabellen |
| TestProductManagement | 4 | CRUD-Operationen |
| TestSearchFilter | 5 | Filterfunktionalität |
| TestMovements | 3 | Bewegungsanzeige & Sortierung |
| TestReports | 4 | Berichterstellung |
| TestDialogs | 7 | Dialog-Modi & Daten |
| TestStatusBar | 4 | Statusleiste |
| TestStockColorCoding | 3 | Bestandsfarben |
| TestExport | 2 | Export-Button |
| **Gesamt** | **39** | |

---

**Testplan erstellt von:** Noah Bodner (Rolle 4)
**Letzte Aktualisierung:** 2026-03-03
