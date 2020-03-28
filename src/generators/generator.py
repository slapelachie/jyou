import os
import subprocess
import shutil
import re
import random
import sys
import logging
import tqdm

from utils.settings import CACHE_PATH, DATA_PATH, DEBUG_MODE
from utils import utils, log

display_re = r"([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)" # Regex to find the monitor resolutions
lockscreen_dir = os.path.join(CACHE_PATH, 'lockscreen')

try:
	os.makedirs(lockscreen_dir, exist_ok=True)
except: raise

logger = log.setup_logger(__name__+'default', logging.INFO, log.defaultLoggingHandler())
tqdm_logger = log.setup_logger(__name__+'.tqdm', logging.INFO, log.TqdmLoggingHandler())

class LockscreenGenerate:
	"""
	Main class for anything to do with lockscreen.

	Arguments:
		image (str) -- location to the image ('/home/bob/pic.png')
	"""

	def __init__(self, image, verbose=False):
		"""
		Default function for the LockscreenGenerate class

		Arguments:
			image (str) -- location to the image ('/home/bob/pic.png')
		"""
		if DEBUG_MODE:
			logger.setLevel(logging.DEBUG)
			tqdm_logger.setLevel(logging.DEBUG)
		elif verbose:
			logger.setLevel(15)
			tqdm_logger.setLevel(15)

		if os.path.isfile(image):
			# If the path is a file, get the image and set itself to that
			self.image = [utils.get_image(image)]
		elif os.path.isdir(image):
			# If the path is a directory, get all images in it and get its absolute path
			self.image = [utils.get_image(os.path.join(image, img)) for img in utils.get_dir_imgs(image)]
		else:
			logger.critical("File does not exist!")
			sys.exit(1)

		# Get the output of xrandr and hash it
		self.screen_md5 = utils.md5(subprocess.check_output(["xrandr"]))[:20]
		

	def generate(self, override=False):
		"""Generate the lockscreen image"""
		# Apply this function to every image in the passed list
		non_gen_imgs = []
		for i in range(len(self.image)):
			image = self.image[i]	

			# Get the images md5 hash
			img_md5 = utils.md5_file(image)[:20]
			# Set the path for the final image
			img_path = os.path.join(lockscreen_dir, img_md5 + "_" + self.screen_md5 + ".png")

			if not os.path.isfile(img_path) or override:
				non_gen_imgs.append([image, img_path])				

		if len(non_gen_imgs) > 0:
			logger.info("Generating lockscreens...")
			for i in tqdm.tqdm(range(len(non_gen_imgs))):
				image = non_gen_imgs[i][0]
				img_path = non_gen_imgs[i][1]

				tmp_imgs = []
				params = ""
				output_img_height=0
				output_img_width=0

				# Execute and get the output from xrandr
				cmd = ['xrandr']
				p = subprocess.check_output(cmd)

				# Get all resolutions
				resolutions = re.findall(display_re,str(p))

				# Repeat for every screen the user has
				for resolution in resolutions:
					width, height, screen_x, screen_y = map(int, resolution)
					# Set a name for the temp image being created for the current resolution
					tmp_img = os.path.join(lockscreen_dir, "tmp_"+ str(width)+"x"+str(height)+"_"+img_md5)
					# Add to the 'to be deleted later' list
					tmp_imgs.append(tmp_img)

					# Check if the temp file already exists
					if not os.path.isfile(tmp_img):
						# Change the size of the image passed from the class
						subprocess.run(["convert", image, '-resize', str(width) + "X" + str(height)+"^", '-gravity', 'Center', '-crop', str(width) + "X" + str(height) + "+0+0", '+repage', tmp_img])
					
					if output_img_width < width+screen_x:
						output_img_width = width+screen_x
					
					if output_img_height < height+screen_y:
						output_img_height = height+screen_y

					# Params for this image when converted later on
					params = params + " " + tmp_img + " -geometry +" + str(screen_x) + "+" + str(screen_y) + " -composite -fill black -colorize 50% -blur 0x4"
				
				tqdm_logger.log(15, "["+ str(i+1) + "/" + str(len(self.image)) + "] Generating lockscreen for: " + image + "...")

				# Create the background for the final image
				subprocess.run(["convert", "-size", str(output_img_width)+"x"+str(output_img_height), "xc:rgb(1,0,0)", img_path])

				# Flatten the arguments to be a one level list item
				args = [["convert", img_path], params.split(" "), [img_path]]
				args = [y for x in args for y in x]
				while "" in args:
					args.remove("")

				# Create the final image
				subprocess.run(args)

				# Remove the temp files
				for file in tmp_imgs:
					os.remove(file)
		else:
			logger.info("No lockscreens to generate.")

	def update(self):
		""" Update the wallpaper based on the parsed image in the parent class """

		# Get the first element of the shuffled list
		images = self.image
		random.shuffle(images)
		image = images[0]
		self.image = [image]

		# Get the md5 hash of the image
		img_md5 = utils.md5_file(image)[:20]
		# Set the image path location
		img_path = os.path.join(lockscreen_dir, img_md5 + "_" + self.screen_md5 + ".png")

		# Copy the image if it exists
		if os.path.isfile(img_path):
			symlink_path = os.path.join(CACHE_PATH, 'current_lockscreen.png')

			if os.path.isfile(symlink_path):
				os.remove(symlink_path)

			os.symlink(img_path, symlink_path)
		else:
			self.generate()
			self.update()
