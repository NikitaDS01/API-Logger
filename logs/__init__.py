import json
import logging.config
import os


def logger_configure():
    logger_config = os.path.join(os.path.abspath(os.path.curdir), "config", "logger_config.json")
    with open(logger_config, encoding="utf-8") as conf_file:
        config = json.load(conf_file)

    log_dir = os.path.join(os.path.abspath(os.path.curdir), "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logging.config.dictConfig(config)
