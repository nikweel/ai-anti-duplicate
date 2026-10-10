# Photo Duplicate Finder AI

[العربية](README.ar.md) · [Български](README.bg.md) · [中文（简体）](README.zh.md) · [繁體中文](README.zh-TW.md) · [Hrvatski](README.hr.md) · [Čeština](README.cs.md) · [Dansk](README.da.md) · [Nederlands](README.nl.md) · [English](README.md) · [Suomi](README.fi.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Ελληνικά](README.el.md) · [हिन्दी](README.hi.md) · [Magyar](README.hu.md) · [Bahasa Indonesia](README.id.md) · [Italiano](README.it.md) · [日本語](README.ja.md) · **한국어** · [Lietuvių](README.lt.md) · [Norsk](README.nb.md) · [Polski](README.pl.md) · [Português](README.pt.md) · [Română](README.ro.md) · [Русский](README.ru.md) · [Slovenčina](README.sk.md) · [Español](README.es.md) · [Svenska](README.sv.md) · [Türkçe](README.tr.md) · [Українська](README.uk.md)

**Photo Duplicate Finder AI**는 파일 크기, 날짜, 해시가 아니라 **사진에 담긴 내용**으로 중복 **사진**(JPG, PNG, WebP 및 카메라 RAW)을 찾아 주는 무료 오픈소스 앱입니다. AI를 사용하므로 크기를 줄이거나, 다시 압축하거나, 조금 자르거나, 회전한 같은 사진도 알아봅니다. 사진 모음 전용이며 문서, 동영상, 그 밖의 파일용이 아닙니다.

> 🛡️ **설계부터 안전합니다:** 프로그램은 파일을 *복사만* 합니다. 원본을 삭제하거나 이동하거나 수정하는 일은 절대 없습니다.

![](docs/screenshots/main.png)

## 사용 방법
1. 사진이 들어 있는 폴더를 선택합니다(모든 하위 폴더 포함).
2. 중복 없는 사진을 저장할 폴더를 선택합니다.
3. 중복 처리 규칙을 고릅니다: 가장 최근 파일, 가장 큰 파일, 가장 높은 해상도, 또는 그룹마다 직접 선택.
4. ‘중복 찾기 및 저장’을 누릅니다. 중복이 없는 사진은 그대로 복사되고, 중복 그룹에서는 선택한 사진만 복사됩니다.

## 다운로드 (Python 설치 불필요)
[Releases](https://github.com/nikweel/photo-duplicate-finder-ai/releases/latest) 페이지에서 사용 중인 시스템용 파일을 내려받으세요:

| 시스템 | 파일 | 실행 방법 |
|---|---|---|
| **Windows** | `…-Setup.exe` | 더블클릭 후 설치 마법사를 따르세요. |
| **Linux** | `….AppImage` / `….deb` | AppImage: 오른쪽 클릭 → 속성 → 프로그램으로 실행 허용 후 더블클릭, 또는 `.deb`: 더블클릭 → 설치. |
| **macOS** | `….dmg` | `.dmg`를 열고 앱을 응용 프로그램으로 끌어다 놓으세요. |

처음 실행하면 설정에서 인식 모델을 선택하고, 프로그램이 한 번 다운로드합니다(인터넷 필요). 이후에는 완전히 오프라인으로 동작합니다.

## 처음 실행할 때 나오는 시스템 경고 (정상입니다)
이 프로그램은 무료이고 코드 서명(유료 인증서)이 없어서 시스템이 경고를 표시할 수 있습니다. 코드는 공개되어 있으며, 릴리스의 `SHA256SUMS.txt`로 내려받은 파일을 검증할 수 있습니다.

- **Windows:** “Windows의 PC 보호” → **추가 정보 → 실행**.
- **macOS:** **시스템 설정 → 개인정보 보호 및 보안**을 열고 아래로 스크롤해 앱 옆의 **그래도 열기**를 누르세요.
- **Linux:** 경고가 없습니다.

## 기능
- AI로 사진 내용 비교 (회전, 축소, 재압축에 영향받지 않음)
- 경량, 중간, 고성능 세 가지 모델과 그래픽 카드 가속
- 수동 검토: 저장할 사진을 여러 장 체크, 마우스를 올리면 확대
- 대상 폴더 파일 이름: 원래 이름 또는 날짜(EXIF, 타임스탬프) 기준, 덮어쓰기 없음
- 모든 하위 폴더 포함
- 30개 언어, 어두운/밝은 테마

## 제작자

[MIT](LICENSE) 라이선스: 상업적 이용을 포함해 모든 용도로 무료입니다.

Nikolay Fedotov — [tech-crm.ru](https://tech-crm.ru/) · [VK](https://vk.ru/id191178167) · [MAX](https://max.ru/u/f9LHodD0cOInyBtQrxPp6Z1O_g2V8Ck-1hzBxWg_l9EN48ubud67NUWeyTM) · [Facebook](https://www.facebook.com/nikweel) · [GitHub](https://github.com/nikweel)
