import locale

from .utils import settings

TEXTS = {
    "ru": {
        "src_btn": "Папка с фотографиями", "dst_btn": "Папка для уникальных", "not_chosen": "не выбрана",
        "rule_newest": "Оставлять самый новый", "rule_largest": "Оставлять самый тяжёлый (вес файла)",
        "rule_resolution": "Оставлять самый большой по разрешению", "rule_manual": "Выбирать вручную для каждого кадра",
        "sens": "Чувствительность поиска:", "strict": "← Строго", "soft": "Мягко →",
        "sens_low": "Строго: только практически одинаковые кадры (разный размер или сжатие). Риск пропустить дубли.",
        "sens_mid": "Сбалансировано: одинаковые кадры, в том числе обрезанные или повёрнутые. Рекомендуется.",
        "sens_high": "Мягко: ищет и просто похожие кадры (серия снимков одной сцены). Риск принять разные фото за дубли.",
        "start": "Найти дубликаты и сохранить", "loading_model": "Загрузка модели...", "ready": "Готово. Выберите папки.",
        "error": "Ошибка", "details": "Подробности: data/logs/app.log", "folders": "Папки", "diff_folders": "Выберите разные папки.",
        "cancelled": "Отменено.", "done": "Готово", "done_status": "Готово: скопировано {n} файлов, найдено групп дублей: {g}",
        "done_box": "Скопировано {n} файлов в\n{dst}", "language": "Язык",
        "review_title": "Дубликаты {n} из {t}", "review_hint": "Нажмите на картинку для увеличения. Выберите файл, который оставить.",
        "cancel": "Отмена", "keep": "Оставить выбранный", "kb": "КБ",
        "scanning": "Поиск файлов...", "analysis": "Анализ: {d}/{t}", "grouping": "Группировка...",
        "model_check": "Проверка модели...", "model_dl": "Загрузка модели: {p}% ({d}/{t} МБ)", "model_mem": "Загрузка модели в память...",
        "model_label": "Модель:", "model_fast": "Быстрая (168 МБ, подходит для процессора)",
        "model_accurate": "Точная (580 МБ, лучше с видеокартой)", "device_label": "Устройство:",
        "device_auto": "Авто", "device_cpu": "Процессор", "device_gpu": "Видеокарта",
        "ready_dev": "Готово. Устройство: {dev}. Выберите папки.",
        "settings": "Настройки", "settings_title": "Настройки", "theme_label": "Тема:", "theme_dark": "Тёмная",
        "theme_light": "Светлая", "theme_system": "Как в системе", "model_group": "Модель распознавания",
        "model_fast_t": "Быстрая", "model_accurate_t": "Точная",
        "model_fast_d": "{mb} МБ. Хорошо работает на процессоре.",
        "model_accurate_d": "{mb} МБ. Лучше различает похожие кадры, рекомендуется с видеокартой.",
        "model_have": "уже скачана", "model_need": "будет скачано {mb} МБ", "ok": "Применить", "close": "Закрыть",
        "choose_model_msg": "Модель распознавания ещё не скачана.\n\nВыберите модель в настройках: после выбора начнётся загрузка.",
        "choose_model_status": "Выберите модель в настройках (⚙).",
        "model_fail": "Не удалось загрузить модель (проверьте интернет): {e}",
    },
    "en": {
        "src_btn": "Photos folder", "dst_btn": "Folder for unique photos", "not_chosen": "not selected",
        "rule_newest": "Keep the newest", "rule_largest": "Keep the largest (file size)",
        "rule_resolution": "Keep the highest resolution", "rule_manual": "Choose manually for each shot",
        "sens": "Search sensitivity:", "strict": "← Strict", "soft": "Soft →",
        "sens_low": "Strict: only practically identical shots (different size or compression). May miss some duplicates.",
        "sens_mid": "Balanced: identical shots, including cropped or rotated ones. Recommended.",
        "sens_high": "Soft: also finds merely similar shots (a burst of the same scene). May treat different photos as duplicates.",
        "start": "Find duplicates and save", "loading_model": "Loading model...", "ready": "Ready. Choose the folders.",
        "error": "Error", "details": "Details: data/logs/app.log", "folders": "Folders", "diff_folders": "Choose different folders.",
        "cancelled": "Cancelled.", "done": "Done", "done_status": "Done: {n} files copied, duplicate groups found: {g}",
        "done_box": "{n} files copied to\n{dst}", "language": "Language",
        "review_title": "Duplicates {n} of {t}", "review_hint": "Click a picture to enlarge it. Choose the file to keep.",
        "cancel": "Cancel", "keep": "Keep selected", "kb": "KB",
        "scanning": "Searching files...", "analysis": "Analysing: {d}/{t}", "grouping": "Grouping...",
        "model_check": "Checking model...", "model_dl": "Downloading model: {p}% ({d}/{t} MB)", "model_mem": "Loading model into memory...",
        "model_label": "Model:", "model_fast": "Fast (168 MB, good for CPU)",
        "model_accurate": "Accurate (580 MB, best with a GPU)", "device_label": "Device:",
        "device_auto": "Auto", "device_cpu": "CPU", "device_gpu": "GPU",
        "ready_dev": "Ready. Device: {dev}. Choose the folders.",
        "settings": "Settings", "settings_title": "Settings", "theme_label": "Theme:", "theme_dark": "Dark",
        "theme_light": "Light", "theme_system": "Follow system", "model_group": "Recognition model",
        "model_fast_t": "Fast", "model_accurate_t": "Accurate",
        "model_fast_d": "{mb} MB. Works well on a CPU.",
        "model_accurate_d": "{mb} MB. Tells similar shots apart better, recommended with a GPU.",
        "model_have": "already downloaded", "model_need": "{mb} MB will be downloaded", "ok": "Apply", "close": "Close",
        "choose_model_msg": "The recognition model has not been downloaded yet.\n\nChoose a model in Settings: the download starts after you choose.",
        "choose_model_status": "Choose a model in Settings (⚙).",
        "model_fail": "Could not load the model (check your internet connection): {e}",
    },
}
LANGS = {"ru": "Русский", "en": "English"}
_lang = "ru"


def _load() -> str:
    lang = settings.get("lang")
    if lang in TEXTS:
        return lang
    try:
        return "ru" if (locale.getlocale()[0] or "").lower().startswith(("ru", "russian")) else "en"
    except Exception:
        return "en"


def init() -> None:
    global _lang
    _lang = _load()


def get_lang() -> str:
    return _lang


def set_lang(lang: str) -> None:
    global _lang
    _lang = lang
    settings.put("lang", lang)


def tr(key: str, **kw) -> str:
    s = TEXTS[_lang][key]
    return s.format(**kw) if kw else s
