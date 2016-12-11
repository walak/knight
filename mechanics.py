from threading import Lock, Thread
from datastore import ResultStore
from time import sleep


class FinishWatch:
    def __init__(self):
        self.finished = False
        self.finish_confirmations = {}
        self.lock = Lock()

    def finish(self):
        self.finished = True

    def register_for_confirmation(self, name):
        self.finish_confirmations[name] = False

    def confirm_finish(self, name):
        self.lock.acquire()
        self.finish_confirmations[name] = True
        self.lock.release()

    def all_confirmed_finished(self):
        self.lock.acquire()
        all_finished = len({v for v in self.finish_confirmations.values() if v == False}) > 0
        self.lock.release()
        return all_finished


class TemporalResultStore(Thread):
    def __init__(self, result_store):
        super().__init__()
        self.items = {}
        self.datalock = Lock()
        self.result_store = result_store

    def queue_items(self, items):
        self.datalock.acquire()
        self.items.update(items)
        self.datalock.release()

    def get_number_items_in_queue(self):
        return len(self.items)

    def run_reconciliation(self):
        self.datalock.acquire()
        items_to_save = self.items
        self.items = {}
        self.result_store.store_batch(items_to_save)
        self.datalock.release()
        sleep(5)
