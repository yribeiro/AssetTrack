import os
import pickle
import unittest

import utils

from backend.datastore import InMemoryDataStore
from backend.models import User, Portfolio, Currencies


class TestInMemoryDataStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.TEST_STORAGE_PATH = os.path.join(os.getcwd(), "test_storage")
        # load and save some dummy data
        cls.TEST_USER = User("John", "Doe", 23, "john.doe@gmail.com")

    def setUp(self):
        if not os.path.isdir(self.TEST_STORAGE_PATH):
            os.makedirs(self.TEST_STORAGE_PATH)

        with open(os.path.join(self.TEST_STORAGE_PATH, "users.pck"), "wb") as fp:
            pickle.dump([self.TEST_USER], fp)

    def tearDown(self):
        if os.path.isdir(self.TEST_STORAGE_PATH):
            for file in os.listdir(self.TEST_STORAGE_PATH):
                os.remove(os.path.join(self.TEST_STORAGE_PATH, file))

            os.rmdir(self.TEST_STORAGE_PATH)

        # clear the contents after a test
        InMemoryDataStore.clear()

    def test_datastore_loads_pck_file(self):
        InMemoryDataStore(users_pck_file=os.path.join(
            self.TEST_STORAGE_PATH, "users.pck"
        ))

        self.assertEqual(InMemoryDataStore._USERS[0].first_name, self.TEST_USER.first_name)
        self.assertEqual(InMemoryDataStore._USERS[0].last_name, self.TEST_USER.last_name)
        self.assertEqual(InMemoryDataStore._USERS[0].age, self.TEST_USER.age)
        self.assertEqual(InMemoryDataStore._USERS[0].email, self.TEST_USER.email)

    def test_datastore_add_user(self):
        # create store with default data
        store = InMemoryDataStore(users_pck_file=os.path.join(self.TEST_STORAGE_PATH, "users.pck"))

        # add a new user
        store.add_user("Jane", "Doe", 18, "jane.doe@gmail.com")
        self.assertEqual(InMemoryDataStore._USERS[1].email, "jane.doe@gmail.com")

        # add an existing email
        with self.assertRaises(ValueError):
            store.add_user(
                self.TEST_USER.first_name, self.TEST_USER.last_name,
                self.TEST_USER.age, self.TEST_USER.email
            )

    def test_datastore_persists_to_disk(self):
        users_file = os.path.join(self.TEST_STORAGE_PATH, "users.pck")
        # get contents of the current file
        with open(users_file, "rb") as fp:
            orig_users = pickle.load(fp)

        # create store and populate with file, then add user
        store = InMemoryDataStore(users_pck_file=users_file)
        store.add_user("Jane", "Doe", 18, "jane.doe@gmail.com")

        # persist to disk
        store.save_to_disk(loc=self.TEST_STORAGE_PATH)

        # get contents and check that list is appended
        with open(users_file, "rb") as fp:
            new_users = pickle.load(fp)

        self.assertGreater(len(new_users), len(orig_users))
        self.assertIsNone(new_users[1].portfolio)

    def test_update_user_portfolio_raises_error_for_invalid_user(self):
        users_file = os.path.join(self.TEST_STORAGE_PATH, "users.pck")
        store = InMemoryDataStore(users_file)

        cash, use, invested, current, long = utils.get_test_assets_and_liabilities()

        with self.assertRaises(ValueError):
            store.update_user_portfolio("test.email@email.com", Portfolio(
                Currencies.GBP, cash, invested, use, current, long
            ))

    def test_update_user_portfolio_persists_change(self):
        pass
