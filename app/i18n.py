import locale

from .locales import LANGUAGES, RTL
from .utils import settings

LANGS = {code: name for code, (name, _) in LANGUAGES.items()}
_lang = "en"


def _system_lang() -> str:
    try:
        code = (locale.getlocale()[0] or "").lower()
    except Exception:
        code = ""
    for prefix, lang in (("russian", "ru"), ("chinese", "zh"), ("spanish", "es"), ("portuguese", "pt"),
                         ("french", "fr"), ("german", "de"), ("japanese", "ja"), ("arabic", "ar"),
                         ("indonesian", "id"), ("turkish", "tr"), ("hindi", "hi"), ("english", "en")):
        if code.startswith(prefix):
            return lang
    return code[:2] if code[:2] in LANGUAGES else "en"


def init() -> None:
    global _lang
    saved = settings.get("lang")
    _lang = saved if saved in LANGUAGES else _system_lang()


def get_lang() -> str:
    return _lang


def is_rtl() -> bool:
    return _lang in RTL


def set_lang(lang: str) -> None:
    global _lang
    if lang in LANGUAGES:
        _lang = lang
        settings.put("lang", lang)


def tr(key: str, **kw) -> str:
    s = LANGUAGES[_lang][1].get(key) or LANGUAGES["en"][1][key]  # нет перевода -> английский
    return s.format(**kw) if kw else s
