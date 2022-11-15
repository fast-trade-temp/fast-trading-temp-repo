import unittest
import pandas as pd


class InterpolateTest(unittest.TestCase):
    def test_ffill_close(self):
        """Testing forward fill with close"""

        date_range = pd.date_range("2000-01-01 09:30:00", "2000-01-01 16:00:00")
