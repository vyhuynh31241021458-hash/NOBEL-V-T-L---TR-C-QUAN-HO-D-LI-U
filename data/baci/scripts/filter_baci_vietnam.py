
from pathlib import Path
import csv
import pandas as pd

# =====================================================
# 1. THIET LAP DUONG DAN
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_DIR / "data_raw"
OUTPUT_DIR = PROJECT_DIR / "data_filtered"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

START_YEAR = 2005
END_YEAR = 2024
CHUNK_SIZE = 100_000

# =====================================================
# 2. TIM MA QUOC GIA VIET NAM
# =====================================================

country_file = RAW_DIR / "country_codes_V202601.csv"

if not country_file.exists():
    raise FileNotFoundError(
        f"Khong tim thay file: {country_file}"
    )

countries = pd.read_csv(
    country_file,
    dtype=str,
    encoding="utf-8-sig"
)

countries.columns = countries.columns.str.strip()

print("Cac cot trong country_codes:")
print(countries.columns.tolist())

# BACI su dung ma quoc gia so, Viet Nam co ma 704.
# Xac minh ma 704 trong bang country_codes truoc khi loc.

code_candidates = [
    c for c in countries.columns
    if c.lower() in ("country_code", "code", "iso3", "iso3num")
]

if not code_candidates:
    print(countries.head(10).to_string(index=False))
    raise ValueError(
        "Chua nhan dien duoc cot ma quoc gia. "
        "Hay kiem tra country_codes."
    )

code_col = code_candidates[0]

vietnam_rows = countries[
    countries[code_col].astype(str).str.strip().isin(
        ["704", "VNM"]
    )
]

print("\nDong thong tin Viet Nam:")
print(vietnam_rows.to_string(index=False))

if vietnam_rows.empty:
    raise ValueError(
        "Khong tim thay Viet Nam trong bang ma quoc gia."
    )

VN_CODE = "704"

# =====================================================
# 3. KHAI BAO KIEU DU LIEU
# =====================================================

DTYPES = {
    "t": "int32",
    "i": "string",
    "j": "string",
    "k": "string",
    "v": "float64",
    "q": "float64",
}

OUTPUT_COLUMNS = [
    "year",
    "exporter_code",
    "importer_code",
    "hs6",
    "trade_value_1000usd",
    "quantity_tonnes",
    "trade_flow",
    "partner_code",
]

MASTER_FILE = OUTPUT_DIR / "vietnam_trade_2005_2024.csv"
SUMMARY_FILE = OUTPUT_DIR / "filter_summary.csv"

if MASTER_FILE.exists():
    MASTER_FILE.unlink()

summary = []

# =====================================================
# 4. DOC VA LOC TUNG NAM
# =====================================================

for year in range(START_YEAR, END_YEAR + 1):

    filename = f"BACI_HS02_Y{year}_V202601.csv"
    input_file = RAW_DIR / filename

    if not input_file.exists():
        raise FileNotFoundError(
            f"Thieu file nam {year}: {input_file}"
        )

    output_file = (
        OUTPUT_DIR / f"vietnam_trade_{year}.csv"
    )

    if output_file.exists():
        output_file.unlink()

    total_rows = 0
    kept_rows = 0
    first_chunk = True

    print(f"\nDang xu ly nam {year}...")

    reader = pd.read_csv(
        input_file,
        dtype=DTYPES,
        chunksize=CHUNK_SIZE,
        keep_default_na=True,
    )

    for chunk in reader:

        total_rows += len(chunk)

        # Chuan hoa ma quoc gia thanh chuoi
        chunk["i"] = chunk["i"].str.strip()
        chunk["j"] = chunk["j"].str.strip()

        # Giu cac dong Viet Nam xuat hoac nhap
        filtered = chunk[
            (chunk["i"] == VN_CODE) |
            (chunk["j"] == VN_CODE)
        ].copy()

        if filtered.empty:
            continue

        # Bo giao dich Viet Nam -> Viet Nam neu co
        filtered = filtered[
            ~(
                (filtered["i"] == VN_CODE) &
                (filtered["j"] == VN_CODE)
            )
        ].copy()

        if filtered.empty:
            continue

        filtered["k"] = filtered["k"].str.zfill(6)

        filtered["trade_flow"] = (
            "Export"
        )

        filtered.loc[
            filtered["j"] == VN_CODE,
            "trade_flow"
        ] = "Import"

        filtered["partner_code"] = (
            filtered["j"]
        )

        filtered.loc[
            filtered["trade_flow"] == "Import",
            "partner_code"
        ] = filtered["i"]

        filtered = filtered.rename(
            columns={
                "t": "year",
                "i": "exporter_code",
                "j": "importer_code",
                "k": "hs6",
                "v": "trade_value_1000usd",
                "q": "quantity_tonnes",
            }
        )

        filtered = filtered[OUTPUT_COLUMNS]

        filtered.to_csv(
            output_file,
            mode="a",
            index=False,
            header=first_chunk,
            encoding="utf-8-sig",
        )

        filtered.to_csv(
            MASTER_FILE,
            mode="a",
            index=False,
            header=not MASTER_FILE.exists(),
            encoding="utf-8-sig",
        )

        first_chunk = False
        kept_rows += len(filtered)

    summary.append({
        "year": year,
        "original_rows": total_rows,
        "vietnam_rows": kept_rows,
        "retention_pct": (
            round(100 * kept_rows / total_rows, 4)
            if total_rows else 0
        ),
    })

    print(
        f"Nam {year}: "
        f"{total_rows:,} dong goc -> "
        f"{kept_rows:,} dong Viet Nam"
    )

# =====================================================
# 5. XUAT BANG THONG KE
# =====================================================

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    SUMMARY_FILE,
    index=False,
    encoding="utf-8-sig",
)

print("\n========== HOAN THANH ==========")
print(summary_df.to_string(index=False))
print(f"\nThu muc ket qua: {OUTPUT_DIR}")
print(f"File tong hop: {MASTER_FILE.name}")
print(f"File thong ke: {SUMMARY_FILE.name}")
