"""
Open the default simple text editor and type text using pyautogui.

- Windows: Notepad
- macOS: TextEdit (plain-text via ``open -e``)
- Linux: gedit (install if missing)

Install: pip install pyautogui flask
"""

from __future__ import annotations

import atexit
import os
import platform
import subprocess
import sys
import tempfile
import time

import pyautogui

pyautogui.PAUSE = 0.25

DEFAULT_TEXT = """Hello from pyautogui!

This text was typed automatically.
"""

_mac_temp_txt: str | None = None


def _cleanup_mac_temp() -> None:
    global _mac_temp_txt
    if _mac_temp_txt and os.path.isfile(_mac_temp_txt):
        try:
            os.remove(_mac_temp_txt)
        except OSError:
            pass
        _mac_temp_txt = None


def _activate_textedit_mac() -> None:
    subprocess.run(
        ["osascript", "-e", 'tell application "TextEdit" to activate'],
        check=False,
        capture_output=True,
    )


def open_text_editor() -> None:
    global _mac_temp_txt
    system = platform.system()
    if system == "Windows":
        subprocess.Popen(["notepad.exe"])
    elif system == "Darwin":
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        _mac_temp_txt = path
        atexit.register(_cleanup_mac_temp)
        subprocess.Popen(["open", "-e", path])
        time.sleep(0.4)
        _activate_textedit_mac()
    else:
        subprocess.Popen(["gedit"])


def run_automation(text: str, *, interval: float = 0.02) -> None:
    """Open the OS text editor, wait for focus, then type ``text``."""
    open_text_editor()
    delay = 2.0 if platform.system() == "Darwin" else 1.5
    time.sleep(delay)
    pyautogui.write(text, interval=interval)


def main() -> None:
    run_automation(DEFAULT_TEXT)


if __name__ == "__main__":
    try:
        main()
    except pyautogui.FailSafeException:
        print("Stopped: mouse moved to screen corner (pyautogui failsafe).", file=sys.stderr)
        sys.exit(1)
