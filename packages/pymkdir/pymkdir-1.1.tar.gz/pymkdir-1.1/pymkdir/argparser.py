"""
Module which holds all the functions required to parse command line
arguments.
"""
import argparse


def get_command_line_args():
    """
    Command line arguments parser. Returns the command-line arguments
    that were input by the user.

    "-d/--directory": str to be used as an os path (optional);
    "-e/--empty": boolean whichi indicates no __init__.py creation (optional);

    Returns:
        dict: dictionary with command-line arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("folder")  # folder name is a required arg
    parser.add_argument("-p", "--path", default="./")
    parser.add_argument("-e", "--empty", default=None, nargs="?", const=True)

    args = vars(parser.parse_args())

    return args
