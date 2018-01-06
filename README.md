﻿# AI Connect Four

This is a fork of an existing python-implementation of Connect Four from https://github.com/EpocDotFr/connectfour

## Improvements:
- Added faster win-condition checking (does not check the whole board after one chip has been played)
- Added an AI which plays random turns
- Added an AI which uses the MinMax-Algorithm
- Optimized Python Code with Cython

## Prerequisites

Python 3.6

## Installation

Clone this repo, and then the usual `pip install -r requirements.txt`.
Then run `bash cython_linux.sh` or `bash cython_windows.sh` dependant on your Operating System.
You can also start the game with python run.py --dev to start the cython_compiltation before starting
the game.

## Usage

```
pip install -r requirements.txt
python run.py --dev # decompiles
```

## Controls

  - <kbd>ESC</kbd> quits to the menu or close the game when already on the menu
  - <kbd>←</kbd> and <kbd>→</kbd> moves the chip respectively to the left and to the right
  - <kbd>↓</kbd> drops the chip in the selected column
  - <kbd>↵</kbd> starts a new game when one is finished
