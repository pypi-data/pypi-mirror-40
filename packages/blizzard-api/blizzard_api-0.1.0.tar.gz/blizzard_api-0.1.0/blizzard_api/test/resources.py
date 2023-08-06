
"""
Blizzard API CLI - Utilities for managing test resources.

Vaughn Kottler 01/07/19
"""

# built-in
import os

def get_item(name):
    """
    Retrieve a test resource by filename.

    :param name: String filename of the requested resource
    :returns: Absolute path to the requested resource
    """

    current_path = os.path.realpath(__file__)
    current_path = os.path.dirname(current_path)
    current_path = os.path.join(current_path, "data" + os.sep)
    return os.path.join(os.path.dirname(current_path), name)
