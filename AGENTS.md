# KeyCodes

Two standalone GUI utilities that show the keycode a framework reports when you press a key. Qt (PySide6) and Pygame return different values for the same key. Users run the script that matches their framework.

## Gotchas

- Both scripts need a display. Under WSL, run them from Windows/PowerShell, or with a working WSLg/X server.
- `LICENSE` (0BSD) is authoritative. The `__license__` strings inside the scripts are stale and do not match it.

## Conventions

- `_version.py` is the single source of the version string. Do not set a version anywhere else.
- Keep the two scripts behaviorally consistent: print each event to the console and the window, and quit on double-Esc (any other key resets the Esc counter).
- The scripts share no code beyond `_version.py`. Keep each one self-contained.

## Build / test

- No tests, no linter config, no build step.
