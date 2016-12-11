from threading import Lock


class ResultStore:
    def __init__(self):
        self.items = {}
        self.datalock = Lock()

    def store_items(self, items):
        self.datalock.acquire()
        self.items.update(items)
        self.datalock.release()
