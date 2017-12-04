from objects import Player
from objects cimport Player
import settings
cimport settings
from screens.game import Game
cimport screens.minmax_ai as minmax
from screens.minmax_ai cimport Move as Move
from screens.minmax_ai cimport PotentialMove as PotentialMove
from cpython cimport bool


cdef long BIG_VALUE = settings.BIG_VALUE


cdef class AlphaBetaAI(minmax.GameMinmaxAI):
    def __init__(self, app):
        if (app is None):
            return
        print('Starting minmax game')
        Game.__init__(self, app)

    cdef Move max_turn(self, int depth, list board, Player ai_player, short current_column):
        # make all possible moves for the current player
        cdef list child_board, potential_moves = []
        cdef int chip_row_stop = 0
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                child_board = self.copy_board(board)
                child_board[column][chip_row_stop] = ai_player.id
                potential_moves.append(PotentialMove(child_board, column))
        # end recursion if depth is reached or no moves possible
        if depth == settings.MAX_DEPTH or len(potential_moves) == 0 or self.did_someone_win(board, depth):
            return Move(self.evaluate_board(board, ai_player, depth), current_column)
        cdef Move move = Move(-BIG_VALUE, 0)
        cdef Move min_move
        for potential_move in potential_moves:
            if depth == 0:
                min_move = self.min_turn(depth + 1, potential_move.board, ai_player, potential_move.column)
                self.increaseMoveScoreIfMiddleColumn(min_move)
            else:
                min_move = self.min_turn(depth + 1, potential_move.board, ai_player, current_column)
            if min_move.score > move.score:
                move = min_move
        return move

    cdef Move min_turn(self, int depth, list board, Player ai_player, short current_column):
        cdef list child_board, potential_moves = []
        cdef int chip_row_stop = 0
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                child_board = self.copy_board(board)
                child_board[column][chip_row_stop] = self.red_player.id
                potential_moves.append(PotentialMove(child_board, column))
        # end recursion if depth is reached or no moves possible
        if depth == settings.MAX_DEPTH or len(potential_moves) == 0 or self.did_someone_win(board, depth):
            return Move(self.evaluate_board(board, ai_player, depth), current_column)
        cdef Move move = Move(BIG_VALUE, 0)
        cdef Move max_move
        for potential_move in potential_moves:
            max_move = self.max_turn(depth + 1, potential_move.board, ai_player, current_column)
            if max_move.score < move.score:
                move = max_move
        return move


if __name__ == "__main__":
    print(min(1, 2))
