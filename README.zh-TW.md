# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · **繁體中文** · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI** 是免費的開源應用程式，透過 AI 比較**相片的內容**，而不是檔案大小、日期或雜湊值，來找出重複的**相片**（JPG、PNG、WebP）。即使相片被縮小、重新壓縮、稍微裁切或旋轉，也能辨識出來。僅適用於相片收藏，不適用於文件、影片或其他檔案。

> 🛡️ **安全為先：**程式只會*複製*檔案，絕不刪除、移動或修改您的原始相片。

![](docs/screenshots/main.png)

## 使用方式
1. 選擇存放相片的資料夾（會包含所有子資料夾）。
2. 選擇用來存放不重複相片的資料夾。
3. 選擇發現重複相片時的處理規則：保留最新的、最大的檔案、解析度最高的，或為每一組手動選擇。
4. 按下「尋找重複項目並儲存」。沒有重複的相片會直接複製，每組重複項目只複製您選定的那一張（或幾張）。

## 下載（不需要安裝 Python）
請從 [Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest) 頁面下載適合您系統的檔案：

| 系統 | 檔案 | 執行方式 |
|---|---|---|
| **Windows** | `…-Setup.exe` | 按兩下，依照安裝程式的指示操作。 |
| **Linux** | `….AppImage` / `….deb` | AppImage：按右鍵 → 內容 → 允許以程式方式執行，然後按兩下；或 `.deb`：按兩下 → 安裝。 |
| **macOS** | `….dmg` | 開啟 `.dmg`，將應用程式拖曳到「應用程式」。 |

第一次啟動時，請在「設定」中選擇辨識模型，程式會下載一次（需要網路），之後即可完全離線使用。

## 第一次啟動時系統可能出現警告（屬正常現象）
本程式免費且未進行程式碼簽署（憑證需要付費），因此系統可能會提出警告。程式碼完全公開，可使用發行版中的 `SHA256SUMS.txt` 驗證下載的檔案。

- **Windows：**「Windows 已保護您的電腦」→ **其他資訊 → 仍要執行**。
- **macOS：**開啟**系統設定 → 隱私權與安全性**，向下捲動並按下應用程式旁的**強制打開**。
- **Linux：**沒有警告。

## 功能
- AI 比較相片內容（旋轉、縮小、重新壓縮都不影響）
- 輕量、中等、重型三種模型，可使用顯示卡加速
- 手動檢視：可勾選多張相片儲存，滑鼠移上去即可放大
- 目的資料夾的檔名：保留原名或依日期（EXIF、時間戳記）命名，絕不覆蓋
- 包含所有子資料夾
- 30 種語言，深色／淺色主題

## 作者

[MIT](LICENSE) 授權：任何用途皆免費，包括商業用途。

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
