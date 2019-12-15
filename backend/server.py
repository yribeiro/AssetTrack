import time

from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from threading import Thread

from backend.datastore import InMemoryDataStore


class BackendServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        # create the flask app and the wsgi server
        self._app = self._create_flask_app()
        self._wsgi_server = None  # has to be set inside the _run_server function
        self._thread = Thread(target=self._run_server)

    @staticmethod
    def _create_flask_app() -> Flask:
        """
        Helper function to create the flask app with the appropriate routes.
        :return: Instance of the Flask route handling object.
        """
        app = Flask(__name__)

        @app.route("/")
        def index():
            return "WebApp Index"

        @app.route("/api/add_user", methods=["POST"])
        def add_user():
            store = InMemoryDataStore()
            user_json = request.get_json(force=True)
            store.add_user(
                firstname=user_json["firstname"], lastname=user_json["lastname"],
                age=user_json["age"], email=user_json["email"]
            )
            return jsonify("Success")

        return app

    def _run_server(self):
        """
        Helper function to start the wsgi server in a separate thread, using the
        pointers to the instantiated WSGI server from the constructor.
        """
        self._wsgi_server = WSGIServer((self.host, self.port), self._app)
        self._wsgi_server.serve_forever()

    def start(self):
        if not self._thread.is_alive():
            self._thread.start()
            print(f"Started BackendServer on {self.host}:{self.port}")
        else:
            print("The BackendServer is already running")

    def stop(self, timeout=2):
        if self._thread.is_alive() and self._wsgi_server is not None:
            # kill the WSGI server and then kill the thread
            self._wsgi_server.stop(timeout=timeout)
            self._wsgi_server.close()
            self._thread.join(timeout=timeout + 2)

            # sleep to give the server time to kill requests
            time.sleep(1)
            if self._thread.is_alive():
                raise OSError("Server Thread did not shutdown cleanly")
            else:
                print("BackendServer successfully shutdown")
        else:
            print("The BackendServer is already shutdown")


if __name__ == "__main__":
    server = BackendServer("localhost", 5000)
    server.start()
    _ = input("Hit enter to kill ... ")
    server.stop()