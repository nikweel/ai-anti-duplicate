#!/bin/sh
# Использование: packaging/linux.sh <версия>  (после pyinstaller; dist/Photo-Duplicate-Finder-AI)
set -e
VER="${1:-0.0.0}"; SRC=dist/Photo-Duplicate-Finder-AI; OUT=release; mkdir -p "$OUT"
DESKTOP='[Desktop Entry]
Type=Application
Name=Photo Duplicate Finder AI
Comment=Поиск дубликатов фотографий с помощью ИИ
Exec=Photo-Duplicate-Finder-AI
Icon=photo-duplicate-finder-ai
Categories=Graphics;Photography;
Terminal=false
StartupWMClass=Photo-Duplicate-Finder-AI'

# --- .deb ---
P=build/deb; rm -rf "$P"; mkdir -p "$P/DEBIAN" "$P/opt" "$P/usr/bin" "$P/usr/share/applications" "$P/usr/share/icons/hicolor/512x512/apps"
cp -r "$SRC" "$P/opt/photo-duplicate-finder-ai"
ln -s /opt/photo-duplicate-finder-ai/Photo-Duplicate-Finder-AI "$P/usr/bin/photo-duplicate-finder-ai"
printf '%s\n' "$DESKTOP" | sed 's|^Exec=.*|Exec=/opt/photo-duplicate-finder-ai/Photo-Duplicate-Finder-AI|' > "$P/usr/share/applications/photo-duplicate-finder-ai.desktop"
cp assets/icon.png "$P/usr/share/icons/hicolor/512x512/apps/photo-duplicate-finder-ai.png"
cat > "$P/DEBIAN/control" <<EOT
Package: photo-duplicate-finder-ai
Version: $VER
Section: graphics
Priority: optional
Architecture: amd64
Maintainer: Nikolay Fedotov <noreply@github.com>
Depends: libgl1, libxkbcommon-x11-0, libxcb-cursor0
Description: Поиск дубликатов фотографий с помощью ИИ
 Сравнивает содержимое снимков (CLIP), а не размер и дату. Только копирует файлы.
EOT
dpkg-deb --build --root-owner-group "$P" "$OUT/Photo-Duplicate-Finder-AI-$VER-amd64.deb"

# --- AppImage ---
A=build/AppDir; rm -rf "$A"; mkdir -p "$A/usr/lib"
cp -r "$SRC" "$A/usr/lib/photo-duplicate-finder-ai"
printf '%s\n' "$DESKTOP" > "$A/photo-duplicate-finder-ai.desktop"
cp assets/icon.png "$A/photo-duplicate-finder-ai.png"; cp assets/icon.png "$A/.DirIcon"
printf '#!/bin/sh\nHERE="$(dirname "$(readlink -f "$0")")"\nexec "$HERE/usr/lib/photo-duplicate-finder-ai/Photo-Duplicate-Finder-AI" "$@"\n' > "$A/AppRun"; chmod +x "$A/AppRun"
[ -x build/appimagetool ] || { mkdir -p build; curl -fsSL -o build/appimagetool https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage; chmod +x build/appimagetool; }
ARCH=x86_64 build/appimagetool --appimage-extract-and-run "$A" "$OUT/Photo-Duplicate-Finder-AI-$VER-x86_64.AppImage"
ls -la "$OUT"
