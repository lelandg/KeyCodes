Now Pygame and Qt keycodes are easily accessible. Yes, they return different values, so you need to code for your platform. Or maybe use the keyboard module instead of platform-specific stuff. Oh! I should write a console version that uses only that. ;-)

Requires Python 3.10 to 3.14. PySide6 provides wheels for Windows (x64 or ARM64), macOS 13 or newer, and Linux with glibc 2.34 or newer (2.39 on ARM64). Run:

`pip install -r requirements.txt`

Then:

`python keycodes_qt.py`

Or:

`python keycodes_pygame.py`

Happy coding!
