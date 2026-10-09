from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton, QVBoxLayout,
)

from .. import i18n
from ..core.model_manager import MODELS, is_downloaded
from ..i18n import tr
from ..utils import settings


class SettingsDialog(QDialog):
    """Язык, тема, модель и устройство. Результат читается из атрибутов после accept()."""

    def __init__(self, parent, model_id: str | None):
        super().__init__(parent)
        self.setWindowTitle(tr("settings_title"))
        self.setMinimumWidth(520)
        self.initial_model = model_id
        lay = QVBoxLayout(self)
        lay.setSpacing(14)

        form = QFormLayout()
        self.lang = QComboBox()
        for code, name in i18n.LANGS.items():
            self.lang.addItem(name, code)
        self.lang.setCurrentIndex(self.lang.findData(i18n.get_lang()))
        self.theme = QComboBox()
        for t in ("dark", "light", "system"):
            self.theme.addItem(tr("theme_" + t), t)
        self.theme.setCurrentIndex(max(0, self.theme.findData(settings.get("theme", "dark"))))
        self.device = QComboBox()
        for d in ("auto", "cpu", "gpu"):
            self.device.addItem(tr("device_" + d), d)
        self.device.setCurrentIndex(max(0, self.device.findData(settings.get("device", "auto"))))
        form.addRow(tr("language") + ":", self.lang)
        form.addRow(tr("theme_label"), self.theme)
        form.addRow(tr("device_label"), self.device)
        lay.addLayout(form)

        lay.addWidget(QLabel(f"<b>{tr('model_group')}</b>"))
        self.group = QButtonGroup(self)
        for mid, spec in MODELS.items():
            rb = QRadioButton(tr(f"model_{mid}_t"))
            have = is_downloaded(mid)
            state = QLabel(tr(f"model_{mid}_d", mb=spec.size_mb) + "\n" +
                           ("✓ " + tr("model_have") if have else "⬇ " + tr("model_need", mb=spec.size_mb)))
            state.setWordWrap(True)
            state.setContentsMargins(28, 0, 0, 6)
            self.group.addButton(rb)
            rb.setProperty("mid", mid)
            lay.addWidget(rb)
            lay.addWidget(state)
            if mid == model_id:
                rb.setChecked(True)

        btns = QHBoxLayout()
        close, ok = QPushButton(tr("close")), QPushButton(tr("ok"))
        ok.setObjectName("primary")
        close.clicked.connect(self.reject)
        ok.clicked.connect(self.accept)
        btns.addStretch()
        btns.addWidget(close)
        btns.addWidget(ok)
        lay.addLayout(btns)

    def chosen_model(self) -> str | None:
        b = self.group.checkedButton()
        return b.property("mid") if b else None
