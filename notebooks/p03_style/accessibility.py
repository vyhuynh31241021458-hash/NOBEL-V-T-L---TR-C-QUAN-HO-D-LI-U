"""Simulate color-vision deficiencies and luminance-based grayscale."""

import numpy as np
from colorspacious import cspace_convert

CVD_TYPES = ("protanomaly", "deuteranomaly", "tritanomaly")


def simulate_cvd(rgb, cvd_type: str, severity: int = 100):
    """Transform sRGB values in [0, 1] using the Machado model."""
    if cvd_type not in CVD_TYPES or not 0 <= severity <= 100:
        raise ValueError("Expected a supported deficiency and severity in [0, 100].")
    space = {"name": "sRGB1+CVD", "cvd_type": cvd_type, "severity": severity}
    return np.clip(cspace_convert(rgb, space, "sRGB1"), 0, 1)


def grayscale(rgb):
    """Convert sRGB to gray using relative luminance in linear RGB."""
    linear = cspace_convert(rgb, "sRGB1", "sRGB1-linear")
    luminance = linear @ np.array([0.2126, 0.7152, 0.0722])
    neutral = np.repeat(luminance[..., np.newaxis], 3, axis=-1)
    return np.clip(cspace_convert(neutral, "sRGB1-linear", "sRGB1"), 0, 1)
