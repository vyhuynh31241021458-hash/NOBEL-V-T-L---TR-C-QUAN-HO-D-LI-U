"""Use one accent to emphasize a selected item."""

from collections.abc import Iterable, Mapping
from .colour_rules import OTHER_COLOR

ACCENT_COLOR = "#0072B2"
CONTEXT_COLOR = OTHER_COLOR
HIGHLIGHT_LINEWIDTH = 3


def highlight_colors(
    labels: Iterable[str], selected: str | Iterable[str], palette: Mapping[str, str] | None = None,
) -> list[str]:
    keys = {selected} if isinstance(selected, str) else set(selected)
    fixed = palette if palette is not None else {}
    return [fixed.get(label, ACCENT_COLOR) if label in keys else CONTEXT_COLOR for label in labels]
