"""
base_test.py
------------
UNIQUE APPROACH #2 - True Unittest + PyTest hybrid
-----------------------------------------------------
The capstone brief explicitly asks for BOTH Unittest and PyTest.
Most solutions just pick one and ignore the other. Here:

  * Every test class inherits from `unittest.TestCase` -> you get
    unittest's setUp/tearDown lifecycle and its rich assertion
    library (assertEqual, assertTrue, assertIn, etc.)
  * The WHOLE suite is discovered, executed, parametrized, marked and
    reported via PyTest (pytest.ini, pytest-html, custom markers).
    PyTest natively supports running unittest.TestCase classes, so we
    get the best of both: unittest's structure + PyTest's ecosystem
    (fixtures for cross-cutting concerns like DB logging, plugins,
    CLI filtering with -m smoke, etc.)

The driver itself is still handed to the test via a PyTest fixture
(see conftest.py) rather than built directly in setUp, so failure
screenshots / DB run-logging hooked into PyTest can access it too.
"""

import unittest

from utils.logger import get_logger

log = get_logger(__name__)


class BaseTest(unittest.TestCase):
    """
    Subclasses get a live `self.driver` because conftest.py's
    `inject_driver` autouse fixture assigns pytest's `driver` fixture
    onto the unittest.TestCase instance before each test method runs.
    """

    driver = None  # populated by the autouse fixture in conftest.py

    def setUp(self):
        log.info(f"===== START TEST: {self._testMethodName} =====")

    def tearDown(self):
        log.info(f"===== END TEST: {self._testMethodName} =====")
