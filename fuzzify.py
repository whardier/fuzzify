# -*- coding: utf-8 -*-

'''
fuzzify
======

rSync fuzzy file pool creation
'''

from __future__ import absolute_import, division, print_function, with_statement

__author__ = 'Shane R. Spencer'
__author_email__ = 'shane@bogomip.com'
__license__ = 'MIT'
__copyright__ = '2014 Shane R. Spencer'
__version__ = '0.0.1'
__url__ = 'https://github.com/whardier/fuzzify'
__description__ = 'rSync fuzzy file pool creation'

import os
import sys

import itertools

import argparse
import logging

import json

import hashlib

import subprocess

import path

class LoggingAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

        logger = logging.getLogger()
        logger.setLevel(getattr(logging, values.upper()))

###############################################################################
## Main

def main():

    ###########################################################################
    ## Parse Arguments

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--logging', action=LoggingAction, default='none', help='debug|info|warning|error|none')

    parser.add_argument('--dirty', action='store_true')

    parser.add_argument('--min-size', default=0)

    parser.add_argument('--pool', default='...fuzzify', help='Pool directory (must be on same partition as source data) and may be relative or absolute to the source directory')

    parser.add_argument('--hash', default=None, choices=('sha1', 'md5', 'sha224', 'sha256', 'sha512', 'sha384'), help='Also create a hash pool')

    parser.add_argument('source_directory')

    args = parser.parse_args()

    logging.debug(repr(args))

    ###########################################################################
    ## Set up initial paths

    source_directory = path.path(args.source_directory).expand().abspath()
    pool_directory = source_directory.joinpath(args.pool).expand().abspath()

    pool_directory.makedirs_p()

    pool_directory.joinpath('.keep').touch()

    logging.info('Source Directory: ' + source_directory)
    logging.info('Pool Directory: ' + pool_directory)

    ###########################################################################
    ## Walk the source path

    for child_directory in itertools.chain([source_directory], source_directory.walkdirs()):

        if pool_directory in child_directory:
            continue

        logging.info('Scanning Directory: ' + child_directory)

        for child_file in child_directory.files():

            logging.info('Scanning File: ' + child_file)

            file_size = child_file.getsize()

            if file_size < args.min_size:
                logging.info('Skipping File: ' + child_file)
                continue

            file_size_string = str(file_size)

            link_directory = pool_directory.joinpath(*file_size_string)

            ## Read the hash and extend the link_directory using the hash hexdigest

            if args.hash:
                hash = child_file.read_hexhash(args.hash)
                link_directory = link_directory.joinpath(hash)

            ## Extend the directory with a filename where the file size is the suffix and the sha512 sum (not configurable) 
            ## of the absolute path of the file is the prefix

            link_file = link_directory.joinpath(file_size_string + '.' + hashlib.sha512(str(child_file).encode('utf-8')).hexdigest()).abspath()

            link_file.parent.makedirs_p()

            if not link_file.exists():
                child_file.link(link_file)

            ## Log regardless of link for cleanup reasons

            link_directory.joinpath('log').write_text(
                    json.dumps(
                        {
                            'source': child_file,
                            'link': link_file,
                        },
                        sort_keys=True
                    ) + os.linesep,
                    append=True
                )

    ###########################################################################
    ## Cleanup

    if not args.dirty:
        for log_file in pool_directory.walkfiles('log'):
            stored_files = list((json.loads(x)['link'] for x in log_file.lines()))

            ## Delete all non matching including log files
            for pool_file in log_file.parent.files():
                if pool_file not in stored_files:
                    if pool_file.name != 'log':
                        logging.info('Removing Dirty File: ' + pool_file)
                    pool_file.unlink_p()
                    pool_file.parent.removedirs_p()

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
