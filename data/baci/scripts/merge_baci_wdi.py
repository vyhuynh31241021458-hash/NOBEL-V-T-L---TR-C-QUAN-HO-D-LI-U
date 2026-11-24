
from pathlib import Path
import pandas as pd
import re

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data_raw"
CLEAN = BASE / "data_clean"

WDI_FILE = RAW / "world_bank_wdi_vietnam_2005_2024.csv"
BACI_FILE = CLEAN / "trade_year.csv"
OUTPUT = CLEAN / "baci_wdi_vietnam_2005_2024.csv"

INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_usd",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_pct",
    "BX.KLT.DINV.CD.WD": "fdi_inflows_usd",
    "TG.VAL.TOTL.GD.ZS": "merchandise_trade_gdp_pct",
    "TX.VAL.MRCH.CD.WT": "wdi_merchandise_exports_usd",
}

# 1. Doc 5 dong chi so WDI
# Bo qua cac dong metadata nam phia duoi
wdi = pd.read_csv(
    WDI_FILE,
    nrows=5,
    encoding="cp1252"
)

required = [
    "Country Code", "Series Code"
]

for col in required:
    if col not in wdi.columns:
        raise ValueError(f"Thieu cot WDI: {col}")

if not (wdi["Country Code"] == "VNM").all():
    raise ValueError("File WDI khong chi chua Viet Nam.")

if set(wdi["Series Code"]) != set(INDICATORS):
    raise ValueError("Danh sach chi so WDI khong khop.")

# 2. Chuyen cot nam thanh dong
year_cols = [
    col for col in wdi.columns
    if re.fullmatch(r"20\d{2} \[YR20\d{2}\]", col)
]

wdi_long = wdi.melt(
    id_vars=["Country Code", "Series Code"],
    value_vars=year_cols,
    var_name="year_label",
    value_name="value"
)

wdi_long["year"] = (
    wdi_long["year_label"]
    .str.extract(r"^(\d{4})")[0]
    .astype(int)
)

wdi_long["value"] = pd.to_numeric(
    wdi_long["value"].replace("..", pd.NA),
    errors="coerce"
)

wdi_long["indicator"] = (
    wdi_long["Series Code"].map(INDICATORS)
)

wdi_clean = wdi_long.pivot(
    index=["Country Code", "year"],
    columns="indicator",
    values="value"
).reset_index()

wdi_clean.columns.name = None

wdi_clean = wdi_clean.rename(
    columns={"Country Code": "country_iso3"}
)

wdi_clean = wdi_clean[
    (wdi_clean["year"] >= 2005)
    & (wdi_clean["year"] <= 2024)
].sort_values("year")

wdi_clean.to_csv(
    CLEAN / "wdi_vietnam_clean.csv",
    index=False,
    encoding="cp1252"
)

# 3. Doc BACI
baci = pd.read_csv(BACI_FILE)

# 4. Ghep theo nam va ma quoc gia
merged = baci.merge(
    wdi_clean,
    on=["year", "country_iso3"],
    how="left",
    validate="one_to_one",
    indicator=True
)

# 5. Tao chi so bo sung
merged["baci_exports_to_gdp_pct"] = (
    merged["export_usd"]
    / merged["gdp_usd"] * 100
)

merged["baci_total_trade_to_gdp_pct"] = (
    merged["total_trade_usd"]
    / merged["gdp_usd"] * 100
)

merged["baci_vs_wdi_exports_pct_diff"] = (
    (
        merged["export_usd"]
        - merged["wdi_merchandise_exports_usd"]
    )
    / merged["wdi_merchandise_exports_usd"]
    * 100
)

# 6. Kiem tra
assert len(merged) == 20, "Khong du 20 nam!"
assert (merged["_merge"] == "both").all(), \
    "Co nam BACI khong ghep duoc WDI!"

print("\nSO GIA TRI WDI THIEU:")
print(
    merged[list(INDICATORS.values())]
    .isna().sum()
)

print("\nKET QUA GHEP:")
print(
    merged[
        [
            "year",
            "export_usd",
            "import_usd",
            "gdp_usd",
            "fdi_inflows_usd",
            "baci_vs_wdi_exports_pct_diff"
        ]
    ].to_string(index=False)
)

merged.drop(columns=["_merge"]).to_csv(
    OUTPUT,
    index=False,
    encoding="cp1252"
)

print("\nDA LUU:", OUTPUT)
print("HOAN THANH!")
