from unittest import TestSuite, TestCase
from model import Knight, Board
from engine import get_next_random_possible_move


class EngineTest(TestCase):
    def test_should_return_possible_moves(self):
        knight = Knight(2, 2)
        board = Board()
        self.assertIsNotNone(get_next_random_possible_move(knight, board))
