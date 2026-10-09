#!/bin/sh
D="$(cd "$(dirname "$0")" && pwd)"
# Регистрируем приложение в меню системы (и ярлык в папке), пути обновляются при каждом запуске
[ -d "$D/runtime/venv" ] && T=false || T=true   # первый запуск показываем в терминале (идёт установка)
mkdir -p "$D/data/logs" "${XDG_DATA_HOME:-$HOME/.local/share}/applications"
cat > "$D/AI-Anti-Duplicate.desktop" <<EOT
[Desktop Entry]
Type=Application
Name=AI Anti-Duplicate
Comment=Поиск дубликатов фотографий с помощью ИИ
Exec="$D/start.sh"
Path=$D
Icon=$D/assets/icon.svg
Terminal=$T
Categories=Graphics;Photography;
EOT
chmod +x "$D/AI-Anti-Duplicate.desktop"
cp "$D/AI-Anti-Duplicate.desktop" "${XDG_DATA_HOME:-$HOME/.local/share}/applications/ai-anti-duplicate.desktop"
export QT_LOGGING_RULES="qt.qpa.wayland.textinput=false"
if [ "$T" = false ]; then exec sh "$D/start.cmd" "$@" >> "$D/data/logs/launch.log" 2>&1; fi
exec sh "$D/start.cmd" "$@"
