from unittest import TestSuite, TestCase

from datastore import StorableMoveHistory
from model import Knight, Board
from engine import get_next_random_possible_move
from simulator import simulate_once
from utils import to_json


class EngineTest(TestCase):
    def test_should_return_possible_moves(self):
        knight = Knight(2, 2)
        board = Board()
        self.assertIsNotNone(get_next_random_possible_move(knight, board))

    def test_should_generate_json_result(self):
        move_history = StorableMoveHistory.from_move_history(simulate_once())
        json = to_json(move_history)
        print(json)
        self.assertIsNotNone(json)
