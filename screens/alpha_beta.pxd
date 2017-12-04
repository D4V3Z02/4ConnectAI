from screens.minmax_ai cimport Move as Move
from objects import Player
from objects cimport Player
cimport screens.minmax_ai as minmax



cdef class AlphaBetaAI(minmax.GameMinmaxAI):
    cdef Move min_turn(self, int depth, list board, Player ai_player, short current_column)
    cdef Move min_turn(self, int depth, list board, Player ai_player, short current_column)