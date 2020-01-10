import os
import pickle
import unittest

from unittest import mock

try:
    from . import utils
except ImportError:
    import utils

from backend.models import User, Portfolio


class TestUserClass(unittest.TestCase):
    def tearDown(self) -> None:
        # delete any pck files in the current working directory
        for file in os.listdir(os.getcwd()):
            if ".pck" in file:
                os.remove(os.path.join(os.getcwd(), file))

    def test_user_can_be_created(self):
        u = utils.get_test_user()
        self.assertEqual(u.first_name, "Yohahn")
        self.assertEqual(u.last_name, "Ribeiro")
        self.assertEqual(u.age, 25)
        self.assertEqual(u.email, "yohahnribeiro29@gmail.com")

    def test_user_is_persisted_to_disk_at_location(self):
        u = utils.get_test_user()
        u.save_to_disk(os.getcwd())

        # check that a pickle file has been saved
        name = str(u._id) + ".pck"
        self.assertTrue(name in os.listdir(os.getcwd()))

        # check that the right values have been saved
        with open(name, "rb") as fp:
            u2 = pickle.load(fp)

        self.assertTrue(isinstance(u2, User))
        self.assertEqual(u.first_name, u2.first_name)
        self.assertEqual(u.last_name, u2.last_name)
        self.assertEqual(u.age, u2.age)
        self.assertEqual(u.email, u2.email)

    def test_user_json_dict_is_generated_correctly(self):
        u = utils.get_test_user()

        ujson = u.to_json()

        # check with camecase keys
        self.assertEqual(ujson["firstName"], u.first_name)
        self.assertEqual(ujson["lastName"], u.last_name)
        self.assertEqual(ujson["age"], u.age)
        self.assertEqual(ujson["email"], u.email)

    def test_user_returns_right_net_worth(self):
        u = utils.get_test_user()

        self.assertIsNone(u.net_worth)  # returns None if no portfolio is set

        mock_port = mock.Mock(spec=Portfolio)
        mock_port.total_assets = 30
        mock_port.total_liabilities = 10
        u.portfolio = mock_port

        self.assertEqual(20, u.net_worth)
