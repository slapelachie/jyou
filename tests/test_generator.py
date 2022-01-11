import unittest
import warnings
from PIL import Image, ImageChops

from jyou import generator

IMAGE_PATH = "tests/assets/test.jpg"
OUT_PATH = "/tmp/jyou-git/"


class TestGenerator(unittest.TestCase):
    def test_get_resolution_image(self):
        # TODO: figure out how to test this
        warnings.warn("Test not implemented")

    def test_get_out_path_from_md5(self):
        path = generator.get_out_path_from_md5(
            "tests/assets/test.jpg", "screen", "/tmp/"
        )
        self.assertEqual(path, "/tmp/31084f2c8577234aeb55_screen.png")

    def test_generate_lockscreen_image(self):
        pass

    def test_get_resolution_dimensions(self):
        dimensions = generator.get_resolution_dimensions(("1920", "1080", "1920", "0"))
        self.assertEqual(dimensions, (1920, 1080))

    def test_get_resolution_offset(self):
        offsets = generator.get_resolution_offset(("1920", "1080", "1920", "0"))
        self.assertEqual(offsets, (1920, 0))

    def test_get_accumlative_dimensions(self):
        dimensions = generator.get_accumulative_dimensions(
            [("1920", "1080", "1920", "0"), ("1920", "1080", "0", "0")]
        )
        self.assertEqual(dimensions, (3840, 1080))

    def test_crop_image_to_dimensions(self):
        image = Image.open(IMAGE_PATH)
        new_image = generator.crop_image_to_dimensions(image, (50, 50))
        self.assertEqual(new_image.size, (50, 50))

    def test_blur_image(self):
        # TODO: compare to blurred image
        # NOTE: Idk why but comparing does not work
        pass

    def test_get_image_path_list_directory(self):
        image_list = generator.get_image_path_list("tests/assets/")
        self.assertTrue(image_list[0].endswith("tests/assets/test.jpg"))

    def test_get_image_path_list_image(self):
        image_list = generator.get_image_path_list("tests/assets/test.jpg")
        self.assertTrue(image_list[0].endswith("tests/assets/test.jpg"))

    def test_get_random_image_path(self):
        # TODO: implement
        warnings.warn("Test not implemented")

    def test_symlink_image(self):
        # TODO: implement
        warnings.warn("Test not implemented")
