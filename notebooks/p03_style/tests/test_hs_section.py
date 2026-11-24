from unittest import TestCase

from p03_style.hs_palette import HS_COLORS, HS_LABELS, HS_ORDER
from p03_style.colour_rules import ordered_present

class HsTests(TestCase):
    def test_fixed_mapping(self):
        self.assertEqual(len(HS_ORDER), 22)
        filtered = ordered_present(HS_ORDER, ("XXI", "I", "Other", "IV"))
        self.assertEqual(filtered, ("I", "IV", "XXI", "Other"))
        self.assertEqual([HS_COLORS[key] for key in filtered],
                         ["#4477AA", "#EE6677", "#661100", "#BDBDBD"])
        self.assertEqual(HS_LABELS["Other"], "Khác")
