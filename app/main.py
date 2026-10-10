import logging
import sys

from . import i18n
from .utils.logging_setup import setup_logging


def main() -> int:
    setup_logging()
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        from .cli import main as cli_main

        return cli_main(sys.argv[2:])
    try:
        from PySide6.QtWidgets import QApplication

        from .gui.main_window import MainWindow

        app = QApplication(sys.argv)
        app.setApplicationName("Photo Duplicate Finder AI")
        app.setDesktopFileName("photo-duplicate-finder-ai")
        app.setStyle("Fusion")
        from .gui import theme
        from .utils import settings

        theme.apply_palette(app, settings.get("theme", "dark"))
        i18n.init()
        from PySide6.QtCore import Qt

        app.setLayoutDirection(Qt.RightToLeft if i18n.is_rtl() else Qt.LeftToRight)
        win = MainWindow()
        win.show()
        return app.exec()
    except Exception:
        logging.exception("Критическая ошибка")
        raise


if __name__ == "__main__":
    sys.exit(main())
