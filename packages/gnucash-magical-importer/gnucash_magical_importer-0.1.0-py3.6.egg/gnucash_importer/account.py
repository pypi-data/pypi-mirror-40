"""Module to handle accounts independently from gnucash."""

#!/usr/bin/env python

import os
from util import Util
from read_entry import OfxReader
from read_entry import QifReader
from read_entry import CsvReader

class Account(object):
    """Abstract class that define an account."""
    _acc_from = None
    _acc_to = None
    _account_src_file = None
    _name = None

    def __init__(self, acc_from, acc_to, acc_src_file, name):
        """Initialize an account and all parameters must be defined."""
        if acc_from is None:
            raise ValueError("acc_from can't be None!! Please, inform the \"account from\" parameter")

        if acc_to is None:
            raise ValueError("acc_to can't be None!! Please, inform the \"account to\" parameter")

        if acc_src_file is None:
            raise ValueError("acc_src_file can't be None!! Please, inform the \"account source file\" parameter")

        self._acc_from = acc_from
        self._acc_to = acc_to
        self._account_src_file = acc_src_file
        self._name = name

    @property
    def acc_from(self):
        return self._acc_from
    @acc_from.setter
    def acc_from(self, value):
        self._acc_from = value
    @acc_from.deleter
    def acc_from(self):
        del self._acc_from

    @property
    def acc_to(self):
        return self._acc_to
    @acc_to.setter
    def acc_to(self, value):
        self._acc_to = value
    @acc_to.deleter
    def acc_to(self):
        del self._acc_to

    @property
    def account_src_file(self):
        return self._account_src_file
    @account_src_file.setter
    def account_src_file(self, value):
        self._account_src_file = value
    @account_src_file.deleter
    def account_src_file(self):
        del self._account_src_file

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    @name.deleter
    def name(self):
        del self._name

    def get_items(self):
        """
        Return transactions from a specific read_entry.

        It is important to know that specific read_entry is determined by file extension.
        """
        file_type = os.path.splitext(self.account_src_file)[1]

        if file_type == "qif":
            return QifReader().get_transactions(self.account_src_file)
        elif file_type == "csv":
            return CsvReader().get_transactions(self.account_src_file)
        else:
            return OfxReader().get_transactions(self.account_src_file)

class GenericAccount(Account):
    """Implement Account and is used when no other account class is specified."""
    DEFAULT_NAME = "USER DEFINED IMPORT"
    def __init__(self, acc_from, acc_to, acc_src_file, name = DEFAULT_NAME):
        """
        This class expose the constructor as in super class.

        A default value is setted for name attribute if not given.
        """
        if name is None:
            name = self.DEFAULT_NAME

        super(GenericAccount, self).__init__(acc_from, acc_to, acc_src_file, name)

# for every source account do:
class Nubank(Account):
    """Implement Account for a specific high-level account: Nubank."""
    def __init__(self, acc_src_file):
        """
        Simplified constructor.

        All information is known before instantiate, except for account source file.
        """
        super(Nubank, self).__init__(Util().DEFAULT_NUBANK_FROM, Util().DEFAULT_NUBANK_TO, acc_src_file, "Nubank")

class CashInWallet(Account):
    """Implement Account for a specific high-level account: Cash in Wallet."""
    def __init__(self, acc_src_file):
        """
        Simplified constructor.

        All information is known before instantiate, except for account source file.
        """
        super(CashInWallet, self).__init__(Util().DEFAULT_CIW_FROM, Util().DEFAULT_CIW_TO, acc_src_file, "Cash in Wallet")

class CefSavingsAccount(Account):
    """Implement Account for a specific high-level account: CEF Savings Account."""
    def __init__(self, acc_src_file):
        """
        Simplified constructor.

        All information is known before instantiate, except for account source file.
        """
        super(CefSavingsAccount, self).__init__(Util().DEFAULT_CEF_SAVINGS_FROM, Util().DEFAULT_CEF_SAVINGS_TO, acc_src_file, "CEF Savings Account")

class ItauCheckingAccount(Account):
    """Implement Account for a specific high-level account: ITAU Checking Account."""
    def __init__(self, acc_src_file):
        """
        Simplified constructor.

        All information is known before instantiate, except for account source file.
        """
        super(ItauCheckingAccount, self).__init__(Util().DEFAULT_ITAU_CHECKING_ACCOUNT_FROM, Util().DEFAULT_ITAU_CHECKING_ACCOUNT_TO, acc_src_file, "ITAU Checking Account")

class ItauSavingsAccount(Account):
    """Implement Account for a specific high-level account: ITAU Savings Account."""
    def __init__(self, acc_src_file):
        """
        Simplified constructor.

        All information is known before instantiate, except for account source file.
        """
        super(ItauSavingsAccount, self).__init__(Util().DEFAULT_ITAU_SAVINGS_FROM, Util().DEFAULT_ITAU_SAVINGS_TO, acc_src_file, "ITAU Savings Account")

class BradescoSavingsAccount(Account):
    """Implement Account for a specific high-level account: BRADESCO Savings Account."""
    def __init__(self, acc_src_file):
        """
        Simplified constructor.

        All information is known before instantiate, except for account source file.
        """
        super(BradescoSavingsAccount, self).__init__(Util().DEFAULT_BRADESCO_SAVINGS_FROM, Util().DEFAULT_BRADESCO_SAVINGS_TO, acc_src_file, "BRADESCO Savings Account")
