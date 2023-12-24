# -*- coding: utf-8 -*-

from .context import pygameobj

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test(self):
        self.assertIsNone(None)


if __name__ == '__main__':
    unittest.main()
