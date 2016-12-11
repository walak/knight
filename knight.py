import time
from threading import Thread

from datastore import Session, ResultStore
from engine import get_random_location, get_next_random_possible_move, move
from model import Knight, Board, MoveHistory
from logging import getLogger, INFO
from utils import get_batch_size
from simulator import Simulator

if __name__ == "__main__":
    finish = False

    start = time.time()
    condition = lambda: not finish

    knight = Knight(2, 2)
    board = Board()
    simulator = Simulator(condition)
    simulator.start()
    while not finish:
        input()
        finish = True
        print("Finishing calculations... wait until worker thread will be finished")
        while not simulator.done:
            time.sleep(1)

    print("Calculation finished on demand. Simulations generated: %i" % simulator.result_counter)
