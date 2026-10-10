# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · **Norsk** · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** er et gratis program med åpen kildekode som finner duplikater av **bilder** (JPG, PNG, WebP) ut fra **det som vises i bildet** — ikke filstørrelse, dato eller hash. Det bruker KI og kjenner derfor igjen samme opptak selv om det er forminsket, komprimert på nytt, beskåret litt eller rotert. Bare for bildesamlinger, ikke for dokumenter, videoer eller andre filer.

> 🛡️ **Trygt fra grunnen av:** programmet *kopierer* bare filer. Det sletter, flytter eller endrer aldri originalene dine.

![](docs/screenshots/main.png)

## Slik bruker du det
1. Velg mappen med bildene dine (alle undermapper tas med).
2. Velg mappen der de unike bildene skal lagres.
3. Velg regel for duplikater: nyeste, største fil, høyeste oppløsning eller manuelt valg for hver gruppe.
4. Klikk «Finn duplikater og lagre». Bilder uten duplikater kopieres som de er, og fra hver duplikatgruppe bare de du har valgt.

## Last ned (du trenger ikke installere Python)
Last ned filen for systemet ditt fra siden [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| System | Fil | Slik starter du |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dobbeltklikk og følg installasjonsveiviseren. |
| **Linux** | `….AppImage` / `….deb` | AppImage: høyreklikk → Egenskaper → Tillat kjøring som program, deretter dobbeltklikk; eller `.deb`: dobbeltklikk → Installer. |
| **macOS** | `….dmg` | Åpne `.dmg` og dra appen til Programmer. |

Ved første oppstart velger du gjenkjenningsmodell i Innstillinger, og programmet laster den ned én gang (internett kreves). Deretter fungerer alt uten nett.

## Systemvarsler ved første oppstart (helt normalt)
Programmet er gratis og ikke kodesignert (sertifikater koster penger), så systemet kan advare. Koden er åpen, og du kan kontrollere nedlastingen med `SHA256SUMS.txt` fra utgivelsen.

- **Windows:** «Windows har beskyttet PC-en din» → **Mer informasjon → Kjør likevel**.
- **macOS:** åpne **Systeminnstillinger → Personvern og sikkerhet**, rull ned og klikk **Åpne likevel** ved siden av appen.
- **Linux:** ingen varsler.

## Funksjoner
- KI-sammenligning av bildeinnhold (rotasjon, forminskning og ny komprimering spiller ingen rolle)
- Tre modeller: lett, middels og tung; akselerasjon med grafikkort
- Manuell gjennomgang: kryss av for flere bilder som skal lagres, hold musepekeren over for å forstørre
- Navn i målmappen: originale eller etter dato (EXIF, tidsstempel), overskriver aldri
- Alle undermapper tas med
- 30 språk, mørkt og lyst tema

## Skaper

[MIT](LICENSE)-lisens: gratis til all bruk, også kommersiell.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
