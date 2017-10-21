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
        self.assertEqual(0, ai_game.get_free_row(6, board=board))
        self.assertEqual(3, ai_game.get_free_row(0, board=board))
        self.assertEqual(4, ai_game.get_free_row(1, board=board))
        self.assertEqual(-1, ai_game.get_free_row(4, board=board))

    def test_evaluate_board(self):

        pass


if __name__ == '__main__':
    unittest.main()
