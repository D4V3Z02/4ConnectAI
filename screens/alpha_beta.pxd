from screens.minmax_ai cimport Move as Move
from objects import Player
from objects cimport Player
cimport screens.minmax_ai as minmax


cdef class AlphaBetaAI(minmax.GameMinmaxAI):
    cdef Move max_turn_alpha_beta(self, int depth, list board, Player ai_player, short current_column, long alpha, long beta)
    cdef Move min_turn_alpha_beta(self, int depth, list board, Player ai_player, short current_column, long alpha, long beta)
    cpdef Move min_max(self, list board, int depth, Player ai_player)
