
from pathlib import Path
import pandas as pd
import numpy as np

# ==========================================
# P03 - VERIFY BACI 2024
# Verify raw trade data and partner codes
# ==========================================

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data_raw"
CLEAN = BASE / "data_clean"
OUT = BASE / "audit_results"

OUT.mkdir(exist_ok=True)

RAW_FILE = RAW / "BACI_HS02_Y2024_V202601.csv"
COUNTRY_FILE = RAW / "country_codes_V202601.csv"
TRADE_FILE = CLEAN / "trade_year.csv"
PARTNER_FILE = CLEAN / "partner_year.csv"

VIETNAM_CODE = 704
YEAR = 2024

print("=" * 65)
print("P03 - VERIFY BACI 2024")
print("=" * 65)

# ------------------------------------------
# 1. Check files
# ------------------------------------------

for file in [
    RAW_FILE, COUNTRY_FILE,
    TRADE_FILE, PARTNER_FILE
]:
    if not file.exists():
        raise FileNotFoundError(
            f"Cannot find file: {file}"
        )

# ------------------------------------------
# 2. Read raw BACI
# ------------------------------------------

print("\n[1] READING RAW BACI 2024")

raw = pd.read_csv(
    RAW_FILE,
    dtype={"k": "string"},
    low_memory=False
)

print("Raw rows:", f"{len(raw):,}")
print("Columns:", raw.columns.tolist())

required = {"t", "i", "j", "k", "v"}

if not required.issubset(raw.columns):
    raise ValueError(
        f"Missing BACI columns: {required - set(raw.columns)}"
    )

for col in ["t", "i", "j", "v"]:
    raw[col] = pd.to_numeric(raw[col], errors="coerce")

print("Missing trade values:", raw["v"].isna().sum())
print("Negative trade values:", (raw["v"] < 0).sum())

# ------------------------------------------
# 3. Select Vietnam transactions
# ------------------------------------------

print("\n[2] FILTERING VIETNAM TRADE")

exports = raw[
    (raw["i"] == VIETNAM_CODE)
    & (raw["j"] != VIETNAM_CODE)
].copy()

imports = raw[
    (raw["j"] == VIETNAM_CODE)
    & (raw["i"] != VIETNAM_CODE)
].copy()

self_trade = raw[
    (raw["i"] == VIETNAM_CODE)
    & (raw["j"] == VIETNAM_CODE)
]

export_usd = exports["v"].sum() * 1000
import_usd = imports["v"].sum() * 1000

print("Export rows:", f"{len(exports):,}")
print("Import rows:", f"{len(imports):,}")
print("Self-trade rows:", f"{len(self_trade):,}")

print("\nRAW BACI 2024 (billion USD):")
print(f"Exports: {export_usd / 1e9:,.3f}")
print(f"Imports: {import_usd / 1e9:,.3f}")
print(f"Total: {(export_usd + import_usd) / 1e9:,.3f}")

# ------------------------------------------
# 4. Compare with processed trade_year
# ------------------------------------------

print("\n[3] COMPARISON WITH CLEANED DATA")

trade = pd.read_csv(TRADE_FILE)

trade24 = trade[
    pd.to_numeric(trade["year"], errors="coerce") == YEAR
]

if len(trade24) != 1:
    raise ValueError(
        "Expected exactly one row for 2024 in trade_year.csv"
    )

clean_export = float(trade24["export_usd"].iloc[0])
clean_import = float(trade24["import_usd"].iloc[0])

comparison = pd.DataFrame([
    {
        "flow": "export",
        "raw_usd": export_usd,
        "clean_usd": clean_export
    },
    {
        "flow": "import",
        "raw_usd": import_usd,
        "clean_usd": clean_import
    }
])

comparison["difference_usd"] = (
    comparison["raw_usd"] - comparison["clean_usd"]
)

comparison["relative_difference_pct"] = (
    comparison["difference_usd"]
    / comparison["raw_usd"].replace(0, np.nan)
    * 100
)

print(comparison.to_string(index=False))

comparison.to_csv(
    OUT / "04_raw_vs_clean_2024.csv",
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------
# 5. Check partner codes
# ------------------------------------------

print("\n[4] CHECKING PARTNER CODES")

countries = pd.read_csv(COUNTRY_FILE)

print("Country lookup columns:",
      countries.columns.tolist())

partner = pd.read_csv(PARTNER_FILE)

partner24 = partner[
    pd.to_numeric(
        partner["year"], errors="coerce"
    ) == YEAR
].copy()

print("2024 unique partner codes:",
      partner24["partner_code"].nunique())

print("2024 unique ISO3 codes:",
      partner24["partner_iso3"].nunique())

# Check duplicated ISO3 mappings
mapping = (
    partner[[
        "partner_code",
        "partner_iso3",
        "partner_name"
    ]]
    .drop_duplicates()
)

duplicate_iso = mapping[
    mapping["partner_iso3"].duplicated(keep=False)
].sort_values("partner_iso3")

print("\nPartner codes sharing an ISO3:")
if duplicate_iso.empty:
    print("None")
else:
    print(duplicate_iso.to_string(index=False))

duplicate_iso.to_csv(
    OUT / "05_duplicate_iso3.csv",
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------
# 6. Top 20 export destinations in 2024
# ------------------------------------------

print("\n[5] TOP 20 EXPORT DESTINATIONS")

exports["partner_code"] = exports["j"].astype("Int64")

top_export = (
    exports.groupby("partner_code", as_index=False)["v"]
    .sum()
    .rename(columns={"v": "value_thousand_usd"})
)

top_export["export_usd"] = (
    top_export["value_thousand_usd"] * 1000
)

top_export = top_export.merge(
    mapping,
    on="partner_code",
    how="left"
)

top_export = top_export.sort_values(
    "export_usd", ascending=False
)

top_export["share_pct"] = (
    top_export["export_usd"] / export_usd * 100
)

print(
    top_export[[
        "partner_code",
        "partner_name",
        "export_usd",
        "share_pct"
    ]].head(20).to_string(index=False)
)

top_export.to_csv(
    OUT / "06_export_partners_2024.csv",
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------
# 7. Summary
# ------------------------------------------

print("\n" + "=" * 65)
print("VERIFICATION SUMMARY")
print("=" * 65)

for _, row in comparison.iterrows():
    if np.isclose(
        row["raw_usd"],
        row["clean_usd"],
        rtol=1e-10,
        atol=1
    ):
        print(f"{row['flow'].upper()}: RAW = CLEAN")
    else:
        print(f"{row['flow'].upper()}: MISMATCH - REVIEW")

print("\nReports saved in:")
print(OUT)

print("\nVERIFY FINISHED")
