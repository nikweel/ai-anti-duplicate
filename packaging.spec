# PyInstaller: pyinstaller packaging.spec
import sys

a = Analysis(
    ["run_app.py"],
    pathex=["."],
    datas=[("assets", "assets")],
    excludes=["tkinter", "PySide6.QtWebEngineCore", "PySide6.QtNetwork", "PySide6.QtQml", "PySide6.QtQuick",
              "PySide6.QtPdf", "PySide6.QtOpenGL", "torch", "matplotlib", "scipy", "pandas"],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="Photo-Duplicate-Finder-AI", console=False,
          icon="assets/icon.ico" if sys.platform == "win32" else None)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="Photo-Duplicate-Finder-AI")
if sys.platform == "darwin":
    app = BUNDLE(coll, name="Photo-Duplicate-Finder-AI.app", icon="assets/icon.icns", bundle_identifier="ru.nikweel.photoduplicatefinderai")
