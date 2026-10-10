# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · **Română** · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** este o aplicație gratuită, open source, care găsește **fotografii** duplicate (JPG, PNG, WebP + RAW) după **ceea ce se vede în imagine**, nu după dimensiune, dată sau hash. Folosește inteligența artificială, așa că recunoaște același cadru chiar dacă a fost micșorat, recomprimat, decupat puțin sau rotit. Este făcută doar pentru colecții de fotografii, nu pentru documente, videoclipuri sau alte fișiere.

> 🛡️ **Sigură prin proiectare:** programul doar *copiază* fișiere. Nu șterge, nu mută și nu modifică niciodată originalele tale.

![](docs/screenshots/main.png)

## Cum se folosește
1. Alege dosarul cu fotografiile tale (subdosarele sunt incluse).
2. Alege dosarul în care se vor salva fotografiile unice.
3. Alege regula pentru dubluri: cea mai nouă, cel mai mare fișier, cea mai mare rezoluție sau alegere manuală pentru fiecare grup.
4. Apasă «Găsește dublurile și salvează». Fotografiile fără dubluri sunt copiate ca atare, iar din fiecare grup de dubluri doar cele alese de tine.

## Descărcare (nu trebuie să instalezi Python)
Descarcă fișierul pentru sistemul tău de pe pagina [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| Sistem | Fișier | Cum se pornește |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dublu clic și urmează expertul de instalare. |
| **Linux** | `….AppImage` / `….deb` | AppImage: clic dreapta → Proprietăți → Permite rularea ca program, apoi dublu clic; sau `.deb`: dublu clic → Instalează. |
| **macOS** | `….dmg` | Deschide `.dmg` și trage aplicația în Applications. |

La prima pornire alegi modelul de recunoaștere în Setări, iar programul îl descarcă o singură dată (e nevoie de internet). Apoi funcționează complet offline.

## Avertismente ale sistemului la prima pornire (este normal)
Programul este gratuit și nu are semnătură digitală (certificatele costă bani), de aceea sistemul te poate avertiza. Codul este deschis, iar descărcarea o poți verifica cu `SHA256SUMS.txt` din versiune.

- **Windows:** «Windows a protejat computerul» → **Mai multe informații → Rulează oricum**.
- **macOS:** deschide **Setări sistem → Confidențialitate și securitate**, derulează în jos și apasă **Deschide oricum** lângă aplicație.
- **Linux:** fără avertismente.

## Funcții
- Compararea conținutului fotografiilor cu AI (rotirea, micșorarea sau recomprimarea nu contează)
- Trei modele: ușor, mediu și greu; accelerare cu placa video
- Verificare manuală: bifează mai multe fotografii de salvat, treci cursorul peste ele pentru mărire
- Nume în dosarul destinație: originale sau după dată (EXIF, marcaj temporal), fără suprascriere
- Include toate subdosarele
- 30 de limbi, temă întunecată și luminoasă

## Autor

Licență [MIT](LICENSE): gratuit pentru orice utilizare, inclusiv comercială.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
