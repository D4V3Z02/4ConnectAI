#!/usr/bin/env bash
# Shell script to build the Connect Four Linux executable.
# The resulting "connectfour_linux" script will be available in the "dist" directory.
#bash cython_linux.sh
bash cython_linux.sh
pyinstaller \
    --noconfirm \
    --log-level=WARN \
    --name="connectfour_linux" \
    --add-data="resources:resources" \
    run.py

find . -name \*.so -exec cp {} ./dist/connectfour_linux \;
#mkdir ./dist/connectfour_linux/networking
#find ./networking -name \*.py -exec cp {} ./dist/connectfour_linux/networking \;
mkdir ./dist/connectfour_linux/screens
find ./screens -name \*.so -exec cp {} ./dist/connectfour_linux/screens \;
find ./screens -name \*.py -exec cp {} ./dist/connectfour_linux/screens \;
cp **.py ./dist/connectfour_linux/