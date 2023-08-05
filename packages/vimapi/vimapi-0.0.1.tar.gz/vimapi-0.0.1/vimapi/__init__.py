# -*- coding: utf-8 -*-

import logging
"""Top-level package for vimapi."""

__author__ = """Julien Harbulot"""
__email__ = 'web@julienh.fr'
__version__ = '0.0.1'
name = "vimapi"

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
logging.getLogger(__name__).addHandler(NullHandler())
