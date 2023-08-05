import logging
import unittest
import gnucash_importer
from gnucash_importer.util import Util
from gnucash_importer.account import GenericAccount, Nubank

class AccountTestCase(unittest.TestCase):
    def test_get_items(self):
        account = Nubank(Util().DEFAULT_ACCOUNT_SRC_FILE)

        self.assertEqual(len(account.get_items()), 9)

    def test_initialize_class(self):
        acc_from = Util().DEFAULT_NUBANK_FROM
        acc_to = Util().DEFAULT_NUBANK_TO
        acc_src_file = Util().DEFAULT_ACCOUNT_SRC_FILE

        with self.assertRaises(ValueError) as context:
            GenericAccount(None, acc_to, acc_src_file)

        self.assertEqual("acc_from can't be None!! Please, inform the \"account from\" parameter", str(context.exception))

        with self.assertRaises(ValueError) as context:
            GenericAccount(acc_from, None, acc_src_file)

        self.assertEqual("acc_to can't be None!! Please, inform the \"account to\" parameter", str(context.exception))

        with self.assertRaises(ValueError) as context:
            GenericAccount(acc_from, acc_to, None)

        self.assertEqual("acc_src_file can't be None!! Please, inform the \"account source file\" parameter", str(context.exception))

        self.assertEqual(len(Nubank(Util().DEFAULT_ACCOUNT_SRC_FILE).get_items()), 9)

        nubank = GenericAccount(acc_from, acc_to, acc_src_file, "nubank")
        self.assertEqual("nubank", str(nubank.name))

        generic = GenericAccount(acc_from, acc_to, acc_src_file, "generic")
        self.assertEqual("generic", str(generic.name))

        generic3 = GenericAccount(acc_from, acc_to, acc_src_file)
        self.assertEqual(GenericAccount.DEFAULT_NAME, str(generic3.name))

        generic_none = GenericAccount(acc_from, acc_to, acc_src_file, None)
        self.assertEqual(GenericAccount.DEFAULT_NAME, str(generic_none.name))
