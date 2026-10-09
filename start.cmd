:<<"::BATCH"
@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cd /d "%~dp0"
set "RT=%~dp0runtime"
set "UV_CACHE_DIR=%RT%\cache"
set "UV_PYTHON_INSTALL_DIR=%RT%\python"
set "UV_PROJECT_ENVIRONMENT=%RT%\venv"
set "UV_MANAGED_PYTHON=1"
if /i not "%~1"=="--hidden" if exist "%RT%\venv" if exist "%RT%\hidden.vbs" ( start "" wscript "%RT%\hidden.vbs" & exit /b )
if not exist "%RT%\uv.exe" (
  echo [AI Anti-Duplicate] Первый запуск: подготовка окружения, нужен интернет...
  mkdir "%RT%" 2>nul
  set "A=x86_64"
  if /i "%PROCESSOR_ARCHITECTURE%"=="ARM64" set "A=aarch64"
  powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; $u='https://github.com/astral-sh/uv/releases/latest/download/uv-!A!-pc-windows-msvc.zip'; Invoke-WebRequest $u -OutFile '%RT%\uv.zip'; Expand-Archive '%RT%\uv.zip' '%RT%\uvtmp' -Force; Copy-Item (Get-ChildItem '%RT%\uvtmp' -Recurse -Filter uv.exe | Select -First 1).FullName '%RT%\uv.exe'; Remove-Item '%RT%\uv.zip','%RT%\uvtmp' -Recurse -Force"
  if not exist "%RT%\uv.exe" ( echo Не удалось скачать uv. Проверьте интернет. & pause & exit /b 1 )
)
if /i "%~1"=="--hidden" goto :hidden
"%RT%\uv.exe" run --python 3.11 --project "%~dp0." python -m app.main
if errorlevel 1 pause
if exist "%RT%\venv" if not exist "%RT%\hidden.vbs" goto :makevbs
exit /b
:makevbs
echo CreateObject("WScript.Shell").Run "cmd /c ""%~f0"" --hidden", 0, False> "%RT%\hidden.vbs"
exit /b
:hidden
mkdir "%~dp0data\logs" 2>nul
"%RT%\uv.exe" run --python 3.11 --project "%~dp0." python -m app.main >> "%~dp0data\logs\launch.log" 2>&1
exit /b
::BATCH
cd "$(dirname "$0")" || exit 1
ROOT="$(pwd)"; RT="$ROOT/runtime"
export UV_CACHE_DIR="$RT/cache" UV_PYTHON_INSTALL_DIR="$RT/python" UV_PROJECT_ENVIRONMENT="$RT/venv" UV_MANAGED_PYTHON=1
if [ ! -x "$RT/uv" ]; then
  echo "[AI Anti-Duplicate] Первый запуск: подготовка окружения, нужен интернет..."
  mkdir -p "$RT"
  case "$(uname -m)" in arm64|aarch64) A=aarch64;; *) A=x86_64;; esac
  case "$(uname -s)" in
    Darwin) T="$A-apple-darwin";;
    *) T="$A-unknown-linux-gnu";;
  esac
  URL="https://github.com/astral-sh/uv/releases/latest/download/uv-$T.tar.gz"
  if command -v curl >/dev/null 2>&1; then curl -fsSL "$URL" -o "$RT/uv.tgz"; else wget -q "$URL" -O "$RT/uv.tgz"; fi
  tar -xzf "$RT/uv.tgz" -C "$RT" && cp "$RT/uv-$T/uv" "$RT/uv" && chmod +x "$RT/uv"
  rm -rf "$RT/uv.tgz" "$RT/uv-$T"
  [ -x "$RT/uv" ] || { echo "Не удалось скачать uv. Проверьте интернет."; read -r _; exit 1; }
fi
if [ "$(uname -s)" = Darwin ] && [ "$1" != --hidden ] && [ -d "$RT/venv" ]; then
  mkdir -p "$ROOT/data/logs"; nohup sh "$ROOT/start.cmd" --hidden >> "$ROOT/data/logs/launch.log" 2>&1 &
  osascript -e 'tell application "Terminal" to close front window' >/dev/null 2>&1; exit 0
fi
[ "$1" = --hidden ] && shift
"$RT/uv" run --python 3.11 --project "$ROOT" python -m app.main "$@" || { echo "Ошибка запуска, см. data/logs"; read -r _; }
