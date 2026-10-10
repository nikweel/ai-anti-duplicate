# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · **Hrvatski** · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** besplatna je aplikacija otvorenog koda koja pronalazi duplikate **fotografija** (JPG, PNG, WebP + RAW) prema **onome što je na slici**, a ne prema veličini, datumu ili hashu. Koristi umjetnu inteligenciju pa prepoznaje isti kadar čak i ako je smanjen, ponovno komprimiran, malo izrezan ili zakrenut. Namijenjena je samo zbirkama fotografija, a ne dokumentima, videozapisima ni drugim datotekama.

> 🛡️ **Sigurno po dizajnu:** program samo *kopira* datoteke. Nikad ne briše, ne premješta i ne mijenja vaše izvornike.

![](docs/screenshots/main.png)

## Kako se koristi
1. Odaberite mapu s fotografijama (uključene su sve podmape).
2. Odaberite mapu u koju će se spremiti jedinstvene fotografije.
3. Odaberite pravilo za duplikate: najnovija, najveća datoteka, najviša razlučivost ili ručni odabir za svaku skupinu.
4. Kliknite «Pronađi duplikate i spremi». Fotografije bez duplikata kopiraju se onakve kakve jesu, a iz svake skupine duplikata samo one koje ste odabrali.

## Preuzimanje (Python nije potrebno instalirati)
Preuzmite datoteku za svoj sustav sa stranice [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| Sustav | Datoteka | Kako pokrenuti |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dvostruki klik i slijedite instalacijski čarobnjak. |
| **Linux** | `….AppImage` / `….deb` | AppImage: desni klik → Svojstva → Dopusti izvršavanje kao program, zatim dvostruki klik; ili `.deb`: dvostruki klik → Instaliraj. |
| **macOS** | `….dmg` | Otvorite `.dmg` i povucite aplikaciju u Applications. |

Pri prvom pokretanju u Postavkama odaberete model prepoznavanja, a program ga jednom preuzme (potreban je internet). Nakon toga radi potpuno izvan mreže.

## Upozorenja sustava pri prvom pokretanju (to je normalno)
Program je besplatan i nije potpisan certifikatom (certifikati se plaćaju), pa vas sustav može upozoriti. Kod je otvoren, a preuzeto možete provjeriti pomoću `SHA256SUMS.txt` iz izdanja.

- **Windows:** «Windows je zaštitio vaše računalo» → **Dodatne informacije → Ipak pokreni**.
- **macOS:** otvorite **Postavke sustava → Privatnost i sigurnost**, pomaknite se prema dolje i kliknite **Ipak otvori** pokraj aplikacije.
- **Linux:** bez upozorenja.
- Podrška za RAW datoteke fotoaparata (CR2, NEF, ARW, DNG i dr.) — izvornik se ne mijenja

## Mogućnosti
- Usporedba sadržaja fotografija umjetnom inteligencijom (zakretanje, smanjivanje i ponovna kompresija ne smetaju)
- Tri modela: lagan, srednji i težak; ubrzanje grafičkom karticom
- Ručna provjera: označite više fotografija za spremanje, prijeđite mišem za povećanje
- Nazivi u odredišnoj mapi: izvorni ili prema datumu (EXIF, vremenska oznaka), bez prepisivanja
- Uključuje sve podmape
- 30 jezika, tamna i svijetla tema

## Autor

Licenca [MIT](LICENSE): besplatno za svaku uporabu, uključujući komercijalnu.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
