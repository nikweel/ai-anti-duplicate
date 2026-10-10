# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Lietuvių** · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** — nemokama atvirojo kodo programa, kuri randa pasikartojančias **nuotraukas** (JPG, PNG, WebP + RAW) pagal **tai, kas pavaizduota**, o ne pagal dydį, datą ar maišą. Ji naudoja dirbtinį intelektą, todėl atpažįsta tą patį kadrą, net jei jis sumažintas, iš naujo suspaustas, šiek tiek apkirptas ar pasuktas. Skirta tik nuotraukų rinkiniams, ne dokumentams, vaizdo įrašams ar kitiems failams.

> 🛡️ **Saugu iš pagrindų:** programa tik *kopijuoja* failus. Ji niekada neištrina, neperkelia ir nekeičia jūsų originalų.

![](docs/screenshots/main.png)

## Kaip naudotis
1. Pasirinkite aplanką su nuotraukomis (įtraukiami visi poaplankiai).
2. Pasirinkite aplanką, kuriame bus išsaugotos unikalios nuotraukos.
3. Pasirinkite dublikatų taisyklę: naujausią, didžiausią failą, aukščiausią skiriamąją gebą arba rankinį pasirinkimą kiekvienai grupei.
4. Spustelėkite „Rasti dublikatus ir išsaugoti“. Nuotraukos be dublikatų nukopijuojamos nepakeistos, o iš kiekvienos dublikatų grupės — tik jūsų pasirinktos.

## Atsisiuntimas (Python diegti nereikia)
Atsisiųskite savo sistemai skirtą failą puslapyje [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| Sistema | Failas | Kaip paleisti |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dukart spustelėkite ir sekite diegimo vedlį. |
| **Linux** | `….AppImage` / `….deb` | AppImage: dešinysis pelės klavišas → Ypatybės → Leisti vykdyti kaip programą, tada dukart spustelėkite; arba `.deb`: dukart spustelėkite → Įdiegti. |
| **macOS** | `….dmg` | Atidarykite `.dmg` ir nuvilkite programą į Applications. |

Pirmą kartą paleidę nustatymuose pasirenkate atpažinimo modelį, o programa jį atsisiunčia vieną kartą (reikia interneto). Vėliau viskas veikia be interneto.

## Sistemos įspėjimai pirmą kartą paleidus (tai normalu)
Programa nemokama ir nepasirašyta sertifikatu (sertifikatai mokami), todėl sistema gali įspėti. Kodas atviras, o atsisiuntimą galite patikrinti su leidimo `SHA256SUMS.txt`.

- **Windows:** „Windows apsaugojo jūsų kompiuterį“ → **Daugiau informacijos → Vis tiek vykdyti**.
- **macOS:** atidarykite **Sistemos nustatymai → Privatumas ir sauga**, slinkite žemyn ir spustelėkite **Vis tiek atidaryti** šalia programos.
- **Linux:** įspėjimų nėra.

## Galimybės
- Nuotraukų turinio palyginimas dirbtiniu intelektu (pasukimas, sumažinimas ar pakartotinis suspaudimas netrukdo)
- Trys modeliai: lengvas, vidutinis ir sunkus; spartinimas vaizdo plokšte
- Rankinis tikrinimas: pažymėkite kelias nuotraukas išsaugoti, užveskite žymeklį, kad padidintumėte
- Pavadinimai paskirties aplanke: originalūs arba pagal datą (EXIF, laiko žyma), niekada neperrašo
- Įtraukia visus poaplankius
- 30 kalbų, tamsi ir šviesi tema

## Autorius

[MIT](LICENSE) licencija: nemokama bet kokiam naudojimui, įskaitant komercinį.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
