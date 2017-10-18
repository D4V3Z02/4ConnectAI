from screens import menu
from collections import deque
import objects
from objects import Player
import pygame
import settings
import utils
import logging
import sys
import objects
from screens.game import Game
import copy
import random


class RandomAI(Game):
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
        best_move, highest_move_score = self.evaluate_next_turn(self.board, 5, self.current_player, self.current_opponent)
        self.place_chip_ai(best_move)
        print('AI move:', best_move, highest_move_score)

    def evaluate_next_turn(self, board: dict, depth: int, current_player: Player, current_opponent: Player) -> int:
        """
        Returns the column of the best move
        :param board: the current board
        :param depth: the depth of the search
        """
        # iterate over possible placements
        possible_moves = {}
        copied_board = copy.deepcopy(board)
        for column, value in board.items():
            child_board = copy.deepcopy(copied_board)
            chip_row_stop = self.get_free_row(column, board=child_board)
            # check if there is a free row in the current column
            if chip_row_stop >= 0:
                # make a move in the copied board
                child_board[column][chip_row_stop] = current_player.name
                possible_moves[column] = self.recursive_search(depth-1, child_board, current_opponent)
        highest_move_score = -99999999
        best_move = None
        moves = list(possible_moves.items())
        random.shuffle(moves)
        for move, alpha in moves:
            if alpha >= highest_move_score:
                highest_move_score = alpha
                best_move = move
        return best_move, highest_move_score

    def recursive_search(self, depth: int, board: dict, player: Player):
        return 0

    def place_chip_ai(self, column) -> None:
        for i in range(column):
            self.move_chip_right()
        self.place_chip()
        """
        self.current_player_chip.rect.right += settings.IMAGES_SIDE_SIZE*column
        self.current_player_chip_column = column
        self.place_chip(column=column)
        """

    def is_ai_playing(self) -> bool:
        return self.current_player.name == settings.PLAYER_YELLOW_NAME

    def evaluate_board(self, board: dict) -> int:
        """Scores the passed board for the ai"""
        score = 0
        # Check each columns from left to right
        for x in range(0, settings.COLS):
            consecutive_chips = 0
            previous_chip = None
            for y in range(0, settings.ROWS):
                cell = board[x][y]
                if cell == self.current_player.name and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == self.current_player.name and cell == previous_chip:
                    consecutive_chips += 1
                elif cell != self.current_player.name:
                    consecutive_chips = 0
                previous_chip = cell
        # Check each rows from top to bottom
        for y in range(0, settings.ROWS):
            consecutive_chips = 0
            previous_chip = None
            for x in range(0, settings.COLS):
                cell = board[x][y]
                if cell == self.current_player.name and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == self.current_player.name and cell == previous_chip:
                    consecutive_chips += 1
                elif cell != self.current_player.name:
                    consecutive_chips = 0
                previous_chip = cell
        # Check each "/" diagonal starting at the top left corner
        x = 0
        for y in range(0, settings.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1))
            if consecutive_chips == 4:
                return True
        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = settings.ROWS - 1
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1))
        # Check each "\" diagonal starting at the bottom left corner
        x = 0
        for y in range(settings.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1))
        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1))
        return False

    def count_consecutive_diagonal_chips(self, consecutive_chips, previous_chip, x, y, direction,
                                         board) -> int:
        if not self.is_valid_position(x, y):
            return consecutive_chips
        cell = board[x][y]
        if cell == self.current_player.name and consecutive_chips == 0:
            self.current_consecutive_chips.append((x, y))
            consecutive_chips = 1
        elif cell == self.current_player.name and cell == previous_chip:
            self.current_consecutive_chips.append((x, y))
            consecutive_chips += 1
        elif cell != self.current_player.name:
            consecutive_chips = 0
        if consecutive_chips == 4:
            return consecutive_chips
        x, y = self.compute_direction_pos(x, y, direction)
        previous_chip = cell
        return self.count_consecutive_diagonal_chips(consecutive_chips, previous_chip, x, y,
                                                     direction)
