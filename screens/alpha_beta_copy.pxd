from screens.ai cimport Move as Move
from screens.ai cimport PotentialMove as PotentialMove
from objects import Player
from objects cimport Player
from screens.minmax_ai import GameMinmaxAI as GameMinmaxAI
from screens.minmax_ai cimport GameMinmaxAI as GameMinmaxAI


cdef class AlphaBetaAICopy(GameMinmaxAI):
    cdef Move max_turn_alpha_beta(self, int depth, list board, Player ai_player, short current_column, long alpha, long beta)
    cdef Move min_turn_alpha_beta(self, int depth, list board, Player ai_player, short current_column, long alpha, long beta)
    cpdef Move min_max(self, list board, int depth, Player ai_player)
