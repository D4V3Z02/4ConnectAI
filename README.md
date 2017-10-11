# AI Connect Four

This is a continuation of an existing python-implementation of 4connect https://github.com/EpocDotFr/connectfour/issues

## Improvements:
- Added faster win-condition checking (does not check the whole board after one chip has been played)

## TODO:

- This game is going to get an AI-opponent

# Connect Four

The [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) game, implemented in Python.

<p align="center">
  <img src="https://raw.githubusercontent.com/EpocDotFr/connectfour/master/screenshot.png">
</p>

## Features

  - All the Connect Four rules
  - Chips that made the player win are highlighted
  - Sound effects!
  - Musics!
  - Two players, either:
    - On the same computer
    - (WIP) LAN game
    - (WIP) Online game

## Prerequisites

Python 3.6

## Installation

Clone this repo, and then the usual `pip install -r requirements.txt`.

## Usage

```
python run.py [--dev]
```

`--dev` enable WIP features (like network games).

## Controls

  - <kbd>ESC</kbd> quits to the menu or close the game when already on the menu
  - <kbd>←</kbd> and <kbd>→</kbd> moves the chip respectively to the left and to the right
  - <kbd>↓</kbd> drops the chip in the selected column
  - <kbd>↵</kbd> starts a new game when one is finished

## Credits

- EpocDotFr for letting me use his existing source code and assets