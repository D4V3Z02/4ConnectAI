from screens import menu
from collections import deque
import objects
import pygame
import settings
import utils
import logging
import sys
from screens.game import Game


class GameAgainstAI(Game):
    def __init__(self, app):
        Game.__init__(self, app)

    def update(self) -> None:
        self.draw_background()
        self.execute_update_dependant_on_state()
        self.draw_header(self.status_text, self.status_color)
        self.chips.draw(self.app.window)
        self.draw_board()

    def update_while_playing(self) -> None:
        if not self.current_player_chip:
            self.current_player_chip = self.current_player.chip()
            self.chips.add(self.current_player_chip)
            self.current_player_chip.rect.left = 0
            self.current_player_chip.rect.top = settings.COLUMN_CHOOSING_MARGIN_TOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.execute_operation_while_playing(event.key)
        self.status_text = self.current_player.name + ' player\'s turn'
        self.status_color = self.current_player.color