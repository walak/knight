import time
from threading import Thread

from datastore import Session, ResultStore
from engine import get_random_location, get_next_random_possible_move, move
from model import Knight, Board, MoveHistory
from logging import getLogger, INFO


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


def simulate_completely_to_list(list, continue_condition=lambda: True, flush_condition=lambda: False,
                                flush_action=None):
    while continue_condition():
        list.append(simulate_once())
        if flush_condition():
            if flush_action:
                flush_action()

    if flush_action:
        flush_action()

    return list


LOG = getLogger("Simulator")
LOG.setLevel(INFO)


class Simulator(Thread):
    def __init__(self, continue_condition):
        super().__init__()
        self.results = []
        self.result_counter = 0
        self.continue_condition = continue_condition
        self.flush_condition = lambda: self.should_flush()
        self.flush_action = lambda: self.flush()
        self.done = False

    def run(self):
        simulate_completely_to_list(self.results, self.continue_condition, self.flush_condition, self.flush_action)
        self.done = True
        return

    def should_flush(self):
        return len(self.results) >= 5000

    def flush(self):
        session = Session()
        store = ResultStore(session)
        saved_results = store.store_batch(self.results)
        self.result_counter += len(self.results)
        LOG.info(
            "%i simulations generated, %i results stored to DB (duplicates have been skipped). %i generated totally."
            % (len(self.results), saved_results, self.result_counter))
        self.results.clear()
        session.close()


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

    print("Calculation finished on demand. Simulations generated: %i" % len(simulator.results))
