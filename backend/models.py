import os
import pickle
import uuid


class User:
    """
    Class to contain the details of an individual user
    """
    def __init__(self, first_name: str, last_name: str, age: int, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self._id = uuid.uuid1()

    def save_to_disk(self, loc: str):
        """
        Function to persist the user to disk as a .pck file at the specified location.
        The user is saved with it's unique uuid, that is created on instantiation.

        :param loc: os.path location to save to
        """
        fname = str(self._id) + ".pck"
        with open(os.path.join(loc, fname), "wb") as fp:
            pickle.dump(self, fp)

        print(f"Saved user to disk as {fname}")
