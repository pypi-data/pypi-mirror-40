#!/usr/bin/env python
""" opensoundscape.py -- Opensoundscape
Usage:
    opensoundscape.py [-hv]
    opensoundscape.py init [-i <ini>]

Options:
    -h --help               Print this screen and exit
    -v --version            Print the version of opensoundscape.py
    -i --ini <ini>          Specify an override file [default: opensoundscape.ini]
"""

from docopt import docopt

def run():
    arguments = docopt(__doc__, version="opensoundscape.py version 0.1.0")

    if arguments["init"]:
        print("Hello, Init!")
