"""
Wrapper around the ``vim`` module.
Exports additional functions and falls back to a mock backend
when vim is not available.
"""

import logging
logger = logging.getLogger(__name__)

try:
    import vim as backend
except ImportError as e:
    logger.info(e)
    from . import mock_vim as backend


def get_arg(name):
    return eval(f'a:{name}')


def get_args(names):
    return [get_arg(n) for n in names]


def get_opts_args_list():
    return get_arg('000')


def eval(s):
    return backend.eval(s)


def command(s):
    return backend.command(s)
