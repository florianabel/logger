from unittest import TestCase
# from pytest import capfd

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

def test_log_level_filtering():
    logger = getLogger()
    logger.setLogLevel('WARNING')
    isEnabledForWarning = logger.isEnabledFor(WARNING)
    isEnabledForInfo = logger.isEnabledFor(INFO)
    assert isEnabledForWarning == True
    assert isEnabledForInfo == False


def test_log_to_console(capsys):
    logger = getLogger()
    logger.setLogLevel('DEBUG')
    logger.debug("Testing console output")
    out, err = capsys.readouterr()
    assert out == "Testing console output\n"

def test_log_to_console_filtered(capsys):
    logger = getLogger()
    logger.setLogLevel('WARNING')
    logger.warning("Testing console for warning")
    out, err = capsys.readouterr()
    assert out == "Testing console for warning\n"
    logger.info("Testing console for info")
    out, err = capsys.readouterr()
    assert out == ""