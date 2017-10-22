import screens.game as game
import settings
import pygame
import sys
import time


class AIGame(game.Game):

    def __init__(self, app):
        if (app is None):
            return
        game.Game.__init__(self, app)

    def update_while_playing(self):
        if not self.current_player_chip:
            self.current_player_chip = self.current_player.chip()
            self.chips.add(self.current_player_chip)
            self.current_player_chip.rect.left = 0
            self.current_player_chip.rect.top = settings.COLUMN_CHOOSING_MARGIN_TOP
        if self.is_ai_playing():
            self.update_ai_player()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not self.is_ai_playing():
                self.execute_operation_while_playing(event.key)
            elif event.type == pygame.KEYDOWN and self.is_ai_playing() and event.key == pygame.K_ESCAPE:
                self.navigate_to_menu()
        self.status_text = self.current_player.name + ' player\'s turn'
        self.status_color = self.current_player.color

    def update_ai_player(self):
        t1 = time.time()
        best_move, highest_move_score = self.min_max(self.board, settings.DEPTH, self.current_player)
        self.place_chip_ai(best_move)
        print('ai turn took',  time.time() - t1)
        print('Move Chosen:', best_move, 'Move Score', highest_move_score)
