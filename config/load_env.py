"""Carga el .env en la raíz del repositorio antes de leer settings."""
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent.parent
_env_path = _ROOT / ".env"
if _env_path.is_file():
    load_dotenv(_env_path)
