# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · **Magyar** · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

A **Photo Duplicate Finder AI** ingyenes, nyílt forráskódú alkalmazás, amely az ismétlődő **fényképeket** (JPG, PNG, WebP + RAW) **a képen látható tartalom** alapján találja meg, nem a méret, a dátum vagy az ellenőrzőösszeg szerint. Mesterséges intelligenciát használ, ezért felismeri ugyanazt a felvételt akkor is, ha kicsinyítették, újratömörítették, kissé megvágták vagy elforgatták. Kizárólag fotógyűjteményekhez készült, dokumentumokhoz, videókhoz és más fájlokhoz nem.

> 🛡️ **Biztonságos már a tervezésnél:** a program csak *másol*. Soha nem töröl, nem helyez át és nem módosít semmit az eredeti fájlokon.

![](docs/screenshots/main.png)

## Használat
1. Válassza ki a fényképeket tartalmazó mappát (az almappákat is bevonja).
2. Válassza ki a mappát, ahová az egyedi fényképek kerülnek.
3. Válasszon szabályt a duplikátumokhoz: legújabb, legnagyobb fájl, legnagyobb felbontás vagy kézi választás csoportonként.
4. Kattintson a „Duplikátumok keresése és mentés” gombra. A duplikátum nélküli fényképek változatlanul átmásolódnak, minden duplikátumcsoportból pedig csak az Ön által választott(ak).

## Letöltés (Python telepítése nem szükséges)
Töltse le a rendszeréhez való fájlt a [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest) oldalról:

| Rendszer | Fájl | Indítás |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dupla kattintás, majd kövesse a telepítőt. |
| **Linux** | `….AppImage` / `….deb` | AppImage: jobb gomb → Tulajdonságok → Futtatás programként engedélyezése, majd dupla kattintás; vagy `.deb`: dupla kattintás → Telepítés. |
| **macOS** | `….dmg` | Nyissa meg a `.dmg` fájlt, és húzza az alkalmazást az Alkalmazások mappába. |

Az első indításkor a Beállításokban kiválasztja a felismerési modellt, a program pedig egyszer letölti (internet szükséges). Utána teljesen offline működik.

## Rendszerfigyelmeztetések az első indításkor (ez normális)
A program ingyenes, és nincs tanúsítvánnyal aláírva (a tanúsítvány fizetős), ezért a rendszer figyelmeztethet. A kód nyílt, a letöltést a kiadás `SHA256SUMS.txt` fájljával ellenőrizheti.

- **Windows:** „A Windows megvédte a számítógépét” → **További információ → Futtatás mégis**.
- **macOS:** nyissa meg a **Rendszerbeállítások → Adatvédelem és biztonság** részt, görgessen lefelé, és kattintson az alkalmazás melletti **Megnyitás mindenképp** gombra.
- **Linux:** nincs figyelmeztetés.
- Fényképezőgépek RAW fájljainak támogatása (CR2, NEF, ARW, DNG stb.) — az eredeti sosem módosul

## Funkciók
- A fényképek tartalmának összehasonlítása MI-vel (az elforgatás, kicsinyítés, újratömörítés nem zavar)
- Három modell: könnyű, közepes és nehéz; gyorsítás videokártyával
- Kézi ellenőrzés: több fényképet is bejelölhet mentésre, az egeret fölé víve nagyíthat
- Nevek a célmappában: eredeti vagy dátum szerinti (EXIF, időbélyeg), soha nem ír felül
- Az összes almappát bevonja
- 30 nyelv, sötét és világos téma

## Szerző

[MIT](LICENSE) licenc: ingyenes bármilyen célra, kereskedelmire is.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
