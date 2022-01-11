import unittest
import warnings

from jyou import config_handler


class TestConfigHandler(unittest.TestCase):
    def test_parse_config(self):
        warnings.warn("Test not implemented")

    def test_save_config(self):
        warnings.warn("Test not implemented")

    def test_load_config(self):
        warnings.warn("Test not implemented")

    def test_compare_flag_with_config(self):
        self.assertEqual(
            config_handler.compare_flag_with_config("test", "tset"), "test"
        )
        self.assertEqual(config_handler.compare_flag_with_config("test", None), "test")
        self.assertEqual(config_handler.compare_flag_with_config(None, "test"), "test")
