import logging
import sys

from . import i18n
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
        from PySide6.QtGui import QColor, QPalette

        pal = QPalette()
        for role, color in ((QPalette.Window, "#1b1e26"), (QPalette.WindowText, "#e6e9ef"), (QPalette.Base, "#2a2f3a"),
                            (QPalette.AlternateBase, "#22262f"), (QPalette.Text, "#e6e9ef"), (QPalette.Button, "#2a2f3a"),
                            (QPalette.ButtonText, "#e6e9ef"), (QPalette.Highlight, "#3d73f0"),
                            (QPalette.HighlightedText, "#ffffff"), (QPalette.ToolTipBase, "#2a2f3a"),
                            (QPalette.ToolTipText, "#e6e9ef")):
            pal.setColor(role, QColor(color))
        app.setPalette(pal)
        i18n.init()
        win = MainWindow()
        win.show()
        return app.exec()
    except Exception:
        logging.exception("Критическая ошибка")
        raise


if __name__ == "__main__":
    sys.exit(main())
