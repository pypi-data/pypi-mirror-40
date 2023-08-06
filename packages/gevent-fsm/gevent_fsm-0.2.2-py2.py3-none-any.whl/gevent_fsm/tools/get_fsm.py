#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
    get_fsm [options] <uuid> <output>

Options:
    -h, --help        Show this page
    --debug            Show debug logging
    --verbose        Show verbose logging
"""
from docopt import docopt
import logging
import sys
import requests

SERVER_URL = "https://fsm-designer-svg.com/prototype/download?diagram_id="

logger = logging.getLogger('get_fsm')


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = docopt(__doc__, args)
    if parsed_args['--debug']:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    response = requests.get(SERVER_URL + parsed_args['<uuid>'])
    if response.status_code == requests.codes.ok:
        with open(parsed_args['<output>'], 'w') as f:
                f.write(response.text)
        return 0
    else:
        print("No such FSM found")
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
