cimport screens.game as game
import settings
import pygame
import sys
import time


cdef class AIGame(game.Game):
    cpdef update_while_playing(self)
    cdef update_ai_player(self)