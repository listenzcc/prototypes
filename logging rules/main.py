import sys
import logging
from loguru import logger

logger.remove()

# Both info and above
logger.add(sys.stderr, level='INFO')

# Only info
logger.add(
    'info.pure.log', filter=lambda record: record["level"].no < logging.WARNING, level='INFO')

# Both info and above
logger.add(
    'info.log', level='INFO')

# Warning and above
logger.add('error.log', level='WARNING')

logger.debug('debug')
logger.info('info')

try:
    1/0
except Exception as err:
    logger.opt(exception=True).error(err)
