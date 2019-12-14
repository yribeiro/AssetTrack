import sys

from typing import List
from threading import Lock

from backend.models import User


class InMemoryDataStore:
    # define in memory global storage
    _USERS: List[User] = []

    _USERS_LOCK: Lock = Lock()

    def __init__(self):
        pass

    def add_user(self, firstname: str, lastname: str, age: int, email: str):
        with self._USERS_LOCK:
            if list(filter(lambda user: user.email == email, self._USERS)):
                raise ValueError("This email address has already been registered")
            else:
                u = User(firstname, lastname, age, email)
                self._USERS.append(u)
                print(f"Added new user {u.first_name} {u.last_name}", file=sys.stdout)
