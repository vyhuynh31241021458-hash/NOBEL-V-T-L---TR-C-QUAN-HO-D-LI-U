"""T05: merge survey records and compare BACI at HS Chapter level.

Assumption: equal HS Chapter codes are suitable for broad comparison across
HS2022 and HS2002. Chapter coverage may differ between revisions.
"""
import argparse
from pathlib import Path

import pandas as pd


def read_table(path, aliases, required):
    table = pd.read_csv(path, dtype="string", encoding="utf-8-sig")
    table.columns = table.columns.str.strip()
    for original, canonical in aliases.items():
        if original in table and canonical not in table:
            table = table.rename(columns={original: canonical})
    missing = set(required) - set(table.columns)
    if missing:
        raise ValueError(f"{path}: thiếu cột {sorted(missing)}")
    return table


def check_key(table, keys, label):
    for key in keys:
        table[key] = table[key].str.strip().replace("", pd.NA)
    bad = table[keys].isna().any(axis=1) | table.duplicated(keys, keep=False)
    if bad.any():
        examples = table.loc[bad, keys].head().to_dict("records")
        raise ValueError(f"{label}: khóa thiếu hoặc trùng {examples}")


def chapter_codes(values, label, allow_missing=False):
    clean = values.str.strip().replace("", pd.NA)
    valid = clean.str.fullmatch(r"[0-9]{1,2}").fillna(False)
    valid &= pd.to_numeric(clean, errors="coerce").between(1, 97).fillna(False)
    valid &= ~clean.eq("77").fillna(False)
    bad = ~valid & (clean.notna() if allow_missing else True)
    if bad.any():
        raise ValueError(f"{label}: Chapter không hợp lệ {clean[bad].unique().tolist()}")
    return clean.str.zfill(2)


def merge_records(base, lookup, label):
    key = "record_id"
    check_key(lookup, [key], label)
    extra = lookup.loc[~lookup[key].isin(base[key]), key].tolist()
    missing = base.loc[~base[key].isin(lookup[key]), key].tolist()
    if missing or extra:
        raise ValueError(
            f"{label}: thiếu {len(missing)} mã {missing[:10]}, "
            f"dư {len(extra)} mã {extra[:10]}."
        )
    overlap = (set(base.columns) & set(lookup.columns)) - {key}
    if overlap:
        raise ValueError(f"{label}: tên cột trùng bảng chính {sorted(overlap)}")
    return base.merge(lookup, on=key, how="left", validate="one_to_one", sort=False)


def run(args):
    base = read_table(args.survey, {}, [
        "record_id", "store", "product_name", "origin_country", "price_vnd",
    ])
    check_key(base, ["record_id"], "Task 1")
    if len(base) != args.expected_rows:
        raise ValueError(f"Task 1 có {len(base)} mẫu, dự kiến {args.expected_rows}.")

    price_columns = ["record_id", "category_clean", "price_tier", "price_normalized", "task4_note"]
    prices = read_table(args.segment, {
        "Mã sản phẩm": "record_id",
        "category_clean (ngành hàng đã được phân loại)": "category_clean",
        "price_comparable_vnd": "price_normalized",
    }, price_columns)
    # Comparisons need the unit along with the normalized price.
    price_columns += [c for c in ("price_comparison_unit", "price_comparison_group") if c in prices]

    hs_columns = ["record_id", "hs_section", "hs2"]
    hs = read_table(args.hs, {
        "Mã sản phẩm": "record_id", "Section": "hs_section", "section": "hs_section",
        "section_code": "hs_section", "Chapter": "hs2", "chapter": "hs2",
        "hs_chapter": "hs2", "Chapter HS2022": "hs2",
        "Ghi chú": "hs_note", "classification_note": "hs_note", "notes": "hs_note",
    }, hs_columns)
    hs["hs2"] = chapter_codes(hs["hs2"], "HS2022", allow_missing=True)
    hs = hs.rename(columns={"hs_section": "hs2022_section", "hs_note": "hs2022_note"})
    hs_columns = ["record_id", "hs2022_section", "hs2"]
    if "hs2022_note" in hs:
        hs_columns.append("hs2022_note")

    final = merge_records(base, prices[price_columns].copy(), "Task 4")
    final = merge_records(final, hs[hs_columns].copy(), "Task 2")
    if args.collectors:
        collectors = read_table(args.collectors, {}, ["record_id", "collector"])
        final = merge_records(final, collectors[["record_id", "collector"]].copy(), "Người thu")
        final["collector"] = final.collector.str.strip().replace("", pd.NA)
    else:
        final["collector"] = pd.NA

    if not final["record_id"].equals(base["record_id"]):
        raise RuntimeError("Thứ tự hoặc số lượng record_id đã thay đổi sau ghép.")

    baci = read_table(args.product_year, {}, ["year", "hs2", "trade_flow", "trade_usd"])
    baci["hs2"] = chapter_codes(baci["hs2"], "BACI HS2002")
    trade_keys = ["year", "hs2", "trade_flow"]
    # product_year.csv is already at year × Chapter × flow grain.
    check_key(baci, trade_keys, "BACI product_year")
    if not baci["year"].str.fullmatch(r"[0-9]{4}").all():
        raise ValueError("BACI product_year: năm không hợp lệ.")
    if not baci["trade_flow"].isin({"Export", "Import"}).all():
        raise ValueError("BACI product_year: chiều thương mại không hợp lệ.")
    baci["trade_usd"] = pd.to_numeric(baci["trade_usd"], errors="raise")
    if baci["trade_usd"].isna().any() or not baci["trade_usd"].between(0, float("inf"), inclusive="left").all():
        raise ValueError("BACI product_year: kim ngạch thiếu hoặc không hợp lệ.")
    baci_summary = baci.groupby(trade_keys, as_index=False)["trade_usd"].sum()
    chapters = set(final["hs2"].dropna())
    print("Chapter chỉ có trong khảo sát:", sorted(chapters - set(baci["hs2"])))
    print("Chapter chỉ có trong BACI:", sorted(set(baci["hs2"]) - chapters))
    print("HS2022 và HS2002 được so sánh theo Chapter; phạm vi mã có thể thay đổi giữa hai phiên bản.")
    if args.partner_year:
        partners = read_table(args.partner_year, {}, ["year", "trade_flow", "partner_code"])
        check_key(partners, ["year", "trade_flow", "partner_code"], "BACI partner_year")
        print(f"Bảng đối tác đã kiểm tra: {len(partners)} dòng.")

    dimensions = ["hs2", "store", "origin_country", "category_clean", "price_tier"]
    survey_summary = (final.groupby(dimensions, dropna=False).size()
                      .rename("product_count").reset_index())
    if survey_summary["product_count"].sum() != len(base):
        raise RuntimeError("Tổng số mẫu trong bảng tổng hợp không khớp.")
    for column in dimensions:
        print(f"Thiếu {column}: {int(final[column].isna().sum())} mẫu.")
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    for name, table in {
        "survey_final.csv": final,
        "survey_hs_summary.csv": survey_summary,
        "baci_hs_summary.csv": baci_summary,
    }.items():
        table.to_csv(output / name, index=False, encoding="utf-8-sig")
    print(f"Task 5: {len(base)} mẫu đầu vào, {len(final)} mẫu đầu ra; {len(baci_summary)} dòng BACI.")


def main():
    root = Path(__file__).resolve().parents[2]
    survey_dir = root / "P03 Survey" / "data_clean"
    baci_dir = root / "P03 Baci" / "data_clean"
    defaults = {
        "survey": survey_dir / "survey_clean.csv",
        "segment": survey_dir / "survey_segment_All.csv",
        "hs": survey_dir.parent / "data_raw" / "hs" / "hs2022_final.csv",
        "product-year": baci_dir / "product_year.csv",
        "partner-year": baci_dir / "partner_year.csv",
        "collectors": root / "docs" / "collector_by_record.csv",
        "output-dir": survey_dir,
    }
    parser = argparse.ArgumentParser(
        description="T05: Ghép khảo sát và tổng hợp BACI theo HS Chapter."
    )
    for option, default in defaults.items():
        parser.add_argument(f"--{option}", type=Path, default=default)
    parser.add_argument("--expected-rows", type=int, default=398)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
