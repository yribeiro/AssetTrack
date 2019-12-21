import enum
import os
import pickle
import uuid

from datetime import datetime


class Currencies(enum.Enum):
    """
    Valid currencies to create portfolios with.
    """
    GBP = 1
    USD = 2
    EUR = 3
    INR = 4


class Other:
    """
    Class used to capture other assets and liabilities not covered by the below classes.
    Note: Assumption is that this currency is consistent with the top level asset.
    """

    def __init__(self, title=None, amount=0):
        self.title = title
        self.amount = amount


class CashAssets:
    """
    Class to contain the values of personal cash asset items.
    """

    def __init__(
            self, checking_acs=0, savings_acs=0, money_market_accounts=0,
            savings_bonds=0, cds=0, life_insurance=0, other=Other()
    ):
        self.checking_acs = checking_acs
        self.savings_acs = savings_acs
        self.money_market_accounts = money_market_accounts
        self.savings_bonds = savings_bonds
        self.cds = cds
        self.life_insurance = life_insurance
        self.other = other

    @property
    def total(self):
        total = self.checking_acs + self.savings_acs + self.life_insurance
        total += self.money_market_accounts + self.savings_bonds + self.cds
        total += self.other.amount
        return total


class InvestedAssets:
    """
    Class to contain the values of personal invested asset items.
    """

    def __init__(
            self, brokerage=0, other_tax=Other(), ira=0, roth_ira=0,
            k401=0, sep_ira=0, keogh=0, pension=0, annuity=0, real_estate=0, sole_prop=0,
            partnership=0, c_corp=0, s_corp=0, limited_liability_company=0,
            other_business=Other()
    ):
        self.roth_ira = roth_ira
        self.k401 = k401
        self.sep_ira = sep_ira
        self.keogh = keogh
        self.pension = pension
        self.annuity = annuity
        self.real_estate = real_estate
        self.sole_prop = sole_prop
        self.partnership = partnership
        self.c_corp = c_corp
        self.s_corp = s_corp
        self.limited_liability_company = limited_liability_company
        self.other_business = other_business
        self.ira = ira
        self.other_tax = other_tax
        self.brokerage = brokerage

    @property
    def total(self):
        total = self.roth_ira + self.k401 + self.sep_ira + self.keogh
        total += self.pension + self.annuity + self.real_estate + self.sole_prop + self.partnership
        total += self.c_corp + self.s_corp + self.limited_liability_company + self.ira
        total += self.brokerage + self.other_business.amount + self.other_tax.amount
        return total


class UseAssets:
    """
    Class to contain the values of personal use asset items.
    """

    def __init__(
            self, principal_home=0, vacation_home=0, vehicles=0,
            home_furnishings=0, arts_and_antiques=0, jewelry_and_furs=0, other=Other()
    ):
        self.vacation_home = vacation_home
        self.vehicles = vehicles
        self.home_furnishings = home_furnishings
        self.arts_and_antiques = arts_and_antiques
        self.jewelry_and_furs = jewelry_and_furs
        self.other = other
        self.principal_home = principal_home

    @property
    def total(self):
        total = self.vacation_home + self.vehicles + self.home_furnishings
        total += self.arts_and_antiques + self.jewelry_and_furs + self.principal_home
        total += self.other.amount
        return total


class CurrentLiabilities:
    """
    Class to contain the values of personal current liabilities items.
    """

    def __init__(self, credit_card_balance=0, income_tax_owed=0, other=Other()):
        self.credit_card_balance = credit_card_balance
        self.income_tax_owed = income_tax_owed
        self.other = other

    @property
    def total(self):
        total = self.credit_card_balance + self.income_tax_owed + self.other.amount
        return total


class LongTermLiabilities:
    """
    Class to contain the values of personal current liabilities items.
    """

    def __init__(
            self, home_mortgage=0, home_equity_loan=0, rent_properties_mortgage=0,
            car_loans=0, student_loans=0, life_insurance_policy_loans=0, other=Other()
    ):
        self.home_mortgage = home_mortgage
        self.home_equity_loan = home_equity_loan
        self.rent_properties_mortgage = rent_properties_mortgage
        self.car_loans = car_loans
        self.student_loans = student_loans
        self.life_insurance_policy_loans = life_insurance_policy_loans
        self.other = other

    @property
    def total(self):
        total = self.home_mortgage + self.home_equity_loan + self.rent_properties_mortgage
        total += self.car_loans + self.student_loans + self.life_insurance_policy_loans
        total += self.other.amount
        return total


class Portfolio:
    """
    Class containing a snapshot of the user's asset portfolio
    Based on: https://www.schwabmoneywise.com/public/file/P-4038856/Net-Worth-Worksheet.pdf
    """

    def __init__(
            self, currency: Currencies, cash_assets: CashAssets, invested_assets: InvestedAssets,
            use_assets: UseAssets, current_liabilities: CurrentLiabilities, long_term_liabilities: LongTermLiabilities,
            timestamp=datetime.now()
    ):
        if not isinstance(currency, Currencies):
            raise ValueError("Expected type Currencies")

        self.currency = currency
        self.cash_assets = cash_assets
        self.invested_assets = invested_assets
        self.use_assets = use_assets
        self.current_liabilities = current_liabilities
        self.long_term_liabilities = long_term_liabilities
        self.timestamp = timestamp  # this may be overwritten

    @property
    def total_assets(self):
        return self.cash_assets.total + self.invested_assets.total + self.use_assets.total

    @property
    def total_liabilities(self):
        return self.current_liabilities.total + self.long_term_liabilities.total

    @property
    def net_worth(self):
        return self.total_assets - self.total_liabilities


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
        self.portfolio = None

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

    def to_json(self):
        """
        Function to create dictionary representation of the class.

        :return: Dictionary version of the User class.
        """
        user_json = dict()
        user_json["firstName"] = self.first_name
        user_json["lastName"] = self.last_name
        user_json["age"] = self.age
        user_json["email"] = self.email
        return user_json
