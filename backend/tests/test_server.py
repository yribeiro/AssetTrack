import requests
import socket
import time
import unittest

from backend.server import BackendServer


class TestBackendServer(unittest.TestCase):
    def setUp(self):
        self.host = "localhost"
        self.port = 50123

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
        time.sleep(1)  # sleep to allow server to start

        # make a request on the add user end point as get
        resp = requests.get(f"http://{self.host}:{self.port}/api/add_user")
        self.assertEqual(resp.status_code, 405)

        # make valid request as post with user data
        resp = requests.post(
            f"http://{self.host}:{self.port}/api/add_user",
            json={
                "firstname": "Yohahn", "lastname": "Ribeiro",
                "age": 25, "email": "  yohahnribeiro29@gmail.com"
            }
        )
        self.assertEqual(resp.status_code, 200)

        # make valid request with same email address
        resp = requests.post(
            f"http://{self.host}:{self.port}/api/add_user",
            json={
                "firstname": "Yohahn", "lastname": "Ribeiro",
                "age": 25, "email": "  yohahnribeiro29@gmail.com"
            }
        )
        self.assertEqual(500, resp.status_code)

        server.stop()
