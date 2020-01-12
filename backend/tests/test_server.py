import requests
import socket
import time
import unittest

try:
    from . import utils
except ImportError:
    import utils

from backend.server import BackendServer
from backend.datastore import InMemoryDataStore
from backend.models import Currencies, Portfolio


class TestBackendServer(unittest.TestCase):
    def setUp(self):
        self.host = "localhost"
        self.port = 50123
        # add to the datastore
        store = InMemoryDataStore()
        store.add_user("John", "Doe", 23, "john.doe@gmail.com")

    def tearDown(self):
        store = InMemoryDataStore()
        store.clear()

    def test_server_startup(self):
        server = BackendServer(host=self.host, port=self.port)
        server.start()
        time.sleep(1)  # sleep to allow server to start

        # try and bind to the socket and handle error
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with self.assertRaises(OSError):
            s.bind((self.host, self.port))  # Try to open port
        s.close()

        server.stop()

    def test_server_responds_to_http_request_on_base(self):
        server = BackendServer(host=self.host, port=self.port)
        server.start()
        time.sleep(1)  # sleep to allow server to start
        resp = requests.get(f"http://{self.host}:{self.port}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, "WebApp Index")
        server.stop()

    def test_server_shutdown(self):
        server = BackendServer(host=self.host, port=self.port)
        server.start()
        time.sleep(1)  # sleep to allow server to start
        server.stop()

        # try and bind to the socket and handle error
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))  # Try to open port - passes if connection is made
        s.close()

    def test_server_add_user_endpoint(self):
        server = BackendServer(host=self.host, port=self.port)
        server.start()

        # make a request on the add user end point as get
        resp = requests.get(f"http://{self.host}:{self.port}/api/add_user")
        self.assertEqual(resp.status_code, 405)

        # make valid request as post with user data
        u = utils.get_test_user()
        resp = requests.post(
            f"http://{self.host}:{self.port}/api/add_user",
            json={
                "firstname": u.first_name, "lastname": u.last_name,
                "age": u.age, "email": u.email
            }
        )
        self.assertEqual(resp.status_code, 200)

        # make valid request with same email address
        resp = requests.post(
            f"http://{self.host}:{self.port}/api/add_user",
            json={
                "firstname": u.first_name, "lastname": u.last_name,
                "age": u.age, "email": u.email
            }
        )
        self.assertEqual(500, resp.status_code)

        server.stop()

    def test_server_update_user_portfolio_endpoint(self):
        server = BackendServer(host=self.host, port=self.port)
        server.start()

        # make a request on the end point as get
        resp = requests.get(f"http://{self.host}:{self.port}/api/update_user_portfolio")
        self.assertEqual(resp.status_code, 405)

        # make valid request to the endpoint
        json_data = dict()
        json_data["currency"] = Currencies.GBP.name
        json_data["email"] = "john.doe@gmail.com"

        # generate asset and liabilities data
        cash, use, invested, current, long = utils.get_test_assets_and_liabilities()

        # cash Assets
        vals = {utils.to_camel_case(k): v for k, v in cash.__dict__.items()}
        vals["other"] = cash.other.__dict__
        json_data["cashAssets"] = vals

        # use Assets
        vals = {utils.to_camel_case(k): v for k, v in use.__dict__.items()}
        vals["other"] = use.other.__dict__
        json_data["useAssets"] = vals

        # invested Assets
        vals = {utils.to_camel_case(k): v for k, v in invested.__dict__.items()}
        vals["otherTax"] = invested.other_tax.__dict__
        vals["otherBusiness"] = invested.other_business.__dict__
        json_data["investedAssets"] = vals

        vals = {utils.to_camel_case(k): v for k, v in current.__dict__.items()}
        vals["other"] = current.other.__dict__
        json_data["currentLiabilities"] = vals

        vals = {utils.to_camel_case(k): v for k, v in long.__dict__.items()}
        vals["other"] = long.other.__dict__
        json_data["longTermLiabilities"] = vals

        resp = requests.post(f"http://{self.host}:{self.port}/api/update_user_portfolio", json=json_data)
        self.assertEqual(resp.status_code, 200)

        server.stop()

    def test_server_get_user_endpoint(self):
        server = BackendServer(host=self.host, port=self.port)
        server.start()

        # make request without email in args
        resp = requests.get(f"http://{self.host}:{self.port}/api/get_user")
        self.assertEqual(resp.status_code, 500)

        # make request with email in args
        resp = requests.get(
            f"http://{self.host}:{self.port}/api/get_user",
            params={"email": "john.doe@gmail.com"}
        )

        self.assertEqual(resp.json()["firstName"], "John")
        self.assertEqual(resp.json()["lastName"], "Doe")

        server.stop()

    def test_server_get_user_net_worth_endpoint(self):
        server = BackendServer(host=self.host, port=self.port)
        server.start()

        # make request with no portfolio leading to a none
        resp = requests.get(
            f"http://{self.host}:{self.port}/api/get_net_worth",
            params={"email": "john.doe@gmail.com"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.json())

        # mock portfolio
        mock_port = utils.get_test_portfolio()
        InMemoryDataStore().update_user_portfolio("john.doe@gmail.com", mock_port)

        # test
        resp = requests.get(
            f"http://{self.host}:{self.port}/api/get_net_worth",
            params={"email": "john.doe@gmail.com"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mock_port.total_assets - mock_port.total_liabilities, resp.json())

        server.stop()

    def test_server_get_user_assets_endpoint(self):
        server = BackendServer(host=self.host, port=self.port)
        server.start()

        # make request with no portfolio leading to a none
        resp = requests.get(
            f"http://{self.host}:{self.port}/api/get_assets",
            params={"email": "john.doe@gmail.com"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.json())

        # mock portfolio
        mock_port = utils.get_test_portfolio()
        InMemoryDataStore.update_user_portfolio("john.doe@gmail.com", mock_port)

        # test
        resp = requests.get(
            f"http://{self.host}:{self.port}/api/get_assets",
            params={"email": "john.doe@gmail.com"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mock_port.total_assets, resp.json())

        server.stop()

    def test_server_get_user_liabilities_endpoint(self):
        server = BackendServer(host=self.host, port=self.port)
        server.start()

        # make request with no portfolio leading to a none
        resp = requests.get(
            f"http://{self.host}:{self.port}/api/get_liabilities",
            params={"email": "john.doe@gmail.com"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.json())

        mock_port = utils.get_test_portfolio()
        InMemoryDataStore().update_user_portfolio("john.doe@gmail.com", mock_port)

        # test
        resp = requests.get(
            f"http://{self.host}:{self.port}/api/get_liabilities",
            params={"email": "john.doe@gmail.com"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(mock_port.total_liabilities, resp.json())

        server.stop()
