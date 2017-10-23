from cpython cimport bool

cdef class Game:
    cdef public list board
    cdef public dict state_mapping
    cdef public dict button_mapping_while_playing
    cdef public tuple last_chip_pos
    cdef public app
    cdef public current_player_chip
    cdef public current_player
    cdef public current_opponent
    cdef public status_text
    cdef public status_color
    cdef public chips
    cdef public current_consecutive_chips
    cdef public red_player
    cdef public yellow_player
    cdef public board_cell_image
    cdef public board_cell_highlighted_image
    cdef public sounds_volume
    cdef public musics_volume
    cdef public placed_sound
    cdef public column_change_sound
    cdef public column_full_sound
    cdef public win_sound
    cdef public applause_sound
    cdef public boo_sound
    cdef public title_font
    cdef public normal_font
    cdef public state
    cdef current_player_chip_column
    cdef highlighted_chips


    cdef init_new_game(self)
    cdef execute_update_dependant_on_state(self)
    cpdef execute_operation_while_playing(self, pygame_button)
    cpdef bool is_valid_position(self, int x, int y)
    cdef set_highlighted_chips(self)
    cdef public bool clear_consecutive_chips_if_false(self, bool condition)
    cdef check_horizontal_win(self)
    cpdef int get_free_row(self, int column, board)
    cdef bool check_vertical_win(self)
    cdef bool check_diagonal_left_to_right(self)
    cdef bool check_diagonal_right_to_left(self)
    cdef bool has_current_player_won(self)
    cdef bool did_no_one_win(self)
    cdef draw_board(self)
    cdef draw_background(self)
    cdef draw_header(self, status_text, status_color)
    cpdef place_chip(self)
    cpdef move_chip_left(self)
    cpdef move_chip_right(self)
    cpdef navigate_to_menu(self)
    cpdef update_while_playing(self)
    cpdef update_while_won(self)
    cpdef update_while_draw(self)
    cdef check_for_quitting(self, pygame_event)
    cpdef update(self)
