# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · **Svenska** · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** är ett gratis program med öppen källkod som hittar dubbletter av **foton** (JPG, PNG, WebP) utifrån **vad som syns i bilden**, inte filstorlek, datum eller hash. Det använder AI och känner därför igen samma bild även om den förminskats, komprimerats om, beskurits lite eller roterats. Endast för fotosamlingar, inte för dokument, videor eller andra filer.

> 🛡️ **Säkert redan från grunden:** programmet *kopierar* bara filer. Det raderar, flyttar eller ändrar aldrig dina original.

![](docs/screenshots/main.png)

## Så här gör du
1. Välj mappen med dina foton (alla undermappar ingår).
2. Välj mappen där de unika fotona ska sparas.
3. Välj regel för dubbletter: nyaste, största filen, högsta upplösning eller manuellt val för varje grupp.
4. Klicka på ”Hitta dubbletter och spara”. Foton utan dubbletter kopieras som de är, och från varje dubblettgrupp bara de du valt.

## Hämta (du behöver inte installera Python)
Hämta filen för ditt system från sidan [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| System | Fil | Så startar du |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dubbelklicka och följ installationsguiden. |
| **Linux** | `….AppImage` / `….deb` | AppImage: högerklicka → Egenskaper → Tillåt körning som program, sedan dubbelklick; eller `.deb`: dubbelklick → Installera. |
| **macOS** | `….dmg` | Öppna `.dmg` och dra appen till Program. |

Vid första start väljer du igenkänningsmodell i Inställningar och programmet hämtar den en gång (internet krävs). Därefter fungerar allt offline.

## Systemvarningar vid första start (helt normalt)
Programmet är gratis och inte kodsignerat (certifikat kostar pengar), så systemet kan varna. Koden är öppen och du kan kontrollera nedladdningen med `SHA256SUMS.txt` från releasen.

- **Windows:** ”Windows skyddade din dator” → **Mer information → Kör ändå**.
- **macOS:** öppna **Systeminställningar → Integritet och säkerhet**, scrolla ned och klicka på **Öppna ändå** bredvid appen.
- **Linux:** inga varningar.

## Funktioner
- AI-jämförelse av fotoinnehåll (rotering, förminskning eller omkomprimering spelar ingen roll)
- Tre modeller: lätt, medel och tung; acceleration med grafikkort
- Manuell granskning: kryssa i flera foton att spara, håll muspekaren över för att förstora
- Namn i målmappen: original eller efter datum (EXIF, tidsstämpel), skriver aldrig över
- Alla undermappar ingår
- 30 språk, mörkt och ljust tema

## Upphovsman

[MIT](LICENSE)-licens: gratis för allt bruk, även kommersiellt.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
