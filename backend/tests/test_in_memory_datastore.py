import os
import pickle
import unittest

from backend.datastore import InMemoryDataStore
from backend.models import User


class TestInMemoryDataStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.TEST_STORAGE_PATH = os.path.join(os.getcwd(), "test_storage")
        if not os.path.isdir(cls.TEST_STORAGE_PATH):
            os.makedirs(cls.TEST_STORAGE_PATH)

        # load and save some dummy data
        cls.TEST_USER = User("John", "Doe", 23, "john.doe@gmail.com")

        with open(os.path.join(cls.TEST_STORAGE_PATH, "users.pck"), "wb") as fp:
            pickle.dump([cls.TEST_STORAGE_PATH], fp)

    def tearDown(self):
        if os.path.isdir(self.TEST_STORAGE_PATH):
            for file in os.listdir(self.TEST_STORAGE_PATH):
                os.remove(os.path.join(self.TEST_STORAGE_PATH, file))

            os.rmdir(self.TEST_STORAGE_PATH)

    def test_datastore_loads_pck_file(self):
        pass

    def test_datastore_add_user(self):
        pass

    def test_datastore_persists_to_disk(self):
        pass
