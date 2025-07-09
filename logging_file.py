#!/usr/bin/env python3


# region Module Docstring and Imports.
"""Creates the logging configuration for the Thermo Tracker app."""

import logging

from constants import Paths

# endregion.


# region Logging Configurations.


def logging_configuration() -> None:
    """Configures the logging settings for the application."""
    logging.basicConfig(
        filename=Paths.LOG_PATH,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def disable_logging() -> None:
    """Disables logging by setting the level to INFO."""
    logging.disable(logging.INFO)


# endregion.
