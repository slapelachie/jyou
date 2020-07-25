import os
import subprocess
import shutil
import re
import random
import sys
import logging
import tqdm
from PIL import Image, ImageFilter

from .settings import CACHE_PATH, DATA_PATH, DEBUG_MODE
from . import utils, log

logger = log.setup_logger(__name__+'default', logging.WARN, log.defaultLoggingHandler())
tqdm_logger = log.setup_logger(__name__+'.tqdm', logging.WARN, log.TqdmLoggingHandler())

class LockscreenGenerator:
	"""
	Main class for anything to do with lockscreen.

	Arguments:
		image (str) -- location to the image ('/home/bob/pic.png')
	"""

	def __init__(self, image):
		self.progressbar = False
		self.verbose_logging = False
		self.image = None
		self.override = False
		self.blur_stength = 0
		self.brightness = 1
		self.screen_md5 = utils.md5(subprocess.check_output(["xrandr"]))[:20]
		self.lockscreen_dir = os.path.join(DATA_PATH, 'lockscreen')

		if DEBUG_MODE:
			logger.setLevel(logging.DEBUG)
			tqdm_logger.setLevel(logging.DEBUG)
		elif self.verbose_logging:
			logger.setLevel(logging.INFO)
			tqdm_logger.setLevel(logging.INFO)

		try:
			os.makedirs(self.lockscreen_dir, exist_ok=True)
		except: raise

		self.image = getImageList(image)
		if not self.image:
			logger.critical("File does not exist!")
			sys.exit(1)

	def setVerboseLogging(self, state):
		self.verbose_logging = state

	def setOutputPath(self, path):
		self.lockscreen_dir = os.path.expanduser(path)

	def setProgress(self, state):
		self.progressbar = state

	def setOverride(self, state):
		self.override = state

	def setBlur(self, blur_stength):
		self.blur_stength = blur_stength

	def setBrightness(self, brightness):
		self.brightness = brightness

	def generate(self):
		"""Generate the lockscreen image"""
		# Apply this function to every image in the passed list
		non_generated_images = []
		for i in range(len(self.image)):
			image_path = self.image[i]	
			out_path = getOutPathFromMD5(image_path, self.screen_md5, self.lockscreen_dir)

			if not os.path.isfile(out_path) or self.override:
				non_generated_images.append({
					'image_path': image_path,
					'out_path': out_path
				})				

		resolutions = getResolutions()

		if len(non_generated_images) > 0:
			for i in tqdm.tqdm(range(len(non_generated_images)), bar_format=log.bar_format, disable=not self.progressbar):
				# Save the image
				out_path = non_generated_images[i]['out_path']
				lockscreen_image = generateLockscreenImage(non_generated_images[i]['image_path'], resolutions, self.blur_stength, self.brightness)
				lockscreen_image.save(out_path)
		else:
			logger.info("No lockscreens to generate.")

	def update(self):
		""" Update the wallpaper based on the parsed image in the parent class """
		self.image = getRandomImage(self.image)

		image_md5 = utils.md5_file(self.image)[:20]
		image_path = os.path.join(self.lockscreen_dir, image_md5 + "_" + self.screen_md5 + ".png")

		# Copy the image if it exists
		if os.path.isfile(image_path):
			symlink_path = os.path.join(DATA_PATH, 'current_lockscreen.png')
			symlinkImage(image_path, symlink_path)

			# Run postscripts
			utils.run_post_scripts()
		else:
			self.generate()
			self.update()

def getResolutions():
	display_re = r"([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)" # Regex to find the monitor resolutions
	cmd = ['xrandr']
	p = subprocess.check_output(cmd)
	return re.findall(display_re,str(p))

def getOutPathFromMD5(image_path, screen_md5, out_dir):
	image_md5 = utils.md5_file(image_path)[:20]
	return os.path.join(out_dir, image_md5 + "_" + screen_md5 + ".png")

def generateLockscreenImage(image_path, resolutions, blur, brightness):
	screens = []
	screens_offset = []
	output_image_width, output_image_height = getOutputResolution(resolutions)
	image = Image.open(image_path).convert("RGB") 

	# Repeat for every screen the user has
	for resolution in resolutions:
		resolution_image = cropImageToResolution(image, resolution)
		if blur:
			resolution_image = blurImage(resolution_image, blur)
		screens.append(resolution_image)
		screens_offset.append(getResolutionOffset(resolution))

	output_image = Image.new('RGB', (output_image_width, output_image_height), (0, 0, 0))

	# Add the images in their locations onto the new image
	for i in range(len(screens)):
		output_image.paste(screens[i], screens_offset[i])
				
	if brightness:
		try:
			if not float(brightness) == 1.0:
				output_image = output_image.point(lambda p: p * float(brightness))
		except:
			tqdm_logger.warning("Parsed brightness is not an integer, not changing brightness...")

	return output_image

def getResolutionDimensions(resolution):
	width, height, screen_x, screen_y = map(int, resolution)
	return (width, height)

def getResolutionOffset(resolution):
	width, height, screen_x, screen_y = map(int, resolution)
	return (screen_x, screen_y)

def getOutputResolution(resolutions):
	output_width, output_height = (0,0)
	for resolution in resolutions:
		resolution_width, resolution_height = getResolutionDimensions(resolution)
		resolution_x, resolution_y = getResolutionOffset(resolution)

		if output_width < resolution_width+resolution_x:
			output_width = resolution_width+resolution_x
	
		if output_height < resolution_height+resolution_y:
			output_height = resolution_height+resolution_y

	return (output_width, output_height)

def cropImageToResolution(image, resolution):
	image_width, image_height = image.size
	width, height = getResolutionDimensions(resolution)

	ratio = min(image_width/width, image_height/height)
	ratio_dimensions = (int(image_width/ratio), int(image_height/ratio))
	resized_image = image.resize(ratio_dimensions, Image.LANCZOS)

	crop_box = (
		(ratio_dimensions[0]-width)/2,
		(ratio_dimensions[1]-height)/2,
		(ratio_dimensions[0]+width)/2,
		(ratio_dimensions[1]+height)/2
	)

	cropped_image = resized_image.crop(crop_box)

	return cropped_image

def blurImage(image, blur):
	if not int(blur) == 0:
		image = image.filter(ImageFilter.GaussianBlur(int(blur)))

	return image

def getImageList(image_path):
	if os.path.isfile(image_path):
		return [utils.get_image(image_path)]
	elif os.path.isdir(image_path):
		return [utils.get_image(os.path.join(image_path, img)) for img in utils.get_dir_imgs(image_path)]
	else:
		return None

def getRandomImage(images):
	random.shuffle(images)
	return images[0]

def symlinkImage(image_path, symlink_path):
	if os.path.isfile(symlink_path):
		os.remove(symlink_path)

	os.symlink(image_path, symlink_path)