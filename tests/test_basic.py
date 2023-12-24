# -*- coding: utf-8 -*-

from .context import pygameobj

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test(self):
        assert True


if __name__ == '__main__':
    unittest.main()