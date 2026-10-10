# AI Anti-Duplicate

[English](README.md) · [Русский](README.ru.md) · **中文** · [Español](README.es.md) · [हिन्दी](README.hi.md) · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [العربية](README.ar.md) · [Bahasa Indonesia](README.id.md) · [Türkçe](README.tr.md)

免费、开源的重复照片查找工具：通过 AI 比较**照片内容**，而不是文件大小、日期或哈希。即使照片被缩小、重新压缩、轻微裁剪或旋转，也能识别。

> 🛡️ **绝对安全：**程序只会*复制*文件，绝不删除、移动或修改您的原始照片。

![](docs/screenshots/main.png)

## 使用方法
1. 选择照片所在的文件夹（会包含所有子文件夹）。
2. 选择保存唯一照片的目标文件夹。
3. 选择发现重复照片时的处理规则：保留最新的、最大的文件、分辨率最高的，或为每一组手动选择。
4. 点击“查找重复项并保存”。没有重复的照片会直接复制，每组重复项只复制您选定的那一张（或几张）。

## 下载（无需安装 Python）
从 [Releases](https://github.com/nikweel/ai-anti-duplicate/releases/latest) 页面下载适合您系统的文件：

| 系统 | 文件 | 如何运行 |
|---|---|---|
| **Windows** | `…-Setup.exe` | 双击，按安装程序提示操作。 |
| **Linux** | `….AppImage` / `….deb` | AppImage：右键 → 属性 → 允许作为程序执行，然后双击；或 `.deb`：双击 → 安装。 |
| **macOS** | `….dmg` | 打开 `.dmg`，将应用拖到“应用程序”。 |

首次启动时，在“设置”中选择识别模型，程序会下载一次（需要网络），之后可完全离线使用。

## 首次启动时系统可能弹出警告（正常现象）
本程序免费且未做代码签名（证书需要付费），所以系统可能提示。代码完全开源，可用发布页中的 `SHA256SUMS.txt` 校验下载文件。

- **Windows：**“Windows 已保护你的电脑” → 点击**更多信息 → 仍要运行**。
- **macOS：**打开**系统设置 → 隐私与安全性**，向下滚动并点击应用旁的**仍要打开**。
- **Linux：**没有警告。

## 功能
- AI 比较照片内容（旋转、缩放、压缩都不影响）
- 轻量、中等、重型三种识别模型，可使用显卡加速
- 手动检查：可勾选多张照片保存，鼠标悬停放大查看
- 目标文件夹文件名：保留原名或按日期重命名（EXIF 拍摄日期、时间戳），冲突时绝不覆盖
- 包含所有子文件夹
- 12 种界面语言，深色/浅色主题

## 作者

[MIT](LICENSE) 许可：免费用于任何用途，包括商业用途。

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
