import time
from threading import Thread

from engine import get_random_location, get_next_random_possible_move, move
from model import Knight, Board, MoveHistory


def create_random_knight():
    return Knight(*(get_random_location(Board.BOARD_SIZE)))


def simulate_once():
    board = Board()
    knight = create_random_knight()
    moves_so_far = []
    next_move = get_next_random_possible_move(knight, board)
    while next_move is not None:
        moves_so_far.append(move(knight, board, next_move))
        next_move = get_next_random_possible_move(knight, board)
    return MoveHistory(moves_so_far, knight, board)


def simulate_until(condition=lambda: True):
    history = []
    simulate_until_to_list(condition, history)
    return history


def simulate_until_to_list(condition, history_list):
    while condition():
        history_list.append(simulate_once())


class Simulator(Thread):
    def __init__(self, condition):
        super().__init__()
        self.results = []
        self.condition = condition

    def run(self):
        simulate_until_to_list(self.condition, self.results)
        return


if __name__ == "__main__":
    start = time.time()
    condition = lambda: time.time() - start <= 1.0

    history = simulate_until(condition)
    print(len(history))
