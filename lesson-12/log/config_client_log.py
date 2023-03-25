import logging
from logging.handlers import RotatingFileHandler
import os
from functools import wraps
import inspect


handler = RotatingFileHandler(filename=os.path.join('.', 'log', 'client.log'), maxBytes=2000, backupCount=10)
formater = logging.Formatter("%(asctime)s %(levelname)s %(pathname)s %(message)s")
handler.setFormatter(formater)
client_logger = logging.getLogger('client_log')
client_logger.addHandler(handler)
client_logger.setLevel(logging.INFO)

formater = logging.Formatter("%(asctime)s %(message)s")
handler.setFormatter(formater)

client_logger_decorator = logging.getLogger('client_log_decorator')
client_logger_decorator.addHandler(handler)
client_logger_decorator.setLevel(logging.INFO)


def log(function):
    def wrapper(*args, **kwargs):
        client_logger_decorator.info(f'Функция {function.__name__} вызвана из функции {inspect.stack()[1][3]}')
        result = function(*args, **kwargs)
        return result
    return wrapper