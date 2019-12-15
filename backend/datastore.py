import os
import pickle
import sys

from typing import List
from threading import Lock

from backend import STORAGE_PATH
from backend.models import User


class InMemoryDataStore:
    # define in memory global storage
    _USERS: List[User] = []

    _USERS_LOCK: Lock = Lock()

    def __init__(self, users_pck_file: str = None):
        """
        Constructor

        :param users_pck_file: .pck file that contains a stored user list.
        """
        if users_pck_file is not None:
            with open(users_pck_file, "rb") as fp:
                InMemoryDataStore._USERS = pickle.load(fp)

    @staticmethod
    def add_user(firstname: str, lastname: str, age: int, email: str):
        with InMemoryDataStore._USERS_LOCK:
            if list(filter(lambda user: user.email == email, InMemoryDataStore._USERS)):
                raise ValueError("This email address has already been registered")
            else:
                u = User(firstname, lastname, age, email)
                InMemoryDataStore._USERS.append(u)
                print(f"Added new user {u.first_name} {u.last_name}", file=sys.stdout)

    @staticmethod
    def save_to_disk():
        """
        Function to persist the data storage to disk. Stored in the backend storage
        area.
        """
        file_path = os.path.join(STORAGE_PATH, "users.pck")
        with open(file_path, "wb") as fp:
            pickle.dump(InMemoryDataStore._USERS, fp)

        print(f"Saved all users to file: {file_path}")
