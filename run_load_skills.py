"""Helper runner to execute ingestion/load_skills_to_postgres.py with correct sys.path.

Usage:
  cd c:/Users/DELL/Desktop/careerpulse
  python run_load_skills.py
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Ensure project root is on sys.path so `utils` (and other top-level packages) resolve.
sys.path.insert(0, str(ROOT))

runpy.run_path(str(ROOT / "igestion" / "load_skills_to_postgres.py"), run_name="__main__")

