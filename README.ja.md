# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · **日本語** · [한국어](README.ko.md) · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

ファイルサイズや日付、ハッシュではなく、**写真の内容**で重複を見つける無料のオープンソースツールです。AI を使うため、縮小・再圧縮・軽いトリミング・回転をした同じ写真も見つけられます。

> 🛡️ **安全設計：**このプログラムはファイルを*コピーするだけ*です。元の写真を削除・移動・変更することは決してありません。

![](docs/screenshots/main.png)

## 使い方
1. 写真が入っているフォルダを選びます（サブフォルダもすべて対象）。
2. 重複のない写真の保存先フォルダを選びます。
3. 重複が見つかったときのルールを選びます：最新、最大のファイル、最高解像度、またはグループごとに手動で選択。
4. 「重複を検索して保存」を押します。重複のない写真はそのままコピーされ、重複グループからは選んだ写真だけがコピーされます。

## ダウンロード（Python のインストール不要）
[Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest) ページからお使いの環境のファイルをダウンロードしてください：

| OS | ファイル | 起動方法 |
|---|---|---|
| **Windows** | `…-Setup.exe` | ダブルクリックしてインストーラーの指示に従います。 |
| **Linux** | `….AppImage` / `….deb` | AppImage：右クリック → プロパティ → プログラムとして実行を許可、その後ダブルクリック。または `.deb`：ダブルクリック → インストール。 |
| **macOS** | `….dmg` | `.dmg` を開き、アプリを「アプリケーション」へドラッグします。 |

初回起動時に「設定」で認識モデルを選ぶと、プログラムが一度だけダウンロードします（インターネットが必要）。その後は完全にオフラインで動作します。

## 初回起動時のシステム警告（正常です）
本プログラムは無料で、コード署名（有料の証明書）をしていないため、システムが警告を出すことがあります。コードは公開されており、リリースの `SHA256SUMS.txt` でダウンロードを検証できます。

- **Windows：**「Windows によって PC が保護されました」→ **詳細情報 → 実行**。
- **macOS：****システム設定 → プライバシーとセキュリティ**を開き、下へスクロールしてアプリの横の**このまま開く**を押します。
- **Linux：**警告はありません。

## 機能
- AI による写真内容の比較（回転・縮小・再圧縮の影響を受けません）
- 軽量・標準・高精度の3種類のモデル。グラフィックスカードで高速化
- 手動確認：複数の写真にチェックして保存、カーソルを合わせて拡大
- 保存先のファイル名：元の名前または日付（EXIF、タイムスタンプ）。上書きは一切なし
- すべてのサブフォルダを対象
- 30言語、ダーク／ライトテーマ

## 作者

[MIT](LICENSE) ライセンス：商用を含め、あらゆる用途で無料です。

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
