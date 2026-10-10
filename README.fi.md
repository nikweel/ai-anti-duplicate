# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · **Suomi** · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** on ilmainen avoimen lähdekoodin sovellus, joka löytää kaksoiskappaleet **valokuvista** (JPG, PNG, WebP + RAW) **kuvan sisällön** perusteella — ei tiedostokoon, päivämäärän tai tiivisteen mukaan. Se käyttää tekoälyä, joten se tunnistaa saman kuvan, vaikka se olisi pienennetty, pakattu uudelleen, hieman rajattu tai käännetty. Tarkoitettu vain valokuvakokoelmille, ei asiakirjoille, videoille tai muille tiedostoille.

> 🛡️ **Turvallinen jo suunnittelussa:** ohjelma vain *kopioi* tiedostoja. Se ei koskaan poista, siirrä tai muuta alkuperäisiä.

![](docs/screenshots/main.png)

## Näin käytät
1. Valitse kansio, jossa kuvasi ovat (alikansiot otetaan mukaan).
2. Valitse kansio, johon yksilölliset kuvat tallennetaan.
3. Valitse sääntö kaksoiskappaleille: uusin, suurin tiedosto, suurin resoluutio tai käsin valinta jokaiselle ryhmälle.
4. Paina ”Etsi kaksoiskappaleet ja tallenna”. Kuvat ilman kaksoiskappaleita kopioidaan sellaisenaan, ja jokaisesta ryhmästä vain valitsemasi kuva(t).

## Lataus (Pythonia ei tarvitse asentaa)
Lataa järjestelmääsi sopiva tiedosto [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest)-sivulta:

| Järjestelmä | Tiedosto | Käynnistys |
|---|---|---|
| **Windows** | `…-Setup.exe` | Kaksoisnapsauta ja seuraa asennusohjelmaa. |
| **Linux** | `….AppImage` / `….deb` | AppImage: hiiren oikea → Ominaisuudet → Salli suoritus ohjelmana, sitten kaksoisnapsautus; tai `.deb`: kaksoisnapsautus → Asenna. |
| **macOS** | `….dmg` | Avaa `.dmg` ja vedä sovellus Ohjelmat-kansioon. |

Ensimmäisellä käynnistyskerralla valitset tunnistusmallin Asetuksista, ja ohjelma lataa sen kerran (tarvitaan internet). Sen jälkeen kaikki toimii ilman verkkoa.

## Järjestelmän varoitukset ensimmäisellä käynnistyksellä (täysin normaalia)
Ohjelma on ilmainen eikä ole koodiallekirjoitettu (varmenteet maksavat), joten järjestelmä voi varoittaa. Koodi on avointa, ja latauksen voi tarkistaa julkaisun `SHA256SUMS.txt`-tiedostolla.

- **Windows:** ”Windows suojasi tietokonettasi” → **Lisätietoja → Suorita silti**.
- **macOS:** avaa **Järjestelmäasetukset → Tietosuoja ja turvallisuus**, vieritä alas ja napsauta sovelluksen vieressä **Avaa silti**.
- **Linux:** ei varoituksia.
- Tukee kameroiden RAW-tiedostoja (CR2, NEF, ARW, DNG ym.) — alkuperäistä ei muuteta

## Ominaisuudet
- Kuvien sisällön vertailu tekoälyllä (kääntäminen, pienentäminen tai uudelleenpakkaus ei haittaa)
- Kolme mallia: kevyt, keskiraskas ja raskas; kiihdytys näytönohjaimella
- Käsin tarkistus: valitse useita tallennettavia kuvia, suurenna viemällä hiiri päälle
- Nimet kohdekansiossa: alkuperäiset tai päivämäärän mukaan (EXIF, aikaleima), ei koskaan ylikirjoitusta
- Kaikki alikansiot mukana
- 30 kieltä, tumma ja vaalea teema

## Tekijä

[MIT](LICENSE)-lisenssi: ilmainen kaikkeen käyttöön, myös kaupalliseen.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
