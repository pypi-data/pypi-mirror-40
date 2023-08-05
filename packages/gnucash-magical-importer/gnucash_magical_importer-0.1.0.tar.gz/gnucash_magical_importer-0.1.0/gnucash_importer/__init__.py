#!/usr/bin/env python3

import logging
import argparse
import sys
from cli import Cli
from util import Util
from ledger import Ledger
from read_entry import OfxReader, QifReader, CsvReader
from account import GenericAccount, Nubank, CashInWallet, CefSavingsAccount, ItauCheckingAccount, ItauSavingsAccount, BradescoSavingsAccount

name = "gnucash_magical_importer"
__all__ = ["account", "cli", "ledger", "ncurses", "red_entry", "util"] # TODO verify what that's meaning
with open('gnucash_importer/version.py') as f:
    exec(f.read())
