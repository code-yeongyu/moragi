from moragi.configs import logger

from .cli import cli_app


def main():
    logger.setup_logger()
    cli_app()
