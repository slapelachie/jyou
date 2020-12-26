import unittest
import os
import shutil
from PIL import Image

from jyou import generator

out_path = "/tmp/jyou-git/"


class TestGenerator(unittest.TestCase):
    def test_getOutPathFromMD5(self):
        path = generator.getOutPathFromMD5("tests/assets/test.jpg", "screen", "/tmp/")
        self.assertEqual(path, "/tmp/31084f2c8577234aeb55_screen.png")

    def test_getResolutionDimensions(self):
        dimensions = generator.getResolutionDimensions(("1920", "1080", "1920", "0"))
        self.assertEqual(dimensions, (1920, 1080))

    def test_getResolutionOffset(self):
        offsets = generator.getResolutionOffset(("1920", "1080", "1920", "0"))
        self.assertEqual(offsets, (1920, 0))

    def test_getOutputResolution(self):
        dimensions = generator.getOutputResolution(
            [("1920", "1080", "1920", "0"), ("1920", "1080", "0", "0")]
        )
        self.assertEqual(dimensions, (3840, 1080))

    def test_cropImageToResolution(self):
        image = Image.open("tests/assets/test.jpg")
        new_image = generator.cropImageToResolution(image, (50, 50, 0, 0))
        self.assertEqual(new_image.size, (50, 50))

    def test_convertResolutionToList(self):
        resolution_list = generator.convertResolutionToList(
            "1920x1080+0+0, 1920x1080+1920+0"
        )
        self.assertEqual(resolution_list, [(1920, 1080, 0, 0), (1920, 1080, 1920, 0)])

    def test_generateSingleFileSingleResolution(self):
        lockscreen_out_dir = os.path.join(out_path, "lockscreen")
        backend = generator.LockscreenGenerator("tests/assets/test.jpg")
        backend.setOutputPath(out_path)
        backend.setResolution([(1920, 1080, 0, 0)])
        backend.generate()
        output_image_path = os.path.join(
            lockscreen_out_dir,
            "31084f2c8577234aeb55_34bca0784f2e76070371dc4afc9a97fd.png",
        )
        output_image_size = Image.open(output_image_path).size
        self.assertEqual(output_image_size, (1920, 1080))
        shutil.rmtree(out_path)

    def test_generateSingleFileDoubleResolution(self):
        lockscreen_out_dir = os.path.join(out_path, "lockscreen")
        backend = generator.LockscreenGenerator("tests/assets/test.jpg")
        backend.setOutputPath(out_path)
        backend.setResolution([(1920, 1080, 0, 0), (1920, 1080, 1920, 0)])
        backend.generate()
        output_image_path = os.path.join(
            lockscreen_out_dir,
            "31084f2c8577234aeb55_2dc53337e74f76026e6abe67cbc00e42.png",
        )
        output_image_size = Image.open(output_image_path).size
        self.assertEqual(output_image_size, ((1920 * 2), 1080))
        shutil.rmtree(out_path)

    def test_updateFile(self):
        backend = generator.LockscreenGenerator("tests/assets/test.jpg")
        backend.setOutputPath(out_path)
        backend.setResolution([(1920, 1080, 0, 0)])
        backend.update()
        self.assertTrue(
            os.path.isfile(os.path.join(out_path, "current_lockscreen.png"))
        )
        shutil.rmtree(out_path)