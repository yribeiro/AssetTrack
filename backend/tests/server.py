from flask import Flask
from gevent.pywsgi import WSGIServer
from threading import Thread


class BackendServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._app = self._create_flask_app()
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

        return app

    def _run_server(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass
