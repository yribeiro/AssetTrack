from backend.models import CashAssets, UseAssets, Other, User, Currencies
from backend.models import InvestedAssets, CurrentLiabilities, LongTermLiabilities
from backend.models import Portfolio

from typing import Tuple


def get_test_assets_and_liabilities() -> Tuple[CashAssets, UseAssets,
                                               InvestedAssets, CurrentLiabilities, LongTermLiabilities]:
    """
    Utility function to generate assets and liability data.
    :return: Tuple(CashAssets, UseAssets, InvestedAssets, CurrentLiabilities, LongTermLiabilities)
    """
    cash = CashAssets(1, 2, 3, 4, 5, 6, Other("Test", 7))
    use = UseAssets(10, 20, 30, 40, 50, 60, Other("TestUse", 70))
    invested = InvestedAssets(
        1.5, Other("TestInvest", 2.5), 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5,
        11.5, 12.5, 13.5, 14.5, 15.5, Other("TestInvest", 16.5)
    )
    current = CurrentLiabilities(0, 1.1, Other("TestCurrent", 1.3))
    long = LongTermLiabilities(10, 20, 30, 40, 50, 60, Other(amount=70))

    return cash, use, invested, current, long


def get_test_user():
    """
    Function to return an instance of User()
    :return: User() with name Yohahn Ribeiro 25 yohahnribeiro29@gmail.com
    """
    fname, lname = "Yohahn", "Ribeiro"
    age = 25
    email = "yohahnribeiro29@gmail.com"
    return User(fname, lname, age, email)


def get_test_portfolio() -> Portfolio:
    """
    Function to return a populated instance of Portfolio() with GBP
    :return: new Portfolio()
    """
    cash, use, invested, current, long = get_test_assets_and_liabilities()
    p = Portfolio(
        Currencies.GBP, cash, invested, use, current, long
    )
    return p


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])
