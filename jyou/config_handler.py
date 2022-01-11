"""File for handling config files"""
import copy
import os
import json
from typing import Dict

import pickle
from . import settings

CONFIG_FILE_PATH = os.path.join(settings.CONFIG_PATH, "config.json")

DEFAULT_CONFIG = {
    "blur": 0,
    "brightness": 1,
    "out_directory": "$HOME/.local/share/jyou/",
    "progress": False,
    "debug": False,
}


def parse_config() -> Dict:
    """
    Parses and returns the config file, creating a new one if it does not exist

    Returns:
        (Dict): a dictionary containing the config file
    """
    config = copy.copy(DEFAULT_CONFIG)

    try:
        with open(CONFIG_FILE_PATH, encoding="UTF-8") as config_file:
            loaded_config = json.load(config_file)
            config.update(loaded_config)
    except IOError:
        save_config(config)

    return config


def save_config(config: Dict):
    """
    Saves the config to the config location

    Arguments:
        config (Dict): the config
    """
    config_path = os.path.dirname(CONFIG_FILE_PATH)
    if not os.path.isdir(config_path):
        os.mkdir(config_path)

    with open(CONFIG_FILE_PATH, "wb") as config_file:
        config_file.write(
            json.dumps(config, indent=4, separators=(",", ": ")).encode("utf-8")
        )


def load_config(config_file_path: str) -> Dict:
    """
    Load the config from the specified location

    Arguments:
        config_file_path (str): the path to the config file

    Returns:
        (Dict): the config
    """
    with open(config_file_path, "rb") as config_file:
        return pickle.load(config_file, encoding="utf-8")


def compare_flag_with_config(flag: bool, config_option: bool) -> bool:
    """
    Compares the value of the given flag with the config option, with the flag
    taking more presedence over the conifg

    Arguments:
        flag (bool): the flag
        config_option (bool): the option in the config

    Returns:
        (bool): the result
    """
    if flag:
        return flag

    return config_option
