import sys
import os
import logging
from common.constants import LOGGING_LEVEL
sys.path.append('../')

client_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client.log')
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(client_formatter)
steam.setLevel(logging.INFO)
log_file = logging.FileHandler(path, encoding='utf8')
log_file.setFormatter(client_formatter)

logger = logging.getLogger('client_src')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    logger.critical('Test critical event')
    logger.error('Test error event')
    logger.debug('Test debug event')
    logger.info('Test info event')