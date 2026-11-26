"""Load and validate the cleaned BACI data for C02."""

from csv import DictReader
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import re

from notebooks.house_style.house_style import HS_ORDER, OTHER, TRADE_FLOW_ORDER

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "clean"
YEARS = tuple(range(2005, 2025))
MILESTONES = (2005, 2010, 2015, 2020, 2024)
CHAPTERS = ("84", "85")


@dataclass(frozen=True)
class C02Data:
    groups: tuple[str, ...]
    sections: dict[tuple[int, str, str], Decimal]
    products: dict[tuple[int, str, str], Decimal]
    totals: dict[tuple[int, str], Decimal]
    import_groups: tuple[str, ...]
    import_sections: dict[tuple[int, str, str], Decimal]

    def share(self, year, flow, group):
        values = self.import_sections if flow == "Import" else self.sections
        return values[year, flow, group] / self.totals[year, flow]


def read_values(path, code_field, *, extra_fields=()):
    values = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = DictReader(stream)
        fields = {"year", "trade_flow", code_field, "trade_usd", *extra_fields}
        if missing := fields.difference(reader.fieldnames or ()):
            raise ValueError(f"{path.name}: thiếu cột {sorted(missing)}")
        for row in reader:
            line = reader.line_num
            try:
                if any(not (row[field] or "").strip() for field in fields):
                    raise ValueError("thiếu giá trị")
                year = int(row["year"])
                flow, code = row["trade_flow"], row[code_field]
                amount = Decimal(row["trade_usd"])
                if flow not in TRADE_FLOW_ORDER or not amount.is_finite() or amount < 0:
                    raise ValueError("chiều thương mại hoặc kim ngạch không hợp lệ")
                if code_field == "hs2" and not re.fullmatch(r"[0-9]{2}", code):
                    raise ValueError("hs2 phải có hai ký tự số")
                if code_field == "section_code" and code not in HS_ORDER[:-1]:
                    raise ValueError("mã phần HS không hợp lệ")
                if year not in YEARS:
                    continue
                key = (year, flow, code)
                if key in values:
                    raise ValueError(f"trùng khóa {key}")
                values[key] = amount
            except (ValueError, ArithmeticError) as error:
                raise ValueError(f"{path.name}:{line}: {error}") from error
    return values


def require_coverage(values, codes, filename):
    for year in YEARS:
        for flow in TRADE_FLOW_ORDER:
            for code in codes:
                if (year, flow, code) not in values:
                    raise ValueError(f"{filename}: thiếu {(year, flow, code)}")


def group_sections(raw, rank_flow, flows):
    codes = [code for code in HS_ORDER if code != OTHER]
    require_coverage(raw, codes, "section_year.csv")
    # Stable ties follow the shared HS order.
    top = sorted(codes, key=lambda code: -sum(raw[y, rank_flow, code] for y in MILESTONES))[:5]
    groups = (*top, OTHER)
    others = [code for code in codes if code not in top]
    totals = {}
    grouped = {}
    for year in YEARS:
        for flow in flows:
            key = (year, flow)
            total = sum(raw[year, flow, code] for code in codes)
            totals[key] = total
            for code in top:
                grouped[year, flow, code] = raw[year, flow, code]
            grouped[year, flow, OTHER] = sum(raw[year, flow, code] for code in others)
            if total <= 0 or sum(grouped[year, flow, code] for code in groups) != total:
                raise ValueError(f"Tổng phần HS không hợp lệ sau khi gộp: {key}")
    return groups, grouped, totals


def load_data(data_dir=DATA_DIR):
    """Check the input schema and return exact USD values, shared groups and totals."""
    data_dir = Path(data_dir)
    sections = read_values(data_dir / "section_year.csv", "section_code", extra_fields=("section_name",))
    products = read_values(data_dir / "product_year.csv", "hs2")
    require_coverage(products, sorted({key[2] for key in products} | set(CHAPTERS)), "product_year.csv")
    groups, grouped, totals = group_sections(sections, 'Export', TRADE_FLOW_ORDER)
    import_groups, import_sections, _ = group_sections(sections, 'Import', ('Import',))
    for year, flow in totals:
        if sum(amount for (y, f, _), amount in products.items() if (y, f) == (year, flow)) != totals[year, flow]:
            raise ValueError(f"Tổng kim ngạch theo chương và phần lệch nhau: {(year, flow)}")
    return C02Data(groups, grouped, products, totals, import_groups, import_sections)
