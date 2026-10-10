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
        "review_title": "Дубликаты {n} из {t}", "review_hint": "Отметьте все файлы, которые нужно сохранить (можно несколько): клик по фото или галочке. Наведите курсор на фото, чтобы увеличить.", "select_all": "Выбрать все", "select_none": "Снять выбор",
        "cancel": "Отмена", "keep": "Сохранить выбранные", "kb": "КБ",
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
        "names_group": "Имена файлов при копировании", "recursive": "Искать во вложенных папках",
        "nm_mode_keep": "Оставить имена как есть", "nm_mode_date": "Переименовать по дате",
        "nm_src_exif": "Дата съёмки (EXIF), если нет — дата файла", "nm_src_created": "Дата создания файла",
        "nm_src_modified": "Дата изменения файла",
        "nm_fmt_dash": "Дата и время: 2024-05-01_12-30-45", "nm_fmt_compact": "Дата и время: 20240501_123045",
        "nm_fmt_ts": "Timestamp (секунды): 1714566645", "nm_fmt_ts_ms": "Timestamp (миллисекунды): 1714566645000",
        "nm_fmt_custom": "Свой шаблон…", "nm_custom_hint": "Шаблон: %Y %m %d %H %M %S, {ts} — секунды, {ms} — миллисекунды",
        "nm_conf_counter": "При совпадении имён: добавить номер (_1, _2…)",
        "nm_conf_prefix": "При совпадении имён: добавить префикс — имя папки (затем номер)",
        "nm_example": "Пример: {name}", "nm_safe": "Файлы никогда не перезаписываются: при совпадении имён подбирается новое имя.",
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
        "review_title": "Duplicates {n} of {t}", "review_hint": "Tick every file you want to save (you can pick several): click a photo or its checkbox. Hover a photo to enlarge it.", "select_all": "Select all", "select_none": "Clear",
        "cancel": "Cancel", "keep": "Save selected", "kb": "KB",
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
        "names_group": "File names when copying", "recursive": "Search in subfolders",
        "nm_mode_keep": "Keep names as they are", "nm_mode_date": "Rename by date",
        "nm_src_exif": "Shooting date (EXIF), else file date", "nm_src_created": "File creation date",
        "nm_src_modified": "File modification date",
        "nm_fmt_dash": "Date and time: 2024-05-01_12-30-45", "nm_fmt_compact": "Date and time: 20240501_123045",
        "nm_fmt_ts": "Timestamp (seconds): 1714566645", "nm_fmt_ts_ms": "Timestamp (milliseconds): 1714566645000",
        "nm_fmt_custom": "Custom pattern…", "nm_custom_hint": "Pattern: %Y %m %d %H %M %S, {ts} = seconds, {ms} = milliseconds",
        "nm_conf_counter": "On name conflict: add a number (_1, _2…)",
        "nm_conf_prefix": "On name conflict: add a prefix — source folder name (then a number)",
        "nm_example": "Example: {name}", "nm_safe": "Files are never overwritten: on a name conflict a new name is chosen.",
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
