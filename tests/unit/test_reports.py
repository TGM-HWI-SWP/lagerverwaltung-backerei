"""Unit tests für die Report‑Klassen"""

import pytest
from src.domain.product import Product
from src.domain.warehouse import Movement
from src.reports import InventoryReport, MovementReport


def make_sample_products():
    return {
        "P1": Product(id="P1", name="A", description="", price=1.0, quantity=5, category="x"),
        "P2": Product(id="P2", name="B", description="", price=2.0, quantity=0, category="y"),
        "P3": Product(id="P3", name="C", description="", price=3.0, quantity=2, category="x"),
    }


def make_sample_movements():
    return [
        Movement(id="m1", product_id="P1", product_name="A", quantity_change=5, movement_type="IN"),
        Movement(id="m2", product_id="P1", product_name="A", quantity_change=-2, movement_type="OUT"),
    ]


class TestInventoryReport:
    def test_empty(self):
        r = InventoryReport({})
        assert "Lager ist leer" in r.generate()

    def test_content_and_flags(self):
        products = make_sample_products()
        r = InventoryReport(products)
        out = r.generate()
        assert "P1" in out and "A" in out
        assert "!!! KNAPP !!!" in out  # weil P3 < 10
        assert "LEER" in out  # P2
        assert "Gesamtwert Lager" in out


class TestMovementReport:
    def test_empty(self):
        r = MovementReport([])
        assert "Keine Lagerbewegungen" in r.generate()

    def test_chronology_and_format(self):
        movs = make_sample_movements()
        r = MovementReport(movs)
        out = r.generate()
        assert "BEWEGUNGSPROTOKOLL" in out
        # erster Eintrag vor zweitem
        assert out.index("m1") < out.index("m2")
