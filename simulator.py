from logging import getLogger, INFO
from threading import Thread

from datastore import Session, ResultStore
from engine import get_random_location, get_next_random_possible_move, move
from model import Knight, MoveHistory, Board
from utils import get_batch_size


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
    def __init__(self, continue_condition, finish_watch, app_config):
        super().__init__()
        self.app_config = app_config
        self.results = []
        self.result_counter = 0
        self.continue_condition = continue_condition
        self.flush_condition = lambda: self.should_flush()
        self.flush_action = lambda: self.flush()
        self.done = False
        self.finish_watch_handle = finish_watch.register()

    def run(self):
        simulate_completely_to_list(self.results, self.continue_condition, self.flush_condition, self.flush_action)
        self.finish_watch_handle.confirm_finish()
        self.done = True
        return

    def should_flush(self):
        return len(self.results) >= self.app_config.get_batch_size()

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
