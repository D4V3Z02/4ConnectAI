cimport screens.game as game
from objects cimport Player
from cpython cimport bool


cdef class AIGame(game.Game):
    cdef long BIG_VALUE
    cpdef update_while_playing(self)
    cdef update_ai_player(self)
    cdef long turns_analyzed_by_ai
    cdef object generate_right_header_text(self)
    cdef list copy_board(self, list board)
    cdef Move increaseMoveScoreIfMiddleColumn(self, Move move)
    cdef bool did_player_win(self, list board, Player current_player)
    cpdef bool is_ai_playing(self)
    cdef tuple compute_direction_pos(self, int x, int y, direction)
    cdef int count_consecutive_diagonal_chips(self, int consecutive_chips, previous_chip, int x, int y, direction,
                                         list board, Player current_player)
    cdef bool did_someone_win(self, list board)
    cdef long evaluate_board(self, list board, Player current_player, short depth)
    cdef long evaluate_rows(self, list board, Player current_player)
    cdef long evaluate_columns(self, list board, Player current_player)
    cdef long get_move_score(self, int chip_count, int column)
    cpdef void place_chip_ai(self, int column)

cdef class PotentialMove:
    cdef public list board
    cdef public short column
    cdef public short row_stop


cdef class Move:
    cdef public long score
    cdef public short column
