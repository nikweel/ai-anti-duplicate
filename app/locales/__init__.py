from . import ar, de, en, es, fr, hi, id, ja, pt, ru, tr, zh

# код -> (название на самом языке, словарь строк); порядок = порядок в списке выбора
LANGUAGES = {
    "en": ("English", en.T), "ru": ("Русский", ru.T), "zh": ("中文（简体）", zh.T), "es": ("Español", es.T),
    "hi": ("हिन्दी", hi.T), "pt": ("Português", pt.T), "fr": ("Français", fr.T), "de": ("Deutsch", de.T),
    "ja": ("日本語", ja.T), "ar": ("العربية", ar.T), "id": ("Bahasa Indonesia", id.T), "tr": ("Türkçe", tr.T),
}
RTL = {"ar"}
