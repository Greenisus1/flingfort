# Flingfort

An original fullscreen, color terminal slingshot game. Launch stone balls at block towers and knock out green targets. Supports SSH, no desktop or external Python packages required. Original name, art and code; no Angry Birds assets or branding.

Adjust angle with A/D or Left/Right, power with W/S or Up/Down, Space to fire. R restarts, N advances after clearing the fort, P pauses, Q quits. The dotted arc previews the opening flight, not the entire landing. Towers have simple support-collapse physics, not a realistic rigid-body simulation. Seven shots per level; unlimited retries and increasing forts.

## Run

`python3 flingfort.py` in a terminal at least 70 columns x 22 rows. Smaller screens show a resize prompt rather than broken layout. Pi App Store discovers this repository in Games using app-store.sh. The installer checks Python/curses and installs Debian Python only when needed. No network downloads or pip packages at launch.

Linux physics tests and real pseudo-terminal resize/quit checks passed. Raspberry Pi hardware gameplay is not yet tested. MIT, copyright 2026 Greenisus1.
