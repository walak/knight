import time

from mechanics import FinishWatch
from model import Knight, Board
from simulator import Simulator

if __name__ == "__main__":
    finish_watch = FinishWatch()

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
