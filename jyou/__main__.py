#!/usr/bin/env python3

# JYOU
# Author: SlapeLachie
# Lockscreen manager

import argparse
import sys
import os.path
import logging
import shutil

from jyou import utils,log,config_handler
from jyou.settings import DATA_PATH, CONFIG_PATH, CACHE_PATH
from jyou.generator import LockscreenGenerator

logger = log.setup_logger(__name__, logging.ERROR, log.defaultLoggingHandler())

def get_args():
	""" Get the args parsed from the command line and does arg handling stuff """

	arg = argparse.ArgumentParser(description="Generate and switch lockscreen images")

	arg.add_argument('-v', action='store_true',
		help='Verbose logging')

	arg.add_argument("-g", action="store_true",
		help="Generate themes")

	arg.add_argument("-i", metavar="\"path/to/dir\"",
		help="The input file or directory")

	arg.add_argument('-b', metavar="radius",
		help="Radius for the blur")
	
	arg.add_argument('-d', metavar="brightness",
		help="The brightness of the image (darker < 1.0 < lighter)")

	arg.add_argument('--override', action="store_true",
		help="Override exisiting lockscreen")

	arg.add_argument("--clear", action="store_true",
		help="Clear all data relating to JYOU")

	arg.add_argument("--progress", action="store_true",
		help="Display progress")

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

	verbose_logging = True if args.v else False
	log_level = getLogLevel(verbose_logging)
	logger.setLevel(log_level)

	if args.i:
		blur_strength = config_handler.compareFlagWithConfig(args.b, config_handler.parse_config()['blur'])
		brightness = config_handler.compareFlagWithConfig(args.d, config_handler.parse_config()['brightness'])
		progress = config_handler.compareFlagWithConfig(args.progress, config_handler.parse_config()['progress'])
		output_path = os.path.join(config_handler.parse_config()['out_directory'], 'lockscreen')

		generator = LockscreenGenerator(args.i)
		generator.setBlur(blur_strength)
		generator.setBrightness(brightness)
		generator.setVerboseLogging(verbose_logging)
		generator.setOverride(args.override)
		generator.setProgress(progress)
		generator.setOutputPath(output_path)

		if args.g:
			generator.generate()
		else:
			generator.update()
	
	elif args.clear:
		clear = input("Are you sure you want to remove the cache relating to JYOU? [y/N] ").lower()
		if(clear == "y"):
			try:
				shutil.rmtree(DATA_PATH)
			except:
				raise
			logger.info("Cleared JYOU cache folders")
		else:
			logger.warning("Canceled clearing cache folders...")

def main():
	# Create required directories
	try:
		os.makedirs(DATA_PATH, exist_ok=True)
		os.makedirs(CONFIG_PATH, exist_ok=True)
	except:
		raise

	parser = get_args()
	parse_args(parser)

def getLogLevel(verbose_logging):
	if verbose_logging:
		return logging.INFO
	else:
		return logging.WARNING

if __name__ == "__main__":
	main()