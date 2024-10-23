# src/logger.py

"""
Logger module to set up logging configuration.
"""

import logging


def setup_logging(log_filename: str, verbose: bool):
    """
    Sets up logging configuration.
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        filename=log_filename,
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'
    )

    # Also output to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logging.getLogger().addHandler(console_handler)
