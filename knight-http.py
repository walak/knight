from flask import Flask, request
from flask import Response

from mechanics import FinishHandle, FinishWatch, TemporalResultStore
from datastore import ResultStore, StorableMoveHistory
from jsonpickle import unpickler

App = Flask(__name__)
finish_watch = FinishWatch()
temporal_store = TemporalResultStore(finish_watch)


@App.route("/status")
def status():
    return "OK!"


@App.route("/store_one", methods=["POST"])
def store_one():
    json = request.get_json(force=True)
    smh = StorableMoveHistory.from_dict(json)
    temporal_store.queue_items([smh])
    return Response(status=200)


@App.route("/store_bundle", methods=["POST"])
def store_bundle():
    json = request.get_json(force=True)
    stories = [StorableMoveHistory.from_dict(s) for s in json]
    temporal_store.queue_items(stories)
    return Response(status=200)


if __name__ == "__main__":
    temporal_store.start()
    App.run(port=3333, threaded=True)
