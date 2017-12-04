from cpython cimport bool


cdef short FPS
cdef short IMAGES_SIDE_SIZE
cdef short COLS
cdef short ROWS
cdef short COLUMN_CHOOSING_MARGIN_TOP
cdef short BOARD_MARGIN_TOP
cdef tuple WINDOW_SIZE
cdef short LAN_PORT
cdef short LAN_TIMEOUT
cdef str CONFIG_FILE
cdef bool EMPTY_SYMBOL
cdef dict DEFAULT_CONFIG
cdef str PLAYER_RED_NAME
cdef short PLAYER_RED_ID
cdef str PLAYER_YELLOW_NAME
cdef short PLAYER_YELLOW_ID
cdef str RED_CHIP_IMAGE
cdef str YELLOW_CHIP_IMAGE
cdef str GAME_NAME
cdef short MAX_DEPTH
cdef short MAX_DEPTH_AB
cdef short MIDDLE_MULTIPLIER
cdef long CHIP_COUNT_1_MULTIPLIER
cdef long CHIP_COUNT_2_MULTIPLIER
cdef long CHIP_COUNT_3_MULTIPLIER
cdef long CHIP_COUNT_4_MULTIPLIER
cdef long BIG_VALUE
