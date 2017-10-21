import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import unittest
from screens.minmax_ai import GameMinmaxAI
from objects import Player
import objects


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
        board = [[None, None, None, None, None, 'Yellow'],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        ai_game = GameMinmaxAI(None)
        red = objects.RedPlayer()
        yellow = objects.YellowPlayer()
        ai_game.current_player = yellow
        ai_game.current_opponent = red
        self.assertEqual(ai_game.evaluate_columns(board=board, current_player=yellow), 10)
        self.assertEqual(ai_game.evaluate_rows(board=board, current_player=yellow), 10)
        # combination in column should return 100, two times one chip in a row therefore 20
        board = [[None, None, None, None, 'Yellow', 'Yellow'],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        self.assertEqual(ai_game.evaluate_columns(board=board, current_player=yellow), 100)
        self.assertEqual(ai_game.evaluate_rows(board=board, current_player=yellow), 20)
        board = [[None, None, None, 'Yellow', 'Red', 'Yellow'],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        # two times one chip in a column -> 20, two times one chip in a row therefore 20
        self.assertEqual(ai_game.evaluate_columns(board=board, current_player=yellow), 20)
        self.assertEqual(ai_game.evaluate_rows(board=board, current_player=yellow), 20)
        board = [[None, None, None, None, 'Yellow', 'Yellow'],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, 'Yellow', 'Yellow'],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None],
                 [None, None, None, None, None, None]]
        # chips in the middle (index 2 - 4) give quadruple score
        self.assertEqual(ai_game.evaluate_columns(board=board, current_player=yellow), 500)
        self.assertEqual(ai_game.evaluate_rows(board=board, current_player=yellow), 100)

if __name__ == '__main__':
    unittest.main()
