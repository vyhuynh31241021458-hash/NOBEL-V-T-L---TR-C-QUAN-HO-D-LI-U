"""
TASK 1 - LÀM SẠCH DỮ LIỆU KHẢO SÁT (350 sản phẩm tại AEON Bình Tân và GO! An Lạc)

Cách chạy (từ thư mục gốc của repo):
    python "P03 Survey/scripts/task1_clean.py"

Đầu vào : P03 Survey/data_raw/survey_350.csv        (KHÔNG sửa file này)
Đầu ra  : P03 Survey/data_clean/survey_clean.csv      (bảng sạch)
          P03 Survey/data_clean/task1_issues_log.csv  (nhật ký lỗi + cách xử lý)

Ý nghĩa cột origin_country: NƠI SẢN XUẤT ("Made in"), không phải quốc gia của thương hiệu.
Nếu nhãn ghi riêng xuất xứ thương hiệu thì lưu ở cột brand_origin.
"""
import re
import unicodedata
from pathlib import Path

import pandas as pd

# ----------------------------------------------------------------------
# 1. CẤU HÌNH
# ----------------------------------------------------------------------
BASE = Path(__file__).resolve().parents[1]          # thư mục "P03 Survey"
RAW = BASE / "data_raw" / "survey_350.csv"
OUT = BASE / "data_clean" / "survey_clean.csv"
LOG = BASE / "data_clean" / "task1_issues_log.csv"

COLS = {                       # vai trò -> tên cột thật trong file CSV
    "stt": "STT",
    "id": "Mã sản phẩm",
    "store": "Siêu thị",
    "date": "Ngày khảo sát",
    "time": "Giờ khảo sát",
    "name": "Tên sản phẩm",
    "spec": "Thông tin chi tiết",
    "brand": "Thương hiệu",
    "price": "Giá (VNĐ)",
    "origin": "Xuất xứ nguyên văn trên nhãn",
}
REQUIRED = ["id", "name", "price", "origin", "date", "store"]

DATE_RANGE = None            # ví dụ ("2026-11-01", "2026-11-30") để bắt ngày gõ nhầm
PRICE_MIN, PRICE_MAX = 1_000, 10_000_000
HIGH_PRICE_RATIO = 10        # giá > 10 lần giá giữa của cả bảng thì nhắc kiểm tra lại

# ----------------------------------------------------------------------
# 2. BẢNG QUY ĐỔI QUỐC GIA (khóa: viết thường, không dấu)
# ----------------------------------------------------------------------
COUNTRY = {
    "viet nam": "Việt Nam", "vn": "Việt Nam", "vietnam": "Việt Nam",
    "thai lan": "Thái Lan", "thailand": "Thái Lan", "thai": "Thái Lan", "tl": "Thái Lan",
    "trung quoc": "Trung Quốc", "china": "Trung Quốc", "prc": "Trung Quốc", "tq": "Trung Quốc",
    "han quoc": "Hàn Quốc", "han": "Hàn Quốc", "korea": "Hàn Quốc",
    "south korea": "Hàn Quốc", "seul korea": "Hàn Quốc",
    "nhat ban": "Nhật Bản", "nhat": "Nhật Bản", "japan": "Nhật Bản",
    "malaysia": "Malaysia", "indonesia": "Indonesia",
    "singapore": "Singapore", "singapor": "Singapore",
    "my": "Mỹ", "usa": "Mỹ", "us": "Mỹ", "united states": "Mỹ",
    "dai loan": "Đài Loan", "taiwan": "Đài Loan",
    "phap": "Pháp", "france": "Pháp", "duc": "Đức", "germany": "Đức",
    "y": "Ý", "italy": "Ý", "uc": "Úc", "australia": "Úc",
    "anh": "Anh", "uk": "Anh", "philippines": "Philippines",
    "an do": "Ấn Độ", "india": "Ấn Độ", "new zealand": "New Zealand",
    "ha lan": "Hà Lan", "thuy si": "Thụy Sĩ", "tay ban nha": "Tây Ban Nha",
    "campuchia": "Campuchia", "cambodia": "Campuchia", "canada": "Canada",
    "bi": "Bỉ", "ba lan": "Ba Lan", "tho nhi ky": "Thổ Nhĩ Kỳ",
    "hong kong": "Hồng Kông",
}
PREFIX = re.compile(r"^(?:made in|san xuat tai|san xuat|sx tai|sx|xuat xu)\s*[:\-]?\s*")

UNIT_MAP = {"kg": "kg", "g": "g", "gr": "g", "gam": "g", "gram": "g",
            "ml": "ml", "l": "l", "lit": "l", "lít": "l"}
# Số + đơn vị khối lượng/dung tích. Bỏ qua dạng khoảng như "20-80g" (định lượng giấy).
SPEC_RE = re.compile(
    r"(?<![\d.,\-])(?:(\d+)\s*[x×*]\s*)?(\d+(?:[.,]\d+)?)\s*(kg|gram|gam|gr|ml|lít|lit|g|l)\b",
    re.I)
PRICE_OK = re.compile(r"\d{1,3}(?:[. ]\d{3})*")      # 7.000 | 319 000 | 7.844.700

# ----------------------------------------------------------------------
# 3. HÀM HỖ TRỢ
# ----------------------------------------------------------------------
issues = []


def log(rid, field, raw, problem, action, status="Đã sửa"):
    """status: 'Đã sửa' | 'Cần xác minh' | 'Ghi chú'"""
    issues.append({"record_id": rid, "field": field, "raw_value": raw,
                   "problem": problem, "action": action, "status": status})


def clean_text(x):
    x = "" if x is None or (isinstance(x, float) and pd.isna(x)) else str(x)
    x = unicodedata.normalize("NFC", x)
    return re.sub(r"\s+", " ", x).strip()


def strip_accents(s):
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def norm_key(s):
    return strip_accents(clean_text(s)).lower().strip(" .,;")


def find_country(text):
    """Tìm quốc gia trong một đoạn chữ ngắn (thử cả cụm, rồi từng cụm con)."""
    k = norm_key(text)
    if k in COUNTRY:
        return COUNTRY[k]
    words = k.split()
    for n in (3, 2, 1):                       # ưu tiên cụm dài ("thai lan", "new zealand")
        for i in range(len(words) - n + 1):
            g = " ".join(words[i:i + n])
            if g in COUNTRY:
                return COUNTRY[g]
    return None


def parse_price(raw):
    s = clean_text(raw).lower()
    if not s:
        return None, "missing"
    if not PRICE_OK.fullmatch(s):             # ví dụ "233 00" -> không biết là 23.300 hay 233.000
        return None, "malformed"
    return int(re.sub(r"\D", "", s)), ("spaces" if " " in s else "ok")


def parse_origin(raw):
    """Trả về (nơi sản xuất, xuất xứ thương hiệu, trạng thái, ghi chú)."""
    s = clean_text(raw)
    if not s:
        return "", "", "missing", ""
    key = norm_key(s)
    k = PREFIX.sub("", key).strip()
    if k in COUNTRY:                                          # trường hợp đơn giản
        return COUNTRY[k], "", "ok", ""
    made = brand = None                                       # trường hợp có nhiều thông tin
    m = re.search(r"thuong hieu\s+(.+?)(?=\s*,?\s*(?:san xuat|sx)\b|$)", key)
    if m:
        brand = find_country(m.group(1))
    m = re.search(r"(?:san xuat|sx)\s*(?:tai\s+)?(.+?)(?=\s+(?:nhap khau|chiu|cap phep)|,|$)", key)
    if m:
        made = find_country(m.group(1))
    if "cap phep" in key:                                     # "VN cấp phép TL": chưa rõ nơi sản xuất
        first = find_country(key.split("cap phep")[0])
        return (first or ""), "", "verify", "Nhãn ghi 'cấp phép' - chưa rõ nơi sản xuất thật"
    if made:
        note = ""
        if brand and brand != made:
            note = f"Thương hiệu thuộc {brand}, sản xuất tại {made}"
        elif brand:
            note = f"Thương hiệu thuộc {brand}"
        return made, (brand or ""), "complex", note
    return s, "", "verify", "Không tách được nơi sản xuất"


def parse_spec(raw):
    s = clean_text(raw)
    if not s:
        return "", "", None, "", ""
    m = SPEC_RE.search(s)
    if m:
        count, val, unit = m.group(1), float(m.group(2).replace(",", ".")), m.group(3).lower()
        unit = UNIT_MAP.get(unit, unit)
        std = f"{count}x{val:g} {unit}" if count else f"{val:g} {unit}"
        return s, std, val, unit, "dung tích/khối lượng"
    kind = "kích cỡ (size)" if s.lower().startswith("size") else "mô tả khác"
    return s, "", None, "", kind


def parse_time(raw):
    s = clean_text(raw).lower()
    if not s:
        return ""
    m = re.fullmatch(r"(\d{1,2})\s*[h:n]\s*(\d{1,2})(?::\d{2})?", s)   # 'n' = gõ nhầm chữ h
    return f"{int(m.group(1)):02d}:{int(m.group(2)):02d}" if m else None


# ----------------------------------------------------------------------
# 4. ĐỌC DỮ LIỆU
# ----------------------------------------------------------------------
raw = pd.read_csv(RAW, dtype=str, keep_default_na=False, encoding="utf-8-sig")
n_before = len(raw)
print(f"Số dòng ban đầu: {n_before}")

absent = [COLS[k] for k in REQUIRED if COLS[k] not in raw.columns]
if absent:
    raise SystemExit(f"Không thấy cột: {absent}\nCác cột hiện có: {list(raw.columns)}\n"
                     "Hãy sửa dict COLS cho khớp.")


def col(key):
    c = COLS.get(key)
    return c if c in raw.columns else None


raw["source_row"] = raw.index + 2           # số dòng trong Google Sheet (dòng 1 = tiêu đề)

# ----------------------------------------------------------------------
# 5. DÒNG TRÙNG HOÀN TOÀN (bỏ qua STT, mã, giờ khi so sánh)
# ----------------------------------------------------------------------
skip = {col("stt"), col("id"), col("time"), "source_row"}
cmp_cols = [c for c in raw.columns if c not in skip]
norm = raw[cmp_cols].apply(lambda s: s.map(clean_text).str.lower())
dup = norm.duplicated(keep="first")
for _, r in raw[dup].iterrows():
    log(r[COLS["id"]], "(cả dòng)", "", "Trùng hoàn toàn với dòng trước", "Đã xóa dòng trùng")
raw = raw[~dup].copy()

# ----------------------------------------------------------------------
# 6. record_id: dùng lại mã sản phẩm có sẵn nếu hợp lệ
# ----------------------------------------------------------------------
ids = raw[COLS["id"]].map(clean_text)
if ids.ne("").all() and ids.is_unique:
    raw["record_id"] = ids
    print("Mã sản phẩm đầy đủ và không trùng -> dùng làm record_id (giữ nguyên).")
else:
    bad = ids[(ids == "") | ids.duplicated(keep=False)]
    for i, v in bad.items():
        log(f"dòng {raw.at[i, 'source_row']}", "record_id", v, "Mã thiếu hoặc trùng",
            "Tạo mã mới SPxxx", "Cần xác minh")
    raw["record_id"] = raw["source_row"].map(lambda n: f"SP{n - 1:03d}")

# ----------------------------------------------------------------------
# 7. THƯƠNG HIỆU: gom các cách viết hoa/thường khác nhau về một dạng
# ----------------------------------------------------------------------
bcol = col("brand")
brand_canon = {}
if bcol:
    b = raw[bcol].map(clean_text)
    for key, grp in b[b != ""].groupby(b[b != ""].str.lower()):
        brand_canon[key] = grp.value_counts().index[0]      # dạng xuất hiện nhiều nhất

# ----------------------------------------------------------------------
# 8. LÀM SẠCH TỪNG DÒNG
# ----------------------------------------------------------------------
rows = []
for _, r in raw.iterrows():
    rid = r["record_id"]
    o = {"record_id": rid}
    o["stt_goc"] = r[col("stt")] if col("stt") else ""
    o["store"] = clean_text(r[COLS["store"]])
    o["product_name"] = clean_text(r[COLS["name"]])
    if not o["store"]:
        log(rid, "store", "", "Thiếu tên siêu thị", "Để trống", "Cần xác minh")
    if not o["product_name"]:
        log(rid, "product_name", "", "Thiếu tên sản phẩm", "Để trống", "Cần xác minh")

    # thương hiệu
    if bcol:
        b_raw = r[bcol]
        b_clean = clean_text(b_raw)
        if not b_clean:
            log(rid, "brand", "", "Thiếu thương hiệu (có thể sản phẩm không có hãng)",
                "Để trống, cần xem lại nhãn", "Cần xác minh")
        else:
            canon = brand_canon[b_clean.lower()]
            if canon != b_clean:
                log(rid, "brand", b_raw, "Cùng thương hiệu nhưng viết hoa/thường khác nhau",
                    f"Thống nhất thành '{canon}'")
            b_clean = canon
        o["brand"], o["brand_raw"] = b_clean, b_raw

    # giá
    p_raw = r[COLS["price"]]
    price, st = parse_price(p_raw)
    o["price_raw"], o["price_vnd"] = p_raw, price
    if st == "missing":
        log(rid, "price", p_raw, "Thiếu giá", "Để trống", "Cần xác minh")
    elif st == "malformed":
        log(rid, "price", p_raw, "Giá sai định dạng, không rõ bao nhiêu số 0",
            "Để trống giá, KHÔNG đoán - cần xem lại nhãn giá", "Cần xác minh")
    elif st == "spaces":
        log(rid, "price", p_raw, "Giá viết cách bằng dấu cách thay vì dấu chấm",
            f"Chuẩn hóa thành {price}")
    if price is not None and not (PRICE_MIN <= price <= PRICE_MAX):
        log(rid, "price", p_raw, f"Giá ngoài khoảng {PRICE_MIN:,}-{PRICE_MAX:,} VNĐ",
            "Giữ nguyên, cần kiểm tra", "Cần xác minh")

    # xuất xứ
    ox_raw = r[COLS["origin"]]
    made, brand_o, st, note = parse_origin(ox_raw)
    o.update({"origin_raw": ox_raw, "origin_country": made, "brand_origin": brand_o,
              "origin_note": note})
    if st == "missing":
        o["origin_country"] = "Không rõ"
        log(rid, "origin", ox_raw, "Thiếu xuất xứ", "Ghi 'Không rõ'", "Cần xác minh")
    elif st == "verify":
        log(rid, "origin", ox_raw, note, f"Tạm ghi '{made}', cần xác minh", "Cần xác minh")
    elif st == "complex":
        log(rid, "origin", ox_raw, "Nhãn ghi gộp nhiều thông tin (thương hiệu / nơi sản xuất)",
            f"Tách: nơi sản xuất = {made}" + (f"; thương hiệu = {brand_o}" if brand_o else ""))
    elif clean_text(ox_raw) != made:
        log(rid, "origin", ox_raw, "Cách viết xuất xứ không thống nhất (viết tắt/sai chính tả)",
            f"Chuẩn hóa thành '{made}'")
    o["made_in_vietnam"] = "" if o["origin_country"] in ("", "Không rõ") else \
        ("Có" if o["origin_country"] == "Việt Nam" else "Không")

    # quy cách / thông tin chi tiết
    if col("spec"):
        s_raw = r[COLS["spec"]]
        text, std, val, unit, kind = parse_spec(s_raw)
        o.update({"spec_raw": s_raw, "spec_text": text, "spec_std": std,
                  "spec_value": val, "spec_unit": unit, "spec_type": kind})
        if not text:
            log(rid, "spec", "", "Thiếu thông tin chi tiết", "Để trống", "Ghi chú")

    # ngày + giờ
    d_raw = r[COLS["date"]]
    d = pd.to_datetime(clean_text(d_raw), dayfirst=True, errors="coerce") if clean_text(d_raw) else pd.NaT
    o["date_raw"] = d_raw
    if pd.isna(d):
        o["survey_date"] = ""
        log(rid, "date", d_raw, "Thiếu hoặc sai định dạng ngày", "Để trống", "Cần xác minh")
    else:
        o["survey_date"] = d.strftime("%Y-%m-%d")
        if DATE_RANGE and not (pd.Timestamp(DATE_RANGE[0]) <= d <= pd.Timestamp(DATE_RANGE[1])):
            log(rid, "date", d_raw, "Ngày ngoài khoảng khảo sát", "Giữ nguyên", "Cần xác minh")
    if col("time"):
        t_raw = r[COLS["time"]]
        t = parse_time(t_raw)
        o["time_raw"] = t_raw
        if t == "":
            o["survey_time"] = ""
            log(rid, "time", "", "Thiếu giờ khảo sát", "Để trống", "Ghi chú")
        elif t is None:
            o["survey_time"] = ""
            log(rid, "time", t_raw, "Giờ sai định dạng", "Để trống", "Cần xác minh")
        else:
            o["survey_time"] = t
            if t_raw.strip() != t:
                log(rid, "time", t_raw, "Giờ viết dạng '9h10' hoặc thiếu số 0 / gõ nhầm chữ",
                    f"Chuẩn hóa thành {t}")

    o["source_row"] = r["source_row"]
    rows.append(o)

df = pd.DataFrame(rows)

# ----------------------------------------------------------------------
# 9. GIÁ CAO BẤT THƯỜNG + NGHI TRÙNG (chỉ đánh dấu, không xóa)
# ----------------------------------------------------------------------
df["price_vnd"] = pd.to_numeric(df["price_vnd"], errors="coerce")
median_all = df["price_vnd"].median()
for _, r in df[df["price_vnd"] > median_all * HIGH_PRICE_RATIO].iterrows():
    log(r["record_id"], "price", int(r["price_vnd"]),
        f"Giá cao hơn {HIGH_PRICE_RATIO} lần giá giữa của cả bảng ({int(median_all):,} VNĐ)",
        "Giữ nguyên, đối chiếu ảnh nhãn giá (có thể đúng nếu là đồ điện tử/mỹ phẩm cao cấp)",
        "Cần xác minh")

key = [c for c in ["store", "product_name", "brand", "spec_text", "price_vnd"] if c in df.columns]
for i in df[df.duplicated(subset=key, keep=False)].index:
    log(df.at[i, "record_id"], "(cả dòng)", "", "Nghi trùng (cùng siêu thị, tên, hãng, quy cách, giá)",
        "Giữ lại, cần xác nhận", "Cần xác minh")

# ----------------------------------------------------------------------
# 10. GẮN TRẠNG THÁI + XUẤT FILE
# ----------------------------------------------------------------------
log_df = pd.DataFrame(issues, columns=["record_id", "field", "raw_value", "problem",
                                       "action", "status"])
flag = log_df[log_df["status"] == "Cần xác minh"].groupby("record_id")["field"] \
    .agg(lambda s: ";".join(sorted(set(s))))
df["verify_fields"] = df["record_id"].map(flag).fillna("")
df["verify_status"] = df["verify_fields"].map(lambda x: "Cần xác minh" if x else "OK")

order = ["record_id", "stt_goc", "store", "survey_date", "survey_time", "product_name",
         "brand", "spec_text", "spec_std", "spec_value", "spec_unit", "spec_type",
         "price_vnd", "origin_country", "brand_origin", "made_in_vietnam", "origin_note",
         "verify_status", "verify_fields",
         "brand_raw", "price_raw", "spec_raw", "origin_raw", "date_raw", "time_raw", "source_row"]
df = df[[c for c in order if c in df.columns]]
assert df["record_id"].is_unique, "record_id bị trùng!"

OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT, index=False, encoding="utf-8-sig")
log_df.to_csv(LOG, index=False, encoding="utf-8-sig")

# ----------------------------------------------------------------------
# 11. BÁO CÁO NHANH
# ----------------------------------------------------------------------
print("\n===== KẾT QUẢ =====")
print(f"Trước xử lý : {n_before} dòng")
print(f"Sau xử lý   : {len(df)} dòng (xóa {n_before - len(df)} dòng trùng hoàn toàn)")
print(f"Cần xác minh: {(df['verify_status'] == 'Cần xác minh').sum()} dòng")
print("\nSố mục nhật ký theo loại:")
print(log_df.groupby(["status", "field"]).size().to_string())
print("\nNơi sản xuất sau chuẩn hóa:")
print(df["origin_country"].value_counts().to_string())
if "spec_type" in df:
    print("\nLoại 'thông tin chi tiết':")
    print(df["spec_type"].replace("", "(trống)").value_counts().to_string())
print(f"\nĐã lưu: {OUT}\nĐã lưu: {LOG}")
