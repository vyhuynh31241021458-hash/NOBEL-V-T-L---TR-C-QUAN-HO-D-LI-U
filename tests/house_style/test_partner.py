from unittest import TestCase

from notebooks.house_style import ordered_present
from notebooks.house_style import PARTNER_COLORS, PARTNER_HATCHES, PARTNER_ORDER, partner_group

class PartnerTests(TestCase):
    def test_fixed_order_and_colors(self):
        self.assertEqual(PARTNER_ORDER, ("CHN", "USA", "KOR", "JPN", "THA", "Other"))
        filtered = ordered_present(PARTNER_ORDER, ("Other", "JPN", "CHN"))
        self.assertEqual(filtered, ("CHN", "JPN", "Other"))
        self.assertEqual([PARTNER_COLORS[key] for key in filtered], ["#0072B2", "#CC79A7", "#BDBDBD"])
        self.assertEqual(len(set(PARTNER_HATCHES.values())), 6)

    def test_missing_and_aggregates_are_distinct_from_other(self):
        self.assertIsNone(partner_group(None))
        self.assertIsNone(partner_group("WLD"))
        self.assertIsNone(partner_group("N/A"))
        self.assertEqual(partner_group(" vnm "), "Other")
        self.assertEqual(partner_group(" tha "), "THA")
