# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · **Bahasa Indonesia** · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

Alat gratis dan sumber terbuka yang menemukan foto duplikat berdasarkan **isi gambar**, bukan ukuran, tanggal, atau hash. Memakai AI, sehingga mengenali foto yang sama meskipun diperkecil, dikompres ulang, dipotong sedikit, atau diputar.

> 🛡️ **Aman sejak dirancang:** program hanya *menyalin* berkas. Tidak pernah menghapus, memindahkan, atau mengubah foto asli Anda.

![](docs/screenshots/main.png)

## Cara memakai
1. Pilih folder berisi foto Anda (semua subfolder disertakan).
2. Pilih folder tujuan untuk foto unik.
3. Pilih aturan untuk duplikat: terbaru, berkas terbesar, resolusi tertinggi, atau pilih manual untuk setiap grup.
4. Klik «Cari duplikat dan simpan». Foto tanpa duplikat disalin apa adanya, dan dari setiap grup duplikat hanya foto yang Anda pilih.

## Unduh (tidak perlu memasang Python)
Unduh berkas untuk sistem Anda dari halaman [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest):

| Sistem | Berkas | Cara menjalankan |
|---|---|---|
| **Windows** | `…-Setup.exe` | Klik dua kali dan ikuti pemasang. |
| **Linux** | `….AppImage` / `….deb` | AppImage: klik kanan → Properti → Izinkan eksekusi sebagai program, lalu klik dua kali; atau `.deb`: klik dua kali → Pasang. |
| **macOS** | `….dmg` | Buka `.dmg` dan seret aplikasi ke Applications. |

Saat pertama dijalankan, pilih model pengenalan di Pengaturan dan program mengunduhnya sekali (perlu internet). Setelah itu berjalan sepenuhnya offline.

## Peringatan sistem saat pertama kali dijalankan (wajar)
Program ini gratis dan tidak ditandatangani sertifikat kode (sertifikat berbayar), sehingga sistem bisa memberi peringatan. Kodenya terbuka, dan unduhan dapat diperiksa dengan `SHA256SUMS.txt` dari rilis.

- **Windows:** «Windows melindungi PC Anda» → **Info lebih lanjut → Tetap jalankan**.
- **macOS:** buka **Pengaturan Sistem → Privasi & Keamanan**, gulir ke bawah dan klik **Tetap Buka** di samping aplikasi.
- **Linux:** tanpa peringatan.

## Fitur
- Perbandingan isi foto dengan AI (diputar, diperkecil, atau dikompres ulang tidak masalah)
- Tiga model: ringan, sedang, dan berat; dipercepat dengan kartu grafis
- Tinjau manual: centang beberapa foto untuk disimpan, arahkan kursor untuk memperbesar
- Nama berkas di folder tujuan: asli atau menurut tanggal (EXIF, stempel waktu), tanpa pernah menimpa
- Menyertakan semua subfolder
- 30 bahasa, tema gelap dan terang

## Pembuat

Lisensi [MIT](LICENSE): gratis untuk penggunaan apa pun, termasuk komersial.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
