"""Services package re-export.

Keep the implementation in `warehouse_service.py` and re-export the main
service class from here so `from src.services import WarehouseService` works
consistently.
"""

from .warehouse_service import WarehouseService

__all__ = ["WarehouseService"]
