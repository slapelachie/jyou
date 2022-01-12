#!/usr/bin/env python3
"""
JYOU
Author: slapeLachie <lslape@slapelachie.xyz>

Simple lockscreen manager for tiling window managers. Generates a lockscreen for
multiscreened i3lock.
"""

import argparse
import sys
import os.path
import logging
import shutil

from jyou.__init__ import __version__, __author__, __email__
from jyou import log, config_handler
from jyou.settings import DATA_PATH, CONFIG_PATH
from jyou.generator import LockscreenGenerator

logger = log.setup_logger(__name__, logging.ERROR, log.DefaultLoggingHandler())


def get_args():
    """Get the args parsed from the command line and does arg handling stuff"""

    arg = argparse.ArgumentParser(description="Generate and switch lockscreen images")

    arg.add_argument(
        "-v", "--version", action="store_true", help="Display current version"
    )
    arg.add_argument("-g", "--generate", action="store_true", help="Generate themes")
    arg.add_argument(
        "-i", "--input", metavar='"path/to/dir"', help="The input file or directory"
    )
    arg.add_argument("-r", "--radius", metavar="radius", help="Radius for the blur")
    arg.add_argument("--verbose", action="store_true", help="Verbose logging")
    arg.add_argument(
        "-b",
        "--brightness",
        metavar="brightness",
        help="The brightness of the image (darker < 1.0 < lighter)",
    )
    arg.add_argument(
        "--override", action="store_true", help="Override exisiting lockscreen file"
    )
    arg.add_argument(
        "--clear", action="store_true", help="Clear all data relating to JYOU"
    )
    arg.add_argument("--progress", action="store_true", help="Display progress")

    return arg


def parse_args(parser):
    """
    Parses the arguments onto different actions

    Arguments:
            parser (idk) -- the argument parser
    """

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.version:
        print(f"JYOU {__version__} by {__author__} <{__email__}>")
        sys.exit(0)

    verbose_logging = bool(args.verbose)
    log_level = get_log_level(verbose_logging)
    logger.setLevel(log_level)

    if args.input:
        blur_strength = config_handler.compare_flag_with_config(
            args.radius, config_handler.parse_config()["blur"]
        )
        brightness = config_handler.compare_flag_with_config(
            args.brightness, config_handler.parse_config()["brightness"]
        )
        progress = config_handler.compare_flag_with_config(
            args.progress, config_handler.parse_config()["progress"]
        )
        output_path = config_handler.parse_config()["out_directory"]

        generator = LockscreenGenerator(
            args.input,
            progress_bar=progress,
            verbose_logging=verbose_logging,
            override=args.override,
            blur_strength=blur_strength,
            brightness=brightness,
            output_path=output_path,
        )

        if args.generate:
            generator.generate()
        else:
            generator.update()

    elif args.clear:
        clear = input(
            "Are you sure you want to remove the cache relating to JYOU? [y/N] "
        ).lower()
        if clear == "y":
            shutil.rmtree(DATA_PATH)
            logger.info("Cleared JYOU cache folders")
        else:
            logger.warning("Canceled clearing cache folders...")


def main():
    # Create required directories
    os.makedirs(DATA_PATH, exist_ok=True)
    os.makedirs(CONFIG_PATH, exist_ok=True)

    parser = get_args()
    parse_args(parser)


def get_log_level(verbose_logging):
    if verbose_logging:
        return logging.INFO

    return logging.WARNING


if __name__ == "__main__":
    main()
