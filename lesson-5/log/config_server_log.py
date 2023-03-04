import logging
from logging.handlers import TimedRotatingFileHandler
import os


handler = TimedRotatingFileHandler(filename=os.path.join('.', 'log', 'server.log'), when="midnight", backupCount=10)
formater = logging.Formatter("%(asctime)s %(levelname)s %(pathname)s %(message)s")
handler.setFormatter(formater)

server_logger = logging.getLogger('server_log')
server_logger.addHandler(handler)
server_logger.setLevel(logging.INFO)