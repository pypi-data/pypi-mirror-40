from __future__ import print_function

import sys
import time
import traceback
import argparse
import os
import subprocess
import random
from collections import namedtuple

# Appending current working directory to sys.path
# So that user can run randomtester from the directory where sut.py is located
current_working_dir = os.getcwd()
sys.path.append(current_working_dir)

if "--help" not in sys.argv:
    import sut as SUT


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('expfile', metavar='filename', type=str, default=None,
                        help='Path to the experiment definition file.')
    parser.add_argument('--outputDir', type=str, default='.',
                        help="Directory to store results")

    parsed_args = parser.parse_args(sys.argv[1:])
    return (parsed_args, parser)


def make_config(pargs, parser):
    """
    Process the raw arguments, returning a namedtuple object holding the
    entire configuration, if everything parses correctly.
    """
    pdict = pargs.__dict__
    # create a namedtuple object for fast attribute lookup
    key_list = list(pdict.keys())
    arg_list = [pdict[k] for k in key_list]
    Config = namedtuple('Config', key_list)
    nt_config = Config(*arg_list)
    return nt_config


def main():

    parsed_args, parser = parse_args()
    config = make_config(parsed_args, parser)
    print(('Running experiments using config={}'.format(config)))

    sut = SUT.sut()

    timeout = config.timeout

    if not ((config.coverage) or (config.coverMore) or (config.decompose)):
        try:
            sut.stopCoverage()
        except BaseException:
            pass

    R = None
