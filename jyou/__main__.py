#!/usr/bin/env python3

# JYOU
# Author: SlapeLachie
# Lockscreen manager

import argparse
import sys
import os.path
import logging
import shutil

from . import utils,log
from .settings import DATA_PATH, CONFIG_PATH, CACHE_PATH
from .generator import LockscreenGenerate

logger = log.setup_logger(__name__, logging.INFO, log.defaultLoggingHandler())

def get_args():
	""" Get the args parsed from the command line and does arg handling stuff """

	arg = argparse.ArgumentParser(description="Generate and switch lockscreen images")

	arg.add_argument('-v', action='store_true',
		help='Verbose Logging')

	arg.add_argument('-q', action='store_true',
		help='Allow only error logging')
		
	arg.add_argument("-g", action="store_true",
		help="generate themes")

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

	VERBOSE_MODE = True if args.v else False

	if args.q:
		pass

	if args.i:
		if args.g:
			LockscreenGenerate(args.i, VERBOSE_MODE).generate(args.b, args.d)
		else:
			LockscreenGenerate(args.i, VERBOSE_MODE).update()	
	
	if args.clear:
		clear = input("Are you sure you want to remove the cache relating to JYOU? [y/N] ").lower()
		if(clear == "y"):
			try:
				shutil.rmtree(CACHE_PATH)
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

if __name__ == "__main__":
	main()