

cdef class Player:
    cdef public short score
    cdef public str name
    cdef public short id
    cdef public chip
    cdef public color

cdef class RedPlayer(Player):
    pass


cdef class YellowPlayer(Player):
    pass