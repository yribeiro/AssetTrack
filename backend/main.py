import os

from backend import STORAGE_PATH
from backend.models import CashAssets, UseAssets, InvestedAssets, Other, Portfolio
from backend.models import CurrentLiabilities, LongTermLiabilities, Currencies
from backend.server import BackendServer
from backend.datastore import InMemoryDataStore

if __name__ == "__main__":
    # figure out if a folder exists - if it doesn't then create one
    if not os.path.isdir(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)

    if "users.pck" in os.listdir(STORAGE_PATH):
        # load data into memory
        InMemoryDataStore(users_pck_file=os.path.join(STORAGE_PATH, "users.pck"))
    else:
        InMemoryDataStore().add_user("John", "Doe", 29, "john.doe@gmail.com")

        cash = CashAssets(1, 2, 3, 4, 5, 6, Other("Test", 7))
        use = UseAssets(10, 20, 30, 40, 50, 60, Other("TestUse", 70))
        invested = InvestedAssets(
            1.5, Other("TestInvest", 2.5), 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5,
            11.5, 12.5, 13.5, 14.5, 15.5, Other("TestInvest", 16.5)
        )
        current = CurrentLiabilities(0, 111.1, Other("TestCurrent", 21.3))
        long = LongTermLiabilities(10, 20, 30, 40, 50, 60, Other(amount=70))

        p = Portfolio(Currencies.GBP, cash, invested, use, current, long)

        InMemoryDataStore().update_user_portfolio("john.doe@gmail.com", p)

    # start the servers
    server = BackendServer("localhost", 5000)
    server.start()
    _ = input("Hit enter to kill ... ")
    server.stop()

    # persist the data to disk
    InMemoryDataStore().save_to_disk()
