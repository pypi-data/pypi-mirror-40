# TODO implement this workarround to make test discover work
import sys
sys.path.append('gnucash_importer')

"""
All tests can receive an OS var (DEBUG_TEST) to determine if logging will be used during tests.
A typical use case can be the debug of tests itself.
"""
import os, logging
from gnucash_importer.util import Util
if os.environ.get('DEBUG_TEST', False) in ['TRUE', 'True', 'true', '1', 't', 'y', 'yes']:
    loglevel = logging.DEBUG
    logformat = Util.LOG_FORMAT_DEBUG
    logging.basicConfig(level = loglevel, format = logformat)
