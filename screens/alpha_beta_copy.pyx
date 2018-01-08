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

cdef long BIG_VALUE = settings.BIG_VALUE

cdef class AlphaBetaAICopy(GameMinmaxAI):
    def __init__(self, app):
        self.turns_analyzed_by_ai = 0
        if (app is None):
            return
        print('Starting alpha_beta game')
        Game.__init__(self, app)

    cpdef Move min_max(self, list board, int depth, Player ai_player):
        """
        Returns the best move found by the alpha_beta algorithm
        """
        self.turns_analyzed_by_ai = 0
        return self.max_turn_alpha_beta(0, self.copy_board(board), ai_player, -1, -BIG_VALUE,
                                        +BIG_VALUE)

    cdef Move max_turn_alpha_beta(self, int depth, list board, Player ai_player,
                                  short first_round_column, long alpha, long beta):
        # make all possible moves for the current player
        self.turns_analyzed_by_ai += 1
        cdef list child_board, potential_moves = []
        cdef int chip_row_stop = 0
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                child_board = self.copy_board(board)
                child_board[column][chip_row_stop] = ai_player.id
                potential_moves.append(PotentialMove(child_board, column))
        # end recursion if depth is reached or no moves possible
        if depth == settings.MAX_DEPTH_AB or len(potential_moves) == 0 or self.did_someone_win(
                board):
            #print('ret max', self.evaluate_board(board, ai_player, depth), first_round_column)
            return Move(self.evaluate_board(board, ai_player, depth), first_round_column)
        cdef Move max_move = Move(alpha, 0)
        cdef Move min_move
        for potential_move in potential_moves:
            if depth == 0:
                min_move = self.min_turn_alpha_beta(depth + 1, potential_move.board, ai_player,
                                                    potential_move.column, max_move.score, beta)
                min_move = self.increaseMoveScoreIfMiddleColumn(min_move)
                print('Top level score and column:', min_move.score, min_move.column)
            else:
                min_move = self.min_turn_alpha_beta(depth + 1, potential_move.board, ai_player,
                                                    first_round_column, max_move.score, beta)
            if min_move.score > max_move.score:
                max_move = min_move
                if max_move.score >= beta:
                    #print('break beta', max_move.score)
                    break
        return max_move

    cdef Move min_turn_alpha_beta(self, int depth, list board, Player ai_player,
                                  short first_round_column, long alpha, long beta):
        self.turns_analyzed_by_ai += 1
        cdef list child_board, potential_moves = []
        cdef int chip_row_stop = 0
        for column in range(len(board)):
            chip_row_stop = self.get_free_row(column, board=board)
            if chip_row_stop >= 0:
                child_board = self.copy_board(board)
                child_board[column][chip_row_stop] = self.red_player.id
                potential_moves.append(PotentialMove(child_board, column))
        # end recursion if depth is reached or no moves possible
        if depth == settings.MAX_DEPTH_AB or len(potential_moves) == 0 or self.did_someone_win(
                board):
            #print('ret min', self.evaluate_board(board, ai_player, depth), first_round_column)
            return Move(self.evaluate_board(board, ai_player, depth), first_round_column)
        cdef Move min_move = Move(beta, 0)
        cdef Move max_move
        for potential_move in potential_moves:
            max_move = self.max_turn_alpha_beta(depth + 1, potential_move.board, ai_player,
                                                first_round_column, alpha, min_move.score)
            if max_move.score < min_move.score:
                min_move = max_move
                if min_move.score <= alpha:
                    #print('break alpha', max_move.score)
                    break
        return min_move

if __name__ == "__main__":
    print(min(1, 2))
