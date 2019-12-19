import time

from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from threading import Thread

from backend.datastore import InMemoryDataStore
from backend.models import CashAssets, UseAssets, InvestedAssets, Other, Portfolio
from backend.models import Currencies, CurrentLiabilities, LongTermLiabilities


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

        @app.route("/api/update_user_portfolio", methods=["POST"])
        def update_user_portfolio():
            store = InMemoryDataStore()
            json_data = request.get_json(force=True)

            cash_json = json_data["cashAssets"]
            cash = CashAssets(
                cash_json["checkingAcs"], cash_json["savingsAcs"], cash_json["moneyMarketAccounts"],
                cash_json["savingsBonds"], cash_json["cds"], cash_json["lifeInsurance"],
                Other(cash_json["other"]["title"], cash_json["other"]["amount"])
            )

            invested_json = json_data["investedAssets"]
            invested = InvestedAssets(
                invested_json["brokerage"],
                Other(invested_json["otherTax"]["title"], invested_json["otherTax"]["amount"]),
                invested_json["ira"], invested_json["rothIra"], invested_json["k401"], invested_json["sepIra"],
                invested_json["keogh"], invested_json["pension"], invested_json["annuity"], invested_json["realEstate"],
                invested_json["soleProp"], invested_json["partnership"], invested_json["cCorp"], invested_json["sCorp"],
                invested_json["limitedLiabilityCompany"],
                Other(invested_json["otherBusiness"]["title"], invested_json["otherBusiness"]["amount"])
            )

            use_json = json_data["useAssets"]
            use = UseAssets(
                use_json["principalHome"], use_json["vacationHome"], use_json["vehicles"],
                use_json["homeFurnishings"], use_json["artsAndAntiques"], use_json["jewelryAndFurs"],
                Other(use_json["other"]["title"], use_json["other"]["amount"])
            )

            current_json = json_data["currentLiabilities"]
            current = CurrentLiabilities(
                current_json["creditCardBalance"], current_json["incomeTaxOwed"],
                Other(current_json["other"]["title"], current_json["other"]["amount"])
            )

            long_json = json_data["longTermLiabilities"]
            long = LongTermLiabilities(
                long_json["homeMortgage"], long_json["homeEquityLoan"], long_json["rentPropertiesMortgage"],
                long_json["carLoans"], long_json["studentLoans"], long_json["lifeInsurancePolicyLoans"],
                Other(long_json["other"]["title"], long_json["other"]["amount"])
            )

            currency = Currencies[json_data["currency"]]
            email = json_data["email"]

            store.update_user_portfolio(
                email=email, portfolio=Portfolio(currency, cash, invested, use, current, long)
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
