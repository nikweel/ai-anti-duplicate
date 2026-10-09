def build_style(px: int) -> str:
    r = px // 2
    return f"""
* {{ font-size: {px}px; }}
QMainWindow, QDialog, QMessageBox {{ background: #1b1e26; }}
QLabel, QRadioButton, QCheckBox {{ color: #e6e9ef; }}
QPushButton {{
    background: #2a2f3a; color: #e6e9ef; border: 1px solid #3a4150;
    border-radius: {r}px; padding: {px // 3}px {px}px;
}}
QPushButton:hover {{ background: #343b49; }}
QPushButton:disabled {{ color: #6b7384; background: #22262f; border-color: #2a2f3a; }}
QPushButton#primary {{ background: #3d73f0; color: white; border: none; font-weight: 600; padding: {px // 2}px {px}px; }}
QPushButton#primary:hover {{ background: #5086ff; }}
QPushButton#primary:disabled {{ background: #2c3a63; color: #7f8aa8; }}
QComboBox {{ background: #2a2f3a; color: #e6e9ef; border: 1px solid #3a4150; border-radius: {r}px; padding: {px // 3}px {px // 2}px; }}
QComboBox:disabled {{ color: #6b7384; }}
QComboBox QAbstractItemView {{
    background: #2a2f3a; color: #e6e9ef; border: 1px solid #3a4150;
    selection-background-color: #3d73f0; selection-color: white; outline: 0;
}}
QProgressBar {{ border: none; background: #2a2f3a; color: #e6e9ef; border-radius: {r // 2 + 2}px; text-align: center; height: {px}px; }}
QProgressBar::chunk {{ background: #3d73f0; border-radius: {r // 2 + 2}px; }}
QSlider::groove:horizontal {{ height: 6px; background: #3a4150; border-radius: 3px; }}
QSlider::sub-page:horizontal {{ background: #5b86e8; border-radius: 3px; }}
QSlider::handle:horizontal {{ width: {px + 6}px; height: {px + 6}px; margin: -{(px + 6 - 6) // 2}px 0; border-radius: {(px + 6) // 2}px; background: #3d73f0; }}
QToolTip {{ background: #2a2f3a; color: #e6e9ef; border: 1px solid #3a4150; }}
"""
