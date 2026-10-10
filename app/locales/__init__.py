from . import (ar, bg, cs, da, de, el, en, es, fi, fr, hi, hr, hu, id, it, ja, ko, lt, nb, nl, pl, pt, ro, ru, sk, sv,
               tr, uk, zh, zh_TW)

# код -> (название на самом языке, название по-английски, словарь строк)
_ALL = {
    "ar": ("العربية", "Arabic", ar.T), "bg": ("Български", "Bulgarian", bg.T), "zh": ("中文（简体）", "Chinese (Simplified)", zh.T),
    "zh_TW": ("繁體中文", "Chinese (Traditional)", zh_TW.T), "hr": ("Hrvatski", "Croatian", hr.T), "cs": ("Čeština", "Czech", cs.T),
    "da": ("Dansk", "Danish", da.T), "nl": ("Nederlands", "Dutch", nl.T), "en": ("English", "English", en.T),
    "fi": ("Suomi", "Finnish", fi.T), "fr": ("Français", "French", fr.T), "de": ("Deutsch", "German", de.T),
    "el": ("Ελληνικά", "Greek", el.T), "hi": ("हिन्दी", "Hindi", hi.T), "hu": ("Magyar", "Hungarian", hu.T),
    "id": ("Bahasa Indonesia", "Indonesian", id.T), "it": ("Italiano", "Italian", it.T), "ja": ("日本語", "Japanese", ja.T),
    "ko": ("한국어", "Korean", ko.T), "lt": ("Lietuvių", "Lithuanian", lt.T), "nb": ("Norsk", "Norwegian", nb.T),
    "pl": ("Polski", "Polish", pl.T), "pt": ("Português", "Portuguese", pt.T), "ro": ("Română", "Romanian", ro.T),
    "ru": ("Русский", "Russian", ru.T), "sk": ("Slovenčina", "Slovak", sk.T), "es": ("Español", "Spanish", es.T),
    "sv": ("Svenska", "Swedish", sv.T), "tr": ("Türkçe", "Turkish", tr.T), "uk": ("Українська", "Ukrainian", uk.T),
}
# список для выбора: по алфавиту (по английскому названию), подпись — «на самом языке (по-английски)»
LANGUAGES = {c: v for c, v in sorted(_ALL.items(), key=lambda kv: kv[1][1].lower())}
LABELS = {c: (n if n == e else f"{n} ({e})") for c, (n, e, _) in LANGUAGES.items()}
STRINGS = {c: v[2] for c, v in LANGUAGES.items()}
RTL = {"ar"}
