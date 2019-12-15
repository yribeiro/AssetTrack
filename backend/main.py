import os

from backend import STORAGE_PATH
from backend.server import BackendServer
from backend.datastore import InMemoryDataStore

if __name__ == "__main__":
    # figure out if a folder exists - if it doesn't then create one
    if not os.path.isdir(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)

    if os.listdir(STORAGE_PATH):
        # load data into memory
        pass

    # start the servers
