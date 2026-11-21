"""PyInstaller build script — produces dist/rdr2-modmenu.exe."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "rdr2-modmenu",
        "--paths", str(ROOT / "src"),
        "--add-data", f"{ROOT / 'config'};config",
        "--add-data", f"{ROOT / 'src' / 'rdr2_modmenu' / 'script_hook'};script_hook",
        str(ROOT / "src" / "rdr2_modmenu" / "cli.py"),
    ]
    print(" ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())