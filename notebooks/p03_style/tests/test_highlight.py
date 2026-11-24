from unittest import TestCase

from p03_style.highlight import highlight_colors
from p03_style.partner_palette import PARTNER_COLORS
from p03_style.trade_flow import TRADE_FLOW_COLORS, TRADE_FLOW_LINESTYLES, TRADE_FLOW_ORDER

class HighlightTests(TestCase):
    def test_preserve_fixed_color(self):
        self.assertEqual(highlight_colors(("CHN", "USA"), "USA", PARTNER_COLORS),
                         ["#BDBDBD", "#E69F00"])
        self.assertEqual(highlight_colors(("CHN",), ()), ["#BDBDBD"])

    def test_trade_flow_channels(self):
        self.assertEqual(TRADE_FLOW_ORDER, ("Export", "Import"))
        self.assertEqual(TRADE_FLOW_COLORS["Export"], "#22577A")
        self.assertEqual(TRADE_FLOW_COLORS["Import"], "#B86E24")
        self.assertNotEqual(TRADE_FLOW_LINESTYLES["Export"], TRADE_FLOW_LINESTYLES["Import"])
