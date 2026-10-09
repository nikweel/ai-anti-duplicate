from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication, QIcon, QPixmap
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QDialog, QFileDialog, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QProgressBar, QSizePolicy,
    QPushButton, QRadioButton, QSlider, QVBoxLayout, QWidget,
)

from ..utils.paths import ICON
from ..data.models import DuplicateGroup
from ..services.exporter import export_unique
from .. import i18n
from ..i18n import tr
from ..services.selection import RULES, pick_newest
from .style import build_style
from .workers import ModelWorker, ScanWorker


class ScaledImage(QLabel):
    """Картинка, которая подстраивается под размер виджета; клик по ней -> clicked."""

    clicked = Signal()

    def __init__(self, path, min_size=120):
        super().__init__()
        self._pm = QPixmap(str(path))
        self.setMinimumSize(min_size, min_size)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)

    def resizeEvent(self, e):
        if not self._pm.isNull():
            self.setPixmap(self._pm.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        super().resizeEvent(e)

    def mousePressEvent(self, e):
        self.clicked.emit()


class PreviewPopup(QDialog):
    """Крупный предпросмотр; закрывается кликом в любое место вне окна (или по картинке)."""

    def __init__(self, img, parent):
        super().__init__(parent, Qt.Popup)
        screen = (parent.screen() if parent else QGuiApplication.primaryScreen()).availableGeometry()
        w, h = int(screen.width() * 0.8), int(screen.height() * 0.85)
        self.resize(w, h)
        self.move(screen.center().x() - w // 2, screen.center().y() - h // 2)
        lay = QVBoxLayout(self)
        pic = ScaledImage(img.path, 200)
        pic.setCursor(Qt.ArrowCursor)
        pic.clicked.connect(self.close)
        px = QPixmap(str(img.path))
        cap = QLabel(f"{img.path.name} — {px.width()}×{px.height()}, {img.size / 1024:.0f} {tr('kb')}")
        cap.setAlignment(Qt.AlignCenter)
        lay.addWidget(pic, 1)
        lay.addWidget(cap)


class ReviewDialog(QDialog):
    """Duplicates of one shot: choose which file to keep."""

    def __init__(self, group: DuplicateGroup, n: int, total: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("review_title", n=n, t=total))
        self.group = group
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.resize(1000, 600)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(tr("review_hint")))
        row = QHBoxLayout()
        self.buttons = QButtonGroup(self)
        for i, img in enumerate(group.images):
            col = QVBoxLayout()
            pic = ScaledImage(img.path)
            pic.clicked.connect(lambda img=img: PreviewPopup(img, self).exec())
            rb = QRadioButton(f"{img.path.name}\n{img.size / 1024:.0f} {tr('kb')}")
            self.buttons.addButton(rb, i)
            col.addWidget(pic, 1)
            col.addWidget(rb)
            row.addLayout(col, 1)
        lay.addLayout(row, 1)
        self.buttons.button(group.keep).setChecked(True)
        btns = QHBoxLayout()
        cancel, ok = QPushButton(tr("cancel")), QPushButton(tr("keep"))
        cancel.clicked.connect(self.reject)
        ok.clicked.connect(self._accept)
        ok.setDefault(True)
        ok.setObjectName("primary")
        btns.addStretch()
        btns.addWidget(cancel)
        btns.addWidget(ok)
        lay.addLayout(btns)

    def _accept(self):
        self.group.keep = self.buttons.checkedId()
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Anti-Duplicate")
        self.setMinimumWidth(520)
        self.setWindowIcon(QIcon(str(ICON)))
        self.model = None
        self.src: Path | None = None
        self.dst: Path | None = None
        self.worker = None
        self._status_key = "loading_model"

        w = QWidget()
        self.setCentralWidget(w)
        lay = QVBoxLayout(w)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(12)

        top = QHBoxLayout()
        top.addStretch()
        self.lang_lbl = QLabel()
        self.lang = QComboBox()
        for code, name in i18n.LANGS.items():
            self.lang.addItem(name, code)
        self.lang.setCurrentIndex(self.lang.findData(i18n.get_lang()))
        self.lang.currentIndexChanged.connect(self._lang_changed)
        top.addWidget(self.lang_lbl)
        top.addWidget(self.lang)
        lay.addLayout(top)

        self.src_btn, self.src_lbl = self._picker(lay, self.pick_src)
        self.dst_btn, self.dst_lbl = self._picker(lay, self.pick_dst)
        self.rule = QComboBox()
        for rid in RULES:
            self.rule.addItem("", rid)
        lay.addWidget(self.rule)
        self.sens_title = QLabel()
        lay.addWidget(self.sens_title)
        srow = QHBoxLayout()
        self.sens = QSlider(Qt.Horizontal)
        self.sens.setRange(0, 100)
        self.sens.setValue(33)
        self.sens.valueChanged.connect(self._sens_changed)
        self.strict_lbl, self.soft_lbl = QLabel(), QLabel()
        srow.addWidget(self.strict_lbl)
        srow.addWidget(self.sens, 1)
        srow.addWidget(self.soft_lbl)
        lay.addLayout(srow)
        self.sens_hint = QLabel()
        self.sens_hint.setWordWrap(True)
        lay.addWidget(self.sens_hint)
        self.start = QPushButton()
        self.start.setObjectName("primary")
        self.start.setEnabled(False)
        self.start.clicked.connect(self.run)
        self.bar = QProgressBar()
        self.status = QLabel()
        for x in (self.start, self.bar, self.status):
            lay.addWidget(x)
        self.retranslate()

        self.worker = ModelWorker()
        self.worker.progress.connect(self.on_progress)
        self.worker.loaded.connect(self.on_model)
        self.worker.failed.connect(self.on_error)
        self.worker.start()

    def _picker(self, lay, slot):
        row = QHBoxLayout()
        btn = QPushButton()
        lbl = QLabel()
        btn.clicked.connect(slot)
        btn.setMinimumWidth(190)
        row.addWidget(btn)
        row.addWidget(lbl, 1)
        lay.addLayout(row)
        return btn, lbl

    def retranslate(self):
        self.lang_lbl.setText(tr("language") + ":")
        self.src_btn.setText(tr("src_btn"))
        self.dst_btn.setText(tr("dst_btn"))
        self.src_lbl.setText(str(self.src) if self.src else tr("not_chosen"))
        self.dst_lbl.setText(str(self.dst) if self.dst else tr("not_chosen"))
        for i in range(self.rule.count()):
            self.rule.setItemText(i, tr("rule_" + self.rule.itemData(i)))
        self.sens_title.setText(tr("sens"))
        self.strict_lbl.setText(tr("strict"))
        self.soft_lbl.setText(tr("soft"))
        self._sens_changed(self.sens.value())
        self.start.setText(tr("start"))
        if self._status_key:
            self.status.setText(tr(self._status_key))

    def _lang_changed(self):
        i18n.set_lang(self.lang.currentData())
        self.retranslate()

    def threshold(self) -> float:
        return 0.98 - self.sens.value() * 0.0018  # 0 -> 0.98 (strict), 100 -> 0.80 (soft)

    def _sens_changed(self, v: int):
        self.sens_hint.setText(tr("sens_low" if v < 25 else "sens_mid" if v < 60 else "sens_high"))

    def _refresh(self):
        self.start.setEnabled(bool(self.model and self.src and self.dst))

    def pick_src(self):
        if d := QFileDialog.getExistingDirectory(self, tr("src_btn")):
            self.src = Path(d)
            self.src_lbl.setText(d)
            self._refresh()

    def pick_dst(self):
        if d := QFileDialog.getExistingDirectory(self, tr("dst_btn")):
            self.dst = Path(d)
            self.dst_lbl.setText(d)
            self._refresh()

    def on_progress(self, frac, msg):
        self._status_key = None
        self.bar.setValue(int(frac * 100))
        self.status.setText(msg)

    def on_error(self, msg):
        self._busy(False)
        QMessageBox.critical(self, tr("error"), f"{msg}\n\n{tr('details')}")

    def on_model(self, model):
        self.model = model
        self._status_key = "ready"
        self.status.setText(tr("ready"))
        self._refresh()

    def _busy(self, busy: bool):
        for x in (self.src_btn, self.dst_btn, self.rule, self.sens, self.start):
            x.setEnabled(not busy)
        if not busy:
            self._refresh()

    def run(self):
        if self.src == self.dst:
            QMessageBox.warning(self, tr("folders"), tr("diff_folders"))
            return
        self._busy(True)
        self.worker = ScanWorker(self.model, self.src, self.dst, self.threshold())
        self.worker.progress.connect(self.on_progress)
        self.worker.done.connect(self.on_done)
        self.worker.failed.connect(self.on_error)
        self.worker.start()

    def on_done(self, images, groups):
        try:
            if groups and not self._resolve(groups):
                self.status.setText(tr("cancelled"))
                return
            n = export_unique(self.dst, groups, images)
            self.status.setText(tr("done_status", n=n, g=len(groups)))
            QMessageBox.information(self, tr("done"), tr("done_box", n=n, dst=self.dst))
        except Exception as e:
            self.on_error(str(e))
        finally:
            self._busy(False)

    def _resolve(self, groups) -> bool:
        pick = RULES[self.rule.currentData()]
        for n, g in enumerate(groups, 1):
            g.keep = (pick or pick_newest)(g)
            if pick is None and ReviewDialog(g, n, len(groups), self).exec() != QDialog.Accepted:
                return False
        return True

    def resizeEvent(self, e):
        # the interface scales together with the window
        px = int(max(13, min(30, 13 * self.width() / 560)))
        if px != getattr(self, "_px", None):
            self._px = px
            self.setStyleSheet(build_style(px))
        super().resizeEvent(e)

    def closeEvent(self, e):
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.wait(3000)
        super().closeEvent(e)
