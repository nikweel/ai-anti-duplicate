# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · **Türkçe** · [Українська](README.uk.md)

Yinelenen fotoğrafları dosya boyutuna, tarihe veya karma değerine göre değil, **görüntünün içeriğine** göre bulan ücretsiz, açık kaynaklı bir araç. Yapay zekâ kullandığı için aynı fotoğrafı küçültülmüş, yeniden sıkıştırılmış, hafifçe kırpılmış veya döndürülmüş olsa bile tanır.

> 🛡️ **Tasarım gereği güvenli:** Program yalnızca dosyaları *kopyalar*. Orijinal fotoğraflarınızı asla silmez, taşımaz veya değiştirmez.

![](docs/screenshots/main.png)

## Nasıl kullanılır
1. Fotoğraflarınızın bulunduğu klasörü seçin (tüm alt klasörler dahildir).
2. Benzersiz fotoğrafların kaydedileceği klasörü seçin.
3. Kopyalar için kuralı seçin: en yeni, en büyük dosya, en yüksek çözünürlük veya her grup için elle seçim.
4. «Kopyaları bul ve kaydet»e basın. Kopyası olmayan fotoğraflar olduğu gibi kopyalanır; her kopya grubundan ise yalnızca sizin seçtiğiniz fotoğraf(lar).

## İndirme (Python kurmanız gerekmez)
Sisteminize uygun dosyayı [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest) sayfasından indirin:

| Sistem | Dosya | Nasıl çalıştırılır |
|---|---|---|
| **Windows** | `…-Setup.exe` | Çift tıklayın ve kurulum sihirbazını izleyin. |
| **Linux** | `….AppImage` / `….deb` | AppImage: sağ tık → Özellikler → Program olarak çalıştırmaya izin ver, sonra çift tıklayın; veya `.deb`: çift tıkla → Kur. |
| **macOS** | `….dmg` | `.dmg` dosyasını açın ve uygulamayı Uygulamalar'a sürükleyin. |

İlk açılışta Ayarlar'dan tanıma modelini seçersiniz; program onu bir kez indirir (internet gerekir). Sonrasında tamamen çevrimdışı çalışır.

## İlk açılışta sistem uyarıları (normaldir)
Program ücretsizdir ve kod imzalı değildir (sertifikalar ücretlidir), bu yüzden sistem uyarı verebilir. Kod açıktır; indirmeyi sürümdeki `SHA256SUMS.txt` ile doğrulayabilirsiniz.

- **Windows:** «Windows bilgisayarınızı korudu» → **Daha fazla bilgi → Yine de çalıştır**.
- **macOS:** **Sistem Ayarları → Gizlilik ve Güvenlik**'i açın, aşağı kaydırıp uygulamanın yanındaki **Yine de Aç**'a tıklayın.
- **Linux:** uyarı yok.

## Özellikler
- Yapay zekâ ile fotoğraf içeriği karşılaştırması (döndürme, küçültme, yeniden sıkıştırma sorun olmaz)
- Üç model: hafif, orta ve ağır; ekran kartıyla hızlandırma
- Elle inceleme: kaydetmek için birden fazla fotoğrafı işaretleyin, büyütmek için üzerine gelin
- Hedef klasörde dosya adları: orijinal veya tarihe göre (EXIF, zaman damgası); asla üzerine yazmaz
- Tüm alt klasörler dahil
- 30 dil, koyu ve açık tema

## Yazar

[MIT](LICENSE) lisansı: ticari olanlar dahil her kullanım için ücretsiz.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
