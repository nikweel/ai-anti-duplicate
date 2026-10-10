import locale

from .locales import LABELS, RTL, STRINGS
from .utils import settings

LANGS = dict(LABELS)  # код -> подпись для списка выбора (по алфавиту)
_lang = "en"

# названия языков в локалях Windows («Russian_Russia») и коды POSIX («ru_RU»); порядок важен: «chinese traditional» раньше «chinese»
_PREFIXES = (("zh_tw", "zh_TW"), ("zh_hk", "zh_TW"), ("zh_mo", "zh_TW"), ("chinese (traditional)", "zh_TW"),
             ("chinese", "zh"), ("zh", "zh"), ("russian", "ru"), ("spanish", "es"), ("portuguese", "pt"), ("french", "fr"),
             ("german", "de"), ("japanese", "ja"), ("arabic", "ar"), ("indonesian", "id"), ("turkish", "tr"),
             ("hindi", "hi"), ("english", "en"), ("italian", "it"), ("polish", "pl"), ("ukrainian", "uk"), ("dutch", "nl"),
             ("czech", "cs"), ("swedish", "sv"), ("greek", "el"), ("romanian", "ro"), ("hungarian", "hu"),
             ("bulgarian", "bg"), ("danish", "da"), ("finnish", "fi"), ("norwegian", "nb"), ("nb", "nb"), ("nn", "nb"),
             ("no_", "nb"), ("slovak", "sk"), ("croatian", "hr"), ("lithuanian", "lt"), ("korean", "ko"))


def detect_lang(code: str) -> str:
    code = (code or "").lower().replace("-", "_")
    for prefix, lang in _PREFIXES:
        if code.startswith(prefix):
            return lang
    return code[:2] if code[:2] in STRINGS else "en"


def _system_lang() -> str:
    try:
        return detect_lang(locale.getlocale()[0] or "")
    except Exception:
        return "en"


def init() -> None:
    global _lang
    saved = settings.get("lang")
    _lang = saved if saved in STRINGS else _system_lang()


def get_lang() -> str:
    return _lang


def is_rtl() -> bool:
    return _lang in RTL


def set_lang(lang: str) -> None:
    global _lang
    if lang in STRINGS:
        _lang = lang
        settings.put("lang", lang)


def tr(key: str, **kw) -> str:
    s = STRINGS[_lang].get(key) or STRINGS["en"][key]  # нет перевода -> английский
    return s.format(**kw) if kw else s
