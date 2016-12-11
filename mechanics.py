from threading import Lock, Thread
from time import sleep

from utils import generate_random_id


class FinishHandle:
    def __init__(self, lock):
        self.finished = False
        self.lock = lock
        self.id = generate_random_id()

    def confirm_finish(self):
        self.lock.acquire()
        self.finished = True
        self.lock.release()


class FinishWatch:
    def __init__(self):
        self.finished = False
        self.finish_handlers = set()
        self.lock = Lock()

    def finish(self):
        self.finished = True

    def register(self):
        handle = FinishHandle(self.lock)
        self.__lock()
        self.finish_handlers.add(handle)
        return handle

    def all_confirmed_finished(self):
        self.__lock()
        all_finished = len({f.finished for f in self.finish_handlers if f.finished == False}) > 0
        self.__unlock()
        return all_finished

    def __lock(self):
        self.lock.acquire()

    def __unlock(self):
        self.lock.release()


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
