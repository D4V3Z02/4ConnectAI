#!/usr/bin/env bash
bash cython_windows.sh
pyinstaller --noconfirm --debug --log-level=WARN --name="connectfour_windows" --icon="resources/images/icon.ico" connectfour_windows.spec
cp *.pyd ./dist/connectfour_windows
mkdir ./dist/connectfour_windows/networking
cp networking/*.py ./dist/connectfour_windows/networking
