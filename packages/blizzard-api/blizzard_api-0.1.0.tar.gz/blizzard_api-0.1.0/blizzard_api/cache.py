
"""
Blizzard API CLI - Cache class.

Vaughn Kottler 01/07/19
"""

# built-in
import argparse
import logging
import os

class Cache:
    """ Disk-based cache implementation. """
    #pylint:disable=too-few-public-methods

    log = logging.getLogger(__name__)

    def __init__(self, cache_directory):
        """
        :param cache_directory: Path to an existing cache directory or a
                                location that one should be created
        :raises: argparse.ArgumentTypeError, for use with argparse
        """

        # ensure access to this directory (or viability of creation)
        if not os.path.isdir(cache_directory):
            try:
                os.makedirs(cache_directory)
            except OSError as exc:
                Cache.log.error(exc)
                raise argparse.ArgumentTypeError(exc)
        try:
            os.listdir(cache_directory)
        except OSError as exc:
            Cache.log.error(exc)
            raise argparse.ArgumentTypeError(exc)

        self.directory = cache_directory
