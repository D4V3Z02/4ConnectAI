from objects import Player
from objects cimport Player
import settings
cimport settings
from screens.game import Game
from screens.minmax_ai import GameMinmaxAI as GameMinmaxAI
from screens.minmax_ai cimport GameMinmaxAI as GameMinmaxAI
from screens.ai cimport Move as Move
from screens.ai cimport PotentialMove as PotentialMove
from cpython cimport bool


cdef class AlphaBetaAI(GameMinmaxAI):
    def __init__(self, app):
        self.turns_analyzed_by_ai = 0
        if (app is None):
            return
        print('Starting alpha_beta game')
        GameMinmaxAI.__init__(self, app)

    cpdef Move min_max(self, list board, int depth, Player ai_player):
        """
        Returns the best move found by the alpha_beta algorithm
        """
        self.turns_analyzed_by_ai = 0
        return self.max_turn_alpha_beta(0, self.copy_board(board), ai_player, -1, -self.BIG_VALUE,
                                        self.BIG_VALUE)

    cdef Move max_turn_alpha_beta(self, int depth, list board, Player ai_player,
                                  short first_round_column, long alpha, long beta):
        self.turns_analyzed_by_ai += 1
        cdef list potential_moves = []
        cdef int chip_row_stop = 0
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                potential_moves.append(PotentialMove(board, column, chip_row_stop))
        # end recursion if depth is reached or no moves possible
        if depth == settings.MAX_DEPTH_AB or len(potential_moves) == 0 or self.did_someone_win(
                board):
            return Move(self.evaluate_board(board, ai_player, depth), first_round_column)
        cdef Move max_move = Move(alpha, first_round_column)
        cdef Move min_move
        cdef list max_move_list_first_level = []
        for potential_move in potential_moves:
            if depth == 0:
                board[potential_move.column][potential_move.row_stop] = ai_player.id
                min_move = self.min_turn_alpha_beta(depth + 1, potential_move.board, ai_player,
                                                    potential_move.column, max_move.score, beta)
                board[potential_move.column][potential_move.row_stop] = settings.EMPTY_SYMBOL
                max_move_list_first_level.append(min_move)
            else:
                board[potential_move.column][potential_move.row_stop] = ai_player.id
                min_move = self.min_turn_alpha_beta(depth + 1, potential_move.board, ai_player,
                                                    first_round_column, max_move.score, beta)
                board[potential_move.column][potential_move.row_stop] = settings.EMPTY_SYMBOL
            if min_move.score > max_move.score:
                max_move = min_move
                if max_move.score >= beta:
                    break
        cdef Move move_after_middle_column_evaluation
        # add middle multiplier after alpha_beta evaluation, else middle multiplier affects beta cutoff
        if depth == 0:
            for move in max_move_list_first_level:
                move_after_middle_column_evaluation = self.increaseMoveScoreIfMiddleColumn(move)
                print('Top level score and column:', move_after_middle_column_evaluation.score,
                      move_after_middle_column_evaluation.column)
                if move_after_middle_column_evaluation.score > max_move.score:
                    max_move = move
        return max_move

    cdef Move min_turn_alpha_beta(self, int depth, list board, Player ai_player,
                                  short first_round_column, long alpha, long beta):
        self.turns_analyzed_by_ai += 1
        cdef list potential_moves = []
        cdef int chip_row_stop = 0
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                potential_moves.append(PotentialMove(board, column, chip_row_stop))
        # end recursion if depth is reached or no moves possible
        if depth == settings.MAX_DEPTH_AB or len(potential_moves) == 0 or self.did_someone_win(
                board):
            return Move(self.evaluate_board(board, ai_player, depth), first_round_column)
        cdef Move min_move = Move(beta, first_round_column)
        cdef Move max_move
        for potential_move in potential_moves:
            board[potential_move.column][potential_move.row_stop] = self.red_player.id
            max_move = self.max_turn_alpha_beta(depth + 1, potential_move.board, ai_player,
                                                first_round_column, alpha, min_move.score)
            board[potential_move.column][potential_move.row_stop] = settings.EMPTY_SYMBOL
            if max_move.score < min_move.score:
                min_move = max_move
                if min_move.score <= alpha:
                    break
        return min_move

if __name__ == "__main__":
    print(min(1, 2))
