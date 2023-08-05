import logging
import gnucash_importer
from gnucash_importer.util import Util
from gnucash_importer.account import Nubank
from gnucash_importer.ledger import Ledger
import unittest
from gnucash import Session, GncCommodity

class LedgerTestCase(unittest.TestCase):
    def setUp(self):
        self.util = Util()
        self.account = Nubank(self.util.DEFAULT_ACCOUNT_SRC_FILE)
        self.ledger = Ledger(self.account, self.util.DEFAULT_CURRENCY, False, self.util.DEFAULT_GNUCASH_FILE)

        session = Session(self.util.DEFAULT_GNUCASH_FILE)
        self.book = session.book
        self.currency = self.book.get_table().lookup('ISO4217', self.util.DEFAULT_CURRENCY)
        session.end()

    # TODO implement catch exception
    def test_get_quantity_transactions(self): # only happy case
        self.assertEqual(self.ledger.get_quantity_transactions(), 36)

    def test_get_gnucash_currency(self):
        currency = self.ledger.get_gnucash_currency(self.book, self.util.DEFAULT_CURRENCY)

        self.assertIsInstance(currency, GncCommodity)
        self.assertEqual(currency.get_fullname(), self.currency.get_fullname())
        self.assertEqual(currency.get_printname(), self.currency.get_printname())
        self.assertEqual(currency.get_unique_name(), self.currency.get_unique_name())
        self.assertEqual(currency.get_user_symbol(), self.currency.get_user_symbol())
        self.assertEqual(currency.is_currency(), self.currency.is_currency())
        self.assertEqual(currency.is_iso(), self.currency.is_iso())
        self.assertEqual(currency.get_mnemonic(), self.currency.get_mnemonic())

    def test_get_gnucash_account(self):
        # Happy case
        gnucash_account = self.ledger.get_gnucash_account(self.book, "Assets:Cash in Wallet") # Testing a balance != 0

        self.assertEqual(-6.0, gnucash_account.GetBalance().to_double())
        self.assertEqual("Cash in Wallet", gnucash_account.GetName())
        self.assertEqual("Assets.Cash in Wallet", gnucash_account.get_full_name())

        # TODO implement the catch if not found root.lookup_by_name

    def test_write(self):
        self.ledger.write()
        self.assertEqual(self.ledger.get_quantity_transactions(), 45)

if __name__ == '__main__':
    unittest.main()
