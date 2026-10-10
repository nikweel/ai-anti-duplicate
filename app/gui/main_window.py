from pathlib import Path

import math
import time

from PySide6.QtCore import QDateTime, QLocale, QSize, QTimer, QUrl, Qt, Signal
from PySide6.QtGui import QDesktopServices, QGuiApplication, QIcon, QKeySequence, QShortcut, QImage, QImageReader, QPainter, QPalette, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication, QFrame, QGridLayout, QToolButton, QScrollArea, QComboBox, QDialog, QFileDialog, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QProgressBar, QSizePolicy,
    QPushButton, QRadioButton, QSlider, QVBoxLayout, QWidget,
)

from ..utils.paths import ICON
from ..data.models import DuplicateGroup
from ..services.exporter import export_unique
from ..services.naming import DATE_FORMATS, NamingOptions, format_date
from datetime import datetime
from PySide6.QtWidgets import QCheckBox, QGroupBox, QLineEdit
from .. import i18n
from ..core.imageio import image_size, is_raw, open_image
from ..core.model_manager import DEFAULT_SENSITIVITY, LEGACY_IDS, MODELS, is_downloaded, threshold_for
from ..utils import settings
from ..i18n import tr
from ..services.selection import RULES, pick_newest
from . import theme
from .settings_dialog import SettingsDialog
from .workers import ExportWorker, ModelWorker, ScanWorker


def load_pixmap(path, max_side: int) -> QPixmap:
    """Картинка для показа (в том числе RAW), уже уменьшенная; с учётом EXIF-поворота."""
    try:
        if not is_raw(path):
            r = QImageReader(str(path))
            r.setAutoTransform(True)
            size = r.size()
            if size.isValid() and max(size.width(), size.height()) > max_side:
                size.scale(max_side, max_side, Qt.KeepAspectRatio)
                r.setScaledSize(size)
            return QPixmap.fromImage(r.read())
        im = open_image(path)
        im.thumbnail((max_side, max_side))
        data = im.tobytes("raw", "RGB")
        return QPixmap.fromImage(QImage(data, im.width, im.height, im.width * 3, QImage.Format_RGB888).copy())
    except Exception:
        return QPixmap()


def _badges(group) -> list[list[str]]:
    """Подсказки к выбору: какой файл самый новый / самый тяжёлый / с самым большим разрешением."""
    from ..core.imageio import image_size

    imgs = group.images
    pix = []
    for im in imgs:
        try:
            w, h = image_size(im.path)
            pix.append(w * h)
        except Exception:
            pix.append(0)
    out = [[] for _ in imgs]
    for key, values in (("badge_newest", [i.mtime for i in imgs]), ("badge_largest", [i.size for i in imgs]),
                        ("badge_hires", pix)):
        top = max(values)
        winners = [k for k, v in enumerate(values) if v == top]
        if len(winners) == 1 and len(set(values)) > 1:
            out[winners[0]].append(key)
    return out


def _dims(path) -> str:
    """Реальное разрешение файла (а не размер миниатюры)."""
    try:
        w, h = image_size(path)
        return f"{w}×{h}"
    except Exception:
        return "?"


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
        self.cap.setText(f"{img.path.name} — {_dims(img.path)}, {img.size / 1024:.0f} {tr('kb')}")
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


class AutoHideLabel(QLabel):
    """Надпись, которая не занимает места, когда пуста."""

    def setText(self, text: str) -> None:
        super().setText(text)
        self.setVisible(bool(text))


def repolish(w: QWidget) -> None:
    w.style().unpolish(w)
    w.style().polish(w)


class PathField(QLineEdit):
    """Поле выбранной папки: клик = «Обзор», можно перетащить папку из файлового менеджера."""

    clicked = Signal()
    dropped = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("path")
        self.setReadOnly(True)
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setProperty("hasValue", False)
        self.setProperty("dropActive", False)

    def set_path(self, text: str) -> None:
        self.setText(text)
        self.setToolTip(text)
        self.setProperty("hasValue", bool(text))
        repolish(self)

    def _dir_from(self, e):
        for u in e.mimeData().urls():
            if u.isLocalFile() and Path(u.toLocalFile()).is_dir():
                return u.toLocalFile()
        return None

    def dragEnterEvent(self, e):
        if self._dir_from(e):
            e.acceptProposedAction()
            self.setProperty("dropActive", True)
            repolish(self)

    def dragLeaveEvent(self, e):
        self.setProperty("dropActive", False)
        repolish(self)

    def dropEvent(self, e):
        self.setProperty("dropActive", False)
        repolish(self)
        if d := self._dir_from(e):
            self.dropped.emit(d)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()


class Card(QFrame):
    """Смысловая группа элементов с заголовком."""

    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(16, 14, 16, 16)
        self.body.setSpacing(10)
        self.title = QLabel()
        self.title.setObjectName("cardTitle")
        self.body.addWidget(self.title)


class Disclosure(QWidget):
    """Сворачиваемый блок «Дополнительно»: редкие настройки не загромождают главное окно."""

    toggled = Signal(bool)

    def __init__(self, opened: bool = False):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.btn = QToolButton()
        self.btn.setObjectName("disclosure")
        self.btn.setCheckable(True)
        self.btn.setChecked(opened)
        self.btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.content = QWidget()
        self.inner = QVBoxLayout(self.content)
        self.inner.setContentsMargins(0, 4, 0, 0)
        self.inner.setSpacing(10)
        lay.addWidget(self.btn)
        lay.addWidget(self.content)
        self.btn.toggled.connect(self._on)
        self._on(opened)

    def _on(self, opened: bool):
        self.btn.setArrowType(Qt.DownArrow if opened else Qt.RightArrow)
        self.content.setVisible(opened)
        self.toggled.emit(opened)


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
        badges = _badges(group)
        self.boxes: list[QCheckBox] = []
        self.pics: list[ScaledImage] = []
        for i, img in enumerate(group.images):
            pic = ScaledImage(img)
            when = QLocale().toString(QDateTime.fromSecsSinceEpoch(int(img.mtime)), QLocale.ShortFormat)
            cb = QCheckBox(f"{img.path.name}\n{img.size / 1024:.0f} {tr('kb')} · {_dims(img.path)}\n{when}")
            cb.toggled.connect(pic.set_selected)
            cb.toggled.connect(self._update_ok)
            pic.toggled.connect(cb.toggle)
            self.boxes.append(cb)
            self.pics.append(pic)
            col = QVBoxLayout()
            col.addWidget(pic, 1)
            col.addWidget(cb)
            if badges[i]:
                tag = QLabel("★ " + " · ".join(tr(b) for b in badges[i]))
                tag.setObjectName("badge")
                col.addWidget(tag)
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
        self.ok.setDefault(True)
        self.ok.setEnabled(False)
        QShortcut(QKeySequence("Ctrl+A"), self, activated=lambda: [b.setChecked(True) for b in self.boxes])
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
        self.setWindowTitle("Photo Duplicate Finder AI")
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
        lay.setContentsMargins(20, 16, 20, 18)
        lay.setSpacing(14)

        # --- шапка
        top = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(QIcon(str(ICON)).pixmap(30, 30))
        title = QLabel("Photo Duplicate Finder AI")
        title.setObjectName("appTitle")
        self.settings_btn = QPushButton()
        self.settings_btn.clicked.connect(self.open_settings)
        self.settings_btn.setShortcut(QKeySequence("Ctrl+,"))
        top.addWidget(logo)
        top.addWidget(title)
        top.addStretch()
        top.addWidget(self.settings_btn)
        lay.addLayout(top)

        # --- карточка «Папки»
        self.card_folders = Card()
        self.src_lbl, self.src_field, self.src_btn = self._folder_row(self.card_folders.body, self.pick_src)
        self.dst_lbl, self.dst_field, self.dst_btn = self._folder_row(self.card_folders.body, self.pick_dst)
        self.src_field.dropped.connect(lambda d: self.set_folder("src", d))
        self.dst_field.dropped.connect(lambda d: self.set_folder("dst", d))
        lay.addWidget(self.card_folders)

        # --- карточка «Параметры поиска»
        self.card_options = Card()
        o = self.card_options.body
        self.rule_lbl = QLabel()
        self.rule = compact(QComboBox())
        for rid in RULES:
            self.rule.addItem("", rid)
        o.addWidget(self.rule_lbl)
        o.addWidget(self.rule)
        self.sens_title = QLabel()
        o.addWidget(self.sens_title)
        srow = QHBoxLayout()
        self.sens = QSlider(Qt.Horizontal)
        self.sens.setRange(0, 100)
        self.sens.setValue(DEFAULT_SENSITIVITY)
        self.sens.valueChanged.connect(self._sens_changed)
        self.strict_lbl, self.soft_lbl = QLabel(), QLabel()
        srow.addWidget(self.strict_lbl)
        srow.addWidget(self.sens, 1)
        srow.addWidget(self.soft_lbl)
        o.addLayout(srow)
        self.sens_hint = QLabel()
        self.sens_hint.setObjectName("muted")
        self.sens_hint.setWordWrap(True)
        o.addWidget(self.sens_hint)
        self.more = Disclosure(bool(settings.get("more_open", False)))
        self.more.toggled.connect(self._more_toggled)
        self._build_names_box(self.more.inner)
        self.open_done = QCheckBox()
        self.open_done.setChecked(bool(settings.get("open_when_done", True)))
        self.open_done.toggled.connect(lambda v: settings.put("open_when_done", v))
        self.more.inner.addWidget(self.open_done)
        o.addWidget(self.more)
        lay.addWidget(self.card_options)

        # --- запуск и ход работы
        self.start = QPushButton()
        self.start.setObjectName("primary")
        self.start.setMinimumHeight(46)
        self.start.setEnabled(False)
        self.start.setShortcut(QKeySequence("Ctrl+Return"))
        self.start.clicked.connect(self.run)
        lay.addWidget(self.start)
        self.hint = AutoHideLabel()
        self.hint.setObjectName("muted")
        self.hint.setAlignment(Qt.AlignCenter)
        self.hint.setWordWrap(True)
        lay.addWidget(self.hint)
        self.bar = QProgressBar()
        self.bar.hide()
        self.pause_btn, self.cancel_btn = QPushButton(), QPushButton()
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.cancel_btn.clicked.connect(self.cancel_work)
        self.pause_btn.hide()
        self.cancel_btn.hide()
        self.cancel_btn.setShortcut(QKeySequence("Esc"))
        prog = QHBoxLayout()
        prog.addWidget(self.bar, 1)
        prog.addWidget(self.pause_btn)
        prog.addWidget(self.cancel_btn)
        lay.addLayout(prog)
        self.status = AutoHideLabel()
        self.status.setWordWrap(True)
        lay.addWidget(self.status)
        sumrow = QHBoxLayout()
        self.summary = QLabel()
        self.summary.setObjectName("summary")
        self.summary.setWordWrap(True)
        self.open_btn = QPushButton()
        self.open_btn.clicked.connect(self.open_destination)
        sumrow.addWidget(self.summary, 1)
        sumrow.addWidget(self.open_btn)
        self.summary_box = QWidget()
        self.summary_box.setLayout(sumrow)
        sumrow.setContentsMargins(0, 0, 0, 0)
        self.summary_box.hide()
        lay.addWidget(self.summary_box)
        lay.addStretch()

        # --- горячие клавиши
        QShortcut(QKeySequence("Ctrl+O"), self, activated=self.pick_src)
        QShortcut(QKeySequence("Ctrl+Shift+O"), self, activated=self.pick_dst)
        self._t0 = None
        self._restore_folders()
        self.retranslate()
        self._fit_to_content()

        QTimer.singleShot(0, self.start_up)

    def _folder_row(self, lay, slot):
        label = QLabel()
        field = PathField()
        btn = QPushButton()
        field.clicked.connect(slot)
        btn.clicked.connect(slot)
        row = QHBoxLayout()
        row.addWidget(field, 1)
        row.addWidget(btn)
        lay.addWidget(label)
        lay.addLayout(row)
        return label, field, btn

    def _more_toggled(self, opened: bool):
        settings.put("more_open", opened)
        QTimer.singleShot(0, self._fit_now)

    def _restore_folders(self):
        for key in ("src", "dst"):
            d = settings.get("last_" + key)
            if d and Path(d).is_dir():
                setattr(self, key, Path(d))

    def set_folder(self, which: str, d: str):
        setattr(self, which, Path(d))
        settings.put("last_" + which, d)
        self.retranslate_paths()
        self._refresh()

    def retranslate_paths(self):
        for field, path in ((self.src_field, self.src), (self.dst_field, self.dst)):
            field.set_path(str(path) if path else "")
            field.setPlaceholderText(tr("not_chosen"))

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
        if need_h <= 0 and need_w <= 0 and step < 3:  # лишнее место внизу убираем
            spare = sa.viewport().height() - sa.widget().sizeHint().height()
            if spare > 12:
                self.resize(self.width(), max(320, self.height() - spare + 4))
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
        QMessageBox.information(self, "Photo Duplicate Finder AI", tr("choose_model_msg"))
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
        self.open_done.setText(tr("open_when_done"))
        self.pause_btn.setText(tr("resume") if self._is_paused() else tr("pause"))
        self.cancel_btn.setText(tr("cancel"))
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
        self.card_folders.title.setText(tr("folders"))
        self.card_options.title.setText(tr("options"))
        self.src_lbl.setText(tr("src_btn"))
        self.dst_lbl.setText(tr("dst_btn"))
        self.src_btn.setText(tr("browse"))
        self.dst_btn.setText(tr("browse"))
        self.src_btn.setToolTip("Ctrl+O")
        self.dst_btn.setToolTip("Ctrl+Shift+O")
        self.more.btn.setText(tr("more_options"))
        self.open_btn.setText(tr("open_folder"))
        self.retranslate_paths()
        self._update_hint()
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
        self._update_hint()

    def _update_hint(self):
        """Объясняем, почему кнопка запуска недоступна (а не просто серая кнопка)."""
        busy = bool(self.worker and self.worker.isRunning())
        if self.start.isEnabled() or busy:
            text = ""
        elif self.model is None and not (self.src and self.dst):
            text = tr("need_folders")
        elif self.model is None:
            text = ""
        else:
            text = tr("need_folders")
        self.hint.setText(text)
        self.start.setToolTip(text or "Ctrl+Enter")

    def pick_src(self):
        start = str(self.src or Path.home())
        if d := QFileDialog.getExistingDirectory(self, tr("src_btn"), start):
            self.set_folder("src", d)

    def pick_dst(self):
        start = str(self.dst or self.src or Path.home())
        if d := QFileDialog.getExistingDirectory(self, tr("dst_btn"), start):
            self.set_folder("dst", d)

    def _eta(self, frac: float) -> str:
        if not self._t0 or frac < 0.03:
            return ""
        elapsed = time.time() - self._t0
        if elapsed < 4:
            return ""
        remaining = elapsed * (1 - frac) / frac
        return tr("eta_less") if remaining < 60 else tr("eta_min", m=math.ceil(remaining / 60))

    def on_progress(self, frac, msg):
        self._status_key = None
        self.bar.setValue(int(frac * 100))
        eta = self._eta(frac)
        self.status.setText(f"{msg} · {eta}" if eta else msg)

    def on_error(self, msg):
        self._busy(False)
        QMessageBox.critical(self, tr("error"), f"{msg}\n\n{tr('details')}")

    def on_model(self, model):
        self.model = model
        self._status_key = None
        self.status.setText(tr("ready_dev", dev=model.device_name))
        self._busy(False)
        QTimer.singleShot(0, self._fit_now)

    def _busy(self, busy: bool, controls: bool = False):
        for x in (self.src_btn, self.dst_btn, self.rule, self.sens, self.start, self.settings_btn, self.recursive,
                  self.names_box, self.open_done):
            x.setEnabled(not busy)
        self.bar.setVisible(busy)
        if busy:
            self.summary_box.hide()
        self.pause_btn.setVisible(busy and controls)
        self.cancel_btn.setVisible(busy and controls)
        self.pause_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        if not busy:
            self._refresh()
        QTimer.singleShot(0, self._fit_now)

    def _is_paused(self) -> bool:
        return bool(self.worker and getattr(self.worker, "paused", False) and self.worker.isRunning())

    def toggle_pause(self):
        w = self.worker
        if not w or not hasattr(w, "pause") or not w.isRunning():
            return
        if w.paused:
            w.resume()
            self.pause_btn.setText(tr("pause"))
        else:
            w.pause()
            self.pause_btn.setText(tr("resume"))
            self.status.setText(tr("paused"))

    def cancel_work(self):
        w = self.worker
        if w and hasattr(w, "cancel") and w.isRunning():
            self.status.setText(tr("stopping"))
            self.pause_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)
            w.cancel()

    def on_cancelled(self):
        self.status.setText(tr("cancelled"))
        self._busy(False)

    def run(self):
        if self.src == self.dst:
            QMessageBox.warning(self, tr("folders"), tr("diff_folders"))
            return
        self._t0 = time.time()
        self.bar.setValue(0)
        self._busy(True, controls=True)
        self.pause_btn.setText(tr("pause"))
        self.worker = ScanWorker(self.model, self.src, self.dst, self.threshold(), True, self.recursive.isChecked())
        self.worker.progress.connect(self.on_progress)
        self.worker.done.connect(self.on_done)
        self.worker.cancelled.connect(self.on_cancelled)
        self.worker.failed.connect(self.on_error)
        self.worker.start()

    def on_done(self, images, groups):
        """Анализ закончен: выбираем, что оставить из групп, затем копируем в отдельном потоке."""
        self._groups = groups
        self.pause_btn.hide()
        self.cancel_btn.hide()
        try:
            if groups and not self._resolve(groups):
                self.status.setText(tr("cancelled"))
                self._busy(False)
                return
        except Exception as e:
            self.on_error(str(e))
            return
        self._busy(True, controls=True)
        self.pause_btn.setText(tr("pause"))
        self.worker = ExportWorker(self.dst, groups, images, self.naming())
        self.worker.progress.connect(self.on_progress)
        self.worker.done.connect(self.on_export_done)
        self.worker.cancelled.connect(self.on_cancelled)
        self.worker.failed.connect(self.on_error)
        self.worker.start()

    def on_export_done(self, n: int):
        groups = getattr(self, "_groups", [])
        self._busy(False)
        self.status.setText("")
        self.summary.setText("✓ " + tr("done_status", n=n, g=len(groups)))
        self.summary_box.show()
        QTimer.singleShot(0, self._fit_now)
        if self.open_done.isChecked():
            self.open_destination()

    def open_destination(self):
        if self.dst:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.dst)))

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
            (self.worker.cancel if hasattr(self.worker, "cancel") else self.worker.requestInterruption)()
            self.worker.wait(3000)
        super().closeEvent(e)
