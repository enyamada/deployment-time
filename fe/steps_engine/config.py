
"""
  Module that contains functions related to reading and handling
  configuration files. The yaml module is leveraged here.

"""

import os
import yaml


class Config(object):


    @staticmethod
    def _read_db_env_config(config):
        """
        Check if any db configuration parameter was specified using a
        environment variable. If so, it must override the value provided
        by the dictionary passed (that must be updated for later use).

        Args:
            config: dictionary containing the db default parameters
        """
        config["host"] = os.environ.get("DB_HOST", \
            os.environ.get("MYSQL_PORT_3306_TCP_ADDR", config["host"]))


    @staticmethod
    def _read_log_env_config(config):
        """
        Check if any log configuration parameter was specified using a
        environment variable. If so, it must override the value provided
        by the dictionary passed (that must be updated for later use).

        Args:
            config: dictionary containing the log default parameters
        """
        config["level"] = os.environ.get("LOG_LEVEL", config["level"])


    def __init__(self, config_file):
        """
        Reads the parameters described in the passed config file (that must be
        a YAML file). Then checks if any of them were overriden by a environment
        variable and  finally returns a dictionary containing the
        setting in effect.

        Args:
            config_file: YAML file to be used as a configuration file.

        """

        with open(config_file, "r") as f:
            self.options = yaml.load(f)

        Config._read_db_env_config(self.options["db"])
        Config._read_log_env_config(self.options["log"])

