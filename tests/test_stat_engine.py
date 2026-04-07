"""Unit tests for StatEngine."""

import unittest

from src.stat_engine import StatEngine, EmptyDataError, DataTypeError


class TestStatEngine(unittest.TestCase):
    def test_mean_on_odd_list(self):
        engine = StatEngine([1, 3, 5])
        self.assertEqual(engine.get_mean(), 3.0)

    def test_median_on_odd_list(self):
        engine = StatEngine([9, 1, 5])
        self.assertEqual(engine.get_median(), 5.0)

    def test_median_on_even_list(self):
        engine = StatEngine([1, 2, 3, 4])
        self.assertEqual(engine.get_median(), 2.5)

    def test_empty_list_raises_error(self):
        with self.assertRaises(EmptyDataError):
            StatEngine([])

    def test_standard_deviation_population_known_value(self):
        engine = StatEngine([2, 4, 4, 4, 5, 5, 7, 9])
        self.assertAlmostEqual(engine.get_standard_deviation(is_sample=False), 2.0, places=7)

    def test_standard_deviation_sample_known_value(self):
        engine = StatEngine([2, 4, 4, 4, 5, 5, 7, 9])
        self.assertAlmostEqual(engine.get_standard_deviation(is_sample=True), 2.1380899353, places=7)

    def test_mode_multimodal(self):
        engine = StatEngine([1, 1, 2, 2, 3])
        self.assertEqual(engine.get_mode(), [1.0, 2.0])

    def test_mode_unique(self):
        engine = StatEngine([1, 2, 3, 4])
        self.assertEqual(engine.get_mode(), "No mode: all values are unique.")

    def test_mixed_types_are_cleaned_or_rejected(self):
        engine = StatEngine([1, 2, "3", 4.5])
        self.assertEqual(engine.data, [1.0, 2.0, 3.0, 4.5])

    def test_bad_type_raises(self):
        with self.assertRaises(DataTypeError):
            StatEngine([1, None, 3])


if __name__ == "__main__":
    unittest.main()
