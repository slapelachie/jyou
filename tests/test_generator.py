import unittest
from PIL import Image

from jyou import generator

class TestGenerator(unittest.TestCase):
    def test_getOutPathFromMD5(self):
        path = generator.getOutPathFromMD5('tests/assets/test.jpg', 'screen', '/tmp/')
        self.assertEqual(path, '/tmp/31084f2c8577234aeb55_screen.png')

    def test_getResolutionDimensions(self):
        dimensions = generator.getResolutionDimensions(('1920', '1080', '1920', '0'))
        self.assertEqual(dimensions, (1920, 1080))

    def test_getResolutionOffset(self):
        offsets = generator.getResolutionOffset(('1920', '1080', '1920', '0'))
        self.assertEqual(offsets, (1920, 0))

    def test_getOutputResolution(self):
        dimensions = generator.getOutputResolution([('1920', '1080', '1920', '0'), ('1920', '1080', '0', '0')])
        self.assertEqual(dimensions, (3840,1080))

    def test_cropImageToResolution(self):
        image = Image.open('tests/assets/test.jpg')
        new_image = generator.cropImageToResolution(image, (50,50,0,0))
        self.assertEqual(new_image.size, (50,50))

    def test_convertResolutionToList(self):
        resolution_list = generator.convertResolutionToList("1920x1080+0+0, 1920x1080+1920+0")
        self.assertEqual(resolution_list, [(1920,1080,0,0),(1920,1080,1920,0)])