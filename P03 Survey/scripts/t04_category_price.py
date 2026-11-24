"""Hoàn thành Task 4: phân loại và xếp giá cho bộ khảo sát P03."""
import argparse
import csv
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

# Ánh xạ đã rà theo tên sản phẩm của đợt khảo sát 398 mẫu.
# Mỗi dòng: tiền tố mã, danh mục, mã đơn hoặc dải mã liên tiếp.
MAPPING = """
AEON|Nước có ga|1-4,5,9
AEON|Nước khoáng và nước uống|6,7
AEON|Trà đóng chai|8,12-15
AEON|Cà phê pha sẵn|10,66-69
AEON|Nước trái cây và nước giải khát vị trái cây|11
AEON|Đồ uống từ sữa|16
AEON|Sữa rửa mặt|17,21,33
AEON|Son môi|18,19,28
AEON|Tẩy trang|20,29
AEON|Chống nắng|22,30
AEON|Trang điểm mặt|23,25,35
AEON|Toner|24,32
AEON|Dưỡng da mặt|26,34
AEON|Dưỡng da cho bé|27
AEON|Mặt nạ dưỡng da|31
AEON|Bánh và snack|36-58
AEON|Nước tăng lực|59-65,70
AEON|Nước lau sàn|71,72,77
AEON|Vệ sinh nhà tắm và bồn cầu|73-76
AEON|Nước rửa chén|78,176,177
AEON|Nước xả vải|79,178,180,181
AEON|Nước giặt|80,81,179
AEON|Tẩy quần áo|82,90
AEON|Vệ sinh máy giặt|83
AEON|Bột giặt|84
AEON|Dưỡng và tạo kiểu tóc|85,91,97-99,101,102
AEON|Sữa tắm|86,88
AEON|Dầu xả và kem ủ tóc|87,89,93,94,100
AEON|Dầu gội|92,95,96
AEON|Dưỡng thể|103-105
AEON|Cáp sạc|106-109
AEON|Sạc dự phòng|110,122,123
AEON|Củ sạc|111,112
AEON|Tai nghe không dây|113,114,116,120
AEON|Tai nghe có dây|115
AEON|Chuột máy tính|117,118
AEON|Bàn phím|119
AEON|Giá đỡ điện thoại|121
AEON|Áo thun và polo|124-131,139
AEON|Áo khoác và áo len|132
AEON|Áo sơ mi và áo kiểu|133
AEON|Quần dài|134,135,137
AEON|Quần short|136
AEON|Váy và đầm|138
AEON|Nón thời trang|140
AEON|Đồ chơi lắp ráp và xếp hình|141,142,146,148,158,159
AEON|Đồ chơi bàn và vận động|143,147,149
AEON|Thú nhồi bông|144
AEON|Đồ chơi nhập vai|145,151,155,156,160
AEON|Đồ chơi xe mô hình|150,153
AEON|Đồ chơi xe điều khiển|152,154,157
AEON|Dụng cụ học tập khác|161,162,166-168,171,173
AEON|Giấy in|163
AEON|Túi giấy|164
AEON|Lịch|165
AEON|Bút và màu vẽ|169,174
AEON|Bút bi|170
AEON|Vở và sổ|172,175
AEON|Cá một nắng và cá chế biến|182,184
AEON|Cá đông lạnh chưa chế biến|183,185,187
AEON|Tôm|186
AEON|Hải sản|188
GO|Tẩy tế bào chết|1
GO|Nhuộm tóc|2
GO|Dưỡng và tạo kiểu tóc|3,7,8
GO|Dầu xả và kem ủ tóc|4,5,175
GO|Dầu gội|6,14-16
GO|Sữa tắm|9,10,22,23,174
GO|Dưỡng thể|11-13
GO|Kem đánh răng|17,18,21
GO|Nước rửa tay|19
GO|Nước rửa chén|20,26,33
GO|Nước giặt|24,28,29,31
GO|Vệ sinh nhà tắm và bồn cầu|25,176,177,179
GO|Viên giặt|27
GO|Xử lý bể phốt|30
GO|Nước xả vải|32
GO|Nước lau sàn|34,35,178,180,181
GO|Váy và đầm|36,43,58,59,61,62
GO|Áo thun và polo|37,45,48,49,51,52,66-68,70
GO|Quần dài|38,55
GO|Áo khoác và áo len|39,50
GO|Dây nịt|40
GO|Nón thời trang|41
GO|Áo sơ mi và áo kiểu|42,60,63-65,69
GO|Dép và sandal|44,54
GO|Tất|46,47
GO|Quần short|53
GO|Nón bảo hiểm|56,57
GO|Bánh và snack|71-86
GO|Kẹo và thạch|87-89
GO|Nước khoáng và nước uống|90
GO|Cà phê pha sẵn|91,153,154
GO|Nước gạo|92,156
GO|Nước dừa|93,145
GO|Nước có ga|94,95
GO|Nước thể thao|96,160
GO|Nước yến|97,155,157
GO|Trà đóng chai|98,101,102,149-152,158
GO|Nước trái cây và nước giải khát vị trái cây|99,103,141-143,147
GO|Nước thạch|100
GO|Đồ uống từ sữa|104,146
GO|Nước tăng lực|105,159
GO|Bút gel|106-115
GO|Bút bi|116-120
GO|Túi đựng bút|121-130
GO|Kéo|131,132
GO|Bút và màu vẽ|133
GO|Đồ chơi nhập vai|134,187,189
GO|Dụng cụ học tập khác|135,136
GO|Vở và sổ|137,138
GO|Nhãn dán|139,140
GO|Kombucha|144,148
GO|Sữa rửa mặt|161-163
GO|Son môi|164,165
GO|Khử mùi|166,172
GO|Tẩy trang|167
GO|Chống nắng|168,173
GO|Dưỡng da mặt|169,170
GO|Nước súc miệng|171
GO|Đồ chơi xe mô hình|182,183,185
GO|Đồ chơi lắp ráp và xếp hình|184,190-195
GO|Đồ chơi xe điều khiển|186,188
GO|Hải sản|196,197,209,210
GO|Tôm|198,200,208
GO|Cá đông lạnh chưa chế biến|199,201-204,206
GO|Cá một nắng và cá chế biến|205,207
"""

# Nhóm hàng bán theo dung tích/khối lượng không được so bằng giá nguyên gói.
MEASURED = set("""
Nước có ga|Nước khoáng và nước uống|Trà đóng chai|Cà phê pha sẵn|Nước trái cây và nước giải khát vị trái cây|Đồ uống từ sữa|Sữa rửa mặt|Son môi|Tẩy trang|Chống nắng|Trang điểm mặt|Toner|Dưỡng da mặt|Dưỡng da cho bé|Bánh và snack|Nước tăng lực|Nước lau sàn|Vệ sinh nhà tắm và bồn cầu|Nước rửa chén|Nước xả vải|Nước giặt|Tẩy quần áo|Bột giặt|Dưỡng và tạo kiểu tóc|Sữa tắm|Dầu xả và kem ủ tóc|Dầu gội|Dưỡng thể|Cá một nắng và cá chế biến|Cá đông lạnh chưa chế biến|Tôm|Hải sản|Tẩy tế bào chết|Nhuộm tóc|Kem đánh răng|Nước rửa tay|Kẹo và thạch|Nước gạo|Nước dừa|Nước thể thao|Nước yến|Nước thạch|Kombucha|Khử mùi|Nước súc miệng
""".strip().split("|"))
UNITS = {"g": (1, "VNĐ/100 g"), "kg": (1000, "VNĐ/100 g"),
         "ml": (1, "VNĐ/100 ml"), "l": (1000, "VNĐ/100 ml")}
FIELDS = ["category_clean", "price_comparison_unit", "price_normalized",
          "group_valid_n", "p33", "p67", "price_tier", "sample_flag", "task4_note",
          "price_display_group"]


def category_map():
    result = {}
    for line in MAPPING.strip().splitlines():
        store, category, spans = line.split("|")
        for span in spans.split(","):
            start, _, end = span.partition("-")
            for number in range(int(start), int(end or start) + 1):
                key = f"{store}_{number:03d}"
                if key in result:
                    raise ValueError(f"Mã bị phân loại hai lần: {key}")
                result[key] = category
    return result


def positive(text):
    try:
        value = float(text)
    except (ValueError, TypeError):
        return None
    return value if math.isfinite(value) and value > 0 else None


def compare_price(row, category):
    name = row["product_name"].casefold()
    spec = row["spec_text"].casefold()
    flags = set(re.findall(r"[a-z]+", row["verify_fields"].casefold()))
    price = positive(row["price_vnd"])
    if "price" in flags or price is None:
        return "", None, "Giá thiếu hoặc cần xác minh theo Task 1"
    if "spec" in flags:
        return "", None, "Quy cách cần xác minh theo Task 1"
    if row["record_id"] in {"GO_017", "GO_071"}:
        return "", None, "Tổng khối lượng của quy cách bán chưa rõ"
    if category in {"Bút bi", "Bút gel", "Tất", "Viên giặt"} or (
        category == "Vệ sinh nhà tắm và bồn cầu" and name.startswith("viên")
    ):
        match = re.search(r"(\d+)\s*(?:cây|bút|viên)\b", spec)
        if not match:
            match = re.search(r"(?:lô|pack|vỉ)\s*(\d+)\b", name)
        if match and int(match[1]) > 0:
            return "VNĐ/đơn vị đếm", price / int(match[1]), ""
        if category in {"Bút bi", "Bút gel", "Tất", "Viên giặt"}:
            return "", None, "Thiếu số lượng trong gói"
        return "VNĐ/gói", price, ""
    if category not in MEASURED:
        return "VNĐ/đơn vị bán", price, ""
    amount = positive(row["spec_value"])
    unit = row["spec_unit"].casefold().strip()
    if amount is None or unit not in UNITS:
        litres = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*l[ií]t", spec.strip())
        if litres:
            amount, unit = positive(litres[1].replace(",", ".")), "l"
    if amount is None or unit not in UNITS:
        return "", None, "Thiếu khối lượng hoặc dung tích hợp lệ"
    multiplier, output_unit = UNITS[unit]
    return output_unit, price * 100 / (amount * multiplier), ""


def quantile(sorted_values, fraction):
    position = (len(sorted_values) - 1) * fraction
    lower = math.floor(position)
    return sorted_values[lower] + (position - lower) * (
        sorted_values[math.ceil(position)] - sorted_values[lower]
    )


def run(source, output):
    final_output = output.with_name("survey_segment_final.csv")
    unclassified_output = output.with_name("survey_segment_unclassified.csv")
    if len({p.resolve() for p in (source, output, final_output, unclassified_output)}) != 4:
        raise ValueError("Đường dẫn file nguồn và ba file đầu ra phải khác nhau.")
    with source.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        original_fields = reader.fieldnames or []
        rows = list(reader)
    ids = [row["record_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("record_id bị trùng")
    categories = category_map()
    groups = defaultdict(list)
    prepared = []
    for row in rows:
        category = categories.get(row["record_id"], "")
        unit, value, note = compare_price(row, category) if category else (
            "", None, "Mã mới: cần bổ sung ánh xạ danh mục"
        )
        key = (category, unit)
        if value is not None:
            groups[key].append(value)
        prepared.append((row, key, value, note))
    thresholds = {}
    for key, values in groups.items():
        values.sort()
        if len(values) >= 3:
            thresholds[key] = quantile(values, 1 / 3), quantile(values, 2 / 3)

    output.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    with (output.open("w", encoding="utf-8-sig", newline="") as stream,
          final_output.open("w", encoding="utf-8-sig", newline="") as final_stream,
          unclassified_output.open("w", encoding="utf-8-sig", newline="") as unclassified_stream):
        writer = csv.DictWriter(stream, fieldnames=original_fields + FIELDS)
        final_writer = csv.DictWriter(final_stream, fieldnames=original_fields + FIELDS)
        unclassified_writer = csv.DictWriter(unclassified_stream, fieldnames=original_fields + FIELDS)
        for csv_writer in (writer, final_writer, unclassified_writer):
            csv_writer.writeheader()
        for row, key, value, note in prepared:
            n = len(groups[key]) if value is not None else None
            p33, p67 = thresholds.get(key, (None, None))
            tier = ""
            if value is not None:
                if n < 3:
                    note = "Nhóm dưới 3 mẫu hợp lệ"
                elif math.isclose(p33, p67, rel_tol=1e-12):
                    note = "P33 và P67 trùng nhau"
                else:
                    tier = "Thấp" if value <= p33 else "Trung bình" if value <= p67 else "Cao"
                    note = "Xếp theo P33/P67 của danh mục và đơn vị"
            counts[tier or note] += 1
            enriched = dict(row, category_clean=key[0], price_comparison_unit=key[1],
                                 price_normalized=value, group_valid_n=n, p33=p33, p67=p67,
                                 price_tier=tier, sample_flag="Ít mẫu" if n in (3, 4) else "",
                                 task4_note=note, price_display_group=(
                                     tier or ("Dưới 3 mẫu hợp lệ" if n is not None and n < 3
                                              else "Chưa xếp – lý do khác")
                                 ))
            writer.writerow(enriched)
            (final_writer if tier else unclassified_writer).writerow(enriched)
    print(f"Hoàn thành Task 4. Tổng số dòng: {len(rows)}")
    for label, count in counts.most_common():
        print(f"{label}: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Đường dẫn survey_clean.csv")
    parser.add_argument("output", type=Path, help="Đường dẫn survey_segment_All.csv")
    args = parser.parse_args()
    run(args.source, args.output)
