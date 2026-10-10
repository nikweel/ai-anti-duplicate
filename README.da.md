# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · **Dansk** · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** er et gratis program med åben kildekode, der finder dubletter af **fotos** (JPG, PNG, WebP) ud fra **det, der er på billedet** — ikke filstørrelse, dato eller hash. Det bruger AI og genkender derfor samme optagelse, selv om den er formindsket, genkomprimeret, beskåret en smule eller roteret. Kun til fotosamlinger, ikke til dokumenter, videoer eller andre filer.

> 🛡️ **Sikkert fra start:** programmet *kopierer* kun filer. Det sletter, flytter eller ændrer aldrig dine originaler.

![](docs/screenshots/main.png)

## Sådan bruges det
1. Vælg mappen med dine fotos (alle undermapper er med).
2. Vælg mappen, hvor de unikke fotos skal gemmes.
3. Vælg regel for dubletter: nyeste, største fil, højeste opløsning eller manuelt valg for hver gruppe.
4. Klik på »Find dubletter og gem«. Fotos uden dubletter kopieres uændret, og fra hver dubletgruppe kun dem, du har valgt.

## Hent (du behøver ikke installere Python)
Hent filen til dit system fra siden [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| System | Fil | Sådan starter du |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dobbeltklik og følg installationsguiden. |
| **Linux** | `….AppImage` / `….deb` | AppImage: højreklik → Egenskaber → Tillad kørsel som program, derefter dobbeltklik; eller `.deb`: dobbeltklik → Installer. |
| **macOS** | `….dmg` | Åbn `.dmg` og træk appen til Programmer. |

Ved første start vælger du genkendelsesmodel i Indstillinger, og programmet henter den én gang (internet påkrævet). Derefter virker alt offline.

## Systemadvarsler ved første start (helt normalt)
Programmet er gratis og ikke kodesigneret (certifikater koster penge), så systemet kan advare. Koden er åben, og du kan kontrollere downloaden med `SHA256SUMS.txt` fra udgivelsen.

- **Windows:** »Windows har beskyttet din pc« → **Flere oplysninger → Kør alligevel**.
- **macOS:** åbn **Systemindstillinger → Anonymitet og sikkerhed**, rul ned og klik på **Åbn alligevel** ved siden af appen.
- **Linux:** ingen advarsler.

## Funktioner
- AI-sammenligning af fotoindhold (rotation, formindskelse og genkomprimering gør ikke noget)
- Tre modeller: let, mellem og tung; acceleration med grafikkort
- Manuel gennemgang: sæt kryds ved flere fotos, der skal gemmes, hold musen over for at forstørre
- Navne i målmappen: originale eller efter dato (EXIF, tidsstempel), overskriver aldrig
- Alle undermapper er med
- 30 sprog, mørkt og lyst tema

## Skaber

[MIT](LICENSE)-licens: gratis til al brug, også kommerciel.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
