
from pathlib import Path
import pandas as pd

# =====================================================
# 1. THU MUC
# =====================================================

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data_raw"
FILTERED = BASE / "data_filtered"
CLEAN = BASE / "data_clean"
CLEAN.mkdir(parents=True, exist_ok=True)

YEARS = range(2005, 2025)
CHUNK_SIZE = 100_000
VN_CODE = "704"

# =====================================================
# 2. DOC BANG MA QUOC GIA
# =====================================================

countries = pd.read_csv(
    RAW / "country_codes_V202601.csv",
    dtype=str,
    encoding="utf-8-sig"
)

countries.columns = countries.columns.str.strip()
countries["country_code"] = (
    countries["country_code"].str.strip()
)

assert (
    countries.loc[
        countries["country_code"] == VN_CODE,
        "country_iso3"
    ].iloc[0] == "VNM"
), "Ma Viet Nam khong khop!"

country_map = (
    countries.drop_duplicates("country_code")
    .set_index("country_code")
)

name_map = country_map["country_name"].to_dict()
iso_map = country_map["country_iso3"].to_dict()

# =====================================================
# 3. DOC BANG MA SAN PHAM
# =====================================================

products = pd.read_csv(
    RAW / "product_codes_HS02_V202601.csv",
    dtype={"code": str, "description": str},
    encoding="utf-8-sig"
)

products.columns = products.columns.str.strip()
products["code"] = products["code"].str.zfill(6)

product_map = (
    products.drop_duplicates("code")
    .set_index("code")["description"]
    .to_dict()
)

# =====================================================
# 4. XU LY TUNG NAM
# =====================================================

trade_year_parts = []
partner_year_parts = []
product_year_parts = []
partner_product_parts = []
quality_parts = []

for year in YEARS:

    file = FILTERED / f"vietnam_trade_{year}.csv"

    if not file.exists():
        raise FileNotFoundError(f"Thieu file: {file}")

    print(f"Dang xu ly nam {year}...")

    year_chunks = []
    partner_chunks = []
    product_chunks = []
    partner_product_chunks = []

    total_rows = 0
    missing_values = 0
    negative_values = 0
    unknown_partners = 0
    unknown_products = 0
    invalid_vn_rows = 0

    reader = pd.read_csv(
        file,
        dtype={
            "year": "int32",
            "exporter_code": str,
            "importer_code": str,
            "hs6": str,
            "trade_flow": str,
            "partner_code": str,
        },
        chunksize=CHUNK_SIZE
    )

    for df in reader:

        total_rows += len(df)

        df["hs6"] = df["hs6"].str.zfill(6)
        df["hs2"] = df["hs6"].str[:2]

        df["trade_value_1000usd"] = pd.to_numeric(
            df["trade_value_1000usd"],
            errors="coerce"
        )

        df["trade_usd"] = (
            df["trade_value_1000usd"] * 1000
        )

        df["partner_iso3"] = (
            df["partner_code"].map(iso_map)
        )

        df["partner_name"] = (
            df["partner_code"].map(name_map)
        )

        df["product_description"] = (
            df["hs6"].map(product_map)
        )

        # Kiem tra chat luong
        missing_values += df["trade_usd"].isna().sum()
        negative_values += (df["trade_usd"] < 0).sum()
        unknown_partners += df["partner_iso3"].isna().sum()
        unknown_products += df[
            "product_description"
        ].isna().sum()

        valid_direction = (
            (
                (df["exporter_code"] == VN_CODE)
                & (df["trade_flow"] == "Export")
            )
            |
            (
                (df["importer_code"] == VN_CODE)
                & (df["trade_flow"] == "Import")
            )
        )

        invalid_vn_rows += (~valid_direction).sum()

        # Khong tu y thay the gia tri thieu bang 0
        if df["trade_usd"].isna().any():
            raise ValueError(
                f"Nam {year} co gia tri thuong mai thieu."
            )

        if (df["trade_usd"] < 0).any():
            raise ValueError(
                f"Nam {year} co gia tri thuong mai am."
            )

        if not valid_direction.all():
            raise ValueError(
                f"Nam {year} co dong sai chieu thuong mai."
            )

        # Tong hop theo nam
        year_chunks.append(
            df.groupby(
                ["year", "trade_flow"],
                as_index=False
            )["trade_usd"].sum()
        )

        # Tong hop theo doi tac
        partner_chunks.append(
            df.groupby(
                [
                    "year",
                    "trade_flow",
                    "partner_code",
                    "partner_iso3",
                    "partner_name"
                ],
                dropna=False,
                as_index=False
            )["trade_usd"].sum()
        )

        # Tong hop theo HS2
        product_chunks.append(
            df.groupby(
                ["year", "trade_flow", "hs2"],
                as_index=False
            )["trade_usd"].sum()
        )

        # Tong hop doi tac x HS2
        partner_product_chunks.append(
            df.groupby(
                [
                    "year",
                    "trade_flow",
                    "partner_code",
                    "hs2"
                ],
                as_index=False
            )["trade_usd"].sum()
        )

    def combine(parts, keys):
        combined = pd.concat(parts, ignore_index=True)
        return combined.groupby(
            keys,
            dropna=False,
            as_index=False
        )["trade_usd"].sum()

    trade_year_parts.append(
        combine(year_chunks, ["year", "trade_flow"])
    )

    partner_year_parts.append(
        combine(
            partner_chunks,
            [
                "year", "trade_flow",
                "partner_code",
                "partner_iso3", "partner_name"
            ]
        )
    )

    product_year_parts.append(
        combine(
            product_chunks,
            ["year", "trade_flow", "hs2"]
        )
    )

    partner_product_parts.append(
        combine(
            partner_product_chunks,
            [
                "year", "trade_flow",
                "partner_code", "hs2"
            ]
        )
    )

    quality_parts.append({
        "year": year,
        "rows": total_rows,
        "missing_trade_value": int(missing_values),
        "negative_trade_value": int(negative_values),
        "unknown_partner_rows": int(unknown_partners),
        "unknown_product_rows": int(unknown_products),
        "invalid_direction_rows": int(invalid_vn_rows)
    })

    print(f"Hoan thanh {year}: {total_rows:,} dong")

# =====================================================
# 5. TAO CAC BANG KET QUA
# =====================================================

trade_long = pd.concat(
    trade_year_parts, ignore_index=True
)

trade_year = trade_long.pivot(
    index="year",
    columns="trade_flow",
    values="trade_usd"
).reset_index()

trade_year.columns.name = None

for col in ["Export", "Import"]:
    if col not in trade_year.columns:
        raise ValueError(f"Thieu du lieu {col}")

trade_year = trade_year.rename(
    columns={
        "Export": "export_usd",
        "Import": "import_usd"
    }
)

trade_year["trade_balance_usd"] = (
    trade_year["export_usd"]
    - trade_year["import_usd"]
)

trade_year["total_trade_usd"] = (
    trade_year["export_usd"]
    + trade_year["import_usd"]
)

trade_year["country_iso3"] = "VNM"

partner_year = pd.concat(
    partner_year_parts, ignore_index=True
)

product_year = pd.concat(
    product_year_parts, ignore_index=True
)

partner_product_year = pd.concat(
    partner_product_parts, ignore_index=True
)

quality = pd.DataFrame(quality_parts)

# =====================================================
# 6. KIEM TRA TONG GIA TRI
# =====================================================

for name, table in [
    ("partner_year", partner_year),
    ("product_year", product_year),
    ("partner_product_year", partner_product_year)
]:
    check = table.groupby(
        ["year", "trade_flow"]
    )["trade_usd"].sum().sort_index()

    reference = trade_long.set_index(
        ["year", "trade_flow"]
    )["trade_usd"].sort_index()

    if not check.index.equals(reference.index):
        raise ValueError(f"Sai nhom du lieu: {name}")

    if not (
        (check - reference).abs()
        <= reference.abs() * 1e-10 + 0.01
    ).all():
        raise ValueError(f"Sai tong gia tri: {name}")

# =====================================================
# 7. LUU FILE CSV
# =====================================================

outputs = {
    "trade_year.csv": trade_year,
    "partner_year.csv": partner_year,
    "product_year.csv": product_year,
    "partner_product_year.csv": partner_product_year,
    "quality_report.csv": quality
}

for filename, table in outputs.items():
    output = CLEAN / filename
    table.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )
    print(f"Da luu: {output}")

print("\n========== HOAN THANH ==========")
print(trade_year.to_string(index=False))
print("\nBAO CAO CHAT LUONG:")
print(quality.to_string(index=False))
