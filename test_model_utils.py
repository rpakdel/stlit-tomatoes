import unittest
from datetime import datetime
from model_utils import get_temperature_category, get_season

class TestModelUtils(unittest.TestCase):

    def test_get_temperature_category_none(self):
        self.assertIsNone(get_temperature_category(None))

    def test_get_temperature_category_values(self):
        self.assertEqual(get_temperature_category(-5), 'Very cold')
        self.assertEqual(get_temperature_category(-3), 'Very cold')
        self.assertEqual(get_temperature_category(-2), 'Cold')
        self.assertEqual(get_temperature_category(9), 'Cold')
        self.assertEqual(get_temperature_category(10), 'Normal')
        self.assertEqual(get_temperature_category(16), 'Normal')
        self.assertEqual(get_temperature_category(17), 'Warm')
        self.assertEqual(get_temperature_category(26), 'Warm')
        self.assertEqual(get_temperature_category(27), 'Hot')
        self.assertEqual(get_temperature_category(35), 'Hot')

    def test_get_season(self):
        # Spring: March 20 - June 19
        self.assertEqual(get_season(datetime(2023, 3, 20)), 'Spring')
        self.assertEqual(get_season(datetime(2023, 6, 19)), 'Spring')

        # Summer: June 20 - Sep 19
        self.assertEqual(get_season(datetime(2023, 6, 20)), 'Summer')
        self.assertEqual(get_season(datetime(2023, 9, 19)), 'Summer')

        # Autumn: Sep 20 - Dec 19
        self.assertEqual(get_season(datetime(2023, 9, 20)), 'Autumn')
        self.assertEqual(get_season(datetime(2023, 12, 19)), 'Autumn')

        # Winter: Dec 20 - March 19
        self.assertEqual(get_season(datetime(2023, 12, 20)), 'Winter')
        self.assertEqual(get_season(datetime(2023, 3, 19)), 'Winter')

if __name__ == '__main__':
    unittest.main()
