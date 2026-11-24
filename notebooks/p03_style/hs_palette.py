"""Fixed HS Section colors and short Vietnamese labels for BACI HS2002."""

from types import MappingProxyType
from .colour_rules import OTHER, OTHER_COLOR

_SECTIONS = (
    ("I", "Động vật và sản phẩm động vật", "#4477AA"),
    ("II", "Sản phẩm thực vật", "#228833"),
    ("III", "Dầu, mỡ động thực vật", "#CCBB44"),
    ("IV", "Thực phẩm chế biến, đồ uống", "#EE6677"),
    ("V", "Khoáng sản", "#886644"),
    ("VI", "Hóa chất", "#AA3377"),
    ("VII", "Nhựa và cao su", "#66CCEE"),
    ("VIII", "Da và sản phẩm từ da", "#994455"),
    ("IX", "Gỗ và sản phẩm gỗ", "#667744"),
    ("X", "Bột giấy và giấy", "#88CCAA"),
    ("XI", "Dệt may", "#332288"),
    ("XII", "Giày dép, mũ và phụ kiện", "#DDCC77"),
    ("XIII", "Đá, gốm và thủy tinh", "#6699CC"),
    ("XIV", "Đá quý và kim loại quý", "#CC6677"),
    ("XV", "Kim loại cơ bản", "#555555"),
    ("XVI", "Máy móc, thiết bị điện", "#117733"),
    ("XVII", "Phương tiện vận tải", "#882255"),
    ("XVIII", "Thiết bị quang học, y tế", "#44AA99"),
    ("XIX", "Vũ khí và đạn dược", "#AA4499"),
    ("XX", "Hàng hóa khác", "#999933"),
    ("XXI", "Tác phẩm nghệ thuật, đồ cổ", "#661100"),
    (OTHER, "Khác", OTHER_COLOR),
)
HS_ORDER = tuple(code for code, _, _ in _SECTIONS)
HS_COLORS = MappingProxyType({code: color for code, _, color in _SECTIONS})
HS_LABELS = MappingProxyType({
    code: label if code == OTHER else f"{code} · {label}"
    for code, label, _ in _SECTIONS
})
