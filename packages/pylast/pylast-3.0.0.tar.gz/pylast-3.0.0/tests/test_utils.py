#!/usr/bin/env python
"""
Unit tests for pylast.py
"""
import unittest

import pylast

from .test_pylast import PyLastTestCase


class TestPyLastUtils(PyLastTestCase):
    def test__number_none(self):
        # Arrange
        string = None

        # Act
        number = pylast._number(string)

        # Assert
        self.assertEqual(number, 0)

    def test__number_empty_string(self):
        # Arrange
        string = ""

        # Act
        number = pylast._number(string)

        # Assert
        self.assertEqual(number, 0)

    def test__number_not_int(self):
        # Arrange
        string = "123.4"

        # Act
        number = pylast._number(string)

        # Assert
        self.assertEqual(number, 123.4)


if __name__ == "__main__":
    unittest.main(failfast=True)
