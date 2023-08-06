
"""
Blizzard API CLI - Credentials class.

Vaughn Kottler 01/07/19
"""

# built-in
import argparse
import json
import logging

class Credentials:
    """ Credentials retrieval from JSON-formatted files. """
    #pylint:disable=too-few-public-methods

    log = logging.getLogger(__name__)

    def __init__(self, credentials_file):
        """
        :param credentials_file: Path to a JSON file containing an
                                 object with 'id' and 'secret' fields
        :raises: argparse.ArgumentTypeError, for use with argparse
        """

        self.creds = None

        # verify file can be opened and decoded as JSON
        try:
            with open(credentials_file, "r") as creds_file:
                self.creds = json.load(creds_file)
        except (json.decoder.JSONDecodeError, FileNotFoundError) as exc:
            Credentials.log.error(exc)
            raise argparse.ArgumentTypeError(exc)

        # verify expected keys are present
        try:
            self.id = self.creds["id"]
            self.secret = self.creds["secret"]
        except KeyError as exc:
            Credentials.log.error("Missing key %s in credentials file.", exc)
            raise argparse.ArgumentTypeError(exc)
