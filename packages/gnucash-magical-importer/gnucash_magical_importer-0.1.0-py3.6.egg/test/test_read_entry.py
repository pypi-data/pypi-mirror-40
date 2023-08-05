from gnucash_importer.read_entry import OfxReader, QifReader, CsvReader
from gnucash_importer.util import Util
import unittest

class EntryReaderTestCase(unittest.TestCase):
    def test_get_transactions_ofx(self):
        transactions = OfxReader().get_transactions(Util().DEFAULT_ACCOUNT_SRC_FILE)
        self.assertEqual(len(transactions), 9)

    @unittest.skip("not implemented yet")
    def test_get_transactions_qif(self):
        pass

    @unittest.skip("not implemented yet")
    def test_get_transactions_csv(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
