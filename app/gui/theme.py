from PySide6.QtGui import QColor, QGuiApplication, QPalette

from ..utils.paths import RESOURCES

CHECK = (RESOURCES / "assets" / "check.svg").as_posix()
from PySide6.QtCore import Qt

COLORS = {
    "dark": dict(bg="#1b1e26", fg="#e6e9ef", panel="#2a2f3a", panel2="#22262f", border="#3a4150", hover="#343b49",
                 muted="#6b7384", muted_fg="#98a1b3", accent="#3d73f0", accent_h="#5086ff", accent_off="#2c3a63", accent_off_fg="#7f8aa8",
                 groove="#3a4150", fill="#5b86e8"),
    "light": dict(bg="#f5f6f8", fg="#1f2430", panel="#ffffff", panel2="#eceef2", border="#d3d7de", hover="#eef1f6",
                  muted="#9aa1ad", muted_fg="#5d6677", accent="#2b5fd9", accent_h="#2451bd", accent_off="#a9b8de", accent_off_fg="#eef1fa",
                  groove="#d3d7de", fill="#8fa8e8"),
}


def resolve(theme: str) -> str:
    if theme in COLORS:
        return theme
    try:  # "system"
        return "dark" if QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark else "light"
    except Exception:
        return "dark"


def apply_palette(app, theme: str) -> None:
    c = COLORS[resolve(theme)]
    pal = QPalette()
    for role, key in ((QPalette.Window, "bg"), (QPalette.WindowText, "fg"), (QPalette.Base, "panel"),
                      (QPalette.AlternateBase, "panel2"), (QPalette.Text, "fg"), (QPalette.Button, "panel"),
                      (QPalette.ButtonText, "fg"), (QPalette.Highlight, "accent"), (QPalette.ToolTipBase, "panel"),
                      (QPalette.ToolTipText, "fg")):
        pal.setColor(role, QColor(c[key]))
    pal.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(pal)


def build_style(px: int, theme: str) -> str:
    c = COLORS[resolve(theme)]
    r = px // 2
    h = px + 6
    return f"""
* {{ font-size: {px}px; }}
QMainWindow, QDialog, QMessageBox {{ background: {c['bg']}; }}
QLabel, QRadioButton, QCheckBox {{ color: {c['fg']}; }}
QPushButton {{
    background: {c['panel']}; color: {c['fg']}; border: 1px solid {c['border']};
    border-radius: {r}px; padding: {px // 3}px {px}px;
}}
QPushButton:hover {{ background: {c['hover']}; }}
QPushButton:disabled {{ color: {c['muted']}; background: {c['panel2']}; border-color: {c['panel2']}; }}
QPushButton#primary {{ background: {c['accent']}; color: white; border: none; font-weight: 600; padding: {px // 2}px {px}px; }}
QPushButton#primary:hover {{ background: {c['accent_h']}; }}
QPushButton#primary:disabled {{ background: {c['accent_off']}; color: {c['accent_off_fg']}; }}
QComboBox {{ min-height: {int(px * 1.5)}px; background: {c['panel']}; color: {c['fg']}; border: 1px solid {c['border']}; border-radius: {r}px; padding: {px // 3}px {px // 2}px; }}
QComboBox:disabled {{ color: {c['muted']}; }}
QComboBox QAbstractItemView {{
    background: {c['panel']}; color: {c['fg']}; border: 1px solid {c['border']};
    selection-background-color: {c['accent']}; selection-color: white; outline: 0;
}}
QProgressBar {{ border: none; background: {c['panel']}; color: {c['fg']}; border-radius: {r // 2 + 2}px; text-align: center; height: {px}px; }}
QProgressBar::chunk {{ background: {c['accent']}; border-radius: {r // 2 + 2}px; }}
QSlider::groove:horizontal {{ height: 6px; background: {c['groove']}; border-radius: 3px; }}
QSlider::sub-page:horizontal {{ background: {c['fill']}; border-radius: 3px; }}
QSlider::handle:horizontal {{ width: {h}px; height: {h}px; margin: -{(h - 6) // 2}px 0; border-radius: {h // 2}px; background: {c['accent']}; }}
QRadioButton::indicator {{ width: {px}px; height: {px}px; border-radius: {px // 2 + 1}px; border: 2px solid {c['muted']}; background: {c['panel']}; }}
QRadioButton::indicator:checked {{ background: {c['accent']}; border-color: {c['accent']}; }}
QCheckBox::indicator {{ width: {px}px; height: {px}px; border-radius: 4px; border: 2px solid {c['muted']}; background: {c['panel']}; }}
QCheckBox::indicator:checked {{ background: {c['accent']}; border-color: {c['accent']}; image: url({CHECK}); }}
QGroupBox {{ color: {c['fg']}; border: 1px solid {c['border']}; border-radius: {r}px; margin-top: {px}px; padding: {px}px {px // 2}px {px // 2}px; }}
QGroupBox::title {{ subcontrol-origin: margin; left: {px}px; padding: 0 4px; }}
QLineEdit {{ min-height: {int(px * 1.5)}px; background: {c['panel']}; color: {c['fg']}; border: 1px solid {c['border']}; border-radius: {r}px; padding: {px // 3}px {px // 2}px; }}
QScrollArea {{ background: transparent; }}
QFrame#card {{ background: {c['panel2']}; border: 1px solid {c['border']}; border-radius: {px}px; }}
QLabel#cardTitle {{ color: {c['fg']}; font-weight: 700; font-size: {px}px; letter-spacing: 0.3px; }}
QLabel#muted {{ color: {c['muted_fg']}; }}
QLabel#appTitle {{ font-size: {int(px * 1.45)}px; font-weight: 700; }}
QLabel#summary {{ color: {c['fg']}; background: {c['panel']}; border: 1px solid {c['border']}; border-radius: {r}px; padding: {px // 2}px {px}px; }}
QLineEdit#path {{ background: {c['panel']}; border: 1px dashed {c['border']}; }}
QLineEdit#path[hasValue="true"] {{ border: 1px solid {c['border']}; }}
QLineEdit#path[dropActive="true"] {{ border: 2px solid {c['accent']}; }}
QToolButton#disclosure {{ background: transparent; border: none; color: {c['accent_h']}; font-weight: 600; padding: {px // 3}px 0; }}
QToolButton#disclosure:hover {{ color: {c['fg']}; }}
QPushButton:focus, QComboBox:focus, QLineEdit:focus, QToolButton:focus {{ border: 2px solid {c['accent']}; }}
QCheckBox:focus, QRadioButton:focus {{ color: {c['fg']}; text-decoration: underline; }}
QLabel#badge {{ color: {c['accent_h']}; font-weight: 600; }}
QToolTip {{ background: {c['panel']}; color: {c['fg']}; border: 1px solid {c['border']}; }}
"""
