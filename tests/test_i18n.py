import re

from app.i18n import LANGS, detect_lang
from app.locales import LANGUAGES, STRINGS

EN = STRINGS["en"]
FIELD = re.compile(r"\{(\w+)\}")


def test_every_language_has_every_key():
    for code, t in STRINGS.items():
        assert set(t) == set(EN), (code, set(EN) ^ set(t))


def test_placeholders_match_english():
    for code, t in STRINGS.items():
        for k, v in t.items():
            assert set(FIELD.findall(v)) == set(FIELD.findall(EN[k])), (code, k)


def test_format_works_for_all():
    args = dict(m=3, n=1, t=2, g=3, dst="x", d=4, p=5, mb=6, dev="CPU", name="a", e="err", ts="", ms="")
    for code, t in STRINGS.items():
        for k, v in t.items():
            if k != "nm_custom_hint":  # там {ts}/{ms} — буквальный текст, не подстановка
                v.format(**args)


def test_thirty_languages_sorted_alphabetically_by_english_name():
    assert len(LANGS) == 30
    english = [e for (_, e, _) in LANGUAGES.values()]
    assert english == sorted(english, key=str.lower)
    for must in ("zh", "zh_TW", "ja", "ko", "de", "fr", "it", "pl", "uk", "nl"):
        assert must in LANGS


def test_system_language_detection():
    cases = {"ru_RU": "ru", "Russian_Russia": "ru", "de_DE": "de", "zh_CN": "zh", "zh_TW": "zh_TW",
             "Chinese (Traditional)_Taiwan": "zh_TW", "Chinese (Simplified)_China": "zh", "ja_JP": "ja", "ko_KR": "ko",
             "nb_NO": "nb", "no_NO": "nb", "nn_NO": "nb", "pt_BR": "pt", "it_IT": "it", "uk_UA": "uk", "sv_SE": "sv",
             "Greek_Greece": "el", "xx_YY": "en", "": "en"}
    for code, lang in cases.items():
        assert detect_lang(code) == lang, code
