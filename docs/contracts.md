# Schnittstellen-Dokumentation (Contracts)

**Version:** 0.2.0  
**Verantwortlich:** Rolle 1 (Contract Owner)  
**Letzte Aktualisierung:** 24. Februar 2026

Diese Datei ist die **zentrale Spezifikation** aller Schnittstellen (Ports) im Projekt. Alle neuen Features müssen hier dokumentiert werden BEVOR sie implementiert werden!

---

## 1. RepositoryPort

**Verantwortlich:** Rolle 2  
**Datei:** `src/ports/__init__.py`  
**Implementierung:** `src/adapters/repository.py`

### Zweck
Abstrakte Schnittstelle für Datenpersistierung. Ermöglicht Austausch zwischen In-Memory, SQLite, JSON usw. ohne Service-Code zu ändern.

### Methoden

| Methode | Input | Output | Exceptions | v0.1 | v0.2 |
|---------|-------|--------|------------|------|------|
| `save_product(product)` | Product | None | ValueError | ✅ | ✅ |
| `load_product(id)` | str | Product\|None | - | ✅ | ✅ |
| `load_all_products()` | - | Dict[str,Product] | - | ✅ | ✅ |
| `delete_product(id)` | str | None | - | ✅ | ✅ |
| `save_movement(movement)` | Movement | None | ValueError | ✅ | ✅ |
| `load_movements()` | - | List[Movement] | - | ✅ | ✅ |

**Beispiele:**
```python
# Produkt speichern
product = Product(id="P001", name="Brot", price=2.99, ...)
repository.save_product(product)

# Produkt laden
product = repository.load_product("P001")
if product is None:
    print("Nicht gefunden")

# Alle Produkte
all_products = repository.load_all_products()  # Dict[str, Product]
```

---

## 2. ReportPort

**Verantwortlich:** Rolle 3  
**Datei:** `src/ports/__init__.py`  
**Implementierung:** `src/adapters/report.py`

### Zweck
Abstrakte Schnittstelle für Report-Generierung.

### Methoden

| Methode | Input | Output | v0.1 | v0.2 |
|---------|-------|--------|------|------|
| `generate_inventory_report()` | - | str | ✅ | ✅ |
| `generate_movement_report()` | - | str | ✅ | ✅ |

**Beispiele:**
```python
# Lagerbestandsbericht
report = report_adapter.generate_inventory_report()
# Rückgabe: "Lagerbestandsbericht vom 24.02.2026..."

# Bewegungsprotokoll
report = report_adapter.generate_movement_report()
# Rückgabe: "Bewegungsprotokoll vom 24.02.2026..."
```

---

## 3. WarehouseService API

**Verantwortlich:** Rolle 2  
**Datei:** `src/services/warehouse_service.py`

### Zentrale Geschäftslogik für Lagerverwaltung

### Konstruktor

```python
def __init__(self, repository: RepositoryPort) -> None
```

**Beispiel:**
```python
repo = InMemoryRepository()
service = WarehouseService(repo)
```

### Produkt-Verwaltung

#### `create_product(...)` → Product
Erstellt und speichert ein neues Produkt.

```python
def create_product(
    self,
    product_id: str,        # z.B. "PRD-001"
    name: str,              # z.B. "Vollkornbrot"
    description: str,       # z.B. "mit Saaten"
    price: float,           # z.B. 2.99
    category: str = "",     # z.B. "Brot"
    initial_quantity: int = 0
) -> Product
```

**Beispiel:**
```python
product = service.create_product(
    product_id="PRD-001",
    name="Vollkornbrot",
    description="Frisches Vollkornbrot",
    price=2.99,
    category="Brot",
    initial_quantity=50
)
# Rückgabe: Product(id="PRD-001", name="Vollkornbrot", ...)
```

**Exceptions:**
- `ValueError`: Wenn product_id leer oder price < 0

#### `get_product(product_id)` → Product|None
Ruft ein einzelnes Produkt ab.

```python
product = service.get_product("PRD-001")
if product:
    print(f"Bestand: {product.quantity}")
```

#### `get_all_products()` → Dict[str, Product]
Ruft alle Produkte ab.

```python
all = service.get_all_products()
for product_id, product in all.items():
    print(f"{product_id}: {product.name} ({product.quantity} Stück)")
```

#### `delete_product(product_id)` → None
Löscht ein Produkt. Ignoriert unbekannte IDs.

```python
service.delete_product("PRD-001")
```

### Bestandsverwaltung

#### `add_to_stock(product_id, quantity, reason, user)` → None
Erhöht den Bestand (Wareneingang).

```python
def add_to_stock(
    self,
    product_id: str,
    quantity: int,          # positive Zahl
    reason: str = "",       # z.B. "Lieferung"
    user: str = "system"    # z.B. "maria"
) -> None
```

**Beispiel:**
```python
service.add_to_stock(
    product_id="PRD-001",
    quantity=30,
    reason="Lieferung",
    user="maria"
)
# Speichert Movement(product_id="PRD-001", quantity_change=+30, type="IN", ...)
```

**Exceptions:**
- `ValueError`: Wenn Produkt nicht existiert

#### `remove_from_stock(product_id, quantity, reason, user)` → None
Verringert den Bestand (Warenausgang).

```python
def remove_from_stock(
    self,
    product_id: str,
    quantity: int,          # positive Zahl
    reason: str = "",       # z.B. "Verkauf"
    user: str = "system"
) -> None
```

**Beispiel:**
```python
service.remove_from_stock(
    product_id="PRD-001",
    quantity=5,
    reason="Verkauf",
    user="kassensystem"
)
```

**Exceptions:**
- `ValueError`: Wenn Bestand unzureichend oder Produkt nicht existiert

### Reporting

#### `get_movements()` → List[Movement]
Ruft alle Lagerbewegungen ab.

```python
movements = service.get_movements()
for mov in movements:
    print(f"{mov.timestamp}: {mov.product_name} {mov.quantity_change}")
```

#### `get_total_inventory_value()` → float
Berechnet den Gesamtwert des Lagers.

```python
total_value = service.get_total_inventory_value()
print(f"Gesamtwert: {total_value:.2f}€")
```

---

## 4. Domain Models

### Product (Dataclass)

**Datei:** `src/domain/product.py`

```python
@dataclass
class Product:
    id: str                                    # Eindeutige ID
    name: str                                  # Produktname
    description: str                           # Beschreibung
    price: float                               # Preis pro Einheit
    quantity: int = 0                          # Aktueller Bestand
    sku: str = ""                              # Lagerhaltungscode
    category: str = ""                         # Kategorie
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None               # Notizen
```

**Wichtige Methoden:**

```python
def update_quantity(self, amount: int) -> None:
    """Bestand ändern (positiv = hinzufügen, negativ = entfernen)"""
    new_quantity = self.quantity + amount
    if new_quantity < 0:
        raise ValueError(f"Ungültige Menge: {new_quantity}")
    self.quantity = new_quantity
    self.updated_at = datetime.now()

def get_total_value(self) -> float:
    """Lagerwert berechnen: Preis × Bestand"""
    return self.price * self.quantity
```

**Validierung:**
- `id`: Nicht leer
- `price`: >= 0
- `quantity`: >= 0

### Movement (Dataclass)

**Datei:** `src/domain/warehouse.py`

```python
@dataclass
class Movement:
    id: str                                    # Eindeutige ID
    product_id: str                            # Referenz zu Product
    product_name: str                          # Name (Snapshot)
    quantity_change: int                       # Menge (+/-)
    movement_type: str                         # "IN" oder "OUT"
    reason: str = ""                           # Grund
    performed_by: str = "system"              # Nutzer/System
    timestamp: datetime = field(default_factory=datetime.now)
```

### Warehouse (Klasse)

```python
class Warehouse:
    id: str                    # Lager-ID
    products: Dict[str, Product]
    created_at: datetime
```

---

## 5. Ordnerstruktur

```
src/
├── domain/                    # Business Entities
│   ├── __init__.py
│   ├── product.py            # Product Dataclass
│   └── warehouse.py          # Warehouse, Movement Dataclass
│
├── ports/                     # Abstrakte Schnittstellen
│   └── __init__.py           # RepositoryPort, ReportPort
│
├── adapters/                  # Konkrete Implementierungen
│   ├── __init__.py
│   ├── repository.py         # InMemoryRepository, RepositoryFactory
│   └── report.py             # ConsoleReportAdapter
│
├── services/                  # Business Logic
│   ├── __init__.py           # Nur: from .warehouse_service import ...
│   └── warehouse_service.py  # WarehouseService Klasse
│
├── ui/                        # Benutzeroberfläche (PyQt6)
│   ├── __init__.py           # main() Funktion
│   ├── main_window.py        # WarehouseMainWindow Klasse
│   └── dialogs.py            # ProductDialogWindow Klasse
│
├── reports/                   # Report-Templates (zukünftig)
│   └── __init__.py
│
└── __init__.py
```

---

## 6. Import-Muster

**Richtig:**
```python
# In main_window.py
from ..services import WarehouseService
from ..adapters.repository import RepositoryFactory

# In warehouse_service.py
from ..domain.product import Product
from ..ports import RepositoryPort
```

**Falsch:**
```python
# ❌ Keine Imports aus __init__.py wenn dort nur die Klasse liegt
from ..services.warehouse_service import WarehouseService  # NEIN!

# ✅ Statt dessen:
from ..services import WarehouseService  # JA!
```

---

## 7. Fehlerbehandlung

<<<<<<< HEAD
### Exception-Typen

```python
# Grundprinzip: Nutze ValueError für ungültige Eingaben
# Nutze beschreibende Fehlermeldungen

raise ValueError("Bestand reicht nicht aus. Verfügbar: 5, Angefordert: 10")
raise ValueError("Produkt PRD-001 nicht gefunden")
raise ValueError("Product ID kann nicht leer sein")
```

### Fehler-Best-Practices

```python
# ✅ GUT
try:
    service.add_to_stock("PRD-001", 10, "Lieferung", "maria")
except ValueError as e:
    print(f"Fehler: {e}")

# ❌ SCHLECHT
try:
    service.add_to_stock("PRD-001", 10)
except:
    pass  # Fehler ignorieren!
```

---

## 8. Test-Integration

Alle Services MÜSSEN mit `InMemoryRepository` testbar sein:

```python
# test_warehouse_service.py
def test_create_product():
    repo = InMemoryRepository()
    service = WarehouseService(repo)
    
    product = service.create_product(
        product_id="TEST-001",
        name="Testprodukt",
        description="Für Tests",
        price=10.0
    )
    
    assert product.id == "TEST-001"
    assert service.get_product("TEST-001") is not None
```

---

## 9. Version-Matrix

| Feature | v0.1 | v0.2 | v0.3 | v0.4 |
|---------|------|------|------|------|
| Create/Read/Delete Produkt | ✅ | ✅ | ✅ | ✅ |
| Add/Remove Stock | ✅ | ✅ | ✅ | ✅ |
| In-Memory Repository | ✅ | ✅ | ✅ | ✅ |
| Movement-Logging | ✅ | ✅ | ✅ | ✅ |
| Basic Reports | ✅ | ✅ | ✅ | ✅ |
| **PyQt6 UI** | ⚠️ | ✅ | ✅ | ✅ |
| **SQLite Repository** | - | - | ✅ | ✅ |
| **Product Kategorien** | - | ✅ | ✅ | ✅ |
| **Advanced Reports** | - | - | ✅ | ✅ |

---

## 10. Änderungen dokumentieren

### Neue Methode hinzufügen

1. **Hier eintragen** in contracts.md
2. Tabelle + Beispiel
3. Code schreiben
4. Tests schreiben
5. Commit: `docs(contracts): neue Methode X hinzugefügt`

### Breaking Change (z.B. Parameter hinzufügen)

1. ⚠️ **Mit Team abstimmen!**
2. Alte Methode markieren als deprecated
3. Neue Methode erstellen
4. Mindestens eine Version überlappen lassen
5. In CHANGELOG.md dokumentieren

---

**Status:** v0.2.0 stabil  
**Nächste Review:** Vor v0.3 Release
=======
- [ ] SQLite-Adapter implementieren
- [ ] GraphML-Report-Generierung
- [ ] Benutzer-Management erweitern
- [ ] Batch-Operationen unterstützen
- [ ] Benutzer-Management erweitern
>>>>>>> feature/rolle2/merge-test-v2
