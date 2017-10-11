This is a continuation of an existing python-implementation of 4connect https://github.com/EpocDotFr/connectfour/issues .

It contains currently a faster checking of the win condition after a player finished a turn and is going to get it's own AI.

# Connect Four

The [Connect Four](https://en.wikipedia.org/wiki/Connect_Four) game, implemented in Python.

<p align="center">
  <img src="https://raw.githubusercontent.com/EpocDotFr/connectfour/master/screenshot.png">
</p>

## Features

  - All the Connect Four rules
  - State of the art graphics
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