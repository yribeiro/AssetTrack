import os
import pickle
import unittest

from backend.models import User


class TestUserClass(unittest.TestCase):
    def tearDown(self) -> None:
        # delete any pck files in the current working directory
        for file in os.listdir(os.getcwd()):
            if ".pck" in file:
                os.remove(os.path.join(os.getcwd(), file))

    def test_user_can_be_created(self):
        u = self._create_test_user()
        self.assertEqual(u.first_name, "Yohahn")
        self.assertEqual(u.last_name, "Ribeiro")
        self.assertEqual(u.age, 25)
        self.assertEqual(u.email, "yohahnribeiro29@gmail.com")

    def test_user_is_persisted_to_disk_at_location(self):
        u = self._create_test_user()
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

    @staticmethod
    def _create_test_user() -> User:
        fname = "Yohahn"
        lname = "Ribeiro"
        age = 25
        email = "yohahnribeiro29@gmail.com"
        return User(fname, lname, age, email)
