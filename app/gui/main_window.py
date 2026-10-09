from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QGuiApplication, QPixmap
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QDialog, QFileDialog, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QProgressBar, QSizePolicy,
    QPushButton, QRadioButton, QSlider, QVBoxLayout, QWidget,
)

from ..data.models import DuplicateGroup
from ..services.exporter import export_unique
from ..services.selection import RULES, pick_newest
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
        cap = QLabel(f"{img.path.name} — {px.width()}×{px.height()}, {img.size / 1024:.0f} КБ")
        cap.setAlignment(Qt.AlignCenter)
        lay.addWidget(pic, 1)
        lay.addWidget(cap)


class ReviewDialog(QDialog):
    """Дубли одного кадра: выбираем, какой файл оставить."""

    def __init__(self, group: DuplicateGroup, n: int, total: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Дубликаты {n} из {total}")
        self.group = group
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.resize(1000, 600)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Нажмите на картинку для увеличения. Выберите файл, который оставить."))
        row = QHBoxLayout()
        self.buttons = QButtonGroup(self)
        for i, img in enumerate(group.images):
            col = QVBoxLayout()
            pic = ScaledImage(img.path)
            pic.clicked.connect(lambda img=img: PreviewPopup(img, self).exec())
            rb = QRadioButton(f"{img.path.name}\n{img.size / 1024:.0f} КБ")
            self.buttons.addButton(rb, i)
            col.addWidget(pic, 1)
            col.addWidget(rb)
            row.addLayout(col, 1)
        lay.addLayout(row, 1)
        self.buttons.button(group.keep).setChecked(True)
        btns = QHBoxLayout()
        cancel, ok = QPushButton("Отмена"), QPushButton("Оставить выбранный")
        cancel.clicked.connect(self.reject)
        ok.clicked.connect(self._accept)
        ok.setDefault(True)
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
        self.model = None
        self.src: Path | None = None
        self.dst: Path | None = None
        self.worker = None

        w = QWidget()
        self.setCentralWidget(w)
        lay = QVBoxLayout(w)
        self.src_btn, self.src_lbl = self._picker(lay, "Папка с фотографиями", self.pick_src)
        self.dst_btn, self.dst_lbl = self._picker(lay, "Папка для уникальных", self.pick_dst)
        self.rule = QComboBox()
        self.rule.addItems(list(RULES))
        lay.addWidget(self.rule)
        lay.addWidget(QLabel("Чувствительность поиска:"))
        srow = QHBoxLayout()
        self.sens = QSlider(Qt.Horizontal)
        self.sens.setRange(0, 100)
        self.sens.setValue(33)
        self.sens.valueChanged.connect(self._sens_changed)
        srow.addWidget(QLabel("← Строго"))
        srow.addWidget(self.sens, 1)
        srow.addWidget(QLabel("Мягко →"))
        lay.addLayout(srow)
        self.sens_hint = QLabel()
        self.sens_hint.setWordWrap(True)
        lay.addWidget(self.sens_hint)
        self._sens_changed(33)
        self.start = QPushButton("Найти дубликаты и сохранить")
        self.start.setEnabled(False)
        self.start.clicked.connect(self.run)
        self.bar = QProgressBar()
        self.status = QLabel("Загрузка модели...")
        for x in (self.start, self.bar, self.status):
            lay.addWidget(x)

        self.worker = ModelWorker()
        self.worker.progress.connect(self.on_progress)
        self.worker.loaded.connect(self.on_model)
        self.worker.failed.connect(self.on_error)
        self.worker.start()

    @staticmethod
    def _picker(lay, text, slot):
        row = QHBoxLayout()
        btn = QPushButton(text)
        lbl = QLabel("не выбрана")
        btn.clicked.connect(slot)
        btn.setMinimumWidth(190)
        row.addWidget(btn)
        row.addWidget(lbl, 1)
        lay.addLayout(row)
        return btn, lbl

    def threshold(self) -> float:
        return 0.98 - self.sens.value() * 0.0018  # 0 -> 0.98 (строго), 100 -> 0.80 (мягко)

    def _sens_changed(self, v: int):
        if v < 25:
            t = "Строго: только практически одинаковые кадры (разный размер или сжатие). Риск пропустить дубли."
        elif v < 60:
            t = "Сбалансировано: одинаковые кадры, в том числе обрезанные или повёрнутые. Рекомендуется."
        else:
            t = "Мягко: ищет и просто похожие кадры (серия снимков одной сцены). Риск принять разные фото за дубли."
        self.sens_hint.setText(t)

    def _refresh(self):
        self.start.setEnabled(bool(self.model and self.src and self.dst))

    def pick_src(self):
        if d := QFileDialog.getExistingDirectory(self, "Папка с фотографиями"):
            self.src = Path(d)
            self.src_lbl.setText(d)
            self._refresh()

    def pick_dst(self):
        if d := QFileDialog.getExistingDirectory(self, "Папка для уникальных"):
            self.dst = Path(d)
            self.dst_lbl.setText(d)
            self._refresh()

    def on_progress(self, frac, msg):
        self.bar.setValue(int(frac * 100))
        self.status.setText(msg)

    def on_error(self, msg):
        self._busy(False)
        QMessageBox.critical(self, "Ошибка", f"{msg}\n\nПодробности: data/logs/app.log")

    def on_model(self, model):
        self.model = model
        self.status.setText("Готово. Выберите папки.")
        self._refresh()

    def _busy(self, busy: bool):
        for x in (self.src_btn, self.dst_btn, self.rule, self.sens, self.start):
            x.setEnabled(not busy)
        if not busy:
            self._refresh()

    def run(self):
        if self.src == self.dst:
            QMessageBox.warning(self, "Папки", "Выберите разные папки.")
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
                self.status.setText("Отменено.")
                return
            n = export_unique(self.dst, groups, images)
            self.status.setText(f"Готово: скопировано {n} файлов, найдено групп дублей: {len(groups)}")
            QMessageBox.information(self, "Готово", f"Скопировано {n} файлов в\n{self.dst}")
        except Exception as e:
            self.on_error(str(e))
        finally:
            self._busy(False)

    def _resolve(self, groups) -> bool:
        pick = RULES[self.rule.currentText()]
        for n, g in enumerate(groups, 1):
            g.keep = (pick or pick_newest)(g)
            if pick is None and ReviewDialog(g, n, len(groups), self).exec() != QDialog.Accepted:
                return False
        return True

    def resizeEvent(self, e):
        # интерфейс масштабируется вместе с окном
        px = int(max(13, min(30, 13 * self.width() / 560)))
        if px != getattr(self, "_px", None):
            self._px = px
            self.setStyleSheet(f"* {{ font-size: {px}px; }} QPushButton {{ padding: {px // 3}px {px // 2}px; }}")
        super().resizeEvent(e)

    def closeEvent(self, e):
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.wait(3000)
        super().closeEvent(e)
