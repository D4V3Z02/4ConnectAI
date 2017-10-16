from screens import menu
from collections import deque
import objects
import pygame
import settings
import utils
import logging
import sys
from screens.game import Game
import copy


class GameAgainstAI(Game):
    def __init__(self, app):
        Game.__init__(self, app)

    def update_while_playing(self) -> None:
        if not self.current_player_chip:
            self.current_player_chip = self.current_player.chip()
            self.chips.add(self.current_player_chip)
            self.current_player_chip.rect.left = 0
            self.current_player_chip.rect.top = settings.COLUMN_CHOOSING_MARGIN_TOP
        if self.is_ai_playing():
            self.update_ai_player()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not self.is_ai_playing():
                self.execute_operation_while_playing(event.key)
            elif event.type == pygame.KEYDOWN and self.is_ai_playing() and event.key == pygame.K_ESCAPE:
                self.navigate_to_menu()
        self.status_text = self.current_player.name + ' player\'s turn'
        self.status_color = self.current_player.color

    def update_ai_player(self) -> None:
        self.place_chip_ai(self.evaluate_next_turn(copy.deepcopy(self.board)))

    def evaluate_next_turn(self, board: dict):
        #print(board)
        # iterate over possible placements
        for key, value in board.items():
            if self.get_free_row(key) >= 0:
                print('return', key)
                return key
        return 2

    def place_chip_ai(self, column) -> None:
        for i in range(column):
            print("test")
            self.move_chip_right()
        self.place_chip()
        """
        self.current_player_chip.rect.right += settings.IMAGES_SIDE_SIZE*column
        self.current_player_chip_column = column
        self.place_chip(column=column)
        """

    def is_ai_playing(self) -> bool:
        return self.current_player.name == settings.PLAYER_YELLOW_NAME
