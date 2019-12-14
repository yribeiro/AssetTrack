

class User:
    """
    Class to contain the details of an individual user
    """
    def __init__(self, first_name: str, last_name: str, age: int, email: str):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email

    def save_to_disk(self, loc: str):
        pass
