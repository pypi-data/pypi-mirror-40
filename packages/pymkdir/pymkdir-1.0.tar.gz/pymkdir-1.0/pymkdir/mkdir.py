"""
Module with the mkdir function that checks for OS permissions and creates
the folder with its __init__.py file.
"""
from __future__ import print_function, unicode_literals

import os


def pymkdir(full_folder_path, command_line_args):
    """
    Creates a Python folder and its __init__.py at the full_folder_path.

    Args:
        full_folder_path (str): full folder path for the folder creation;
        command_line_args (dict): dict with the user command line arguments.
    """
    full_initfile_path = os.path.join(full_folder_path, "__init__.py")
    folder_unicode = "\U0001F4C2"

    # print(f" _ . * . {folder_unicode}  pymkdir {folder_unicode} . * . _")
    print(" _ . * . %s  pymkdir %s . * . _" % (folder_unicode, folder_unicode))

    # print(f"Creating the folder {full_folder_path}...")
    print("Creating the folder %s..." % full_folder_path)
    os.mkdir(full_folder_path)

    if not command_line_args.get("empty"):
        print("Creating the __init__.py file...")

        file = open(full_initfile_path, "w")
        file.close()

    print("Done!")
