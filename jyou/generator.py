import os
import subprocess
import shutil
import re
import random
import sys
import logging
import tqdm

from .settings import CACHE_PATH, DATA_PATH, DEBUG_MODE
from . import utils, log

from PIL import Image, ImageFilter

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
		

	def generate(self, blur=str(8), brightness=str(0.6), override=False):
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

		# Execute and get the output from xrandr
		cmd = ['xrandr']
		p = subprocess.check_output(cmd)

		# Get all resolutions
		resolutions = re.findall(display_re,str(p))

		if len(non_gen_imgs) > 0:
			logger.info("Generating lockscreens...")
			for i in tqdm.tqdm(range(len(non_gen_imgs))):
				image = non_gen_imgs[i][0]
				img_path = non_gen_imgs[i][1]

				img = Image.open(image).convert("RGB") 
				img_width, img_height = img.size

				screens = []
				screens_offset = []
				screens_size = []

				output_img_height=0
				output_img_width=0	

				tqdm_logger.log(15, "["+ str(i+1) + "/" + str(len(self.image)) + "] Generating lockscreen for: " + image + "...")
				# Repeat for every screen the user has
				for resolution in resolutions:
					width, height, screen_x, screen_y = map(int, resolution)
	
					if output_img_width < width+screen_x:
						output_img_width = width+screen_x
					
					if output_img_height < height+screen_y:
						output_img_height = height+screen_y

					screens_size.append((width, height))
					screens_offset.append((screen_x, screen_y))

					ratio = min(img_width/width, img_height/height)
					rwidth = int(img_width/ratio)
					rheight = int(img_height/ratio)

					crop_box = (
						(rwidth-width)/2,
						(rheight-height)/2,
						(rwidth+width)/2,
						(rheight+height)/2
					)

					img = img.resize((rwidth, rheight), Image.LANCZOS)
					img = img.crop(crop_box)

					if blur:
						if blur.isdigit():
							if not int(blur) == 0:
								img = img.filter(ImageFilter.GaussianBlur(int(blur)))
						else:
							tqdm_logger.warning("Parsed blur is not an integer, applying no blur...")
	
					screens.append(img)
	
				# Create the background image
				background = Image.new('RGB', (output_img_width, output_img_height), (0, 0, 0))

				# Add the images in their locations onto the new image
				for i in range(len(screens)):
					background.paste(screens[i], screens_offset[i])
							
				if brightness:
					try:
						if not float(brightness) == 1.0:
							background = background.point(lambda p: p * float(brightness))
					except:
						tqdm_logger.warning("Parsed brightness is not an integer, not changing brightness...")


				# Save the image
				background.save(img_path)
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

			# Run postscripts
			utils.run_post_scripts(image)
		else:
			self.generate()
			self.update()
