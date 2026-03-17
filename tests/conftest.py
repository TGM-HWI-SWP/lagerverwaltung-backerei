"""Pytest Configuration"""

import sys
from pathlib import Path

# Pfad zur src-Verzeichnis hinzufügen
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importiere alle Fixtures für automatische Verfügbarkeit
from .fixtures import *  # noqa: F401,F403
