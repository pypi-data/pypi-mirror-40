"""Main Module responsibility for all command line fuctions."""
#!/usr/bin/env python3

import logging
from termcolor import colored
from util import Util
from ledger import Ledger

class Cli:
    """This class will coordinate all actions."""
    def import_data(account, currency, dry_run, gnucash_file):
        """
        Import data from a given file into a given gnucash file.

        Must have an account and a gnucash file defined.
        Is optional define the currency (default can setted in seupt.cfg - usiing BRL).
        Also, is optional define dry_run (default is **true**).
        """
        logging.info(Util.info("Importing data to ")  + colored("{a}".format(a = account.name), 'yellow', attrs=['bold', 'underline']) + Util.info("'s account"))
        Ledger(account, currency, dry_run, gnucash_file).write()
        # TODO implement report
