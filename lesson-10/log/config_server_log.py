import logging
from logging.handlers import TimedRotatingFileHandler
import os
from functools import wraps
import inspect


handler = TimedRotatingFileHandler(filename=os.path.join('.', 'log', 'server.log'), when="midnight", backupCount=10)
formater = logging.Formatter("%(asctime)s %(levelname)s %(pathname)s %(message)s")
handler.setFormatter(formater)
server_logger = logging.getLogger('server_log')
server_logger.addHandler(handler)
server_logger.setLevel(logging.INFO)

formater = logging.Formatter("%(asctime)s %(message)s")
handler.setFormatter(formater)

server_logger_decorator = logging.getLogger('client_log_decorator')
server_logger_decorator.addHandler(handler)
server_logger_decorator.setLevel(logging.INFO)


def log(function):
    def wrapper(*args, **kwargs):
        server_logger_decorator.info(f'Функция {function.__name__} вызвана из функции {inspect.stack()[1][3]}')
        result = function(*args, **kwargs)
        return result
    return wrapper