"""The main generation file containing tools to generate the needed images"""
import os
import subprocess
import re
import random
import sys
import logging
from typing import List, Tuple

import tqdm
from PIL import Image, ImageFilter, ImageEnhance

from .settings import DATA_PATH, DEBUG_MODE
from . import utils, log

logger = log.setup_logger(
    __name__ + "default", logging.WARN, log.DefaultLoggingHandler()
)
tqdm_logger = log.setup_logger(
    __name__ + ".tqdm", logging.WARN, log.TqdmLoggingHandler()
)


# pylint: disable=too-many-instance-attributes
class LockscreenGenerator:
    """Main class for anything to do with lockscreen"""

    def __init__(self, image_path, **kwargs):
        """
        The initialisation method

        Arguments:
            image_path (str): location to the image ('/home/bob/pic.png')
        """
        self.progress_bar = kwargs.get("progress_bar", False)
        self.verbose_logging = kwargs.get("verbose_logging", False)
        self.override = kwargs.get("override", False)
        self.blur_strength = kwargs.get("blur_strength", 0)
        self.brightness = kwargs.get("brightness", 1)
        self.out_dir = kwargs.get("output_path", DATA_PATH)

        self.resolutions = get_resolution_image()
        self.screen_md5 = utils.md5(
            ",".join(str(i) for j in self.resolutions for i in j)
        )[:20]

        if DEBUG_MODE:
            logger.setLevel(logging.DEBUG)
            tqdm_logger.setLevel(logging.DEBUG)
        elif self.verbose_logging:
            logger.setLevel(logging.INFO)
            tqdm_logger.setLevel(logging.INFO)

        os.makedirs(self.out_dir, exist_ok=True)

        self.image_paths = get_image_path_list(image_path)
        if not self.image_paths:
            logger.critical("File does not exist!")
            sys.exit(1)

    def generate(self):
        """Generate the lockscreen image"""
        # Apply this function to every image in the passed list
        non_generated_images = []
        lockscreen_dir = os.path.join(self.out_dir, "lockscreen")
        os.makedirs(lockscreen_dir, exist_ok=True)

        for image_path in self.image_paths:
            out_path = get_out_path_from_md5(
                image_path, self.screen_md5, lockscreen_dir
            )

            if not os.path.isfile(out_path) or self.override:
                non_generated_images.append(
                    {"image_path": image_path, "out_path": out_path}
                )

        if len(non_generated_images) > 0:
            for i in tqdm.tqdm(
                range(len(non_generated_images)),
                bar_format=log.BAR_FORMAT,
                disable=not self.progress_bar,
            ):
                # Save the image
                out_path = non_generated_images[i]["out_path"]
                lockscreen_image = generate_lockscreen_image(
                    non_generated_images[i]["image_path"],
                    self.resolutions,
                    self.blur_strength,
                    self.brightness,
                )
                lockscreen_image.save(out_path)
        else:
            logger.info("No lockscreens to generate.")

    def update(self):
        """Update the wallpaper based on the parsed image in the parent class"""
        lockscreen_dir = os.path.join(self.out_dir, "lockscreen")
        image_path = get_random_image_path(self.image_paths)
        self.image_paths = [image_path]

        image_out_path = get_out_path_from_md5(
            image_path, self.screen_md5, lockscreen_dir
        )
        # Copy the image if it exists
        if os.path.isfile(image_out_path):
            symlink_path = os.path.join(self.out_dir, "current_lockscreen.png")
            symlink_image(image_out_path, symlink_path)

            # Run postscripts
            utils.run_hooks()
        else:
            self.generate()
            self.update()


def get_resolution_image() -> List[Tuple[int]]:
    """Gets the screen resolution"""
    display_re = r"([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)"  # Regex to find the monitor resolutions

    command_output = subprocess.check_output(["xrandr"])
    resolution_list = [
        [int(j) for j in i] for i in re.findall(display_re, str(command_output))
    ]

    return [tuple(i) for i in resolution_list]


def get_out_path_from_md5(image_path: str, screen_md5: str, out_directory: str) -> str:
    """
    Gets the out path path from the image and screen md5

    Arguments:
        image_path (str):       the path to the image
        screen_md5 (str):       the md5 of the screen
        out_directory (str):    the directory to append to the start of the path

    Returns:
        (str): the generated path
    """
    image_md5 = utils.md5_file(image_path)[:20]
    return os.path.join(out_directory, f"{image_md5}_{screen_md5}.png")


def generate_lockscreen_image(
    image_path: str, resolutions: List[Tuple[int]], blur: int, brightness: float
) -> Image:
    """
    Generates the image for the lockscreen

    Arguments:
        image_path (str): the path to the image
        resolutions (List[tuple]): the resolutions of the screens to generate for
        blur (int): the strength of the blur to be applied
        brightness (float): how bright the image should be

    Returns:
        (PIL.Image): the raw generated image
    """
    screens = []

    image = Image.open(image_path).convert("RGB")
    output_image_width, output_image_height = get_accumulative_dimensions(resolutions)

    # Repeat for every screen the user has
    for resolution in resolutions:
        dimensions = get_resolution_dimensions(resolution)
        resolution_image = crop_image_to_dimensions(image, dimensions)
        if blur:
            resolution_image = blur_image(resolution_image, blur)
        screens.append([resolution_image, get_resolution_offset(resolution)])

    output_image = Image.new(
        "RGB", (output_image_width, output_image_height), (0, 0, 0)
    )

    # Add the images in their locations onto the new image
    for screen in screens:
        output_image.paste(*screen)

    if brightness:
        enhancer = ImageEnhance.Brightness(output_image)
        output_image = enhancer.enhance(brightness)

    return output_image


def get_resolution_dimensions(resolution: Tuple[int]) -> Tuple[int]:
    """
    Gets the width and height from the specified resolution in the form of
    [width, height, offset_x, offset_y]

    Arguments:
        resolution (Tuple[int]): the resolution

    Returns:
        (Tuple[int]): the width and height
    """
    width, height, _, _ = map(int, resolution)
    return (width, height)


def get_resolution_offset(resolution: Tuple[int]) -> Tuple[int]:
    """
    Gets the x offset and y offset from the specified resolution in the form of
    [width, height, offset_x, offset_y]

    Arguments:
        resolution (Tuple[int]): the resolution

    Returns:
        (Tuple[int]): the x offset and the y offset
    """
    _, _, screen_x, screen_y = map(int, resolution)
    return (screen_x, screen_y)


def get_accumulative_dimensions(resolutions: List[Tuple[int]]) -> Tuple[int]:
    """
    Gets the accumlative dimensions of the given resolutions

    Arguments:
        resolutions (List[Tuple[int]]): the list of resolutions

    Returns:
        (Tuple[int]): the width and height of the accumlative dimensions
    """
    output_width, output_height = (0, 0)
    for resolution in resolutions:
        resolution_width, resolution_height = get_resolution_dimensions(resolution)
        resolution_x, resolution_y = get_resolution_offset(resolution)

        if output_width < resolution_width + resolution_x:
            output_width = resolution_width + resolution_x

        if output_height < resolution_height + resolution_y:
            output_height = resolution_height + resolution_y

    return (output_width, output_height)


def crop_image_to_dimensions(image: Image, dimensions: Tuple[int]) -> Image:
    """
    Crops the image to the specified dimensions

    Arguments:
        image (PIL.Image): the image to be cropped
        dimensions (Tuple[int]): the width and height to be cropped to

    Returns:
        (PIL.Image): the cropped image
    """
    image_width, image_height = image.size
    width, height = dimensions

    ratio = min(image_width / width, image_height / height)
    ratio_dimensions = (int(image_width / ratio), int(image_height / ratio))
    resized_image = image.resize(ratio_dimensions, Image.LANCZOS)

    crop_box = (
        (ratio_dimensions[0] - width) / 2,
        (ratio_dimensions[1] - height) / 2,
        (ratio_dimensions[0] + width) / 2,
        (ratio_dimensions[1] + height) / 2,
    )

    cropped_image = resized_image.crop(crop_box)

    return cropped_image


def blur_image(image: Image, blur: int) -> Image:
    """
    Blur the image by the strength given

    Arguments:
        image (PIL.Image): the image to be blurred
        blur (int): the strength to blur the image

    Returns:
        (PIL.Image): the blurred image
    """
    if int(blur) != 0:
        image = image.filter(ImageFilter.GaussianBlur(int(blur)))

    return image


def get_image_path_list(image_directory: str) -> List[str]:
    """
    Gets the absolute image paths within a directory

    Arguments:
        image_directory (str): the path to the image or the directory

    Returns:
        (List[str]): the list of absolute paths to images
    """
    if os.path.isfile(image_directory):
        return [utils.get_absolute_image_path(image_directory)]

    return [
        utils.get_absolute_image_path(os.path.join(image_directory, img))
        for img in utils.get_directory_image_paths(image_directory)
    ]


def get_random_image_path(image_paths: List[str]) -> str:
    """Gets a random path to a image from a given list

    Arguments:
        image_paths (List[str]): a list containing paths to images

    Returns:
        (str): a randomly picked image path
    """
    random.shuffle(image_paths)
    return image_paths[0]


def symlink_image(image_path: str, symlink_path: str):
    """
    Symlink an image to a given path

    Arguments:
        image_path (str):   the path to the original image
        symlink_path(str):  the path to symlink to
    """
    if os.path.isfile(symlink_path):
        os.remove(symlink_path)

    os.symlink(image_path, symlink_path)
