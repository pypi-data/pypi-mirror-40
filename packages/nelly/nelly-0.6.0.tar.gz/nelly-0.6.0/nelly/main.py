#!/usr/bin/env python

#
# (c) 2008-2016 Matthew Oertle
#

import sys
import os
import argparse
import time
import logging

import nelly


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('grammar',
        nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help='Input file')

    argparser.add_argument('--count', '-c',
        type=int, default=-1,
        help='Number of times to run')

    argparser.add_argument('--include', '-i',
        action='append',
        help='Include path')

    argparser.add_argument('--vars', '-v',
        action='append',
        help='Variables to set')

    argparser.add_argument('--debug', '-D',
        action='store_true',
        help='Enable debug logging')

    args = argparser.parse_args()

    logging.basicConfig(
        format  = '%(asctime)s %(levelname)-8s %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        level   = logging.DEBUG if args.debug else logging.INFO
        )

    includes = args.include or []

    variables = {'$count' : 0}
    if args.vars:
        for var in args.vars:
            name,value = var.split('=', 1)
            name = '$'+name
            variables[name] = value

    if args.grammar == sys.stdin:
        logging.info('Reading from stdin')
    else:
        path = os.path.abspath(args.grammar.name)
        path = os.path.dirname(path)
        sys.path.insert(0, path)

    try:
        grammar = args.grammar.read()
    except KeyboardInterrupt:
        return -1;

    logging.debug('Parsing grammar')
    parser = nelly.Parser(includes)
    parser.Parse(grammar)

    logging.debug('Serializing program')
    package = parser.program.Save()

    logging.debug('Loading program')
    program = nelly.Program.Load(package)

    logging.debug('Executing program')
    count = 0
    t1 = time.time()
    try:
        while args.count == -1 or count < args.count:
            sandbox = nelly.Sandbox(variables)
            try:
                sandbox.Execute(program)
            except nelly.error as e:
                logging.error('%s', e)
                break
            count += 1
            variables['$count'] = count
    except KeyboardInterrupt:
        pass
    t2 = time.time()

    logging.info('Ran %d iterations in %.2f seconds (%.2f tps)', count, t2 - t1, count / (t2 - t1))

    return 0


def entry():
    try:
        sys.exit(main())
    except nelly.error as e:
        logging.error('%s', e)
        sys.exit(-1)
