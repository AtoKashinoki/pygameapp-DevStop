"""
    pgapp
This module can be used to create pygame applications.
"""

# import support modules
import os
import glob
import pygame
import numpy

# import pgapp modules
from pgapp.config import *

# print name and version
name = "pgapp"
version = "0.0.0"
print(f"{name} {version} (Python 3.10.7)")

# config directory path
path__config_directory = "./config"
path__display_config = f"{path__config_directory}/display.config"


def config_directory_initial_setup():
    """ create config directory """
    if not glob.glob(path__config_directory):
        os.mkdir(path__config_directory)
    if not glob.glob(path__display_config):
        create_config_file(path__display_config)
    return


if __name__ == name:
    config_directory_initial_setup()
    display_config = Config(path__display_config)
    pass
