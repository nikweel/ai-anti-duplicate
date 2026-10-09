import logging
import sys

from .utils.logging_setup import setup_logging


def main() -> int:
    setup_logging()
    try:
        from PySide6.QtWidgets import QApplication

        from .gui.main_window import MainWindow

        app = QApplication(sys.argv)
        app.setApplicationName("AI Anti-Duplicate")
        app.setDesktopFileName("ai-anti-duplicate")
        app.setStyle("Fusion")
        win = MainWindow()
        win.show()
        return app.exec()
    except Exception:
        logging.exception("Критическая ошибка")
        raise


if __name__ == "__main__":
    sys.exit(main())
