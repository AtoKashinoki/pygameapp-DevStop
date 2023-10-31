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
from pgapp._fromat import DescriptorBasis, FilePath
from pgapp._config import Config, create_config_file
from pgapp import _inheritance as inheritance
inh = inheritance

# print name and version
name = "pgapp"
version = "0.0.0"
print(f"{name} {version} (Python 3.10.7)")

# config directory path
path__config_directory = FilePath("./config")
path__display_config = FilePath(path__config_directory + "display.config")


def config_directory_initial_setup():
    """ create config directory """
    if not glob.glob(path__config_directory.path):
        os.mkdir(path__config_directory.path)
    if not glob.glob(path__display_config.path):
        create_config_file(path__display_config.path)
    return


if __name__ == name:
    """ process when import """
    config_directory_initial_setup()
    display_config = Config(path__display_config.path)
    pass
