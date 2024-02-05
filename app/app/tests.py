"""
Sample tests
"""
from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        result = calc.add(2, 4)
        self.assertEqual(result, 6)

    def test_subtract_numbers(self):
        result = calc.subtract(4, 2)
        self.assertEqual(result, 2)
