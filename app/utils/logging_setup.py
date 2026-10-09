import logging
from logging.handlers import RotatingFileHandler

from .paths import LOG_DIR, ensure_dirs


def setup_logging() -> None:
    ensure_dirs()
    handler = RotatingFileHandler(LOG_DIR / "app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logging.basicConfig(level=logging.INFO, handlers=[handler])
