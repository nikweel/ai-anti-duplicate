from pathlib import Path

from PySide6.QtCore import QSize, QTimer, Qt, Signal
from PySide6.QtGui import QGuiApplication, QIcon, QImageReader, QPainter, QPalette, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication, QFrame, QGridLayout, QScrollArea, QComboBox, QDialog, QFileDialog, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QProgressBar, QSizePolicy,
    QPushButton, QRadioButton, QSlider, QVBoxLayout, QWidget,
)

from ..utils.paths import ICON
from ..data.models import DuplicateGroup
from ..services.exporter import export_unique
from ..services.naming import DATE_FORMATS, NamingOptions, format_date
from datetime import datetime
from PySide6.QtWidgets import QCheckBox, QGroupBox, QLineEdit
from .. import i18n
from ..core.model_manager import DEFAULT_SENSITIVITY, LEGACY_IDS, MODELS, is_downloaded, threshold_for
from ..utils import settings
from ..i18n import tr
from ..services.selection import RULES, pick_newest
from . import theme
from .settings_dialog import SettingsDialog
from .workers import ModelWorker, ScanWorker


def load_pixmap(path, max_side: int) -> QPixmap:
    """Читает картинку сразу уменьшенной (экономит память) и с учётом EXIF-поворота."""
    r = QImageReader(str(path))
    r.setAutoTransform(True)
    size = r.size()
    if size.isValid() and max(size.width(), size.height()) > max_side:
        size.scale(max_side, max_side, Qt.KeepAspectRatio)
        r.setScaledSize(size)
    return QPixmap.fromImage(r.read())


class HoverPreview(QFrame):
    """Крупный предпросмотр при наведении: не перехватывает мышь, исчезает при уходе курсора."""

    def __init__(self):
        super().__init__(None, Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setStyleSheet("HoverPreview { background: #0d0f14; border: 2px solid #3d73f0; } QLabel { color: #e6e9ef; background: transparent; }")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 8, 8, 8)
        self.pic, self.cap = QLabel(), QLabel()
        self.pic.setAlignment(Qt.AlignCenter)
        self.cap.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.pic)
        lay.addWidget(self.cap)

    def show_for(self, img, anchor: QWidget):
        screen = anchor.screen().availableGeometry()
        side = int(min(screen.width(), screen.height()) * 0.78)
        pm = load_pixmap(img.path, side)
        self.pic.setPixmap(pm)
        self.cap.setText(f"{img.path.name} — {pm.width()}×{pm.height()}, {img.size / 1024:.0f} {tr('kb')}")
        self.adjustSize()
        self.move(screen.center().x() - self.width() // 2, screen.center().y() - self.height() // 2)
        self.show()
        self.raise_()


def compact(cb: QComboBox) -> QComboBox:
    """Список не растягивает окно под самую длинную строку (полный текст виден при раскрытии)."""
    cb.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
    cb.setMinimumContentsLength(18)
    cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    return cb


class ScaledImage(QLabel):
    """Миниатюра: клик = переключить выбор, наведение = крупный предпросмотр, рамка у выбранной."""

    toggled = Signal()

    def __init__(self, img, min_size=120):
        super().__init__()
        self.img = img
        self.selected = False
        self._pm = load_pixmap(img.path, 900)
        self._preview = HoverPreview()
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(lambda: self._preview.show_for(self.img, self))
        self.setMinimumSize(min_size, min_size)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)

    def set_selected(self, v: bool):
        self.selected = v
        self.update()

    def resizeEvent(self, e):
        if not self._pm.isNull():
            self.setPixmap(self._pm.scaled(self.size() - QSize(12, 12), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        super().resizeEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.selected:
            p = QPainter(self)
            pen = QPen(self.palette().color(QPalette.Highlight), 5)
            p.setPen(pen)
            p.drawRoundedRect(self.rect().adjusted(3, 3, -3, -3), 8, 8)

    def mousePressEvent(self, e):
        self._timer.stop()
        self._preview.hide()
        self.toggled.emit()

    def enterEvent(self, e):
        self._timer.start(250)  # небольшая задержка, чтобы превью не мелькало при движении мыши
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._timer.stop()
        self._preview.hide()
        super().leaveEvent(e)

    def hideEvent(self, e):
        self._preview.hide()
        super().hideEvent(e)


class ReviewDialog(QDialog):
    """Дубли одного кадра: отмечаем галочками все файлы, которые нужно сохранить (можно несколько)."""

    def __init__(self, group: DuplicateGroup, n: int, total: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("review_title", n=n, t=total))
        self.group = group
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.resize(1100, 650)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(tr("review_hint")))
        grid = QGridLayout()
        cols = min(len(group.images), 4)
        self.boxes: list[QCheckBox] = []
        self.pics: list[ScaledImage] = []
        for i, img in enumerate(group.images):
            pic = ScaledImage(img)
            cb = QCheckBox(f"{img.path.name}\n{img.size / 1024:.0f} {tr('kb')} · {pic._pm.width()}×{pic._pm.height()}")
            cb.toggled.connect(pic.set_selected)
            cb.toggled.connect(self._update_ok)
            pic.toggled.connect(cb.toggle)
            self.boxes.append(cb)
            self.pics.append(pic)
            col = QVBoxLayout()
            col.addWidget(pic, 1)
            col.addWidget(cb)
            grid.addLayout(col, i // cols, i % cols)
        host = QWidget()
        host.setLayout(grid)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(host)
        lay.addWidget(scroll, 1)
        btns = QHBoxLayout()
        all_btn, none_btn = QPushButton(tr("select_all")), QPushButton(tr("select_none"))
        all_btn.clicked.connect(lambda: [b.setChecked(True) for b in self.boxes])
        none_btn.clicked.connect(lambda: [b.setChecked(False) for b in self.boxes])
        cancel, self.ok = QPushButton(tr("cancel")), QPushButton(tr("keep"))
        cancel.clicked.connect(self.reject)
        self.ok.clicked.connect(self._accept)
        self.ok.setObjectName("primary")
        self.ok.setEnabled(False)
        btns.addWidget(all_btn)
        btns.addWidget(none_btn)
        btns.addStretch()
        btns.addWidget(cancel)
        btns.addWidget(self.ok)
        lay.addLayout(btns)

    def _update_ok(self, *_):
        self.ok.setEnabled(any(b.isChecked() for b in self.boxes))

    def _accept(self):
        self.group.keep = [i for i, b in enumerate(self.boxes) if b.isChecked()]
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Anti-Duplicate")
        self.setMinimumWidth(520)
        self.setWindowIcon(QIcon(str(ICON)))
        self.src: Path | None = None
        self.dst: Path | None = None
        self.worker = None
        self.model = None
        self._cur_px = 13
        self._status_key = "loading_model"

        w = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(w)
        self.setCentralWidget(scroll)
        lay = QVBoxLayout(w)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(12)

        top = QHBoxLayout()
        top.addStretch()
        self.settings_btn = QPushButton()
        self.settings_btn.clicked.connect(self.open_settings)
        top.addWidget(self.settings_btn)
        lay.addLayout(top)

        self.src_btn, self.src_lbl = self._picker(lay, self.pick_src)
        self.dst_btn, self.dst_lbl = self._picker(lay, self.pick_dst)
        self.rule_lbl = QLabel()
        lay.addWidget(self.rule_lbl)
        self.rule = compact(QComboBox())
        for rid in RULES:
            self.rule.addItem("", rid)
        lay.addWidget(self.rule)
        self._build_names_box(lay)
        self.sens_title = QLabel()
        lay.addWidget(self.sens_title)
        srow = QHBoxLayout()
        self.sens = QSlider(Qt.Horizontal)
        self.sens.setRange(0, 100)
        self.sens.setValue(DEFAULT_SENSITIVITY)
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
        self.status.setWordWrap(True)
        for x in (self.start, self.bar, self.status):
            lay.addWidget(x)
        self.retranslate()
        self._fit_to_content()

        QTimer.singleShot(0, self.start_up)

    def _fit_to_content(self):
        """Окно сразу вмещает всё содержимое без прокрутки (но не больше экрана)."""
        self._fit_done = False
        self._px_cap = 30
        self.resize(720, 400)

    def showEvent(self, e):
        super().showEvent(e)
        if getattr(self, "_fit_done", True):
            return
        self._fit_done = True
        QTimer.singleShot(0, self._fit_now)

    def _fit_now(self, step: int = 0):
        """Подгоняет окно под содержимое; если экрана не хватает, уменьшает шрифт (до 11 px).
        Идёт короткими шагами, потому что Qt пересчитывает размеры не мгновенно."""
        sa = self.centralWidget()
        avail = (self.screen() or QGuiApplication.primaryScreen()).availableGeometry()
        max_w, max_h = int(avail.width() * 0.95), int(avail.height() * 0.95)
        need_h, need_w = sa.verticalScrollBar().maximum(), sa.horizontalScrollBar().maximum()
        if (need_h > 0 or need_w > 0) and step < 25:
            if ((self.height() >= max_h - 2 and need_h > 0) or (self.width() >= max_w - 2 and need_w > 0)) and self._cur_px > 11:
                self._px_cap = self._cur_px - 1  # не помещается по высоте экрана -> мельче шрифт
                self._px = None
                self._cur_px = self._px_cap
                self.setStyleSheet(theme.build_style(self._px_cap, settings.get("theme", "dark")))
            else:
                self.resize(min(self.width() + need_w, max_w), min(self.height() + need_h, max_h))
        if (need_h > 0 or need_w > 0 or step < 3) and step < 25:  # минимум 3 проверки: Qt пересчитывает размеры с задержкой
            QTimer.singleShot(60, lambda: self._fit_now(step + 1))

    def current_model(self) -> str | None:
        """Выбранная модель; если не выбрана, берём любую уже скачанную."""
        mid = settings.get("model")
        mid = LEGACY_IDS.get(mid, mid)
        if mid in MODELS:
            return mid
        return next((m for m in MODELS if is_downloaded(m)), None)

    def start_up(self):
        mid = self.current_model()
        if mid and is_downloaded(mid):
            self.load_engine(mid)
            return
        self._status_key = "choose_model_status"
        self.status.setText(tr("choose_model_status"))
        QMessageBox.information(self, "AI Anti-Duplicate", tr("choose_model_msg"))
        self.open_settings()

    def load_engine(self, mid: str):
        self.model = None
        self._status_key = "loading_model"
        self.status.setText(tr("loading_model"))
        self.bar.setValue(0)
        self.model_id = mid
        self._busy(True)
        self.worker = ModelWorker(mid, settings.get("device", "auto"))
        self.worker.progress.connect(self.on_progress)
        self.worker.loaded.connect(self.on_model)
        self.worker.failed.connect(self.on_engine_error)
        self.worker.start()

    def open_settings(self):
        if self.worker and self.worker.isRunning():
            return
        old_mid, old_dev = self.current_model(), settings.get("device", "auto")
        dlg = SettingsDialog(self, old_mid)
        if dlg.exec() != QDialog.Accepted:
            if not self.model and self.current_model() and is_downloaded(self.current_model()):
                self.load_engine(self.current_model())
            return
        i18n.set_lang(dlg.lang.currentData())
        QApplication.instance().setLayoutDirection(Qt.RightToLeft if i18n.is_rtl() else Qt.LeftToRight)
        settings.put("theme", dlg.theme.currentData())
        settings.put("device", dlg.device.currentData())
        self.apply_theme()
        self.retranslate()
        self._px_cap = 30
        QTimer.singleShot(0, self._fit_now)  # другой язык — другая длина подписей
        mid = dlg.chosen_model()
        if mid:
            settings.put("model", mid)
        if mid and (mid != old_mid or dlg.device.currentData() != old_dev or not self.model):
            self.load_engine(mid)  # скачает модель, если её ещё нет

    def apply_theme(self):
        theme.apply_palette(QApplication.instance(), settings.get("theme", "dark"))
        self._px = None
        self.setStyleSheet(theme.build_style(getattr(self, "_cur_px", 13), settings.get("theme", "dark")))

    def on_engine_error(self, msg):
        self.on_error(msg)
        self._status_key = "choose_model_status"
        self.status.setText(tr("choose_model_status"))

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

    def _build_names_box(self, lay):
        o = NamingOptions.from_dict(settings.get("naming"))
        self.recursive = QCheckBox()
        self.recursive.setChecked(bool(settings.get("recursive", True)))
        self.recursive.toggled.connect(lambda v: settings.put("recursive", v))
        lay.addWidget(self.recursive)
        self.names_box = QGroupBox()
        g = QVBoxLayout(self.names_box)
        g.setSpacing(8)
        self.nm_mode = compact(QComboBox())
        for k in ("keep", "date"):
            self.nm_mode.addItem("", k)
        self.nm_src = compact(QComboBox())
        for k in ("exif", "created", "modified"):
            self.nm_src.addItem("", k)
        self.nm_fmt = compact(QComboBox())
        for k in DATE_FORMATS:
            self.nm_fmt.addItem("", k)
        self.nm_custom = QLineEdit(o.custom)
        self.nm_custom_hint = QLabel()
        self.nm_custom_hint.setWordWrap(True)
        self.nm_conf = compact(QComboBox())
        for k in ("counter", "prefix"):
            self.nm_conf.addItem("", k)
        self.nm_example = QLabel()
        self.nm_safe = QLabel()
        self.nm_safe.setWordWrap(True)
        for wdg in (self.nm_mode, self.nm_src, self.nm_fmt, self.nm_custom, self.nm_custom_hint, self.nm_conf,
                    self.nm_example, self.nm_safe):
            g.addWidget(wdg)
        for cb, val in ((self.nm_mode, o.mode), (self.nm_src, o.date_source), (self.nm_fmt, o.date_format),
                        (self.nm_conf, o.conflict)):
            cb.setCurrentIndex(max(0, cb.findData(val)))
            cb.currentIndexChanged.connect(self._names_changed)
        self.nm_custom.textChanged.connect(self._names_changed)
        lay.addWidget(self.names_box)

    def naming(self) -> NamingOptions:
        return NamingOptions(self.nm_mode.currentData(), self.nm_src.currentData(), self.nm_fmt.currentData(),
                             self.nm_custom.text() or "%Y-%m-%d_%H-%M-%S", self.nm_conf.currentData())

    def _names_changed(self, *_):
        o = self.naming()
        settings.put("naming", o.to_dict())
        by_date = o.mode == "date"
        self.nm_src.setVisible(by_date)
        self.nm_fmt.setVisible(by_date)
        custom = by_date and o.date_format == "custom"
        self.nm_custom.setVisible(custom)
        self.nm_custom_hint.setVisible(custom)
        try:
            name = (format_date(datetime(2024, 5, 1, 12, 30, 45), o.date_format, o.custom) if by_date else "IMG_0042") + ".jpg"
        except Exception:
            name = "?"
        self.nm_example.setText(tr("nm_example", name=name))

    def retranslate(self):
        self.rule_lbl.setText(tr("rule_label"))
        self.recursive.setText(tr("recursive"))
        self.names_box.setTitle(tr("names_group"))
        for cb, prefix in ((self.nm_mode, "nm_mode_"), (self.nm_src, "nm_src_"), (self.nm_fmt, "nm_fmt_"), (self.nm_conf, "nm_conf_")):
            for i in range(cb.count()):
                cb.setItemText(i, tr(prefix + cb.itemData(i)))
        self.nm_custom_hint.setText(tr("nm_custom_hint"))
        self.nm_safe.setText(tr("nm_safe"))
        self._names_changed()
        self.settings_btn.setText("⚙ " + tr("settings"))
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
        return threshold_for(getattr(self, "model_id", "light"), self.sens.value())

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
        self._status_key = None
        self.status.setText(tr("ready_dev", dev=model.device_name))
        self._busy(False)
        QTimer.singleShot(0, self._fit_now)

    def _busy(self, busy: bool):
        for x in (self.src_btn, self.dst_btn, self.rule, self.sens, self.start, self.settings_btn, self.recursive, self.names_box):
            x.setEnabled(not busy)
        if not busy:
            self._refresh()

    def run(self):
        if self.src == self.dst:
            QMessageBox.warning(self, tr("folders"), tr("diff_folders"))
            return
        self._busy(True)
        self.worker = ScanWorker(self.model, self.src, self.dst, self.threshold(), True, self.recursive.isChecked())
        self.worker.progress.connect(self.on_progress)
        self.worker.done.connect(self.on_done)
        self.worker.failed.connect(self.on_error)
        self.worker.start()

    def on_done(self, images, groups):
        try:
            if groups and not self._resolve(groups):
                self.status.setText(tr("cancelled"))
                return
            n = export_unique(self.dst, groups, images, self.naming())
            self.status.setText(tr("done_status", n=n, g=len(groups)))
            QTimer.singleShot(0, self._fit_now)
            QMessageBox.information(self, tr("done"), tr("done_box", n=n, dst=self.dst))
        except Exception as e:
            self.on_error(str(e))
        finally:
            self._busy(False)

    def _resolve(self, groups) -> bool:
        pick = RULES[self.rule.currentData()]
        for n, g in enumerate(groups, 1):
            if pick is not None:
                g.keep = [pick(g)]
            elif ReviewDialog(g, n, len(groups), self).exec() != QDialog.Accepted:
                return False
        return True

    def resizeEvent(self, e):
        # the interface scales together with the window
        px = int(max(11, min(getattr(self, "_px_cap", 30), 13 * self.width() / 560)))
        if px != getattr(self, "_px", None):
            self._px = self._cur_px = px
            self.setStyleSheet(theme.build_style(px, settings.get("theme", "dark")))
        super().resizeEvent(e)

    def closeEvent(self, e):
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.wait(3000)
        super().closeEvent(e)
