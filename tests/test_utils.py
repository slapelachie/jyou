import unittest

from jyou import utils

class TestUtils(unittest.TestCase):
    def test_md5(self):
        md5 = utils.md5('hello')
        self.assertEqual(md5, '5d41402abc4b2a76b9719d911017c592')

    def test_md5_file(self):
        md5 = utils.md5_file('tests/assets/test.jpg')
        self.assertEqual(md5, '31084f2c8577234aeb5563b95a2786a8')
    
    def test_get_dir_imgs(self):
        images = utils.get_dir_imgs('tests/assets/')
        self.assertEqual(images, ['test.jpg'])