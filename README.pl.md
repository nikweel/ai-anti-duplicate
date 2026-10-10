# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · **Polski** · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** to darmowa aplikacja open source do wyszukiwania duplikatów **zdjęć** (JPG, PNG, WebP + RAW) według **tego, co jest na obrazie**, a nie rozmiaru, daty czy skrótu. Korzysta ze sztucznej inteligencji, więc rozpozna to samo ujęcie nawet po zmniejszeniu, ponownej kompresji, lekkim przycięciu czy obróceniu. Służy tylko do kolekcji zdjęć, nie do dokumentów, filmów ani innych plików.

> 🛡️ **Bezpieczna z założenia:** program tylko *kopiuje* pliki. Nigdy nie usuwa, nie przenosi ani nie zmienia oryginałów.

![](docs/screenshots/main.png)

## Jak używać
1. Wybierz folder ze zdjęciami (podfoldery są uwzględniane).
2. Wybierz folder, w którym zapisane zostaną unikalne zdjęcia.
3. Wybierz regułę dla duplikatów: najnowszy, największy plik, najwyższa rozdzielczość lub ręczny wybór dla każdej grupy.
4. Kliknij „Znajdź duplikaty i zapisz”. Zdjęcia bez duplikatów są kopiowane bez zmian, a z każdej grupy duplikatów — tylko wybrane przez Ciebie.

## Pobieranie (nie trzeba instalować Pythona)
Pobierz plik dla swojego systemu ze strony [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| System | Plik | Jak uruchomić |
|---|---|---|
| **Windows** | `…-Setup.exe` | Dwukrotne kliknięcie i instalator. |
| **Linux** | `….AppImage` / `….deb` | AppImage: prawy przycisk → Właściwości → Zezwól na wykonywanie jako program, potem dwukrotne kliknięcie; albo `.deb`: dwukrotne kliknięcie → Zainstaluj. |
| **macOS** | `….dmg` | Otwórz `.dmg` i przeciągnij aplikację do Programów. |

Przy pierwszym uruchomieniu wybierasz model rozpoznawania w Ustawieniach, a program pobiera go jednorazowo (potrzebny internet). Potem działa całkowicie offline.

## Ostrzeżenia systemu przy pierwszym uruchomieniu (to normalne)
Program jest darmowy i nie jest podpisany certyfikatem (są płatne), dlatego system może ostrzegać. Kod jest otwarty, a pobrany plik sprawdzisz za pomocą `SHA256SUMS.txt` z wydania.

- **Windows:** „System Windows ochronił ten komputer” → **Więcej informacji → Uruchom mimo to**.
- **macOS:** otwórz **Ustawienia systemowe → Prywatność i ochrona**, przewiń w dół i kliknij **Otwórz mimo to** obok aplikacji.
- **Linux:** bez ostrzeżeń.

## Funkcje
- Porównanie zawartości zdjęć przez AI (obrót, zmniejszenie, ponowna kompresja nie przeszkadzają)
- Trzy modele: lekki, średni i ciężki; przyspieszenie kartą graficzną
- Ręczna kontrola: zaznacz kilka zdjęć do zapisania, najedź kursorem, by powiększyć
- Nazwy w folderze docelowym: oryginalne lub według daty (EXIF, znacznik czasu), bez nadpisywania
- Uwzględnia wszystkie podfoldery
- 30 języków, motyw ciemny i jasny

## Autor

Licencja [MIT](LICENSE): za darmo do dowolnego użytku, także komercyjnego.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
