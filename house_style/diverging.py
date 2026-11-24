"""RdBu with equal distances on either side of zero."""

from math import isfinite

from matplotlib import colormaps
from matplotlib.colors import TwoSlopeNorm
from .colour_rules import MISSING_COLOR

DIVERGING_CMAP = colormaps["RdBu"].resampled(257).with_extremes(bad=MISSING_COLOR)


def diverging_norm(vmin: float, vmax: float) -> TwoSlopeNorm:
    if not (isfinite(vmin) and isfinite(vmax) and vmin <= vmax):
        raise ValueError("Expected finite limits in increasing order.")
    limit = max(abs(vmin), abs(vmax)) or 1
    return TwoSlopeNorm(vmin=-limit, vcenter=0, vmax=limit)
