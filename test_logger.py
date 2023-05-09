from unittest import TestCase

from . import getLogger
from . import DEBUG, INFO, WARNING, ERROR

class BaseTesting(TestCase):
    def test_singleton_logger(self):
        logger = getLogger()
        logger2 = getLogger()
        self.assertTrue(logger == logger2)


    def test_default_log_level(self):
        logger = getLogger()
        self.assertTrue(logger.log_level == DEBUG)

    def test_set_log_level(self):
        logger = getLogger()
        logger.setLogLevel(WARNING)
        self.assertTrue(logger.log_level == WARNING)

    def test_set_log_level_by_string(self):
        logger = getLogger()
        logger.setLogLevel('WARNING')
        self.assertTrue(logger.log_level == WARNING)