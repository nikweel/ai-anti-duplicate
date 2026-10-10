import re

from app.locales import LANGUAGES

EN = LANGUAGES["en"][1]
FIELD = re.compile(r"\{(\w+)\}")


def test_every_language_has_every_key():
    for code, (_, t) in LANGUAGES.items():
        assert set(t) == set(EN), (code, set(EN) ^ set(t))


def test_placeholders_match_english():
    for code, (_, t) in LANGUAGES.items():
        for k, v in t.items():
            assert set(FIELD.findall(v)) == set(FIELD.findall(EN[k])), (code, k)


def test_format_works_for_all():
    args = dict(n=1, t=2, g=3, dst="x", d=4, p=5, mb=6, dev="CPU", name="a", e="err", ts="", ms="")
    for code, (_, t) in LANGUAGES.items():
        for k, v in t.items():
            if k != "nm_custom_hint":  # там {ts}/{ms} — буквальный текст, не подстановка
                v.format(**args)
