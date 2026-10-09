import os
import sys
from pathlib import Path

FROZEN = bool(getattr(sys, "frozen", False))
APP_NAME = "AI-Anti-Duplicate"
# папка с ресурсами (иконка и т.п.)
RESOURCES = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))


def _user_data_dir() -> Path:
    if sys.platform == "win32":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / APP_NAME
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support" / APP_NAME
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / APP_NAME


# из исходников — портативно рядом с проектом; из собранной программы — в папке пользователя
ROOT = _user_data_dir() if FROZEN else Path(__file__).resolve().parents[2]
MODELS_DIR = ROOT / "models"
DATA_DIR = ROOT / "data"
LOG_DIR = DATA_DIR / "logs"
CACHE_DIR = DATA_DIR / "cache"
ICON = RESOURCES / "assets" / "icon.svg"


def ensure_dirs() -> None:
    for d in (MODELS_DIR, LOG_DIR, CACHE_DIR):
        d.mkdir(parents=True, exist_ok=True)
