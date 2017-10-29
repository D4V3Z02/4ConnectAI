cimport screens.ai as ai
import screens.ai as ai
cimport objects
from objects cimport Player
from cpython cimport bool


cdef class GameMinmaxAI(ai.AIGame):
    cpdef bool is_ai_playing(self)
    cdef tuple compute_direction_pos(self, int x, int y, direction)
    cdef int count_consecutive_diagonal_chips(self, int consecutive_chips, previous_chip, int x, int y, direction,
                                         list board, Player current_player)
    cdef list get_amount_of_chips_in_a_row(self, list board, Player current_player)
    cdef bool did_someone_win(self, list board, Player current_player)
    cdef list get_enemy_streak(self, list board, Player current_player)
    cdef long evaluate_board(self, list board, Player current_player)
    cdef long evaluate_rows(self, list board, Player current_player)
    cdef long evaluate_columns(self, list board, Player current_player)
    cdef long get_move_score(self, int chip_count, int column)
    cpdef void place_chip_ai(self, int column)
    cdef long min_turn(self, int depth, list board, Player ai_player)
    cdef long max_turn(self, int depth, list board, Player ai_player)
    cdef list copy_board(self, list board)
    cpdef tuple min_max(self, list board, int depth, Player ai_player)
    cdef bool did_someone_win(self, list board, Player current_player)
