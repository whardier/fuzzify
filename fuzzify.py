# -*- coding: utf-8 -*-

"""
fuzzify
======

rSync fuzzy file pool creation
"""

from __future__ import absolute_import, division, print_function, with_statement

__author__ = 'Shane R. Spencer'
__author_email__ = "shane@bogomip.com"
__license__ = 'MIT'
__copyright__ = '2014 Shane R. Spencer'
__version__ = '0.0.1'
__status__ = "Prototype"
__url__ = "https://github.com/whardier/fuzzify"
__description__ = "rSync fuzzy file pool creation"

import os
import sys

import argparse
import logging

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

    parser.add_argument('--hash', default=None, choices=('sha1', 'md5', 'sha224', 'sha256', 'sha512', 'sha384'), help='Also create a hash pool')

    parser.add_argument('directory')

    args = parser.parse_args()

    logging.debug(repr(args))

    ###########################################################################
    ## Set up initial paths

    source_directory = path.path(args.directory)
    destination_directory = source_directory.joinpath('...fuzzify')

    destination_directory.makedirs_p()

    ###########################################################################
    ## Walk the source path

    for source_file in source_directory.walkfiles():

        logging.info(source_file)

    """
    #This is actually more optimal to do before (to enable shorter names for rsync matching)
    if args.cleanup:
        destination_iter = destination_path.walkfiles()
        for file_path in destination_iter:
            if file_path.lstat().st_nlink == 1:
                logging.info('Removing: ' + file_path)
                file_path.remove_p()

    for batch, file_paths in enumerate(
            split_every(args.batch, source_iter)
        ):

        relative_file_paths = []

        for file_path in file_paths:
            #FIXME: Need to ignore slashy files.  There appears to be a standard with most hash tools where if a file has slashes the hash begins with one. 
            if '\\' in file_path:
                continue
            relative_file_paths.append(
                file_path.relpath(source_path)
            )

        logging.debug('Hashing: ' + repr(relative_file_paths))

        file_hash_process = subprocess.Popen(
            [args.hash] + relative_file_paths,
            cwd=source_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        file_hash_process.wait()

        #Use splitlines to avoid file name problems with whitespace stripping
        for line in file_hash_process.stdout.read().splitlines():
            if not line: continue

            hash, file_path = line.split('  ',1)
            file_path = path.path(file_path)

            file_path_hash_process = subprocess.Popen(
                [args.hash],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            file_path_hash_process.stdin.write(file_path)
            file_path_hash_process.stdin.close()

            file_path_hash_process.wait()

            file_path_hash = file_path_hash_process.stdout.readline().split('  ', 1)[0]

            #Create destination dir if not exists
            destination_file_path = destination_path.joinpath(hash[0:2]).joinpath(hash[2:4]).joinpath(hash[4:6]).joinpath(hash[6:])
            destination_file_path.makedirs_p()

            source_file_path = source_path.joinpath(file_path)

            source_file_inode = source_file_path.lstat().st_ino

            found_link = False

            #Make short file names to deal with rsync fuzzy params (Levenshtein Distance <= 25)
            for i in range(len(file_path_hash) + 1):

                destination_file_link_path = destination_file_path.joinpath(
                    file_path_hash[:i]
                )

                try:
                    stat = destination_file_link_path.lstat()
                except:
                    #high chances that this file doesn't exist
                    break
                finally:
                    if stat.st_ino == source_file_inode:
                        found_link = True
                        break

            if not found_link:
                #Destructive for now.  Seems faster than checking files
                logging.info('Linking: ' + file_path)
                destination_file_link_path.remove_p()
                source_file_path.link(destination_file_link_path)
            else:
                logging.info('Found Link: ' + file_path)
    """

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass


print(__name__)
