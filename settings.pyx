from enum import Enum
import pygame
import sys
import gui
import utils
from cpython cimport bool


class GuiTheme(gui.DefaultTheme):
    def __init__(self, sounds_volume=0.5):
        gui.DefaultTheme.__init__(self)
        self.click_sound = utils.load_sound('click.wav', volume=sounds_volume)


class Colors(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 174, 0),
    BLUE = (0, 42, 224)


class GameStates(Enum):
    PLAYING = 2
    WON = 4
    NO_ONE_WIN = 6
    AI = 8


class Events(Enum):
    WINNER_CHIPS_EVENT = pygame.USEREVENT + 1
    GET_ONLINE_GAMES = pygame.USEREVENT + 2
    CLEAN_LAN_GAMES = pygame.USEREVENT + 3


class LobbyStates(Enum):
    HOST_ONLINE_GAME = 2
    HOST_LAN_GAME = 4
    JOIN_ONLINE_GAME = 6
    JOIN_LAN_GAME = 8


class NetworkEngineMode(Enum):
    HOST = 2
    JOIN = 4


# When frozen by PyInstaller, the path to the resources is different
RESOURCES_ROOT = 'resources' if getattr(sys, 'frozen', False) else 'resources'
VERSION = '1.2'
LAN_IDENTIFIER = '51af46a9396f46cdae0eedc4efa9d7a1'

cdef list MUSIC_LIST = ['techno_dreaming.wav', 'techno_celebration.wav', 'electric_rain.wav', 'snake_trance.wav']
cdef short FPS = 30
cdef short IMAGES_SIDE_SIZE = 80
cdef short COLS = 7
cdef short ROWS = 6

cdef short COLUMN_CHOOSING_MARGIN_TOP = 50
cdef short BOARD_MARGIN_TOP = IMAGES_SIDE_SIZE + COLUMN_CHOOSING_MARGIN_TOP
cdef tuple WINDOW_SIZE = (IMAGES_SIDE_SIZE * COLS, (IMAGES_SIDE_SIZE * ROWS) + BOARD_MARGIN_TOP)
cdef short LAN_PORT = 2560
cdef short LAN_TIMEOUT = 5
cdef str CONFIG_FILE = 'connectfour.ini'
cdef dict DEFAULT_CONFIG = {
    'master_server_endpoint': 'https://cfms.epoc.fr/api/',
    'sounds_volume': 0.1,
    'music_volume': 0.2,
    'game_name': ''
}
cdef str PLAYER_RED_NAME = 'RED'
cdef short PLAYER_RED_ID = 1
cdef str PLAYER_YELLOW_NAME = 'YELLOW'
cdef short PLAYER_YELLOW_ID = 2
cdef bool EMPTY_SYMBOL = False
cdef str RED_CHIP_IMAGE = 'red_chip.png'
cdef str YELLOW_CHIP_IMAGE = 'yellow_chip.png'
cdef str GAME_NAME = 'AI Connect Four v'
cdef short MAX_DEPTH = 5
cdef short MAX_DEPTH_AB = 7
cdef short MIDDLE_MULTIPLIER = 2
cdef long CHIP_COUNT_1_MULTIPLIER = 10
cdef long CHIP_COUNT_2_MULTIPLIER = 100
cdef long CHIP_COUNT_3_MULTIPLIER = 1000
cdef long CHIP_COUNT_4_MULTIPLIER = 100000
cdef long BIG_VALUE = 999999999
