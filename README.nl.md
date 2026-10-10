# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · **Nederlands** · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** is een gratis open-sourceprogramma dat dubbele **foto's** (JPG, PNG, WebP) vindt op basis van **wat er op de afbeelding staat**, niet op grootte, datum of hash. Het gebruikt AI en herkent dus dezelfde opname ook als die verkleind, opnieuw gecomprimeerd, een beetje bijgesneden of gedraaid is. Alleen bedoeld voor fotocollecties, niet voor documenten, video's of andere bestanden.

> 🛡️ **Veilig door ontwerp:** het programma *kopieert* alleen bestanden. Het verwijdert, verplaatst of wijzigt je originelen nooit.

![](docs/screenshots/main.png)

## Zo gebruik je het
1. Kies de map met je foto's (alle submappen worden meegenomen).
2. Kies de map waarin de unieke foto's worden opgeslagen.
3. Kies de regel voor duplicaten: de nieuwste, het grootste bestand, de hoogste resolutie of per groep handmatig kiezen.
4. Klik op «Duplicaten zoeken en opslaan». Foto's zonder duplicaat worden ongewijzigd gekopieerd; uit elke duplicaatgroep alleen de foto('s) die jij kiest.

## Downloaden (Python installeren is niet nodig)
Download het bestand voor jouw systeem op de pagina [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| Systeem | Bestand | Starten |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dubbelklik en volg het installatieprogramma. |
| **Linux** | `….AppImage` / `….deb` | AppImage: rechtsklik → Eigenschappen → Uitvoeren als programma toestaan, dan dubbelklikken; of `.deb`: dubbelklik → Installeren. |
| **macOS** | `….dmg` | Open de `.dmg` en sleep de app naar Programma's. |

Bij de eerste start kies je in de Instellingen het herkenningsmodel en het programma downloadt het eenmalig (internet nodig). Daarna werkt alles offline.

## Systeemwaarschuwingen bij de eerste start (normaal)
Het programma is gratis en niet ondertekend met een certificaat (die kosten geld), dus je systeem kan waarschuwen. De code is open en je kunt de download controleren met `SHA256SUMS.txt` uit de release.

- **Windows:** «Windows heeft uw pc beveiligd» → **Meer informatie → Toch uitvoeren**.
- **macOS:** open **Systeeminstellingen → Privacy en beveiliging**, scrol omlaag en klik naast de app op **Toch openen**.
- **Linux:** geen waarschuwingen.

## Functies
- AI-vergelijking van foto-inhoud (draaien, verkleinen of opnieuw comprimeren maakt niet uit)
- Drie modellen: licht, gemiddeld en zwaar; versnelling met een videokaart
- Handmatige controle: vink meerdere foto's aan om te bewaren, ga erover om te vergroten
- Namen in de doelmap: origineel of op datum (EXIF, tijdstempel), nooit overschrijven
- Alle submappen inbegrepen
- 30 talen, donker en licht thema

## Auteur

[MIT](LICENSE)-licentie: gratis voor elk gebruik, ook commercieel.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
