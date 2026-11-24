"""Generate the T12 axis-truncation comparison from BACI data."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from notebooks.p03_style import apply_style, format_number
from notebooks.p03_style.highlight import ACCENT_COLOR
from notebooks.p03_style.theme import BAR_WIDTH, SLIDE_SIZE
from notebooks.p03_style.typography import DIRECT_LABEL, SOURCE, SUBTITLE

APPENDIX = Path(__file__).resolve().parent
SOURCE_CSV = APPENDIX.parents[1] / "data" / "clean" / "trade_year.csv"
YEARS = (2023, 2024)
UPPER_LIMIT = 140
CROPPED_BASELINE = 110


def read_balances():
    with SOURCE_CSV.open(encoding="utf-8-sig", newline="") as stream:
        rows = [
            row for row in csv.DictReader(stream)
            if row["country_iso3"] == "VNM" and int(row["year"]) in YEARS
        ]
    by_year = {int(row["year"]): float(row["trade_balance_usd"]) / 1e9 for row in rows}
    if len(rows) != len(YEARS) or set(by_year) != set(YEARS):
        raise ValueError("Expected one Vietnam trade balance for each selected year.")
    return [by_year[year] for year in YEARS]


def main():
    values = read_balances()
    if not all(CROPPED_BASELINE < value < UPPER_LIMIT for value in values):
        raise ValueError("The selected values must fit both displayed scales.")

    with apply_style():
        fig, panels = plt.subplots(1, 2, figsize=SLIDE_SIZE)
        fig.subplots_adjust(left=0.10, right=0.96, top=0.74, bottom=0.21, wspace=0.36)
        fig.suptitle("Cán cân thương mại hàng hóa của Việt Nam")
        fig.text(0.5, 0.88, "BACI · Việt Nam · 2023–2024", **SUBTITLE)

        for ax, title, baseline, ticks in (
            (panels[0], "A. Biểu đồ trung thực", 0, range(0, UPPER_LIMIT + 1, 20)),
            (panels[1], "B. Minh họa gây hiểu lầm", CROPPED_BASELINE,
             range(CROPPED_BASELINE, UPPER_LIMIT + 1, 5)),
        ):
            bars = ax.bar([str(year) for year in YEARS], values, width=BAR_WIDTH, color=ACCENT_COLOR)
            ax.bar_label(bars, labels=[format_number(value, 2) for value in values],
                         padding=5, **DIRECT_LABEL)
            ax.set_title(title, fontsize=14)
            ax.set_ylabel("Tỷ USD danh nghĩa")
            ax.set(ylim=(baseline, UPPER_LIMIT), yticks=ticks)
            ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: format_number(value)))

        for ax, note in zip(panels, ("Trục Y bắt đầu tại 0 tỷ USD", "Trục Y bị cắt tại 110 tỷ USD")):
            bounds = ax.get_position()
            fig.text(bounds.x0 + bounds.width / 2, 0.13, note, **SUBTITLE)
        fig.text(0.5, 0.055, "Nguồn: CEPII BACI HS2002, bảng trade_year.csv của P03.", **SOURCE)
        fig.savefig(APPENDIX / "t12_honest_vs_misleading.png")
        plt.close(fig)


if __name__ == "__main__":
    main()
