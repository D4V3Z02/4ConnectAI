cimport screens.game as game
cimport screens.minmax_ai
import settings
cimport settings
import pygame
import sys
import time
from cpython cimport bool
from objects cimport Player


cdef class AIGame(game.Game):
    """
    Abstract baseclass for ai algorithms
    """

    def __init__(self, app):
        if (app is None):
            return
        self.BIG_VALUE = settings.BIG_VALUE
        game.Game.__init__(self, app)

    cpdef update_while_playing(self):
        """
        Does the update-handling for the human and ai player.
        :return: void
        """
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

    cdef update_ai_player(self):
        """
        Decides in which column the ai places the chip and places it.
        """
        t1 = time.time()
        move = self.min_max(self.board, settings.MAX_DEPTH, self.yellow_player)
        best_move, highest_move_score = move.column, move.score
        self.place_chip_ai(best_move)
        print('ai turn took',  time.time() - t1)
        print('Move Chosen:', best_move, 'Move Score', highest_move_score)

    cdef list copy_board(self, list board):
        """
        Copy a board in for of nested lists. Does not copy the instances of chips elements in the board
        since only their order in the list itself matters.
        :param board: the board to copy
        :return: the copied board
        """
        return [x[:] for x in board]

    cdef object generate_right_header_text(self):
        return self.normal_font.render('Ai evaluated: ' + str(self.turns_analyzed_by_ai) + ' turns', True, settings.Colors.WHITE.value)

    cdef Move increaseMoveScoreIfMiddleColumn(self, Move move):
        """
        Increase the score of the passed move if it's column is in the middle. The passed element
        is not copied. The method therefore mutates the passed element.
        :param move: move to eventually increase.
        :return: move with increased score.
        """
        cdef short boarder_size = 2
        if move.column > int(settings.COLS / 2) - boarder_size and move.column < int(settings.COLS / 2) + boarder_size:
            move.score = move.score * settings.MIDDLE_MULTIPLIER
        return move

    cpdef void place_chip_ai(self, int column):
        """
        places a chip in the board of the game logic.
        :param column: column to place the chip in
        :return: void
        """
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

    cdef long evaluate_board(self, list board, Player ai_player, short depth):
        """Scores the board for the ai player"""
        cdef int move_score = self.evaluate_columns(board, ai_player)
        move_score += self.evaluate_rows(board, ai_player)
        # Check each "/" diagonal starting at the top left corner
        x = 0
        for y in range(settings.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board,
                                                                      ai_player)
            move_score += self.get_move_score(consecutive_chips, x)
        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = settings.ROWS - 1
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board,
                                                                      ai_player)
            move_score += self.get_move_score(consecutive_chips, x)
        # Check each "\" diagonal starting at the bottom left corner
        x = 0
        for y in range(settings.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board,
                                                                      ai_player)
            move_score += self.get_move_score(consecutive_chips, x)
        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board,
                                                                      ai_player)
            move_score += self.get_move_score(consecutive_chips, x)
        if depth <= 2 and self.did_player_win(board, self.red_player):
           move_score = move_score - self.BIG_VALUE
        if depth <= 2 and self.did_player_win(board, self.yellow_player):
           move_score = self.BIG_VALUE
        return move_score

    cdef bool did_someone_win(self, list board):
        cdef bool ai_won = self.did_player_win(board, self.yellow_player)
        cdef bool human_player_won = self.did_player_win(board, self.red_player)
        if ai_won or human_player_won:
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
                    return True
                previous_chip = cell
        # Check each "/" diagonal starting at the top left corner
        x = 0
        for y in range(0, settings.ROWS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board,
                                                                      current_player)
            if consecutive_chips >= boarder:
                return True
        # Check each "/" diagonal starting at the bottom left + 1 corner
        y = settings.ROWS - 1
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, -1), board,
                                                                      current_player)
            if consecutive_chips >= boarder:
                return True
        # Check each "\" diagonal starting at the bottom left corner
        x = 0
        for y in range(settings.ROWS, -1, -1):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board,
                                                                      current_player)
            if consecutive_chips >= boarder:
                return True
        # Check each "\" diagonal starting at the top left + 1 corner
        y = 0
        for x in range(1, settings.COLS):
            consecutive_chips = self.count_consecutive_diagonal_chips(0, None, x, y, (1, 1), board,
                                                                      current_player)
            if consecutive_chips >= boarder:
                return True
        return False

    cdef int count_consecutive_diagonal_chips(self, int consecutive_chips, previous_chip, int x,
                                              int y, direction,
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
    def __init__(self, board, column, row=0):
        self.board = board
        self.column = column
        self.row_stop=row

