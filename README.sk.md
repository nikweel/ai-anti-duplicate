# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · **Slovenčina** · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** je bezplatná open source aplikácia, ktorá hľadá duplicitné **fotografie** (JPG, PNG, WebP) podľa **toho, čo je na zábere**, nie podľa veľkosti, dátumu či odtlačku. Používa umelú inteligenciu, takže spozná ten istý záber, aj keď bol zmenšený, znova skomprimovaný, mierne orezaný alebo otočený. Je určená len pre zbierky fotografií, nie pre dokumenty, videá či iné súbory.

> 🛡️ **Bezpečná už z princípu:** program iba *kopíruje* súbory. Nikdy nemaže, nepresúva ani neupravuje vaše originály.

![](docs/screenshots/main.png)

## Ako na to
1. Vyberte priečinok s fotografiami (zahrnuté sú všetky podpriečinky).
2. Vyberte priečinok, kam sa uložia jedinečné fotografie.
3. Zvoľte pravidlo pre duplikáty: najnovší, najväčší súbor, najvyššie rozlíšenie alebo ručný výber pre každú skupinu.
4. Kliknite na „Nájsť duplikáty a uložiť“. Fotografie bez duplikátov sa skopírujú bezo zmeny, z každej skupiny duplikátov iba tá (alebo tie), ktoré ste vybrali.

## Stiahnutie (inštalácia Pythonu nie je potrebná)
Stiahnite súbor pre svoj systém zo stránky [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| Systém | Súbor | Ako spustiť |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dvojklik a postupujte podľa inštalátora. |
| **Linux** | `….AppImage` / `….deb` | AppImage: pravé tlačidlo → Vlastnosti → Povoliť spúšťanie ako program, potom dvojklik; alebo `.deb`: dvojklik → Inštalovať. |
| **macOS** | `….dmg` | Otvorte `.dmg` a presuňte aplikáciu do Aplikácií. |

Pri prvom spustení vyberiete v Nastaveniach rozpoznávací model a program ho raz stiahne (je potrebný internet). Potom funguje úplne offline.

## Upozornenia systému pri prvom spustení (je to normálne)
Program je zadarmo a nie je podpísaný certifikátom (tie sú platené), preto vás systém môže varovať. Kód je otvorený a stiahnutý súbor overíte pomocou `SHA256SUMS.txt` z vydania.

- **Windows:** „Systém Windows chránil váš počítač“ → **Ďalšie informácie → Napriek tomu spustiť**.
- **macOS:** otvorte **Nastavenia systému → Súkromie a zabezpečenie**, posuňte sa nadol a kliknite vedľa aplikácie na **Napriek tomu otvoriť**.
- **Linux:** bez upozornení.

## Funkcie
- Porovnanie obsahu fotografií pomocou AI (otočenie, zmenšenie či prekomprimovanie neprekáža)
- Tri modely: ľahký, stredný a ťažký; zrýchlenie grafickou kartou
- Ručná kontrola: zaškrtnite viac fotografií na uloženie, prejdením myšou ich zväčšíte
- Názvy v cieľovom priečinku: pôvodné alebo podľa dátumu (EXIF, časová pečiatka), bez prepisovania
- Zahŕňa všetky podpriečinky
- 30 jazykov, tmavý a svetlý motív

## Autor

Licencia [MIT](LICENSE): zadarmo na akékoľvek použitie, aj komerčné.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
