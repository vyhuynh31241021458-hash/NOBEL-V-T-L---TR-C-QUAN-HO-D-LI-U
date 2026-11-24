"""Light to dark scale for increasing values."""

from math import isfinite
from matplotlib import colormaps
from matplotlib.colors import Normalize
from .colour_rules import MISSING_COLOR

SEQUENTIAL_CMAP = "Blues"
SEQUENTIAL_COLORS = colormaps[SEQUENTIAL_CMAP].with_extremes(bad=MISSING_COLOR)


def sequential_norm(vmin: float, vmax: float) -> Normalize:
    if not (isfinite(vmin) and isfinite(vmax) and vmin <= vmax):
        raise ValueError("Expected finite limits in increasing order.")
    if vmin == vmax:
        vmax += max(1, abs(vmax) * 0.01)
    return Normalize(vmin=vmin, vmax=vmax)
