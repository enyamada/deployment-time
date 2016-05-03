"""
This module contains functions related to logging customization
"""


import logging





def setup_logging(config):
    """
    COnfigures the logging module with the specified configutation.

    Args:
        config: dict with the parameters. The only one supported for now
           is level.
    """

    logger = logging.getLogger("")

    if config["level"] == "debug":
        level = logging.DEBUG
    elif config["level"] == "info":
        level = logging.INFO
    elif config["level"] == "warning":
        level = logging.WARNING
    elif config["level"] == "error":
        level = logging.ERROR
    elif config["level"] == "critical":
        level = logging.CRITICAL
    else:
        level = logging.WARNING

    logger.setLevel(level)
    handler = logging.handlers.RotatingFileHandler(
        config["file"], maxBytes=config["max-bytes"],
        backupCount=config["backup-count"])
    formatter = logging.Formatter("%(asctime)s - %(name)s - " \
        "%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

