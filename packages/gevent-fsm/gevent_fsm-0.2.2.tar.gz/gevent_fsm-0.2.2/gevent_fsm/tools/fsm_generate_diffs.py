#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Red Hat, Inc

"""
Usage:
    fsm_generate_diffs [options] python <design> <implementation>
    fsm_generate_diffs [options] javascript <design> <implementation>

Options:
    -h, --help        Show this page
    --debug            Show debug logging
    --verbose        Show verbose logging
    --initial        Create a new implementation
    --append         Append the newly generated code to the implementation.
"""
from docopt import docopt
import logging
import sys
from . import fsm_diff
from . import transform_fsm
import yaml
from pprint import pformat
from distutils.spawn import find_executable

from jinja2 import PackageLoader, Environment

from subprocess import Popen, PIPE

logger = logging.getLogger('fsm_generate_diffs')




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

    implementation = parsed_args['<implementation>']

    if parsed_args['--initial']:
        b = dict(states=[], transitions=[])
    elif parsed_args['javascript']:
        p = Popen(['./extract.js', implementation], stdout=PIPE)
        output = p.communicate()[0]
        if p.returncode == 0:
            b = yaml.load(output)
        else:
            return 1
    elif parsed_args['python']:
        p = Popen([find_executable('extract_fsm'), implementation], stdout=PIPE)
        output = p.communicate()[0]
        if p.returncode == 0:
            b = yaml.load(output)
        else:
            return 1

    with open(parsed_args['<design>']) as f:
        a = yaml.load(f.read())

    data = fsm_diff.fsm_diff(a, b)
    data = transform_fsm.transform_fsm(data)

    logger.debug(pformat(data))

    env = Environment(loader=PackageLoader("gevent_fsm", "templates"))

    if parsed_args['python']:
        template = env.get_template('fsm.pyt')
    elif parsed_args['javascript']:
        template = env.get_template('fsm.jst')

    if parsed_args['--initial']:
        with open(implementation, "w") as f:
            f.write(template.render(**data))
        Popen([find_executable('autopep8'), '-i', implementation]).communicate()
    elif parsed_args['--append']:
        with open(implementation, "a") as f:
            data['append'] = True
            f.write(template.render(**data))
    else:
        print (template.render(**data))



    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
