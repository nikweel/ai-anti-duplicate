# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · **Čeština** · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** je bezplatná open source aplikace, která hledá duplicitní **fotografie** (JPG, PNG, WebP + RAW) podle **toho, co je na snímku**, nikoli podle velikosti, data či otisku. Používá umělou inteligenci, takže pozná stejný záběr, i když byl zmenšen, znovu komprimován, mírně oříznut nebo otočen. Je určena jen pro sbírky fotografií, ne pro dokumenty, videa či jiné soubory.

> 🛡️ **Bezpečná už z principu:** program pouze *kopíruje* soubory. Nikdy nemaže, nepřesouvá ani neupravuje vaše originály.

![](docs/screenshots/main.png)

## Jak na to
1. Vyberte složku s fotografiemi (zahrnuty jsou všechny podsložky).
2. Vyberte složku, kam se uloží jedinečné fotografie.
3. Zvolte pravidlo pro duplikáty: nejnovější, největší soubor, nejvyšší rozlišení nebo ruční výběr pro každou skupinu.
4. Klikněte na „Najít duplikáty a uložit“. Fotografie bez duplikátů se zkopírují beze změny, z každé skupiny duplikátů jen ta (nebo ty), které jste vybrali.

## Stažení (instalace Pythonu není potřeba)
Stáhněte soubor pro svůj systém ze stránky [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| Systém | Soubor | Jak spustit |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dvojklik a postupujte podle instalátoru. |
| **Linux** | `….AppImage` / `….deb` | AppImage: pravé tlačítko → Vlastnosti → Povolit spouštění jako program, pak dvojklik; nebo `.deb`: dvojklik → Instalovat. |
| **macOS** | `….dmg` | Otevřete `.dmg` a přetáhněte aplikaci do Aplikací. |

Při prvním spuštění vyberete v Nastavení rozpoznávací model a program jej jednou stáhne (je potřeba internet). Poté funguje zcela offline.

## Upozornění systému při prvním spuštění (je to normální)
Program je zdarma a není podepsán certifikátem (ty jsou placené), proto vás systém může varovat. Kód je otevřený a stažený soubor ověříte pomocí `SHA256SUMS.txt` z vydání.

- **Windows:** „Systém Windows ochránil váš počítač“ → **Další informace → Přesto spustit**.
- **macOS:** otevřete **Nastavení systému → Soukromí a zabezpečení**, sjeďte dolů a klikněte vedle aplikace na **Přesto otevřít**.
- **Linux:** bez upozornění.
- Podpora RAW souborů fotoaparátů (CR2, NEF, ARW, DNG a další) — originál se nemění

## Funkce
- Porovnání obsahu fotografií pomocí AI (otočení, zmenšení či překomprimování nevadí)
- Tři modely: lehký, střední a těžký; zrychlení grafickou kartou
- Ruční kontrola: zaškrtněte několik fotografií k uložení, najetím je zvětšíte
- Názvy v cílové složce: původní nebo podle data (EXIF, časové razítko), bez přepisování
- Zahrnuje všechny podsložky
- 30 jazyků, tmavý a světlý motiv

## Autor

Licence [MIT](LICENSE): zdarma pro jakékoli použití, i komerční.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
