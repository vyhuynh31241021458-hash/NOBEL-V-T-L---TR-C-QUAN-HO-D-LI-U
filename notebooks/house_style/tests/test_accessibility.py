from unittest import TestCase

import matplotlib
import numpy as np
from matplotlib.colors import to_rgb

from notebooks.house_style.house_style import apply_style
from notebooks.house_style.house_style import CVD_TYPES, grayscale, simulate_cvd
from notebooks.house_style.house_style import PARTNER_COLORS

class AccessibilityTests(TestCase):
    def test_simulations(self):
        rgb = np.array([to_rgb(color) for color in PARTNER_COLORS.values()])
        gray = grayscale(rgb)
        np.testing.assert_allclose(gray[:, 0], gray[:, 1])
        np.testing.assert_allclose(gray[:, 1], gray[:, 2])
        for kind in CVD_TYPES:
            with self.subTest(kind=kind):
                converted = simulate_cvd(rgb, kind)
                self.assertTrue(np.all((converted >= 0) & (converted <= 1)))
                self.assertFalse(np.allclose(converted, rgb))
                np.testing.assert_allclose(simulate_cvd(rgb, kind, 0), rgb, atol=1e-7)

    def test_theme_and_text_contrast(self):
        with apply_style():
            self.assertEqual(matplotlib.rcParams["savefig.dpi"], 300)
            for key in ("text.color", "axes.labelcolor", "xtick.labelcolor", "ytick.labelcolor"):
                luminance = float(to_rgb(matplotlib.rcParams[key])[0])
                linear = ((luminance + 0.055) / 1.055) ** 2.4
                self.assertGreaterEqual(1.05 / (linear + 0.05), 4.5)
