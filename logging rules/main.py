import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level='INFO')
# logger.add('debug.log', level='DEBUG')

logger.debug('debug')
logger.info('info')
