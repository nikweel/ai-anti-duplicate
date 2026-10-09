#!/bin/sh
# Использование: packaging/linux.sh <версия>  (после pyinstaller; dist/AI-Anti-Duplicate)
set -e
VER="${1:-0.0.0}"; SRC=dist/AI-Anti-Duplicate; OUT=release; mkdir -p "$OUT"
DESKTOP='[Desktop Entry]
Type=Application
Name=AI Anti-Duplicate
Comment=Поиск дубликатов фотографий с помощью ИИ
Exec=AI-Anti-Duplicate
Icon=ai-anti-duplicate
Categories=Graphics;Photography;
Terminal=false
StartupWMClass=AI-Anti-Duplicate'

# --- .deb ---
P=build/deb; rm -rf "$P"; mkdir -p "$P/DEBIAN" "$P/opt" "$P/usr/bin" "$P/usr/share/applications" "$P/usr/share/icons/hicolor/512x512/apps"
cp -r "$SRC" "$P/opt/ai-anti-duplicate"
ln -s /opt/ai-anti-duplicate/AI-Anti-Duplicate "$P/usr/bin/ai-anti-duplicate"
printf '%s\n' "$DESKTOP" | sed 's|^Exec=.*|Exec=/opt/ai-anti-duplicate/AI-Anti-Duplicate|' > "$P/usr/share/applications/ai-anti-duplicate.desktop"
cp assets/icon.png "$P/usr/share/icons/hicolor/512x512/apps/ai-anti-duplicate.png"
cat > "$P/DEBIAN/control" <<EOT
Package: ai-anti-duplicate
Version: $VER
Section: graphics
Priority: optional
Architecture: amd64
Maintainer: Nikolay Fedotov <noreply@github.com>
Depends: libgl1, libxkbcommon-x11-0, libxcb-cursor0
Description: Поиск дубликатов фотографий с помощью ИИ
 Сравнивает содержимое снимков (CLIP), а не размер и дату. Только копирует файлы.
EOT
dpkg-deb --build --root-owner-group "$P" "$OUT/AI-Anti-Duplicate-$VER-amd64.deb"

# --- AppImage ---
A=build/AppDir; rm -rf "$A"; mkdir -p "$A/usr/lib"
cp -r "$SRC" "$A/usr/lib/ai-anti-duplicate"
printf '%s\n' "$DESKTOP" > "$A/ai-anti-duplicate.desktop"
cp assets/icon.png "$A/ai-anti-duplicate.png"; cp assets/icon.png "$A/.DirIcon"
printf '#!/bin/sh\nHERE="$(dirname "$(readlink -f "$0")")"\nexec "$HERE/usr/lib/ai-anti-duplicate/AI-Anti-Duplicate" "$@"\n' > "$A/AppRun"; chmod +x "$A/AppRun"
[ -x build/appimagetool ] || { mkdir -p build; curl -fsSL -o build/appimagetool https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage; chmod +x build/appimagetool; }
ARCH=x86_64 build/appimagetool --appimage-extract-and-run "$A" "$OUT/AI-Anti-Duplicate-$VER-x86_64.AppImage"
ls -la "$OUT"
