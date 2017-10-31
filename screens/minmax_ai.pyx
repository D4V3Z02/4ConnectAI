import screens.menu as menu
from collections import deque
from objects import Player
from objects cimport Player
import settings
cimport settings
import utils
import logging
import sys
import objects
cimport objects
from screens.game import Game
import copy
import random
cimport screens.ai as ai
import screens.ai as ai
from cpython cimport bool


INF = 999999999


cdef class GameMinmaxAI(ai.AIGame):
    def __init__(self, app):
        if (app is None):
            return
        print('Starting minmax game')
        Game.__init__(self, app)

    cpdef Move min_max(self, list board, int depth, Player ai_player):
        """
        Returns the column of the best move
        :param board: the current board
        :param depth: the depth of the search
        """
        # iterate over possible placements
        cdef dict possible_moves = {}
        cdef list copied_board, child_board
        cdef long move_score = 0
        copied_board = self.copy_board(board)
        return self.max_turn(0, copied_board, ai_player, -1)

    cdef list copy_board(self, list board):
        return [x[:] for x in board]

    cdef Move max_turn(self, int depth, list board, Player ai_player, short current_column):
        # make all possible moves for the current player
        cdef list child_board, possible_moves = []
        cdef int chip_row_stop = 0
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                child_board = self.copy_board(board)
                child_board[column][chip_row_stop] = ai_player.id
                possible_moves.append(PotentialMove(child_board, column))
        # end recursion if depth is reached or no moves possible
        if depth == settings.DEPTH or len(possible_moves) == 0 or self.did_someone_win(board, ai_player):
            return Move(self.evaluate_board(board, ai_player, depth), current_column)
        cdef Move move = Move(-INF, 0)
        cdef Move min_move
        for possible_move in possible_moves:
            min_move = self.min_turn(depth + 1, possible_move.board, ai_player, possible_move.column)
            if min_move.score > move.score:
                move = min_move
        return move

    cdef Move increaseMoveScoreIfMiddleColumn(self, Move move):
        if move.column > 2 or move.column < 4:
            move.score = move.score * settings.MIDDLE_MULTIPLIER
        return move

    cdef Move min_turn(self, int depth, list board, Player ai_player, short current_column):
        cdef list child_board, possible_moves = []
        cdef int chip_row_stop = 0
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                child_board = self.copy_board(board)
                child_board[column][chip_row_stop] = self.get_other_player(ai_player).id
                possible_moves.append(PotentialMove(child_board, column))
        # end recursion if depth is reached or no moves possible
        if depth == settings.DEPTH or len(possible_moves) == 0 or self.did_someone_win(board, ai_player):
            return Move(self.evaluate_board(board, ai_player, depth), current_column)
        cdef Move move = Move(INF, 0)
        cdef Move max_move
        for possible_move in possible_moves:
            max_move = self.max_turn(depth + 1, possible_move.board, ai_player, possible_move.column)
            if max_move.score < move.score:
                move = max_move
        return move

    def get_other_player(self, player: Player):
        if player.id == self.current_player.id:
            return self.current_opponent
        else:
            return self.current_player

    cpdef void place_chip_ai(self, int column):
        cdef i = 0
        for i in range(column):
            self.move_chip_right()
        self.place_chip()

    cpdef bool is_ai_playing(self):
        return self.current_player.id == 2

    cdef long get_move_score(self, int chip_count, int column):
        cdef long move_score = 0
        if chip_count == 1:
            move_score = settings.CHIP_COUNT_1_MULTIPLIER
        elif chip_count == 2:
            move_score = settings.CHIP_COUNT_2_MULTIPLIER
        elif chip_count == 3:
            move_score = settings.CHIP_COUNT_3_MULTIPLIER
        elif chip_count >= 4:
            move_score = settings.CHIP_COUNT_4_MULTIPLIER
        return move_score

    cdef long evaluate_columns(self, list board, Player current_player):
        cdef short x = 0, y = 0, consecutive_chips = 0
        cdef long move_score = 0
        # Check each columns from left to right
        for x in range(settings.COLS):
            consecutive_chips = 0
            previous_chip = 0
            for y in range(0, settings.ROWS):
                cell = board[x][y]
                if cell == current_player.id and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == current_player.id and cell == previous_chip:
                    consecutive_chips += 1
                elif cell != current_player.id:
                    move_score += self.get_move_score(consecutive_chips, x)
                    consecutive_chips = 0
                previous_chip = cell
            move_score += self.get_move_score(consecutive_chips, x)
        return move_score

    cdef long evaluate_rows(self, list board, Player current_player):
        cdef short x = 0, y = 0, consecutive_chips = 0
        cdef long move_score = 0
        # Check each rows from top to bottom
        for y in range(settings.ROWS):
            consecutive_chips = 0
            previous_chip = 0
            for x in range(settings.COLS):
                cell = board[x][y]
                if cell == current_player.id and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == current_player.id and cell == previous_chip:
                    consecutive_chips += 1
                elif cell != current_player.id:
                    move_score += self.get_move_score(consecutive_chips, x)
                    consecutive_chips = 0
                previous_chip = cell
            move_score += self.get_move_score(consecutive_chips, x)
        return move_score

    cdef long evaluate_board(self, list board, Player current_player, short depth):
        """Scores the passed board for the passed player"""
        cdef int move_score = self.evaluate_columns(board, current_player)
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
        # if other player won
        if depth <= 2 and self.did_player_win(board, self.red_player):
            move_score = -INF + 1
            print('enemy win', move_score, depth)
            print(board)
        if depth <= 2 and self.did_player_win(board, self.yellow_player):
            move_score = INF - 1
            print('I win', move_score)
            print(board)
        return move_score

    cdef bool did_someone_win(self, list board, Player current_player):
        cdef bool ai_won = self.did_player_win(board, current_player)
        cdef bool human_player_won = self.did_player_win(board, self.get_other_player(current_player))
        if ai_won or human_player_won:
            print('someone won')
            return True
        return False

    cdef bool did_player_win(self, list board, Player current_player):
        cdef short boarder = 4
        # Check each columns from left to right
        cdef short x, y, consecutive_chips = 0
        for x in range(0, settings.COLS):
            consecutive_chips = 0
            previous_chip = None
            for y in range(0, settings.ROWS):
                cell = board[x][y]

                if cell == current_player.id and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == current_player.id and cell == previous_chip:
                    consecutive_chips += 1
                elif cell != current_player.id:
                    consecutive_chips = 0
                if consecutive_chips >= boarder:
                    return True
                previous_chip = cell
        # Check each rows from top to bottom
        for y in range(0, settings.ROWS):
            consecutive_chips = 0
            previous_chip = None
            for x in range(0, settings.COLS):
                cell = board[x][y]
                if cell == current_player.id and consecutive_chips == 0:
                    consecutive_chips = 1
                elif cell == current_player.id and cell == previous_chip:
                    consecutive_chips += 1
                elif cell != current_player.id:
                    consecutive_chips = 0
                if consecutive_chips >= boarder:
                    print('ret True')
                    return True
                print(board)
                print('cell', cell, 'x, y', x, y)
                print('cons', consecutive_chips, 'player', current_player.name)
                previous_chip = cell
        # Check each "/" diagonal starting at the top left corner
        x = 0
        for y in range(0, settings.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board, current_player)
            if consecutive_chips >= boarder:
                return True
        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = settings.ROWS - 1
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board, current_player)
            if consecutive_chips >= boarder:
                return True
        # Check each "\" diagonal starting at the bottom left corner
        x = 0
        for y in range(settings.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board, current_player)
            if consecutive_chips >= boarder:
                return True
        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board, current_player)
            if consecutive_chips >= boarder:
                return True
        return False

    cdef int count_consecutive_diagonal_chips(self, int consecutive_chips, previous_chip, int x, int y, direction,
                                         list board, Player current_player):
        cdef short cell = 0
        if not self.is_valid_position(x, y):
            return consecutive_chips
        cell = board[x][y]
        if cell == current_player.id and consecutive_chips == 0:
            consecutive_chips = 1
        elif cell == current_player.id and cell == previous_chip:
            consecutive_chips += 1
        elif cell != current_player.id:
            consecutive_chips = 0
        if consecutive_chips == 4:
            return consecutive_chips
        x, y = self.compute_direction_pos(x, y, direction)
        previous_chip = cell
        return self.count_consecutive_diagonal_chips(consecutive_chips, previous_chip, x, y,
                                                     direction, board, current_player)

    cdef tuple compute_direction_pos(self, int x, int y, direction):
        x = x + abs(direction[0]) if direction[0] > 0 else x - abs(direction[0])
        y = y + abs(direction[1]) if direction[1] > 0 else y - abs(direction[1])
        return x, y


cdef class Move:

    def __init__(self, score, column):
        self.score = score
        self.column = column


cdef class PotentialMove:

    def __init__(self, board, column):
        self.board = board
        self.column = column


if __name__ == "__main__":
    print(min(1, 2))
