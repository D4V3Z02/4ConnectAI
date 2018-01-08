cimport screens.ai as ai
import screens.ai as ai
cimport objects
from objects cimport Player
from cpython cimport bool
from screens.ai cimport Move as Move
from screens.ai cimport PotentialMove as PotentialMove

cdef class GameMinmaxAICopy(ai.AIGame):
    cdef Move min_turn(self, int depth, list board, Player ai_player, short current_column)
    cdef Move max_turn(self, int depth, list board, Player ai_player, short current_column)
    cpdef Move min_max(self, list board, int depth, Player ai_player)
