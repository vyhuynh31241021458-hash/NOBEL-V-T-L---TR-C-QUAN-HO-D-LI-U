"""Task 1. Làm sạch dữ liệu khảo sát P03."""
import re
from datetime import datetime
from html import unescape
from pathlib import Path

import pandas as pd

SOURCE = {
    "Mã sản phẩm": "record_id", "Siêu thị": "store",
    "Ngày khảo sát": "date_raw", "Tên sản phẩm": "product_name_raw",
    "Thông tin chi tiết": "spec_raw", "Thương hiệu": "brand_raw",
    "Giá (VNĐ)": "price_raw", "Xuất xứ nguyên văn trên nhãn": "origin_raw",
    "Giờ khảo sát": "time_raw",
}
COUNTRIES = {
    "Việt Nam": ("vn", "vietnam"), "Trung Quốc": ("tq", "china"),
    "Thái Lan": ("tl", "thailand"), "Nhật Bản": ("japan",),
    "Hàn Quốc": ("hàn", "korea", "seul korea"),
    "Campuchia": ("cambodia",), "Singapore": ("singapor",),
    **{country: () for country in (
        "Indonesia", "Đài Loan", "Ý", "Malaysia", "Ba Lan", "Mỹ", "Canada",
        "Bỉ", "Pháp", "Úc", "Thổ Nhĩ Kỳ",
    )},
}
ALIASES = {alias.casefold(): country for country, aliases in COUNTRIES.items()
           for alias in (country, *aliases)}
# Carry forward review flags from the survey review, keyed by current record ID.
REVIEW = {
    **{key: "price" for key in (
        "AEON_026", "AEON_112", "AEON_113", "AEON_114", "AEON_116",
        "AEON_118", "AEON_119", "AEON_123", "GO_192",
    )},
    "GO_147": "origin", "GO_203": "spec", "GO_209": "origin",
    "GO_210": "origin", "AEON_186": "origin",
}

def text(value):
    value = re.sub(r"<br\s*/?>", " ", unescape(value), flags=re.I)
    return " ".join(value.replace(r"\t", " ").replace(r"\n", " ").split())

def origin_parts(value):
    value = text(value).casefold()
    brand, country = "", value
    match = re.search(r"(?:sản xuất|\bsx\b|made in)\s*(?:(?:tại|tai)\s+)?(.+)", value)
    if match:
        country = re.split(r"[,;]|\bnhập khẩu\b|\bchịu\b", match[1])[0].strip()
        if value.startswith("xuất xứ thương hiệu"):
            brand_text = value[len("xuất xứ thương hiệu"):match.start()].strip(" ,;:")
            brand = ALIASES.get(brand_text, "")
    else:
        country = re.sub(r"^xuất xứ\s*:?\s*", "", country)
        country = re.split(r"\bcấp phép\b", country)[0].strip()
    return ALIASES.get(country, ""), brand

def parse_price(value):
    clean = re.sub(r"\s|vnđ|vnd|đ|₫", "", value, flags=re.I)
    if re.fullmatch(r"\d+|\d{1,3}(?:[.,]\d{3})+", clean):
        price = int(re.sub(r"[.,]", "", clean))
        return price if price > 0 else None
    return None

def parse_time(value):
    match = re.fullmatch(r"(\d{1,2})\s*[:hn]\s*(\d{1,2})(?::\d{2})?", text(value), re.I)
    if match and int(match[1]) < 24 and int(match[2]) < 60:
        return f"{int(match[1]):02}:{int(match[2]):02}"
    return ""

def parse_spec(value):
    # Keep ambiguous or missing units blank rather than assume a weight.
    amount = re.search(r"(?:(\d+)\s*[×x]\s*)?(\d+(?:[,.]\d+)?)\s*(ml|kg|g|l)\b", value, re.I)
    if amount:
        count, quantity, unit = amount.groups()
        total = int(count or 1) * float(quantity.replace(",", "."))
        return f"{total:g} {unit.lower()}", total, unit.lower(), "dung tích/khối lượng"
    return value, None, "", "mô tả" if value else ""

def clean_survey(input_csv, output_dir="data_clean", notes_dir=None):
    raw = pd.read_csv(input_csv, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    raw.columns = raw.columns.str.strip()
    stt = "STT" if "STT" in raw.columns else "0"
    missing = set([*SOURCE, stt]) - set(raw.columns)
    if missing:
        raise ValueError(f"Thiếu cột đầu vào: {sorted(missing)}")
    data = raw[[stt, *SOURCE]].rename(columns={stt: "stt_goc", **SOURCE})
    data["record_id"] = data.record_id.str.strip().str.upper()
    invalid = ~data.record_id.str.fullmatch(r"(GO|AEON)_\d{3}")
    duplicate = data.record_id.duplicated(keep=False)
    if invalid.any() or duplicate.any():
        raise ValueError(f"Mã sai định dạng hoặc trùng: {data.loc[invalid | duplicate, 'record_id'].tolist()}")
    repeated_stt = data.stt_goc.ne("") & data.stt_goc.duplicated(keep=False)
    rows, audit = [], []
    for index, row in enumerate(data.to_dict("records")):
        key = row["record_id"]
        name = text(row["product_name_raw"])
        spec = text(row["spec_raw"])
        brand = text(row["brand_raw"])
        if brand.casefold() in {"n/a", "na", "-"}:
            brand = ""
        price = parse_price(row["price_raw"])
        time = parse_time(row["time_raw"])
        country, brand_country = origin_parts(row["origin_raw"])
        spec_std, value, unit, spec_type = parse_spec(spec)
        try:
            date = datetime.strptime(text(row["date_raw"]), "%d/%m/%Y").date().isoformat()
        except ValueError:
            date = ""
        fields = {REVIEW[key]} if key in REVIEW else set()
        for field, val in {"price":price, "origin":country, "date":date, "store":text(row["store"]),
                           "product_name":name}.items():
            if not val:
                fields.add(field)
        if row["time_raw"].strip() and not time:
            fields.add("time")
        for field, val in {"survey_time": time, "spec_text": spec, "brand": brand}.items():
            if not val:
                audit.append((key, "Thiếu dữ liệu", field, "Để trống"))
        if repeated_stt.iloc[index]:
            audit.append((key, "STT trùng", row["stt_goc"], "Giữ STT gốc, ghép bằng record_id"))
        if row["store"].strip() in {"GO! Tô Hiến Thành", "AEON Tạ Quang Bửu"} and time:
            audit.append((key, "Giờ ước tính", time, "Giờ phân bổ theo khung khảo sát"))
        for field in sorted(fields):
            audit.append((key, "Cần xác minh", field, "Đối chiếu bảng gốc hoặc nhãn"))
        rows.append({
            "record_id": key, "stt_goc": row["stt_goc"], "store": text(row["store"]),
            "survey_date": date, "survey_time": time, "product_name": name,
            "brand": brand, "spec_text": spec, "spec_std": spec_std, "spec_value": value,
            "spec_unit": unit, "spec_type": spec_type, "price_vnd": price,
            "origin_country": country, "brand_origin": brand_country,
            "made_in_vietnam": (country == "Việt Nam") if country else pd.NA,
            "origin_note": "Theo bảng gốc, cần đối chiếu" if "origin" in fields else "",
            "verify_status": "Cần xác minh" if fields else "OK",
            "verify_fields": ", ".join(sorted(fields)),
            **{col: row[col] for col in (
                "brand_raw", "price_raw", "spec_raw", "origin_raw", "date_raw", "time_raw"
            )}, "source_row": index + 2,
        })
    clean = pd.DataFrame(rows)
    clean["price_vnd"] = clean.price_vnd.astype("Int64")
    audit_table = pd.DataFrame(audit, columns=["record_id", "van_de", "gia_tri", "xu_ly"])
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output / "t01_survey_clean.csv", index=False, encoding="utf-8-sig")
    notes = Path(notes_dir) if notes_dir is not None else output.parent / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    audit_table.to_csv(notes / "t01_issues_log.csv", index=False, encoding="utf-8-sig")
    pending = clean.verify_status.eq("Cần xác minh").sum()
    print(f"Đầu vào: {len(raw)} | Đầu ra: {len(clean)} | Cần xác minh: {pending}")
    print(clean.groupby("store").size().to_string())
    return clean, audit_table

