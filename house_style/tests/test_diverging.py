from unittest import TestCase

import numpy as np
from matplotlib.colors import to_hex
from house_style import DIVERGING_CMAP, diverging_norm

class DivergingTests(TestCase):
    def test_symmetry_center_and_direction(self):
        norm = diverging_norm(-2, 8)
        np.testing.assert_allclose(norm([-8, 0, 8]), [0, 0.5, 1])
        self.assertEqual([to_hex(DIVERGING_CMAP(norm(x))) for x in (-8, 0, 8)],
                         ["#67001f", "#f7f7f7", "#053061"])
        self.assertEqual(diverging_norm(0, 0)(0), 0.5)
