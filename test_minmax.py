import os, sys
import objects
from screens.minmax_ai import GameMinmaxAI
import settings
import unittest


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


class TestStringMethods(unittest.TestCase):

    def test_get_row(self):
        board = [[None, None, None, None, 'Yellow', 'Red'],
             [None, None, None, None, None, 'Yellow'],
             [None, None, None, None, None, 'Yellow'],
             [None, None, None, None, None, 'Yellow'],
             ['Yellow', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Yellow'],
             [None, None, None, None, None, 'Yellow'],
             [None, 'Yellow', 'Red', 'Yellow', 'Red', 'Yellow']]
        ai_game = GameMinmaxAI(None)
        self.assertEqual(ai_game.get_free_row(6, board=board), 0)
        self.assertEqual(ai_game.get_free_row(0, board=board), 3)
        self.assertEqual(ai_game.get_free_row(1, board=board), 4)
        self.assertEqual(ai_game.get_free_row(4, board=board), -1)

    def test_evaluate_board(self):
        red = objects.RedPlayer()
        yellow = objects.YellowPlayer()
        yellow_name = yellow.id
        red_name = red.name
        board = [[None, None, None, None, None, yellow_name],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        ai_game = GameMinmaxAI(None)

        ai_game.current_player = yellow
        ai_game.current_opponent = red
        self.assertEqual(ai_game.evaluate_columns(board=board, current_player=yellow), settings.CHIP_COUNT_1_MULTIPLIER)
        self.assertEqual(ai_game.evaluate_rows(board=board, current_player=yellow), settings.CHIP_COUNT_1_MULTIPLIER)
        # combination in column should return 100, two times one chip in a row therefore 20
        board = [[None, None, None, None, yellow_name, yellow_name],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        self.assertEqual(ai_game.evaluate_columns(board=board, current_player=yellow), settings.CHIP_COUNT_2_MULTIPLIER)
        self.assertEqual(ai_game.evaluate_rows(board=board, current_player=yellow), settings.CHIP_COUNT_1_MULTIPLIER*2)
        board = [[None, None, None, yellow_name, red_name, yellow_name],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        # two times one chip in a column -> 20, two times one chip in a row therefore 20
        self.assertEqual(ai_game.evaluate_columns(board=board, current_player=yellow), settings.CHIP_COUNT_1_MULTIPLIER*2)
        self.assertEqual(ai_game.evaluate_rows(board=board, current_player=yellow), settings.CHIP_COUNT_1_MULTIPLIER*2)
        board = [[None, None, None, None, yellow_name, yellow_name],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, yellow_name, yellow_name],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        # chips in the middle (index 2 - 4) give quadruple score
        self.assertEqual(ai_game.evaluate_columns(board=board, current_player=yellow), settings.CHIP_COUNT_2_MULTIPLIER*2)
        self.assertEqual(ai_game.evaluate_rows(board=board, current_player=yellow), settings.CHIP_COUNT_1_MULTIPLIER*4)

        board = [[None, None, yellow_name, None, None, None],
                 [None, None, None, yellow_name, None, None],
                 [None, None, None, None, yellow_name, None],
                 [None, None, None, None, None, yellow_name],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        # chips in the middle (index 2 - 4) give quadruple score
        self.assertTrue(ai_game.evaluate_board(board=board, ai_player=yellow) >= settings.CHIP_COUNT_4_MULTIPLIER)

        board = [[None, None, None, None, yellow_name, None],
                 [None, None, None, yellow_name, None, None],
                 [None, None, yellow_name, None, None, None],
                 [None, yellow_name, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        # chips in the middle (index 2 - 4) give quadruple score
        self.assertTrue(ai_game.evaluate_board(board=board,
                                               ai_player=yellow) >= settings.CHIP_COUNT_4_MULTIPLIER)

    def test_end_conidition(self):
        ai_game = GameMinmaxAI(None)
        red = objects.RedPlayer()
        yellow = objects.YellowPlayer()
        ai_game.current_player = yellow
        ai_game.current_opponent = red
        board = [[None, None, None, None, yellow.id, yellow.id],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, yellow.id, yellow.id],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        self.assertFalse(ai_game.did_someone_win(board, yellow))
        board = [[None, None, None, None, None, yellow.id],
                 [None, None, yellow.id, None, None, None],
                 [None, None, None, yellow.id, None, None],
                 [None, None, None, None, yellow.id, None],
                 [None, None, None, None, None, yellow.id],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        self.assertTrue(ai_game.did_someone_win(board, yellow))
        board = [[None, None, None, None, None, yellow.id],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, yellow.id],
                 [None, None, None, None, yellow.id, None],
                 [None, None, None, yellow.id, None, None],
                 [None, None, yellow.id, None, None, None],
                 [None, None, None, None, None, None]]
        self.assertTrue(ai_game.did_someone_win(board, yellow))
        board = [[None, None, None, None, None, yellow.id],
                 [None, None, None, None, None, None],
                 [None, None, yellow.id, yellow.id, yellow.id, yellow.id],
                 [None, None, None, None, None, None],
                 [None, None, None, yellow.id, None, None],
                 [None, None, yellow.id, None, None, None],
                 [None, None, None, None, None, None]]
        self.assertTrue(ai_game.did_someone_win(board, yellow))
        board = [[None, None, None, None, None, yellow.id],
                 [None, None, None, None, None, None],
                 [None, None, None, None, yellow.id, yellow.id],
                 [None, None, None, None, None, yellow.id],
                 [None, None, None,  None, None, yellow.id],
                 [None, None, yellow.id, None, None, yellow.id],
                 [None, None, None, None, None, None]]
        self.assertTrue(ai_game.did_someone_win(board, yellow))

if __name__ == '__main__':
    unittest.main()
