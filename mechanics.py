from threading import Lock, Thread
from time import sleep

from utils import generate_random_id
from logging import getLogger, INFO


class FinishHandle:
    def __init__(self, lock):
        self.finished = False
        self.lock = lock
        self.id = generate_random_id()
        self.log = getLogger("Handler-" + self.id)
        self.log.setLevel(INFO)

    def confirm_finish(self):  # excessive logging as I have no idea if it would work #TODO: cut the logging a bit
        self.log.debug("Trying to aquire lock")
        self.lock.acquire()
        self.log.debug("Lock aquired")
        self.finished = True
        self.log.info("Confirmed finish of task")
        self.lock.release()
        self.log.debug("Lock released")


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
    def __init__(self, result_store, finish_watch):
        super().__init__()
        self.items = {}
        self.datalock = Lock()
        self.result_store = result_store
        self.finish_watch = finish_watch
        self.finish_handle = self.finish_watch.register()

    def queue_items(self, items):
        self.datalock.acquire()
        self.items.update(items)
        self.datalock.release()

    def get_number_items_in_queue(self):
        return len(self.items)

    def run(self):
        while not self.finish_watch.finished:
            self.run_reconciliation()
            sleep(5)
        self.finish_handle.confirm_finish()

    def run_reconciliation(self):
        self.datalock.acquire()
        items_to_save = self.items
        self.items = {}
        self.result_store.store_batch(items_to_save)
        self.datalock.release()
