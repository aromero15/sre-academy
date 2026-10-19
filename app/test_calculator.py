# test_calculator.py
import unittest
from calculator import add, divide

class TestCalculator(unittest.TestCase):

    def test_add_positive_numbers(self):
        # Assert that 2 + 3 equals 5
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        # Assert that -1 + -1 equals -2
        self.assertEqual(add(-1, -1), -2)

    def test_divide_valid(self):
        # Assert that 10 / 2 equals 5
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero(self):
        # Assert that dividing by zero raises a ValueError
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
