"""Export one C02 figure or the complete set. Run from the repository root."""

import argparse
from pathlib import Path

from matplotlib import rc_context

from notebooks.house_style.house_style import apply_style

from .bieu_do import plot_c02a, plot_c02b, plot_c02c, plot_c02d, plot_c02e
from .du_lieu import load_data

FIGURES = dict(zip(("C02A", "C02B", "C02C", "C02D", "C02E"),
                   (plot_c02a, plot_c02b, plot_c02c, plot_c02d, plot_c02e)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chart", nargs="?", default="all", choices=("all", *FIGURES))
    args = parser.parse_args()
    data = load_data()
    names = FIGURES if args.chart == "all" else (args.chart,)
    with apply_style(), rc_context({"svg.fonttype": "path"}):
        for name in names:
            fig = FIGURES[name](data)
            for extension in ("png", "svg"):
                fig.savefig(Path(__file__).with_name(f"{name}.{extension}"))
            print(f"{name}: PNG + SVG")


if __name__ == "__main__":
    main()
