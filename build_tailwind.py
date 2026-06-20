"""
Rebuilds app/static/css/tailwind.css after you add/change utility classes in
any template. Tailwind is compiled ahead of time (not the Play CDN), so this
is the one step that needs re-running, the site itself has no build step.

Usage:
    python build_tailwind.py

Downloads the standalone Tailwind CLI (no Node/npm needed) into
./tailwindcss.exe the first time, then reuses it.
"""
import platform
import subprocess
import urllib.request
from pathlib import Path

VERSION = "v3.4.17"  # pinned to match what this project was built against
ROOT = Path(__file__).resolve().parent
BINARY = ROOT / ("tailwindcss.exe" if platform.system() == "Windows" else "tailwindcss")


def binary_url() -> str:
    system = platform.system()
    machine = platform.machine().lower()
    if system == "Windows":
        name = "tailwindcss-windows-x64.exe"
    elif system == "Darwin":
        name = "tailwindcss-macos-arm64" if "arm" in machine else "tailwindcss-macos-x64"
    else:
        name = "tailwindcss-linux-arm64" if "arm" in machine else "tailwindcss-linux-x64"
    return f"https://github.com/tailwindlabs/tailwindcss/releases/download/{VERSION}/{name}"


def main() -> None:
    if not BINARY.exists():
        print(f"Downloading Tailwind CLI {VERSION}...")
        urllib.request.urlretrieve(binary_url(), BINARY)
        BINARY.chmod(0o755)

    subprocess.run(
        [str(BINARY), "-i", "tailwind-input.css", "-o", "app/static/css/tailwind.css", "--minify"],
        cwd=ROOT, check=True,
    )
    print("Done: app/static/css/tailwind.css")


if __name__ == "__main__":
    main()
