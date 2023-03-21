import logging

from rich.logging import RichHandler


def setup_logger():
    FORMAT = '%(message)s'
    logging.basicConfig(level=logging.NOTSET, format=FORMAT, datefmt='[%X]', handlers=[RichHandler()])
