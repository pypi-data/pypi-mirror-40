"""Utility module for logging."""

import logging
import traceback


def _get_null_logger(name='null_logger'):
    null_logger = logging.getLogger(name)
    null_logger.addHandler(logging.NullHandler())
    null_logger.propagate = False
    return null_logger


NULL_LOGGER = _get_null_logger()


def log_traceback(exception, logger):
    """
    Log exception traces.

    :param exception: The exception to log.
    :param logger: The logger to use.
    """
    if logger is None:
        logger = NULL_LOGGER

    logger.error(exception)
    logger.error(traceback.format_exc())
