import time
import unittest

from datetime import datetime

from backend.models import Currencies, Other
from backend.models import CashAssets, UseAssets, InvestedAssets
from backend.models import CurrentLiabilities, LongTermLiabilities
from backend.models import Portfolio


class TestPortfolioAndAssetLiabilities(unittest.TestCase):
    def setUp(self):
        self.cash = CashAssets(1, 2, 3, 4, 5, 6, Other("Test", 7))
        self.use = UseAssets(10, 20, 30, 40, 50, 60, Other("TestUse", 70))
        self.invested = InvestedAssets(
            1.5, Other("TestInvest", 2.5), 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5,
            11.5, 12.5, 13.5, 14.5, 15.5, Other("TestInvest", 16.5)
        )
        self.current = CurrentLiabilities(0, 1.1, Other("TestCurrent", 1.3))
        self.long = LongTermLiabilities(10, 20, 30, 40, 50, 60, Other(amount=70))

        # set the totals manually to check the underlying cash / asset later
        self.assets = 1 + 2 + 3 + 4 + 5 + 6 + 7
        self.assets += 10 + 20 + 30 + 40 + 50 + 60 + 70
        self.assets += 1.5 + 2.5 + 3.5 + 4.5 + 5.5 + 6.5 + 7.5 + 8.5 + 9.5 + 10.5
        self.assets += 11.5 + 12.5 + 13.5 + 14.5 + + 15.5 + 16.5
        self.liabilities = 0 + 1.1 + 1.3 + 10 + 20 + 30 + 40 + 50 + 60 + 70

    def test_portfolio_creation_throws_error_with_invalid_currency(self):
        with self.assertRaises(ValueError):
            _ = Portfolio("GBP", self.cash, self.invested, self.use, self.current, self.long)

    def test_portfolio_creation_successful(self):
        p = Portfolio(
            Currencies.GBP, self.cash, self.invested, self.use, self.current, self.long
        )  # will pass if everything is instantiated correctly
        time.sleep(0.1)
        end = datetime.now()

        # check the timestamp
        self.assertLess(p.timestamp, end)

    def test_portfolio_returns_correct_totals(self):
        p = Portfolio(
            Currencies.GBP, self.cash, self.invested, self.use, self.current, self.long
        )

        self.assertEqual(self.assets, p.total_assets)
        self.assertEqual(self.liabilities, p.total_liabilities)

    def test_portfolio_returns_correct_net_worth(self):
        p = Portfolio(
            Currencies.GBP, self.cash, self.invested, self.use, self.current, self.long
        )
        expected = self.assets - self.liabilities
        self.assertEqual(expected, p.net_worth)
