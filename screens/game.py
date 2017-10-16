from screens import menu
from collections import deque
import objects
import pygame
import settings
import utils
import logging
import sys


class Game:
    def __init__(self, app):
        logging.info('Initializing game')
        self.app = app
        self.last_chip_pos = None
        self.current_player_chip = None
        self.status_text = ""
        self.status_color = settings.COLORS.WHITE.value
        self.button_mapping_while_playing = {pygame.K_LEFT: self.move_chip_left,
                                             pygame.K_RIGHT: self.move_chip_right,
                                             pygame.K_DOWN: self.place_chip,
                                             pygame.K_ESCAPE: self.navigate_to_menu}
        self.state_mapping = {settings.GAME_STATES.PLAYING: self.update_while_playing,
                              settings.GAME_STATES.WON: self.update_while_won,
                              settings.GAME_STATES.NO_ONE_WIN: self.update_while_draw}
        self.chips = pygame.sprite.Group()
        self.current_consecutive_chips = deque(maxlen=4)
        self.red_player = objects.RedPlayer()
        self.yellow_player = objects.YellowPlayer()
        logging.info('Loading images')
        self.board_cell_image = utils.load_image('board_cell.png')
        self.board_cell_highlighted_image = utils.load_image('board_cell_highlighted.png')
        logging.info('Loading sounds')
        self.sounds_volume = self.app.config.getfloat('connectfour', 'sounds_volume')
        self.musics_volume = self.app.config.getfloat('connectfour', 'music_volume')
        self.placed_sound = utils.load_sound('placed.wav', volume=self.sounds_volume)
        self.column_change_sound = utils.load_sound('column_change.wav', volume=self.sounds_volume)
        self.column_full_sound = utils.load_sound('column_full.wav', volume=self.sounds_volume)
        self.win_sound = utils.load_sound('win.wav', volume=self.sounds_volume)
        self.applause_sound = utils.load_sound('applause.wav', volume=self.sounds_volume)
        self.boo_sound = utils.load_sound('boo.wav', volume=self.sounds_volume)
        logging.info('Loading fonts')
        self.title_font = utils.load_font('monofur.ttf', 22)
        self.normal_font = utils.load_font('monofur.ttf', 16)
        self.init_new_game()

    def execute_update_dependant_on_state(self):
        self.state_mapping[self.state]()

    def execute_operation_while_playing(self, pygame_button):
        if self.current_player_chip and pygame_button in self.button_mapping_while_playing:
            self.button_mapping_while_playing[pygame_button]()

    def init_new_game(self):
        logging.info('Starting new game')
        self.state = settings.GAME_STATES.PLAYING
        self.chips.empty()
        self.current_consecutive_chips.clear()
        self.current_player = self.red_player # The starting player is always the red one
        self.current_player_chip = None
        self.current_player_chip_column = 0
        self.board = {}
        self.highlighted_chips = {}
        for x in range(0, settings.COLS):
            self.board[x] = {}
            self.highlighted_chips[x] = {}
            for y in range(0, settings.ROWS):
                self.board[x][y] = None
                self.highlighted_chips[x][y] = None
        logging.info('Loading random music')
        utils.load_random_music(['techno_dreaming.wav', 'techno_celebration.wav', 'electric_rain.wav', 'snake_trance.wav'], volume=self.musics_volume)

    def is_valid_position(self, x, y) -> bool:
        if x < 0 or x > settings.COLS - 1 or y < 0 or y > settings.ROWS - 1:
            return False
        return True

    def set_highlighted_chips(self):
        for chips_position in list(self.current_consecutive_chips):
            self.highlighted_chips[chips_position[0]][chips_position[1]] = True

    def clear_consecutive_chips_if_false(self, condition: bool) -> bool:
        if not condition:
            self.current_consecutive_chips.clear()
        return condition

    def check_horizontal_win(self) -> bool:
        self.current_consecutive_chips.append(self.last_chip_pos)
        chip_x, chip_y = self.last_chip_pos
        space_right = settings.COLS - chip_x - 1
        chip_count = 1
        # check right chips
        if space_right:
            for x in range(chip_x + 1, chip_x + space_right + 1):
                if self.board[x][chip_y] == self.current_player.name:
                    chip_count += 1
                    self.current_consecutive_chips.append((x, chip_y))
                else:
                    break
        # check left chips
        if chip_x:
            for x in range(chip_x - 1, -1, -1):
                if self.board[x][chip_y] == self.current_player.name:
                    chip_count += 1
                    self.current_consecutive_chips.append((x, chip_y))
                else:
                    break
        return self.clear_consecutive_chips_if_false(chip_count >= 4)

    def check_vertical_win(self) -> bool:
        self.current_consecutive_chips.append(self.last_chip_pos)
        chip_x, chip_y = self.last_chip_pos
        chip_count = 1
        # check chips from the top to bottom
        for y in range(chip_y + 1, settings.ROWS):
            if self.board[chip_x][y] == self.current_player.name:
                self.current_consecutive_chips.append((chip_x, y))
                chip_count += 1
            else:
                break
        return self.clear_consecutive_chips_if_false(chip_count >= 4)

    def check_diagonal_left_to_right(self) -> bool:
        self.current_consecutive_chips.append(self.last_chip_pos)
        # check the chips which are "over" the current chip
        chip_x, chip_y = self.last_chip_pos
        chip_count = 1
        x = chip_x + 1
        y = chip_y - 1
        while self.is_valid_position(x, y):
            if self.board[x][y] == self.current_player.name:
                chip_count += 1
                self.current_consecutive_chips.append((x, y))
                x += 1
                y -= 1
            else:
                break
        # check the chips which are "under" the current chip
        x = chip_x - 1
        y = chip_y + 1
        while self.is_valid_position(x, y):
            if self.board[x][y] == self.current_player.name:
                chip_count += 1
                self.current_consecutive_chips.append((x, y))
                x -= 1
                y += 1
            else:
                break
        return self.clear_consecutive_chips_if_false(chip_count >= 4)

    def check_diagonal_right_to_left(self) -> bool:
        self.current_consecutive_chips.append(self.last_chip_pos)
        # check the chips which are "under" the current chip
        chip_x, chip_y = self.last_chip_pos
        chip_count = 1
        # check the chips which are "over" the current chip
        x = chip_x - 1
        y = chip_y - 1
        while self.is_valid_position(x, y):
            if self.board[x][y] == self.current_player.name:
                chip_count += 1
                self.current_consecutive_chips.append((x, y))
                x -= 1
                y -= 1
            else:
                break
        x = chip_x + 1
        y = chip_y + 1
        while self.is_valid_position(x, y):
            if self.board[x][y] == self.current_player.name:
                chip_count += 1
                self.current_consecutive_chips.append((x, y))
                x += 1
                y += 1
            else:
                break
        return self.clear_consecutive_chips_if_false(chip_count >= 4)

    def has_current_player_won(self) -> bool:
        """
        Checks if the current player wins the game.
        This method performs the checks on the whole board in all possible
        direction until 4 consecutive chips are found
        for the current player.
        """
        return self.check_horizontal_win() or self.check_vertical_win() or \
            self.check_diagonal_left_to_right() or self.check_diagonal_right_to_left()

    def did_no_one_win(self) -> bool:
        """Check if no one win the game.
        This method checks every single cell. If all are filled, no one win."""
        for x in range(0, settings.COLS):
            for y in range(0, settings.ROWS):
                if not self.board[x][y]: # The cell is empty: players still can play
                    return False
        return True

    def draw_board(self):
        """Draw the board itself (the game support)."""
        for x in range(0, settings.COLS):
            for y in range(0, settings.ROWS):
                if self.highlighted_chips[x][y] is True:
                    image = self.board_cell_highlighted_image
                else:
                    image = self.board_cell_image

                self.app.window.blit(image, (x * settings.IMAGES_SIDE_SIZE, y * settings.IMAGES_SIDE_SIZE + settings.BOARD_MARGIN_TOP))

    def get_free_row(self, column) -> int:
        """Given a column, get the latest row number which is free."""
        for y, cell in self.board[column].items():
            # If there's nothing in the current cell
            if not cell:
                # If we're in the latest cell or if the next cell isn't empty
                if (y == settings.ROWS - 1) or (not y + 1 > settings.ROWS - 1 and self.board[column][y + 1]):
                    return y
        return -1

    def draw_background(self):
        self.app.window.fill(settings.COLORS.BLACK.value)
        blue_rect_1 = pygame.Rect((0, 0), (settings.WINDOW_SIZE[0], settings.COLUMN_CHOOSING_MARGIN_TOP - 1))
        blue_rect_2 = pygame.Rect((0, settings.COLUMN_CHOOSING_MARGIN_TOP), (settings.WINDOW_SIZE[0], settings.IMAGES_SIDE_SIZE))
        self.app.window.fill(settings.COLORS.BLUE.value, blue_rect_1)
        self.app.window.fill(settings.COLORS.BLUE.value, blue_rect_2)

    def draw_header(self, status_text, status_color):
        # Status
        status = self.title_font.render(status_text, True, status_color)
        status_rect = status.get_rect()
        status_rect.x = 10
        status_rect.centery = 25
        self.app.window.blit(status, status_rect)
        # Game name
        game_name = self.normal_font.render(settings.GAME_NAME + settings.VERSION, True, settings.COLORS.WHITE.value)
        game_name_rect = game_name.get_rect()
        game_name_rect.centery = 25
        game_name_rect.right = self.app.window.get_rect().width - 10
        self.app.window.blit(game_name, game_name_rect)
        # Scores
        pygame.draw.line(self.app.window, settings.COLORS.BLACK.value, (game_name_rect.left - 15, 0), (game_name_rect.left - 15, settings.COLUMN_CHOOSING_MARGIN_TOP - 1))
        scores_yellow = self.title_font.render(str(self.yellow_player.score), True, settings.COLORS.YELLOW.value)
        scores_yellow_rect = scores_yellow.get_rect()
        scores_yellow_rect.centery = 25
        scores_yellow_rect.right = game_name_rect.left - 25
        self.app.window.blit(scores_yellow, scores_yellow_rect)
        dash = self.title_font.render('-', True, settings.COLORS.WHITE.value)
        dash_rect = dash.get_rect()
        dash_rect.centery = 25
        dash_rect.right = scores_yellow_rect.left - 5
        self.app.window.blit(dash, dash_rect)
        scores_red = self.title_font.render(str(self.red_player.score), True, settings.COLORS.RED.value)
        scores_red_rect = scores_red.get_rect()
        scores_red_rect.centery = 25
        scores_red_rect.right = dash_rect.left - 5
        self.app.window.blit(scores_red, scores_red_rect)
        pygame.draw.line(self.app.window, settings.COLORS.BLACK.value, (scores_red_rect.left - 15, 0), (scores_red_rect.left - 15, settings.COLUMN_CHOOSING_MARGIN_TOP - 1))

    def place_chip(self) -> None:
        chip_row_stop = self.get_free_row(self.current_player_chip_column)
        if chip_row_stop >= 0:  # Actually move the chip in the current column and reset the current one (to create a new one later)
            if self.placed_sound:
                self.placed_sound.play()
            self.last_chip_pos = (self.current_player_chip_column, chip_row_stop)
            self.board[self.current_player_chip_column][chip_row_stop] = self.current_player.name
            self.current_player_chip.rect.top += settings.IMAGES_SIDE_SIZE * (chip_row_stop + 1)
            if self.has_current_player_won():
                self.set_highlighted_chips()
                pygame.mixer.music.stop()
                if self.win_sound:
                    self.win_sound.play()
                if self.applause_sound:
                    self.applause_sound.play()
                self.state = settings.GAME_STATES.WON
                pygame.time.set_timer(settings.EVENTS.WINNER_CHIPS_EVENT.value, 600)
                logging.info(self.current_player.name + ' win')
                self.current_player.score += 1
            elif self.did_no_one_win():
                pygame.mixer.music.stop()
                if self.boo_sound:
                    self.boo_sound.play()
                self.state = settings.GAME_STATES.NO_ONE_WIN
                logging.info('No one won')
            else:  # It's the other player's turn if the current player didn't win
                self.current_player = self.yellow_player \
                if isinstance(self.current_player, objects.RedPlayer) else self.red_player
                logging.info(self.current_player.name + ' player turn')
            self.current_player_chip = None
            self.current_player_chip_column = 0
        else:  # The column is full
            if self.column_full_sound:
                self.column_full_sound.play()
            logging.info('{} column full'.format(self.current_player_chip_column))

    def move_chip_left(self) -> None:
        if self.column_change_sound:
            self.column_change_sound.play()
        if self.current_player_chip.rect.left - settings.IMAGES_SIDE_SIZE >= 0:  # The chip will not go beyond the screen
            self.current_player_chip.rect.left -= settings.IMAGES_SIDE_SIZE
            self.current_player_chip_column -= 1
        else:  # The chip will go beyond the screen: put it in the far right
            self.current_player_chip.rect.right = settings.WINDOW_SIZE[0]
            self.current_player_chip_column = settings.COLS - 1

    def move_chip_right(self) -> None:
        if self.column_change_sound:
            self.column_change_sound.play()
        if self.current_player_chip.rect.right + settings.IMAGES_SIDE_SIZE <= settings.WINDOW_SIZE[
            0]:  # The chip will not go beyond the screen
            self.current_player_chip.rect.right += settings.IMAGES_SIDE_SIZE
            self.current_player_chip_column += 1
        else:  # The chip will go beyond the screen: put it in the far left
            self.current_player_chip.rect.left = 0
            self.current_player_chip_column = 0

    def navigate_to_menu(self) -> None:
        self.app.set_current_screen(menu.Menu, True)

    def update_while_playing(self) -> None:
        if not self.current_player_chip:
            self.current_player_chip = self.current_player.chip()
            self.chips.add(self.current_player_chip)
            self.current_player_chip.rect.left = 0
            self.current_player_chip.rect.top = settings.COLUMN_CHOOSING_MARGIN_TOP
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.execute_operation_while_playing(event.key)
        self.status_text = self.current_player.name + ' player\'s turn'
        self.status_color = self.current_player.color

    def update_while_won(self) -> None:
        for event in pygame.event.get():
            self.check_for_quitting(event)
            if event.type == settings.EVENTS.WINNER_CHIPS_EVENT.value:
                for x in range(0, settings.COLS):
                    for y in range(0, settings.ROWS):
                        if isinstance(self.highlighted_chips[x][y], bool):
                            self.highlighted_chips[x][y] = not self.highlighted_chips[x][y]
                pygame.time.set_timer(settings.EVENTS.WINNER_CHIPS_EVENT.value, 600)
        self.status_text = self.current_player.name + ' player wins!'
        self.status_color = self.current_player.color

    def update_while_draw(self)-> None:
        for event in pygame.event.get():
           self.check_for_quitting(event)
        self.status_text = 'DRAW'
        self.status_color = settings.COLORS.WHITE.value

    def check_for_quitting(self, pygame_event) -> None:
        if pygame_event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_ESCAPE:  # The user want to go back to the game menu
                self.navigate_to_menu()
            elif pygame_event.key == pygame.K_RETURN:  # Pressing the Return key will start a new game
                self.init_new_game()

    def update(self) -> None:
        self.draw_background()
        self.execute_update_dependant_on_state()
        self.draw_header(self.status_text, self.status_color)
        self.chips.draw(self.app.window)
        self.draw_board()
