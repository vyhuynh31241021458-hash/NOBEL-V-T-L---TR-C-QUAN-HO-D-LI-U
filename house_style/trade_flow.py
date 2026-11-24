"""Categorical style for trade direction."""

from types import MappingProxyType

TRADE_FLOW_ORDER = ("Export", "Import")
TRADE_FLOW_COLORS = MappingProxyType({"Export": "#22577A", "Import": "#B86E24"})
TRADE_FLOW_LABELS = MappingProxyType({"Export": "Xuất khẩu", "Import": "Nhập khẩu"})
TRADE_FLOW_LINESTYLES = MappingProxyType({"Export": "solid", "Import": "dashed"})
TRADE_FLOW_MARKERS = MappingProxyType({"Export": "o", "Import": "s"})
TRADE_FLOW_HATCHES = MappingProxyType({"Export": "/", "Import": chr(92)})
