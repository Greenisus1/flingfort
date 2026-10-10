#!/bin/bash
# pi-app-store: 1
# pi-app-store-category: games
set -eu
cd -- "$(dirname -- "$0")"
case "${1:-run}" in
 install) command -v python3 >/dev/null || { [ "$(id -u)" -eq 0 ] || exit 1; apt-get update; apt-get install -y python3; }
 python3 -c 'import curses' || { echo 'Python curses is required. Install your distro Python curses package.'; exit 1; }
 echo 'Flingfort ready. Run it from Installed apps.' ;;
 status) command -v python3 >/dev/null && python3 -c 'import curses' ;;
 run) exec python3 flingfort.py ;;
 *) echo 'Use install, status or run';exit 2 ;;
esac
