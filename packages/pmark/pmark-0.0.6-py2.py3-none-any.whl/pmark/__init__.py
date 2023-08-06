# -*- coding: utf-8 -*-
"""
| **@created on:** 20/05/16,
| **@author:** Prathyush SP,
| **@version:** v0.0.1
|
| **Description:**
| Singleton Class
|
| Sphinx Documentation Status:** Complete
|
..todo::
"""
import os
from pmark.logging_config_manager import setup_logging

BMARK_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))


class Singleton(type):
    """
    Singleton Class
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# todo: Prathyush SP: Move logging config to logging manager

setup_logging(default_path=os.path.join("/".join(__file__.split('/')[:-1]), 'config', 'module_logging.yaml'))

# todo: Prathyush SP - Debug code breakages due to changing start method
# import multiprocessing
# multiprocessing.context._force_start_method('spawn')

from pmark.store import MODULE_STORE
from pmark.config_manager import MODULE_CONFIG, MODULE_CONFIG_DATA
from pmark.metadata import metadata as md
from pmark.benchmark import pmonitor
from pmark.benchmark import ftimer
from pmark.benchmark import fmemory

__version__ = md.__version__

if __name__ == '__main__':
    print('module.__init__ success . . .')
