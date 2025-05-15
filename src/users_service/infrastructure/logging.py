"""
Logging Configuration Module

This module is responsible for configuring the logging behavior of the application.
It uses `loguru` as the logging library and dynamically sets the log settings 
based on the environment (debug or production mode).

Key functionalities:
- `set_log()`: Configures the logging system by removing existing handlers 
  and applying the appropriate log settings based on the `DEBUG` flag.

Usage:
    from log_set import set_log
    set_log()  # Call this at the start of your application to configure logging
"""

from loguru import logger
from src.users_service.config.settings import DEBUG, LOG_DEBUG_SETTINGS, LOG_PRODUCTION_SETTINGS


def set_log():
    """
    Sets up the logging configuration for the application.

    This function removes any existing default log handlers and then adds new 
    ones based on the current environment (debug or production mode). It selects 
    the appropriate log settings from the application's configuration.

    - If `DEBUG` is `True`, it applies debug-specific log settings.
    - Otherwise, it applies production log settings.

    Log settings are defined in `LOG_DEBUG_SETTINGS` and `LOG_PRODUCTION_SETTINGS` 
    and are dynamically loaded.

    Example:
        set_log()  # Call this function to initialize logging

    """
    # Remove the default log handler (index 0 refers to the default handler)
    logger.remove(0)

    # Determine log settings based on the environment
    LOG_SETTINGS = LOG_DEBUG_SETTINGS if DEBUG else LOG_PRODUCTION_SETTINGS

    # Apply the selected log settings
    for settings in LOG_SETTINGS:
        sink = settings.pop("sink")  # Extract sink from settings
        logger.add(sink=sink, **settings)
