import logging
print('mock vim')
logger = logging.getLogger(__name__)


def eval(s):
    logger.debug(f'eval: {s}')
    if s.startswith('a:'):
        if s == 'a:000':
            return []
        else:
            return -1
    raise NotImplementedError()


def command(s):
    logger.debug(f'command: {s}')
