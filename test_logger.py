from unittest import TestCase

from . import getLogger

class BaseTesting(TestCase):
    def test_singleton_logger(self):
        logger = getLogger()
        logger2 = getLogger()
        self.assertTrue(logger == logger2)