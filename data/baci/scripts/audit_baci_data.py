
from pathlib import Path
import pandas as pd
import numpy as np

# ============================================
# P03 - MADE IN...?
# DATA AUDIT: CEPII BACI + WORLD BANK WDI
# ============================================

BASE = Path(__file__).resolve().parent.parent
CLEAN = BASE / "data_clean"
RAW = BASE / "data_raw"
OUTPUT = BASE / "audit_results"
OUTPUT.mkdir(exist_ok=True)

FILES = {
    "trade_year": CLEAN / "trade_year.csv",
    "partner_year": CLEAN / "partner_year.csv",
    "product_year": CLEAN / "product_year.csv",
    "partner_product_year": CLEAN / "partner_product_year.csv",
    "quality_report": CLEAN / "quality_report.csv",
    "baci_wdi": CLEAN / "baci_wdi_vietnam_2005_2024.csv",
}

print("=" * 65)
print("P03 - DATA AUDIT")
print("=" * 65)

tables = {}
issues = []
summary = []

# --------------------------------------------
# 1. Check file existence and structure
# --------------------------------------------

print("\n[1] KIEM TRA CAU TRUC FILE")

for name, path in FILES.items():
    if not path.exists():
        print(f"[MISSING] {name}: {path}")
        issues.append(f"Missing file: {name}")
        continue

    # Read only the first rows for schema
    preview = pd.read_csv(path, nrows=5)

    # Load aggregate files for further checks
    df = pd.read_csv(path, low_memory=False)
    tables[name] = df

    missing_cells = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    summary.append({
        "table": name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": missing_cells,
        "duplicate_rows": duplicate_rows
    })

    print(f"\n{name}")
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {df.columns.tolist()}")
    print(f"  Missing cells: {missing_cells:,}")
    print(f"  Exact duplicate rows: {duplicate_rows:,}")

pd.DataFrame(summary).to_csv(
    OUTPUT / "01_structure_audit.csv",
    index=False,
    encoding="utf-8-sig"
)

# --------------------------------------------
# 2. Check annual trade table
# --------------------------------------------

print("\n[2] KIEM TRA TRADE_YEAR")

if "trade_year" in tables:
    df = tables["trade_year"].copy()

    required = [
        "year", "export_usd", "import_usd",
        "trade_balance_usd", "total_trade_usd"
    ]

    if all(c in df.columns for c in required):
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

        expected_years = set(range(2005, 2025))
        actual_years = set(df["year"].dropna().astype(int))

        missing_years = sorted(expected_years - actual_years)
        extra_years = sorted(actual_years - expected_years)

        print("Missing years:", missing_years)
        print("Extra years:", extra_years)
        print("Duplicate years:", int(df["year"].duplicated().sum()))

        if missing_years or extra_years:
            issues.append("Unexpected year coverage")

        if df["year"].duplicated().any():
            issues.append("Duplicate years in trade_year")

        for col in required[1:]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        negative_count = int(
            (df[["export_usd", "import_usd"]] < 0)
            .sum().sum()
        )
        print("Negative export/import values:", negative_count)

        balance_expected = df["export_usd"] - df["import_usd"]
        total_expected = df["export_usd"] + df["import_usd"]

        balance_error = (
            df["trade_balance_usd"] - balance_expected
        ).abs()

        total_error = (
            df["total_trade_usd"] - total_expected
        ).abs()

        print("Max balance formula error (USD):",
              balance_error.max())
        print("Max total formula error (USD):",
              total_error.max())

        if negative_count:
            issues.append("Negative trade values")

        if (balance_error > 1).any():
            issues.append("Trade balance inconsistency")

        if (total_error > 1).any():
            issues.append("Total trade inconsistency")

        print("\n2024 BACI totals (billion USD):")
        d24 = df[df["year"] == 2024]

        if len(d24) == 1:
            for col in [
                "export_usd", "import_usd",
                "trade_balance_usd", "total_trade_usd"
            ]:
                print(f"  {col}: {d24[col].iloc[0] / 1e9:.3f}")
    else:
        print("Unexpected schema:", df.columns.tolist())
        issues.append("Unexpected trade_year schema")

# --------------------------------------------
# 3. Check aggregation consistency
# --------------------------------------------

print("\n[3] KIEM TRA TINH NHAT QUAN CAC BANG")

def identify_columns(df):
    value_candidates = [
        "trade_value_usd", "value_usd",
        "trade_usd", "total_value_usd", "value"
    ]
    flow_candidates = ["trade_flow", "flow", "direction"]

    value_col = next(
        (c for c in value_candidates if c in df.columns),
        None
    )
    flow_col = next(
        (c for c in flow_candidates if c in df.columns),
        None
    )
    return value_col, flow_col


def normalize_flow(s):
    return (
        s.astype(str).str.strip().str.lower()
        .replace({
            "exports": "export",
            "imports": "import"
        })
    )


def aggregate_year_flow(df, name):
    value_col, flow_col = identify_columns(df)

    if value_col is None or flow_col is None:
        print(f"{name}: Cannot detect value/flow columns")
        return None

    temp = df[["year", flow_col, value_col]].copy()
    temp["year"] = pd.to_numeric(
        temp["year"], errors="coerce"
    )
    temp["flow"] = normalize_flow(temp[flow_col])
    temp["value"] = pd.to_numeric(
        temp[value_col], errors="coerce"
    )

    if not temp["flow"].isin(["export", "import"]).all():
        print(f"{name}: Unknown flow labels found")
        issues.append(f"Unknown trade flow: {name}")
        return None

    result = (
        temp.groupby(["year", "flow"], as_index=False)["value"]
        .sum()
    )
    result["table"] = name
    return result


aggregates = []

for name in [
    "partner_year", "product_year",
    "partner_product_year"
]:
    if name in tables:
        result = aggregate_year_flow(tables[name], name)
        if result is not None:
            aggregates.append(result)

if "trade_year" in tables:
    base = tables["trade_year"]

    base_long = base.melt(
        id_vars=["year"],
        value_vars=["export_usd", "import_usd"],
        var_name="flow",
        value_name="value"
    )

    base_long["flow"] = base_long["flow"].replace({
        "export_usd": "export",
        "import_usd": "import"
    })
    base_long["table"] = "trade_year"
    aggregates.insert(0, base_long)

if aggregates:
    all_aggs = pd.concat(aggregates, ignore_index=True)

    comparison = all_aggs.pivot_table(
        index=["year", "flow"],
        columns="table",
        values="value",
        aggfunc="sum"
    ).reset_index()

    for col in [
        "partner_year", "product_year",
        "partner_product_year"
    ]:
        if col in comparison.columns and "trade_year" in comparison:
            diff = (
                comparison[col] - comparison["trade_year"]
            ).abs()

            print(
                f"{col} vs trade_year: "
                f"max absolute difference = {diff.max():,.2f} USD"
            )

            # Floating point tolerance for large totals
            tolerance = np.maximum(
                1.0,
                comparison["trade_year"].abs() * 1e-9
            )

            if (diff > tolerance).any():
                issues.append(f"Aggregate mismatch: {col}")

    comparison.to_csv(
        OUTPUT / "02_aggregation_audit.csv",
        index=False,
        encoding="utf-8-sig"
    )

# --------------------------------------------
# 4. Check country / HS codes
# --------------------------------------------

print("\n[4] KIEM TRA MA DOI TAC VA SAN PHAM")

for name in [
    "partner_year", "product_year",
    "partner_product_year"
]:
    if name not in tables:
        continue

    df = tables[name]

    for col in [
        "partner_code", "partner_iso3",
        "partner_name", "hs2", "hs2_code"
    ]:
        if col in df.columns:
            print(
                f"{name}.{col}: "
                f"missing={df[col].isna().sum()}, "
                f"unique={df[col].nunique(dropna=True)}"
            )

    if "partner_code" in df.columns:
        codes = pd.to_numeric(
            df["partner_code"], errors="coerce"
        )

        self_trade = int((codes == 704).sum())
        print(f"{name}: Vietnam as partner = {self_trade}")

        if self_trade:
            issues.append(f"Self trade found in {name}")

# --------------------------------------------
# 5. BACI vs WDI comparison
# --------------------------------------------

print("\n[5] DOI CHIEU BACI VA WORLD BANK WDI")

if "baci_wdi" in tables:
    df = tables["baci_wdi"].copy()

    required = [
        "year", "export_usd",
        "wdi_merchandise_exports_usd"
    ]

    if all(c in df.columns for c in required):
        for col in required:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

        df["difference_usd"] = (
            df["export_usd"]
            - df["wdi_merchandise_exports_usd"]
        )

        df["difference_pct"] = (
            df["difference_usd"]
            / df["wdi_merchandise_exports_usd"]
            * 100
        )

        report = df[[
            "year", "export_usd",
            "wdi_merchandise_exports_usd",
            "difference_usd", "difference_pct"
        ]].copy()

        report.to_csv(
            OUTPUT / "03_baci_wdi_comparison.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print(report.tail(5).to_string(index=False))

        print(
            "\nLargest absolute percentage difference:",
            f"{report['difference_pct'].abs().max():.2f}%"
        )

        print(
            "NOTE: Difference is a review flag, "
            "not proof that either source is wrong."
        )
    else:
        issues.append("Unexpected BACI-WDI merge schema")

# --------------------------------------------
# 6. Check items for PCA
# --------------------------------------------

print("\n[6] KIEM TRA SO DOI TAC CHO PCA")

if "partner_year" in tables:
    df = tables["partner_year"]

    if "partner_code" in df.columns:
        n_all = df["partner_code"].nunique(dropna=True)

        if "year" in df.columns:
            n_2024 = df.loc[
                pd.to_numeric(
                    df["year"], errors="coerce"
                ) == 2024,
                "partner_code"
            ].nunique(dropna=True)
        else:
            n_2024 = 0

        print("Unique partners, all years:", n_all)
        print("Unique partners, 2024:", n_2024)

        if n_2024 < 20:
            issues.append("Fewer than 20 partners in 2024")

# --------------------------------------------
# 7. Final audit summary
# --------------------------------------------

print("\n" + "=" * 65)
print("AUDIT SUMMARY")
print("=" * 65)

if issues:
    print("CHECKS REQUIRING ATTENTION:")
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")
else:
    print("No structural or arithmetic issues detected.")

print("\nImportant:")
print("- This audit does not prove external data accuracy.")
print("- Check BACI partner codes and coverage separately.")
print("- Review differences against WDI and source methods.")
print("- Check original raw transactions if totals look unusual.")

print("\nAudit reports saved to:")
print(OUTPUT)
print("\nAUDIT FINISHED")
