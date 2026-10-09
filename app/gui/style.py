def build_style(px: int) -> str:
    r = px // 2
    return f"""
* {{ font-size: {px}px; }}
QMainWindow, QDialog {{ background: #f5f6f8; }}
QLabel {{ color: #1f2430; }}
QPushButton {{
    background: #ffffff; color: #1f2430; border: 1px solid #d3d7de;
    border-radius: {r}px; padding: {px // 3}px {px}px;
}}
QPushButton:hover {{ background: #eef1f6; }}
QPushButton:disabled {{ color: #9aa1ad; background: #eceef2; }}
QPushButton#primary {{ background: #2b5fd9; color: white; border: none; font-weight: 600; padding: {px // 2}px {px}px; }}
QPushButton#primary:hover {{ background: #2451bd; }}
QPushButton#primary:disabled {{ background: #a9b8de; color: #eef1fa; }}
QComboBox {{ background: white; border: 1px solid #d3d7de; border-radius: {r}px; padding: {px // 3}px {px // 2}px; }}
QProgressBar {{ border: none; background: #e2e5eb; border-radius: {r // 2 + 2}px; text-align: center; height: {px}px; }}
QProgressBar::chunk {{ background: #2b5fd9; border-radius: {r // 2 + 2}px; }}
QSlider::groove:horizontal {{ height: 6px; background: #d3d7de; border-radius: 3px; }}
QSlider::handle:horizontal {{ width: {px + 6}px; height: {px + 6}px; margin: -{(px + 6 - 6) // 2}px 0; border-radius: {(px + 6) // 2}px; background: #2b5fd9; }}
QSlider::sub-page:horizontal {{ background: #8fa8e8; border-radius: 3px; }}
QRadioButton {{ color: #1f2430; }}
"""
