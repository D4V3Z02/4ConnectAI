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
import time
from screens import ai


DEPTH = 10


class GameMinmaxAI(ai.AIGame):
    def __init__(self, app):
        if (app is None):
            return
        print('Starting minmax game')
        Game.__init__(self, app)

    def update_ai_player(self) -> None:
        t1 = time.time()
        best_move, highest_move_score = self.evaluate_next_turn(self.board, DEPTH, self.current_player)
        self.place_chip_ai(best_move)
        print('ai turn took',  time.time() - t1)
        print('Move Chosen:', best_move, 'Move Score', highest_move_score)

    def evaluate_next_turn(self, board: dict, depth: int, ai_player: Player) -> int:
        """
        Returns the column of the best move
        :param board: the current board
        :param depth: the depth of the search
        """
        # iterate over possible placements
        possible_moves = {}
        copied_board = copy.deepcopy(board)
        for column, value in board.items():
            child_board = copy.copy(copied_board)
            chip_row_stop = self.get_free_row(column, board=child_board)
            # check if there is a free row in the current column
            if chip_row_stop >= 0:
                # make a move in the copied board
                child_board[column][chip_row_stop] = ai_player.name
                possible_moves[column] = self.max(depth - 1, child_board,
                                                               ai_player)
        highest_move_score = -99999999
        best_move = None
        moves = list(possible_moves.items())
        random.shuffle(moves)
        for move, move_score in moves:
            if move_score >= highest_move_score:
                highest_move_score = move_score
                best_move = move
        return best_move, highest_move_score

    def max(self, depth: int, board: dict, player: Player):
        # make all possible moves for the current player
        possible_moves = []
        for column, value in board.items():
            child_board = copy.copy(board)
            chip_row_stop = self.get_free_row(column, board=child_board)
            if chip_row_stop >= 0:
                child_board[column][chip_row_stop] = player.name
                possible_moves.append(child_board)
        # end recursion if depth is reached or no moves possible
        if depth == 0 or len(possible_moves) == 0:
            return self.evaluate_board(board, player)
        move_score = -99999999
        for child in possible_moves:
            move_score = max(move_score, self.min(depth-1, child, player))
        return move_score

    def min(self, depth: int, board: dict, player: Player):
        possible_moves = []
        for column, value in board.items():
            child_board = copy.copy(board)
            chip_row_stop = self.get_free_row(column, board=child_board)
            if chip_row_stop >= 0:
                child_board[column][chip_row_stop] = player.name
                possible_moves.append(child_board)
        # end recursion if depth is reached or no moves possible
        if depth == 0 or len(possible_moves) == 0:
            return self.evaluate_board(board, player)
        move_score = 99999999
        for child in possible_moves:
            move_score = min(move_score, self.max(depth - 1, child, player))
        return move_score

    def get_other_player(self, player: Player) -> Player:
        if player.id == self.current_player.id:
            return self.current_opponent
        else:
            return self.current_player

    def place_chip_ai(self, column) -> None:
        for i in range(column):
            self.move_chip_right()
        self.place_chip()

    def is_ai_playing(self) -> bool:
        return self.current_player.id == 2

    def get_move_score(self, chip_count: int) -> int:
        move_score = 0
        if chip_count == 1:
            move_score = 1e2
        elif chip_count == 2:
            move_score = 1e3
        elif chip_count == 3:
            move_score = 1e4
        elif chip_count >= 4:
            move_score = 1e8
            print('ret BIG')
        #print(move_score)
        return move_score

    def evaluate_board(self, board: dict, current_player: Player) -> int:
        """Scores the passed board for the ai"""
        move_score = 0
        # Check each columns from left to right
        for x in range(settings.COLS):
            consecutive_chips = 0
            previous_chip = None
            for y in range(0, settings.ROWS):
                cell = board[x][y]
                if cell == current_player.name and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == current_player.name and cell == previous_chip:
                    consecutive_chips += 1
                elif cell != current_player.name:
                    move_score += self.get_move_score(consecutive_chips)
                    consecutive_chips = 0
                previous_chip = cell
        # Check each rows from top to bottom
        for y in range(settings.ROWS):
            consecutive_chips = 0
            previous_chip = None
            for x in range(settings.COLS):
                cell = board[x][y]
                if cell == current_player.name and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == current_player.name and cell == previous_chip:
                    consecutive_chips += 1
                elif cell != current_player.name:
                    move_score += self.get_move_score(consecutive_chips)
                    consecutive_chips = 0
                previous_chip = cell
        # Check each "/" diagonal starting at the top left corner
        x = 0
        for y in range(settings.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board, current_player)
            move_score += self.get_move_score(consecutive_chips)
        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = settings.ROWS - 1
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board, current_player)
            move_score += self.get_move_score(consecutive_chips)
        # Check each "\" diagonal starting at the bottom left corner
        x = 0
        for y in range(settings.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board, current_player)
            move_score += self.get_move_score(consecutive_chips)
        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board, current_player)
            move_score += self.get_move_score(consecutive_chips)
        return move_score

    def count_consecutive_diagonal_chips(self, consecutive_chips, previous_chip, x, y, direction,
                                         board: dict, current_player: Player) -> int:
        if not self.is_valid_position(x, y):
            return consecutive_chips
        cell = board[x][y]
        if cell == current_player.name and consecutive_chips == 0:
            consecutive_chips = 1
        elif cell == current_player.name and cell == previous_chip:
            consecutive_chips += 1
        elif cell != current_player.name:
            consecutive_chips = 0
        if consecutive_chips == 4:
            return consecutive_chips
        x, y = self.compute_direction_pos(x, y, direction)
        previous_chip = cell
        return self.count_consecutive_diagonal_chips(consecutive_chips, previous_chip, x, y,
                                                     direction, board, current_player)

    def compute_direction_pos(self, x, y, direction):
        x = x + abs(direction[0]) if direction[0] > 0 else x - abs(direction[0])
        y = y + abs(direction[1]) if direction[1] > 0 else y - abs(direction[1])
        return x, y

if __name__ == "__main__":
    board = {
        0: {0: None, 1: None, 2: None, 3: 'Red', 4: 'Red', 5: 'Red'},
        1: {0: None, 1: None, 2: None, 3: None, 4: 'Red', 5: 'Yellow'},
        2: {0: None, 1: None, 2: None, 3: None, 4: None, 5: 'Red'},
        3: {0: None, 1: None, 2: None, 3: None, 4: None, 5: 'Red'},
        4: {0: None, 1: None, 2: None, 3: None, 4: None, 5: 'Red'},
        5: {0: None, 1: None, 2: None, 3: None, 4: 'Red', 5: 'Yellow'},
        6: {0: None, 1: None, 2: None, 3: None, 4: 'Red', 5: 'Red'}}
    ai_game = GameMinmaxAI(None)
    red = objects.RedPlayer()
    yellow = objects.YellowPlayer()
    ai_game.current_player = yellow
    ai_game.current_opponent = red
    print(ai_game.evaluate_board(board))
