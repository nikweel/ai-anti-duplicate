# AI Anti-Duplicate

**English** · [Русский](README.ru.md) · [中文](README.zh.md) · [Español](README.es.md) · [हिन्दी](README.hi.md) · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [العربية](README.ar.md) · [Bahasa Indonesia](README.id.md) · [Türkçe](README.tr.md)

Free, open-source tool that finds duplicate photos by **what is in the picture**, not by file size, date or hash.
It uses the CLIP AI model, so it recognises the same shot even if it was resized, re-compressed, cropped a little or rotated.

> 🛡️ **Safe by design:** the app only *copies* files. It never deletes, moves or changes your originals.

## Screenshots
*(demo with generated pictures: three scenes each have copies — an edited small one and a rotated one — and two scenes are unique)*

![Main window](docs/screenshots/main.png)
![Choosing which duplicate to keep](docs/screenshots/review.png)
![Settings](docs/screenshots/settings.png)

## How it works
1. Choose the folder with your photos.
2. Choose the folder where unique photos will be saved.
3. Pick a rule for duplicates: **newest**, **largest file**, **highest resolution**, or **choose manually** for every shot (tick one or several files to keep; hover a photo to enlarge it).
4. Press **Find duplicates and save**. You get every photo that has no duplicates, plus the best copy from each group of duplicates.

The interface is dark and available in English and Russian (language switcher in the top-right corner).

The **Sensitivity** slider controls how similar two photos must be: *Strict* finds only near-identical files, *Soft* also finds similar shots from the same scene.

## Reviewing duplicates manually
Choose **"Choose manually for each shot"** and the app shows every group of duplicates in a window:
- All checkboxes start **unticked**: tick **every file you want to save** (one, several or all of them). Useful when a pair was matched by mistake, e.g. the same pose with a different facial expression.
- **Click a photo** (or its checkbox) to select it; a blue frame marks selected photos.
- **Hover a photo** to see it enlarged, with its name, resolution and size.
- *Select all* / *Clear* buttons, and the *Save selected* button stays disabled until you tick at least one file.

## File names when copying
The program searches **all subfolders** (can be switched off with *Search in subfolders*) and **never overwrites or loses a file**. Configure everything before you press the button:
- **Keep names as they are**, or **rename by date**.
- **Date source:** shooting date (EXIF, falls back to the file date), file creation date or file modification date. *(On Linux many file systems do not store a creation date, so the modification date is used.)*
- **Date format:** `2024-05-01_12-30-45`, `20240501_123045`, a Unix **timestamp** (seconds or milliseconds) or your own pattern (`%Y %m %d %H %M %S`, `{ts}`, `{ms}`).
- **On a name conflict:** add a number (`IMG_0001_1.jpg`) or a prefix with the source folder name (`Holiday_IMG_0001.jpg`, then a number if it is still taken). A file that is already in the destination with identical content is simply skipped, so you can safely run the program again.

A list of what was copied where is saved to `data/logs/last_export.csv`.

## Settings (⚙ button)
- **Language:** 12 languages — English, Русский, 中文, Español, हिन्दी, Português, Français, Deutsch, 日本語, العربية, Bahasa Indonesia, Türkçe (Arabic is shown right-to-left). The language is detected from your system on first launch.
- **Theme:** dark, light or follow the system.
- **Recognition model** (the size of each download is shown before you choose):

  | Model | Size | What it is for |
  |---|---|---|
  | **Light** | 44 MB | The fastest; works well on any computer. Good for most photo collections. |
  | **Medium** | 174 MB | Slower, tells similar photos apart more precisely. Comfortable with a graphics card. |
  | **Heavy** | 609 MB | The slowest and the most accurate: notices the smallest differences. Best with a powerful graphics card. |

  On the first launch no model is installed: the app asks you to pick one in Settings and downloads it with a progress bar. Under the hood these are [DINOv2](https://github.com/facebookresearch/dinov2) models (Apache 2.0) converted to ONNX; in our tests they separate real duplicates from merely similar photos better than CLIP while being much smaller.
- **Computing device:** automatic / CPU / GPU. *Automatic* uses the graphics card when available (DirectML on Windows, CoreML on macOS) and falls back to the CPU if anything goes wrong.
- **Matching strictness** (slider on the main window): *Strict* finds only practically identical photos, *Loose* also catches merely similar ones. The default position is calibrated separately for each model.

## Download (no installation of Python needed)
Get the file for your system from the [**Releases**](https://github.com/nikweel/ai-anti-duplicate/releases/latest) page:

| System | File | How to run |
|---|---|---|
| **Windows** | `…-Setup.exe` | Double-click, follow the installer. |
| **Linux (any)** | `….AppImage` | Right-click → Properties → *Allow executing as program*, then double-click. Or in a terminal: `chmod +x *.AppImage && ./*.AppImage` |
| **Linux (Ubuntu/Debian)** | `….deb` | Double-click → *Install*. The app appears in your menu. |
| **macOS** | `….dmg` | Open, drag the app to *Applications*. First launch: right-click → *Open* (the app is not signed). |

On the first launch you choose the AI model in Settings and the app downloads it once (needs internet). After that it works fully offline.

## Security warnings on first launch (this is normal)
The app is free and not code-signed (certificates cost money), so your system may warn you. The app is open source and only *copies* files; you can verify downloads with `SHA256SUMS.txt` from the release (`sha256sum -c SHA256SUMS.txt`).
- **Windows:** "Windows protected your PC" → click **More info → Run anyway**.
- **macOS:** open **System Settings → Privacy & Security**, scroll down and click **Open Anyway** next to the app (on older macOS: right-click the app → *Open*).
- **Linux:** no warnings. For AppImage just allow executing it (right-click → Properties → *Allow executing as program*).

## How the models were chosen
We compared embedding models on real photos: true duplicates (resized, re-compressed, cropped, brightened) against *hard negatives* — the same photo with part of the picture replaced (a stand-in for "same pose, different expression"). The score is the AUC of telling the two groups apart (1.0 = perfect); speed is measured on a CPU.

| Model | Size | AUC | Speed per photo |
|---|---|---|---|
| CLIP ViT-B/32 | 176 MB | 0.836 | ~22 ms |
| CLIP ViT-L/14 | 608 MB | 0.875 | ~325 ms |
| **DINOv2 small (Light)** | 44 MB | 0.889 | ~37 ms |
| **DINOv2 base (Medium)** | 174 MB | 0.894 | ~102 ms |
| **DINOv2 large (Heavy)** | 609 MB | 0.909 | ~330 ms |

This is a small test set (about 40 photos from one machine), so treat the numbers as a trend, not a guarantee. Scripts: `scripts/export_dinov2.py`, `scripts/shrink_onnx.py`.

## Run from source (portable, no manual setup)
Download the repository and double-click `start.cmd` (Windows), `start.command` (macOS) or `start.sh` (Linux).
The first run downloads Python and all dependencies into the local `runtime/` folder automatically.

## Development
- Model export: `scripts/export_dinov2.py` (PyTorch → ONNX) and `scripts/shrink_onnx.py` (fp16 weights; the result matches the original to within 0.0003 similarity). Model files are served from the `v0.1` release and verified by exact size after download.
- Build: `pyinstaller packaging.spec`; packages: `packaging/`; CI: `.github/workflows/build.yml` (push a tag `app-v*`).
- Tests: `pytest`.

Pull requests and ideas are welcome!

## License
[MIT](LICENSE) — free for any use, including commercial. Do whatever you like, just keep the copyright notice.
The models are DINOv2 by Meta AI (Apache 2.0).

## Author
Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
