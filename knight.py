import time
from threading import Thread

from engine import get_random_location, get_next_random_possible_move, move
from model import Knight, Board, MoveHistory, DIRECTIONS
from datastore import Session, ResultStore
from sys import stdin


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
    mh = MoveHistory(moves_so_far, knight, board)
    return mh


def simulate_until(condition=lambda: True):
    history = []
    simulate_until_to_list(condition, history)
    return history


def simulate_until_to_list(condition, history_list):
    while condition():
        history_list.append(simulate_once())


class Simulator(Thread):
    def __init__(self, finish_condition):
        super().__init__()
        self.results = []
        self.finish_condition = finish_condition
        self.done = False

    def run(self):
        simulate_until_to_list(self.finish_condition, self.results)
        self.done = True
        return


if __name__ == "__main__":
    finish = False

    start = time.time()
    condition = lambda: not finish

    knight = Knight(2, 2)
    board = Board()
    simulator = Simulator(condition)
    simulator.start()
    while not (finish or simulator.done):
        input()
        finish = True

    history = simulator.results
    print(len(history))

    session = Session()
    store = ResultStore(session)
    store.store_batch(history)
    session.close()
