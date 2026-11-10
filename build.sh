#! /bin/bash
# will work only for Linux, but not for Windows
# 
set -e

rm -rf build dist

pyinstaller pac-man.py \
    --name pacman \
    --onedir \
    --add-data "assets:assets" \
    --add-data "config.json:." \
    --collect-all your_amazing_package

# Include the in-package instructions the subject asks for
cp README_GAME.txt dist/pacman/README.txt