#!/usr/bin/env python3

import sys
sys.path.append('gnucash_importer')
from termcolor import colored
import configparser
# import datetime
from decimal import Decimal
import xml.etree.ElementTree as ET
from gnucash import Session, Transaction, Split, GncNumeric
# from abc import abstractmethod
from ofxparse import OfxParser  # ofxparse +0.14

import logging
import argparse
import sys
from cli import Cli
from util import Util
from ledger import Ledger
from read_entry import OfxReader, QifReader, CsvReader
from account import GenericAccount, Nubank, CashInWallet, CefSavingsAccount, ItauCheckingAccount, ItauSavingsAccount, BradescoSavingsAccount

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "GNUCash utility to fix xml file and import custom data.")
    parser.add_argument("-dr", "--dry-run", action = 'store_true', help = "actions will *NOT* be writen to gnucash file.")
    parser.add_argument("-q", "--quiet", action = 'store_true', help = "Set *NO* verbose logging i.e.: loglevel = logging.WARN")
    parser.add_argument("-v", "--verbose", action = 'store_true', help = "Set *VERBOSE* logging i.e.: loglevel = logging.DEBUG")
    parser.add_argument("-c", "--currency", default = Util().DEFAULT_CURRENCY, help = "currency used in gnucash. Default is BRL.")
    parser.add_argument("-gf", "--gnucash_file", default = Util().DEFAULT_GNUCASH_FILE, help = "GNUCash xml file to write")
    parser.add_argument("-a", "--account", choices = ["nubank", "ciw", "cef-savings", "itau-cc", "itau-savings", "bradesco-savings", "generic"], required = True, help = "Set account that will be used.")
    parser.add_argument("-af", "--account_src_file", required = True, help = "Set account source to integrate")
    parser.add_argument("-acf", "--account_from", help = "Define from import")
    parser.add_argument("-act", "--account_to", help = "Define to import")

    args = parser.parse_args()
    if args.verbose:
        loglevel = logging.DEBUG
        logformat = Util.LOG_FORMAT_DEBUG
    elif args.quiet:
        loglevel = logging.WARN
        # TODO log to file in this case
        logformat = Util.LOG_FORMAT_FULL
    else:
        loglevel = logging.INFO
        logformat = Util.LOG_FORMAT_SIMPLE

    # TODO config logger by dictnoray - https://realpython.com/python-logging/
    logging.basicConfig(level = loglevel, format = logformat)

    if args.verbose:
        logging.debug(Util.debug("args: {v}".format(v = vars(args))))

    account = None
    if args.account == "nubank":
        account = Nubank(args.account_src_file)
    elif args.account == "ciw":
        account = CashInWallet(args.account_src_file)
    elif args.account == "cef-savings":
        account = CefSavingsAccount(args.account_src_file)
    elif args.account == "itau-cc":
        account = ItauCheckingAccount(args.account_src_file)
    elif args.account == "itau-savings":
        account = ItauSavingsAccount(args.account_src_file)
    elif args.account == "bradesco-savings":
        account = BradescoSavingsAccount(args.account_src_file)
    else:
        try:
            account = GenericAccount(args.account_from, args.account_to, args.account_src_file, args.account)
        except Exception as error:
            logging.error(Util.error("Can't work without account_from || account_to || account_src_file!! Please, inform all parameters!!"))
            logging.error(Util.error("message: {m}".format(m = error)))
            logging.error(Util.error("type: {t} with args {args}".format(t = type(error), args = error.args)))
            sys.exit("Failed execution. Please, see the log above.")

    logging.debug(Util.debug(vars(account)))

    if account is None:
        logging.error(Util.error("Failed with account: need be defined!!!"))
        sys.exit("Failed execution. Please, see the log above.")

    # FIXME args.gnucash_file must be mandatory!!!
    Cli.import_data(account, args.currency, args.dry_run, args.gnucash_file)
    sys.exit(0)
