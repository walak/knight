from flask import Flask

App = Flask(__name__)


@App.route("/status")
def status():
    return "OK!"



if __name__ == "__main__":
    App.run(port=3333, threaded=True)
