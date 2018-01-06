cimport screens.game as game

cdef class AIGame(game.Game):
    cpdef update_while_playing(self)
    cdef update_ai_player(self)
    cdef long turns_analyzed_by_ai
    cdef object generate_right_header_text(self)
