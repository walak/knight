import time
from http import client

from config import AppConfigProvider
from datastore import StorableMoveHistory
from mechanics import FinishWatch
from model import Knight, Board
from simulator import Simulator
from jsonpickle import pickler


class HttpSimulator(Simulator):
    def __init__(self, continue_condition, finish_watch, app_config):
        super().__init__(continue_condition, finish_watch, app_config)

    def prepare_payload(self):
        storable_history = [StorableMoveHistory.from_move_history(mh) for mh in self.results]
        return pickler.encode(storable_history)

    def flush(self):
        payload = self.prepare_payload()

        http_connection = client.HTTPConnection(self.app_config.get_http_host(),
                                                self.app_config.get_http_port())
        http_connection.connect()
        http_connection.request("POST", "/store_bundle", payload)

        http_connection.close()

        self.result_counter += len(self.results)
        self.results.clear()


if __name__ == "__main__":
    finish_watch = FinishWatch()
    app_config = AppConfigProvider().get_config()
    start = time.time()
    condition = lambda: not finish_watch.finished

    simulator = HttpSimulator(condition, finish_watch, app_config)
    simulator.start()

    input()
    print("Finishing calculations... wait until worker thread will be finished")
    finish_watch.finish()
    while not finish_watch.all_confirmed_finished():
        time.sleep(1)

    print("Calculation finished on demand. Simulations generated: %i" % simulator.result_counter)
