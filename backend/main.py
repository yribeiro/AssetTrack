import os

from backend import STORAGE_PATH
from backend.server import BackendServer
from backend.datastore import InMemoryDataStore

if __name__ == "__main__":
    # figure out if a folder exists - if it doesn't then create one
    if not os.path.isdir(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)

    if "users.pck" in os.listdir(STORAGE_PATH):
        # load data into memory
        InMemoryDataStore(users_pck_file=os.path.join(STORAGE_PATH, "users.pck"))

    # start the servers
    server = BackendServer("localhost", 5000)
    server.start()
    _ = input("Hit enter to kill ... ")
    server.stop()

    # persist the data to disk
    InMemoryDataStore().save_to_disk()
