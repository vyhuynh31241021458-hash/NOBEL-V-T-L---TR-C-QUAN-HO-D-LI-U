from unittest import TestCase

from p03_style import (
    format_balance, format_growth, format_number, format_percent,
    format_percentage_points, format_usd, format_vnd, format_year,
)

class FormattingTests(TestCase):
    def test_units_and_signs(self):
        self.assertEqual(format_usd(125.6e9), "125.6 tỷ USD")
        self.assertEqual(format_usd(15.8e6, millions=True), "15.8 triệu USD")
        self.assertEqual(format_balance(27.4e9), "+27.4 tỷ USD")
        self.assertEqual(format_vnd(250000, per="kg"), "250,000 VND/kg")
        self.assertEqual(format_percent(0.256), "25.6%")
        self.assertEqual(format_growth(0.125), "+12.5%")
        self.assertEqual(format_percentage_points(-2.5), "−2.5 pp")
        self.assertEqual(format_number(-0.0001, 1, signed=True), "0.0")
        self.assertEqual(format_year(2024), "2024")
        self.assertEqual(format_usd(None), "N/A")
        self.assertEqual(format_vnd(float("inf")), "N/A")
