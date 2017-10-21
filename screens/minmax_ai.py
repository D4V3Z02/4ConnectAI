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


class GameMinmaxAI(ai.AIGame):
    def __init__(self, app):
        if (app is None):
            return
        print('Starting minmax game')
        Game.__init__(self, app)

    def update_ai_player(self) -> None:
        t1 = time.time()
        best_move, highest_move_score = self.evaluate_next_turn(self.board, settings.DEPTH, self.current_player)
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
        copied_board = self.copy_board(board)
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            # check if there is a free row in the current column
            if chip_row_stop >= 0:
                child_board = copy.copy(copied_board)
                # make a move in the copied board
                child_board[column][chip_row_stop] = ai_player.name
                possible_moves[column] = self.min(depth - 1, child_board,
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

    def copy_board(self, board: list) -> list:
        """
        copied_board = []
        for x in range(len(board)):
            copied_board.append(board[x][:])
        return copied_board
        """
        return [x[:] for x in board]

    def max(self, depth: int, board: list, ai_player: Player)-> int:
        # make all possible moves for the current player
        possible_moves = []
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                child_board = self.copy_board(board)
                child_board[column][chip_row_stop] = ai_player.name
                possible_moves.append(child_board)
        # end recursion if depth is reached or no moves possible
        if depth == 0 or len(possible_moves) == 0:
            """
            own, other = self.evaluate_board(board, ai_player), self.evaluate_board(board,
                                                                                    self.get_other_player(
                                                                                     ai_player))
            print('max', own, other)
            return own - other
            """
            return self.evaluate_board(board, ai_player)
        move_score = -999999999
        for child in possible_moves:
            min_ret = self.min(depth - 1, child, ai_player)
            print('min', min_ret)
            move_score = max(move_score, min_ret)
        return move_score

    def min(self, depth: int, board: list, ai_player: Player) -> int:
        possible_moves = []
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                child_board = self.copy_board(board)
                child_board[column][chip_row_stop] = self.get_other_player(ai_player).name
                print(child_board)
                possible_moves.append(child_board)
        # end recursion if depth is reached or no moves possible
        if depth == 0 or len(possible_moves) == 0:
            """
            own, other = self.evaluate_board(board, ai_player), self.evaluate_board(board, self.get_other_player(ai_player))
            print('min',own, other)
            return own - other
            """
            return self.evaluate_board(board, ai_player)
        move_score = 999999999
        for child in possible_moves:
            max_ret = self.max(depth - 1, child, ai_player)
            print('max', max_ret)
            move_score = min(move_score, max_ret)
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

    def get_move_score(self, chip_count: int, column: int) -> int:
        move_score = 0
        multiplier = 1
        if column >= 2 and column <= 4:
            multiplier = settings.MIDDLE_MULTIPLIER
        if chip_count == 1:
            move_score = settings.CHIP_COUNT_1_MULTIPLIER * multiplier
        elif chip_count == 2:
            move_score = settings.CHIP_COUNT_2_MULTIPLIER * multiplier
        elif chip_count == 3:
            move_score = settings.CHIP_COUNT_3_MULTIPLIER * multiplier
        elif chip_count >= 4:
            move_score = settings.CHIP_COUNT_4_MULTIPLIER * multiplier
        return move_score

    def evaluate_columns(self, board: dict, current_player: Player) -> int:
        move_score = 0
        # Check each columns from left to right
        for x in range(settings.COLS):
            consecutive_chips = 0
            previous_chip = None
            for y in range(0, settings.ROWS):
                cell = board[x][y]
                if cell == current_player.name and consecutive_chips == 0:
                    consecutive_chips = 1
                    print(consecutive_chips)
                elif cell == current_player.name and cell == previous_chip:
                    consecutive_chips += 1
                elif cell != current_player.name:
                    move_score += self.get_move_score(consecutive_chips, x)
                    consecutive_chips = 0
                previous_chip = cell
            move_score += self.get_move_score(consecutive_chips, x)
        return move_score

    def evaluate_rows(self, board: dict, current_player: Player) -> int:
        move_score = 0
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
                    move_score += self.get_move_score(consecutive_chips, x)
                    print(move_score)
                    consecutive_chips = 0
                previous_chip = cell
            move_score += self.get_move_score(consecutive_chips, x)
        return move_score

    def evaluate_board(self, board: dict, current_player: Player) -> int:
        """Scores the passed board for the ai"""
        move_score = self.evaluate_columns(board, current_player)
        move_score += self.evaluate_rows(board, current_player)
        # Check each "/" diagonal starting at the top left corner
        x = 0
        for y in range(settings.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board, current_player)
            move_score += self.get_move_score(consecutive_chips, x)
        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = settings.ROWS - 1
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board, current_player)
            move_score += self.get_move_score(consecutive_chips, x)
        # Check each "\" diagonal starting at the bottom left corner
        x = 0
        for y in range(settings.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board, current_player)
            move_score += self.get_move_score(consecutive_chips, x)
        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board, current_player)
            move_score += self.get_move_score(consecutive_chips, x)
        #enemy_chips_in_a_row = self.get_amount_of_enemy_chips_in_a_row(board, current_player)
        #print(enemy_chips_in_a_row)
        return move_score

    def get_amount_of_enemy_chips_in_a_row(self, board: dict, current_player: Player, boarder=3) -> list:
        enemy_player = self.get_other_player(current_player)
        consecutive_chip_counts = []
        # Check each columns from left to right
        for x in range(0, settings.COLS):
            consecutive_chips = 0
            previous_chip = None
            for y in range(0, settings.ROWS):
                cell = board[x][y]
                if cell == enemy_player.name and consecutive_chips == 0:
                    self.current_consecutive_chips.append((x, y))
                    consecutive_chips = 1
                elif cell == enemy_player.name and cell == previous_chip:
                    self.current_consecutive_chips.append((x, y))
                    consecutive_chips += 1
                elif cell != enemy_player.name:
                    consecutive_chips = 0
                if consecutive_chips >= boarder:
                    consecutive_chip_counts.append(consecutive_chips)
                previous_chip = cell
        # Check each rows from top to bottom
        for y in range(0, settings.ROWS):
            consecutive_chips = 0
            previous_chip = None
            for x in range(0, settings.COLS):
                cell = board[x][y]
                if cell == enemy_player.name and consecutive_chips == 0:
                    self.current_consecutive_chips.append((x, y))
                    consecutive_chips = 1
                elif cell == enemy_player.name and cell == previous_chip:
                    self.current_consecutive_chips.append((x, y))
                    consecutive_chips += 1
                elif cell != enemy_player.name:
                    consecutive_chips = 0
                if consecutive_chips >= boarder:
                    consecutive_chip_counts.append(consecutive_chips)
                previous_chip = cell
        # Check each "/" diagonal starting at the top left corner
        x = 0
        for y in range(0, settings.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board, enemy_player)
            if consecutive_chips >= boarder:
                consecutive_chip_counts.append(consecutive_chips)
        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = settings.ROWS - 1
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board, enemy_player)
            if consecutive_chips >= boarder:
                consecutive_chip_counts.append(consecutive_chips)
        # Check each "\" diagonal starting at the bottom left corner
        x = 0
        for y in range(settings.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board, enemy_player)
            if consecutive_chips >= boarder:
                consecutive_chip_counts.append(consecutive_chips)
        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board, enemy_player)
            if consecutive_chips >= boarder:
                consecutive_chip_counts.append(consecutive_chips)
        return consecutive_chip_counts

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
    board = [[None, None, None, None, 'Yellow', 'Red'],
             [None, None, None, None, None, 'Yellow'],
             [None, None, None, None, None, 'Yellow'],
             [None, None, None, None, None, 'Yellow'],
             [None, None, None, None, None, 'Yellow'],
             [None, None, None, None, None, 'Yellow'],
             [None, 'Yellow', 'Red', 'Yellow', 'Red', 'Yellow']]
    print([x[:] for x in board])
    ai_game = GameMinmaxAI(None)
    print(ai_game.get_free_row(6, board=board))
    print(ai_game.copy_board(board))
    #red = objects.RedPlayer()
    #yellow = objects.YellowPlayer()
    #ai_game.current_player = yellow
    #ai_game.current_opponent = red
    #print(ai_game.evaluate_board(board))
