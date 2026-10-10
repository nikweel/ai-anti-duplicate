#!/bin/sh
D="$(cd "$(dirname "$0")" && pwd)"
# Регистрируем приложение в меню системы (и ярлык в папке), пути обновляются при каждом запуске
[ -d "$D/runtime/venv" ] && T=false || T=true   # первый запуск показываем в терминале (идёт установка)
mkdir -p "$D/data/logs" "${XDG_DATA_HOME:-$HOME/.local/share}/applications"
cat > "$D/Photo-Duplicate-Finder-AI.desktop" <<EOT
[Desktop Entry]
Type=Application
Name=Photo Duplicate Finder AI
Comment=Поиск дубликатов фотографий с помощью ИИ
Exec="$D/start.sh"
Path=$D
Icon=$D/assets/icon.svg
Terminal=$T
Categories=Graphics;Photography;
EOT
chmod +x "$D/Photo-Duplicate-Finder-AI.desktop"
cp "$D/Photo-Duplicate-Finder-AI.desktop" "${XDG_DATA_HOME:-$HOME/.local/share}/applications/photo-duplicate-finder-ai.desktop"
export QT_LOGGING_RULES="qt.qpa.wayland.textinput=false"
if [ "$T" = false ]; then exec sh "$D/start.cmd" "$@" >> "$D/data/logs/launch.log" 2>&1; fi
exec sh "$D/start.cmd" "$@"
