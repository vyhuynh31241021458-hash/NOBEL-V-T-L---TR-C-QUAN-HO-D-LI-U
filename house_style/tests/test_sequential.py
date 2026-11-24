from unittest import TestCase

import numpy as np
from house_style.accessibility import grayscale
from house_style.colour_rules import MISSING_COLOR, color_for_value
from house_style.sequential import SEQUENTIAL_COLORS, sequential_norm

class SequentialTests(TestCase):
    def test_lightness_and_missing(self):
        norm = sequential_norm(0, 100)
        rgb = SEQUENTIAL_COLORS(norm(np.linspace(0, 100, 256)))[:, :3]
        self.assertTrue(np.all(np.diff(grayscale(rgb)[:, 0]) < 0))
        self.assertEqual(color_for_value(None, cmap=SEQUENTIAL_COLORS, norm=norm), MISSING_COLOR)
        self.assertNotEqual(color_for_value(0, cmap=SEQUENTIAL_COLORS, norm=norm), MISSING_COLOR)
        self.assertEqual(sequential_norm(0, 0)(0), 0)
