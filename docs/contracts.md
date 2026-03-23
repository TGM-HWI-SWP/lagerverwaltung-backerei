# Schnittstellen-Dokumentation (Contracts)

## Übersicht

Diese Datei dokumentiert alle externen Schnittstellen des Projekts. Sie wird von Rolle 1 (Contract Owner) gepflegt und aktualisiert bei jeder Änderung.

---

## 1. RepositoryPort

**Verantwortlich:** Rolle 2 (Businesslogik)

### Beschreibung
Abstrakte Schnittstelle für Datenpersistenz. Ermöglicht den Austausch zwischen verschiedenen Speicheradaptern (In-Memory, SQLite, JSON, etc.)

### Methoden

#### `save_product(product: Product) -> None`
Speichert ein Produkt.

**Parameter:**
- `product`: Product-Instanz

**Exceptions:**
- Keine

**Implementierungen:**
- `InMemoryRepository` (v0.1)

#### `load_product(product_id: str) -> Optional[Product]`
Lädt ein einzelnes Produkt.

**Parameter:**
- `product_id`: Eindeutige Produkt-ID

**Return:**
- `Product` oder `None` falls nicht gefunden

**Implementierungen:**
- `InMemoryRepository` (v0.1)

#### `load_all_products() -> Dict[str, Product]`
Lädt alle Produkte.

**Return:**
- Dictionary mit Product-IDs als Keys

**Implementierungen:**
- `InMemoryRepository` (v0.1)

#### `delete_product(product_id: str) -> None`
Löscht ein Produkt.

**Parameter:**
- `product_id`: Eindeutige Produkt-ID

**Exceptions:**
- Keine (ignoriert unbekannte IDs)

**Implementierungen:**
- `InMemoryRepository` (v0.1)

#### `save_movement(movement: Movement) -> None`
Speichert eine Lagerbewegung.

**Parameter:**
- `movement`: Movement-Instanz

**Implementierungen:**
- `InMemoryRepository` (v0.1)

#### `load_movements() -> List[Movement]`
Lädt alle Lagerbewegungen.

**Return:**
- Liste von Movement-Objekten

**Implementierungen:**
- `InMemoryRepository` (v0.1)

---

## 2. ReportPort

**Verantwortlich:** Rolle 3 (Reports & Qualität)

### Beschreibung
Abstrakte Schnittstelle für Report-Generierung.

### Methoden

#### `generate_inventory_report() -> str`
Generiert einen Lagerbestandsbericht.

**Return:**
- Formatierter String-Bericht

**Implementierungen:**
- `ConsoleReportAdapter` (v0.1)

#### `generate_movement_report() -> str`
Generiert ein Bewegungsprotokoll.

**Return:**
- Formatierter String-Bericht

**Implementierungen:**
- `ConsoleReportAdapter` (v0.1)

---

## 3. GUIPort

**Verantwortlich:** Rolle 4 (GUI)

### Beschreibung
Abstrakte Schnittstelle für die Benutzeroberfläche. Definiert Callbacks und Events, die von WarehouseService ausgelöst werden.

### Methoden

#### `on_product_created(product: Product) -> None`
Callback wenn Produkt erstellt wurde.

**Parameter:**
- `product`: Neue Product-Instanz

#### `on_product_deleted(product_id: str) -> None`
Callback wenn Produkt gelöscht wurde.

**Parameter:**
- `product_id`: Gelöschte Produkt-ID

#### `on_product_updated(product: Product) -> None`
Callback wenn Produkt aktualisiert wurde.

**Parameter:**
- `product`: Aktualisierte Product-Instanz

#### `on_movement_recorded(movement: Movement) -> None`
Callback wenn Lagerbewegung aufgezeichnet wurde.

**Parameter:**
- `movement`: Neue Movement-Instanz

#### `show_error(message: str, error_type: str) -> None`
Zeigt Fehlermeldung in GUI an.

**Parameter:**
- `message: str` - Fehlermeldung
- `error_type: str` - Fehlertyp ("ERROR", "WARNING", "INFO")

#### `refresh_display() -> None`
Aktualisiert die GUI-Ansicht.

---

## 4. WarehouseService

**Verantwortlich:** Rolle 2 (Businesslogik)

### Beschreibung
Service-Klasse für zentrale Lagerverwaltungslogik.

### Methoden

#### `create_product(...) -> Product`
Erstellt ein neues Produkt.

**Parameter:**
- `product_id: str` - Eindeutige ID
- `name: str` - Produktname
- `description: str` - Beschreibung
- `price: float` - Preis
- `category: str` - Kategorie (optional)
- `initial_quantity: int` - Anfangsbestand

**Return:**
- Neue Product-Instanz

**Exceptions:**
- `ValueError`: Bei ungültigen Eingaben

#### `add_to_stock(product_id: str, quantity: int, reason: str, user: str) -> None`
Erhöht den Bestand.

**Parameter:**
- `product_id: str`
- `quantity: int` - Menge
- `reason: str` - Grund (optional)
- `user: str` - Benutzer (default: "system")

**Exceptions:**
- `ValueError`: Wenn Produkt nicht existiert

#### `remove_from_stock(product_id: str, quantity: int, reason: str, user: str) -> None`
Verringert den Bestand.

**Parameter:**
- `product_id: str`
- `quantity: int` - Menge
- `reason: str` - Grund (optional)
- `user: str` - Benutzer (default: "system")

**Exceptions:**
- `ValueError`: Wenn Bestand unzureichend oder Produkt nicht existiert

#### `get_product(product_id: str) -> Optional[Product]`
Ruft ein einzelnes Produkt ab.

**Return:**
- Product oder None

#### `get_all_products() -> Dict[str, Product]`
Ruft alle Produkte ab.

**Return:**
- Dictionary mit allen Produkten

#### `get_movements() -> List[Movement]`
Ruft alle Lagerbewegungen ab.

**Return:**
- Liste aller Movements

#### `get_total_inventory_value() -> float`
Berechnet den Gesamtwert des Lagers.

**Return:**
- Wert in Euro

---

## 5. Exception Handling

### Custom Exceptions

#### `ProductNotFoundError`
Wird geworfen wenn ein Produkt nicht existiert.

**Trigger:**
- `get_product(product_id)` mit ungültiger ID
- `add_to_stock()` mit ungültiger Produkt-ID
- `remove_from_stock()` mit ungültiger Produkt-ID
- `delete_product()` mit ungültiger Produkt-ID

#### `InsufficientStockError`
Wird geworfen wenn Bestand zu gering ist.

**Trigger:**
- `remove_from_stock()` mit Menge > Bestand

**Attribute:**
- `product_id: str`
- `requested: int`
- `available: int`

#### `InvalidProductDataError`
Wird geworfen bei ungültigen Eingaben.

**Trigger:**
- `create_product()` mit leerem Namen
- Negative Preise oder Mengen
- Ungültiges SKU-Format

**Attribute:**
- `field: str` - Name des ungültigen Feldes
- `value: str` - Ungültiger Wert

#### `RepositoryError`
Wird geworfen bei Persistierungs-Problemen.

**Trigger:**
- SQLite Datenbankfehler
- JSON Datei nicht lesbar/schreibbar
- Disk-Speicher voll

---

## 6. Adapter Implementierungen

### InMemoryRepository (v0.1)
- Speichert Produkte & Movements in RAM
- Daten gehen bei Neustart verloren
- Für Tests & Prototyping

### SQLiteRepository (v0.3 geplant)
- Persistente Speicherung in SQLite
- ACID-Garantien
- Schnittstelle: Identisch zu RepositoryPort

### JSONRepository (v0.3 geplant)
- Speichert in JSON-Dateien
- Human-readable Daten
- Für einfache Setups ohne DB

### ConsoleReportAdapter (v0.1)
- Text-basierte Reports
- Ausgabe auf Console/Terminal

### FileReportAdapter (v0.3 geplant)
- Speichert Reports als Dateien (CSV, PDF)
- Exportfunktion für Geschäftseigentümer

---

## 7. Report-Formate

### Inventory Report Format
```
Lagerbestandsbericht vom: 2025-02-10 14:30:00
==================================================
Produkt-ID | Name              | Bestand | Wert
-----------+-------------------+---------+--------
PRD-001    | Brot Vollkorn     | 45      | 225,00€
PRD-002    | Croissant         | 120     | 480,00€
PRD-003    | Kuchen Schoko     | 12      | 144,00€
-----------+-------------------+---------+--------
GESAMT     |                   | 177     | 849,00€
```

**JSON-Alternative (für APIs):**
```json
{
  "report_date": "2025-02-10T14:30:00",
  "products": [
    {"id": "PRD-001", "name": "Brot Vollkorn", "quantity": 45, "value": 225.00},
    {"id": "PRD-002", "name": "Croissant", "quantity": 120, "value": 480.00}
  ],
  "total_quantity": 177,
  "total_value": 849.00
}
```

### Movement Report Format
```
Bewegungsprotokoll vom: 2025-02-01 bis 2025-02-10
==================================================
Zeit              | Produkt      | Typ    | Menge | Grund         | Nutzer
------------------+--------------+--------+-------+---------------+---------
2025-02-10 14:30 | Brot Vollk.  | IN     | +20   | Lieferung     | maria
2025-02-10 13:15 | Croissant    | OUT    | -5    | Verkauf       | system
2025-02-10 12:00 | Kuchen Scho. | CORR   | +2    | Bestandsprüf. | peter
```

**JSON-Alternative:**
```json
{
  "report_period": {"start": "2025-02-01T00:00:00", "end": "2025-02-10T23:59:59"},
  "movements": [
    {"timestamp": "2025-02-10T14:30:00", "product_id": "PRD-001", "quantity_change": 20, "type": "IN", "reason": "Lieferung", "user": "maria"}
  ]
}
```

---

## 8. Validierungsregeln

### Product
| Feld | Typ | Required | Validierung | Beispiel |
|------|-----|----------|-------------|----------|
| `id` | str | Ja | 3-20 Zeichen, nur alphanumerisch + `-` | "PRD-001" |
| `name` | str | Ja | Min 3, Max 100 Zeichen | "Brot Vollkorn" |
| `description` | str | Nein | Max 500 Zeichen | "Vollkornbrot mit Saaten" |
| `price` | float | Ja | ≥ 0.01, Max 2 Dezimale | 3.50 |
| `quantity` | int | Ja | ≥ 0 | 45 |
| `sku` | str | Ja | 3-20 Zeichen, Format: `CATEGORY-NUMBER` | "BREAD-001" |
| `category` | str | Ja | Aus vordefinierter Liste | "Brot", "Backware", "Kuchen" |
| `notes` | str | Nein | Max 200 Zeichen | "Kühl lagern" |

### Movement
| Feld | Typ | Required | Validierung | Beispiel |
|------|-----|----------|-------------|----------|
| `id` | str | Ja (Auto) | UUID oder Sequence | "MOV-20250210-001" |
| `product_id` | str | Ja | Muss existierendes Produkt sein | "PRD-001" |
| `quantity_change` | int | Ja | ≠ 0, Min -1000, Max +1000 | 20 oder -5 |
| `movement_type` | str | Ja | Enum: "IN", "OUT", "CORRECTION" | "IN" |
| `reason` | str | Nein | Max 200 Zeichen | "Lieferung", "Verkauf" |
| `performed_by` | str | Ja | Min 3, Max 50 Zeichen | "maria" |

### Kategorien (vordefiniert)
- Brot
- Backware
- Kuchen
- Süßes
- Sonstiges

---

## 9. Domain Models

### Product

**Attribute:**
- `id: str` - Eindeutige ID
- `name: str` - Produktname
- `description: str` - Beschreibung
- `price: float` - Preis pro Einheit
- `quantity: int` - Bestand
- `sku: str` - Stock Keeping Unit
- `category: str` - Kategorie
- `created_at: datetime` - Erstellungsdatum
- `updated_at: datetime` - Änderungsdatum
- `notes: str` - Anmerkungen

**Methoden:**
- `update_quantity(amount: int) -> None` - Bestand ändern
- `get_total_value() -> float` - Gesamtwert berechnen

### Movement

**Attribute:**
- `id: str` - Eindeutige Bewegungs-ID
- `product_id: str` - Verweis auf Produkt
- `product_name: str` - Name des Produkts
- `quantity_change: int` - Mengenänderung (+/-)
- `movement_type: str` - "IN", "OUT", "CORRECTION"
- `reason: str` - Grund (optional)
- `timestamp: datetime` - Zeitstempel
- `performed_by: str` - Benutzer

---

## Versionshistorie der Contracts

### v0.1 (2025-01-20)
- RepositoryPort: Grundlegende CRUD-Operationen
- ReportPort: Basis-Report-Generierung
- WarehouseService: Kern-Use-Cases
- Product: Basis-Domain-Model
- Movement: Lagerbewegungen-Protokoll

---

## Zukünftige Änderungen

- [ ] SQLite-Adapter implementieren
- [ ] GraphML-Report-Generierung
- [ ] Benutzer-Management erweitern
- [ ] Batch-Operationen unterstützen
