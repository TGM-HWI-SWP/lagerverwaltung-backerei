"""Tests für SQLiteRepository"""

import os
import tempfile
from datetime import datetime

import pytest

from src.adapters.repository import SQLiteRepository
from src.domain.product import Product
from src.domain.warehouse import Movement


def make_product(pid="P1"):
    return Product(
        id=pid,
        name="Test",
        description="",
        price=1.0,
        quantity=5,
    )


def make_movement(mid="m1"):
    return Movement(
        id=mid,
        product_id="P1",
        product_name="Test",
        quantity_change=5,
        movement_type="IN",
        timestamp=datetime.now(),
    )


def test_save_and_load(tmp_path):
    db_file = tmp_path / "test.db"
    repo = SQLiteRepository(str(db_file))

    p = make_product()
    repo.save_product(p)
    assert repo.load_product(p.id).id == p.id

    # reopen repository to ensure persistence
    repo2 = SQLiteRepository(str(db_file))
    assert repo2.load_product(p.id).name == "Test"


def test_movements_persist(tmp_path):
    db_file = tmp_path / "moves.db"
    repo = SQLiteRepository(str(db_file))
    m = make_movement()
    repo.save_movement(m)
    assert len(repo.load_movements()) == 1

    # reopen
    repo2 = SQLiteRepository(str(db_file))
    assert len(repo2.load_movements()) == 1


def test_delete_product(tmp_path):
    db_file = tmp_path / "del.db"
    repo = SQLiteRepository(str(db_file))
    p = make_product("X")
    repo.save_product(p)
    repo.delete_product("X")
    assert repo.load_product("X") is None
    # also gone from db
    repo2 = SQLiteRepository(str(db_file))
    assert repo2.load_product("X") is None
