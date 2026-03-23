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

## [v0.4] - 24.02.2026

### Implementiert
- **Inventur-Logik:** `adjust_stock_inventory` erstellt, um Bestandsdifferenzen automatisch zu berechnen und als ADJUST-Bewegung zu loggen.
- **Preisanpassungs-Feature:** `update_category_prices` implementiert für prozentuale Massen-Updates von Produktpreisen innerhalb einer Kategorie.
- **Reporting (Report A):** `ConsoleReportAdapter` grundlegend überarbeitet: Tabellarische Darstellung, Status-Indikatoren (OK/KNAPP/LEER) und Zusammenfassung kritischer Bestände.
- **Validierung:** Sicherheits-Checks in `create_product` für Preise (nicht negativ), Namen (Mindestlänge) und Bestände hinzugefügt.

### Tests geschrieben
- `tests/unit/test_warehouse_service.py`: Unit-Tests für Inventur-Abgleich, Mindestbestand-Erkennung und Produktlöschung.
- `test_report_warning_indicator`: Integrationstest für die korrekte Anzeige von Warnungen im Report A.

### Mergekonflikt(e)
- Keine

### Commits
feat(service/repo): implement business logic sprint 1 (week 4)

test(unit): add comprehensive unit tests for WarehouseService



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
