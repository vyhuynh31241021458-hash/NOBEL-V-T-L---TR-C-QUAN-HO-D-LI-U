"""Export the same design under five viewing conditions at 300 DPI."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.ticker import FuncFormatter

from house_style import DIVERGING_CMAP, apply_style, diverging_norm, format_number, sequential_norm
from house_style.accessibility import CVD_TYPES, grayscale, simulate_cvd
from house_style.colour_rules import MISSING_COLOR, MISSING_LABEL, color_for_value, ordered_present
from house_style.highlight import highlight_colors
from house_style.hs_palette import HS_COLORS, HS_LABELS, HS_ORDER
from house_style.partner_palette import PARTNER_COLORS, PARTNER_HATCHES, PARTNER_LABELS, PARTNER_ORDER
from house_style.sequential import SEQUENTIAL_COLORS
from house_style.theme import BAR_WIDTH, ZERO_LINE, declutter
from house_style.trade_flow import TRADE_FLOW_COLORS, TRADE_FLOW_LABELS, TRADE_FLOW_ORDER
from house_style.typography import DIRECT_LABEL, SOURCE, SUBTITLE

OUTPUT = Path(__file__).resolve().parent
MODES = dict(zip(
    ("original", "protanopia", "deuteranopia", "tritanopia", "greyscale"),
    (None, *CVD_TYPES, "gray"),
))
EXPORTS = dict(zip(PARTNER_ORDER, (94.0, 140.5, 28.4, 26.5, 15.0, 185.7)))
SECTIONS = {"II": 19.7, "XI": 49.8, "XII": 34.0, "XV": None, "XVI": 277.4, "XX": 26.4}
BALANCE = {"CHN": -64.7, "USA": 127.9, "KOR": -29.9, "JPN": 10.6, "THA": 0}


def transform(colors, mode):
    rgb = np.asarray([to_rgb(color) for color in colors])
    if mode is None:
        return rgb
    if mode == "gray":
        return grayscale(rgb)
    return simulate_cvd(rgb, mode)


def swatches(ax, entries, mode, columns):
    ax.set_xlim(0, columns)
    ax.set_ylim((len(entries) + columns - 1) // columns, 0)
    ax.axis("off")
    colors = transform([color for _, color in entries], mode)
    for index, ((label, original), rgb) in enumerate(zip(entries, colors)):
        row, col = divmod(index, columns)
        ax.add_patch(plt.Rectangle((col, row + 0.08), 0.20, 0.55, color=rgb, ec=None))
        ax.text(col + 0.24, row + 0.35, f"{label}\n{original}", va="center", fontsize=8)


def strip(ax, palette, labels, mode):
    positions = np.linspace(0, 1, 257)
    colors = transform(palette(positions), mode)
    ax.imshow(colors[np.newaxis, :, :], aspect="auto", interpolation="nearest", extent=(0, 1, 0, 1))
    ax.set_xticks(np.linspace(0, 1, len(labels)), labels)
    ax.set_yticks([])


def save_palette(folder, name, mode):
    fig, axes = plt.subplots(5, figsize=(13, 9), layout="constrained",
                             gridspec_kw={"height_ratios": [1.2, 4, 1, 0.5, 0.5]})
    fig.suptitle("Bảng màu P03", x=0.02, ha="left")
    for ax, title in zip(axes, ("Đối tác", "HS Section · HS2002", "Chiều thương mại và dữ liệu thiếu",
                                "Tuần tự · Blues", "Phân kỳ · RdBu")):
        ax.set_title(title, fontsize=12)
    swatches(axes[0], [(PARTNER_LABELS[key], PARTNER_COLORS[key]) for key in PARTNER_ORDER], mode, 4)
    swatches(axes[1], [(HS_LABELS[key], HS_COLORS[key]) for key in HS_ORDER], mode, 4)
    flows = [(TRADE_FLOW_LABELS[key], TRADE_FLOW_COLORS[key]) for key in TRADE_FLOW_ORDER]
    swatches(axes[2], [*flows, (MISSING_LABEL, MISSING_COLOR)], mode, 4)
    strip(axes[3], SEQUENTIAL_COLORS, ("Thấp · #F7FBFF", "Cao · #08306B"), mode)
    strip(axes[4], DIVERGING_CMAP, ("Âm · #67001F", "0 · #F7F7F7", "Dương · #053061"), mode)
    fig.savefig(folder / f"palette_{name}.png")
    plt.close(fig)


def draw_bars(ax, title, order, values, labels, colors, mode, *, hatches=None, emphasis=None, signed=False):
    keys = ordered_present(order, values)
    y = np.arange(len(keys))
    rgb = transform([colors[key] for key in keys], mode)
    for index, (key, color) in enumerate(zip(keys, rgb)):
        value = values[key]
        if value is None:
            ax.scatter(0, index, marker="X", facecolor=color, edgecolor="#555555", zorder=3)
            ax.annotate(MISSING_LABEL, (0, index), xytext=(8, 0), textcoords="offset points",
                        va="center", **DIRECT_LABEL)
            continue
        hatch = hatches.get(key, "") if hatches else ""
        bars = ax.barh(index, value, height=BAR_WIDTH, color=color, hatch=hatch,
                       edgecolor="#555555" if hatch or key == emphasis else "none", linewidth=0.6)
        label_style = DIRECT_LABEL | ({"fontweight": "bold"} if key == emphasis else {})
        ax.bar_label(bars, labels=[format_number(value, 1, signed=signed)], padding=4, **label_style)
    ax.set_yticks(y, [labels[key] for key in keys])
    if emphasis in keys:
        ax.get_yticklabels()[keys.index(emphasis)].set_fontweight("bold")
    ax.invert_yaxis()
    ax.margins(x=0.25)
    ax.set_title(title, fontsize=13)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: format_number(value)))
    declutter(ax, quantitative_axis="x")
    if signed:
        low, high = min(values.values()), max(values.values())
        padding = (high - low) * 0.35
        ax.set_xlim(low - padding, high + padding)
        ax.axvline(0, **ZERO_LINE)


def save_charts(folder, name, mode):
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.subplots_adjust(left=0.16, right=0.96, bottom=0.11, top=0.85, hspace=0.48, wspace=1.15)
    fig.suptitle("Áp dụng house style P03", x=0.04, ha="left", y=0.98)
    fig.text(0.04, 0.90, "Xuất khẩu và cán cân thương mại · Tỷ USD", **SUBTITLE)
    fig.text(0.04, 0.03, "Nguồn dữ liệu minh họa. N/A là giá trị thiếu.", **SOURCE)
    partner_ax, category_ax, sequential_ax, balance_ax, highlight_ax, empty_ax = axes.flat
    draw_bars(partner_ax, "Xuất khẩu theo đối tác", PARTNER_ORDER, EXPORTS, PARTNER_LABELS,
              PARTNER_COLORS, mode, hatches=PARTNER_HATCHES)
    hs_fixed = {key: HS_COLORS[key] if value is not None else MISSING_COLOR for key, value in SECTIONS.items()}
    draw_bars(category_ax, "HS · Màu theo ngành", HS_ORDER, SECTIONS, HS_LABELS, hs_fixed, mode)
    seq_norm = sequential_norm(0, max(value for value in SECTIONS.values() if value is not None))
    hs_seq = {key: color_for_value(value, cmap=SEQUENTIAL_COLORS, norm=seq_norm)
              for key, value in SECTIONS.items()}
    draw_bars(sequential_ax, "HS · Màu theo kim ngạch", HS_ORDER, SECTIONS, HS_LABELS, hs_seq, mode)
    div_norm = diverging_norm(min(BALANCE.values()), max(BALANCE.values()))
    balance_colors = {key: DIVERGING_CMAP(div_norm(value)) for key, value in BALANCE.items()}
    draw_bars(balance_ax, "Cán cân thương mại", PARTNER_ORDER, BALANCE, PARTNER_LABELS,
              balance_colors, mode, signed=True)
    selected = PARTNER_ORDER[0]
    highlight = dict(zip(EXPORTS, highlight_colors(EXPORTS, selected, PARTNER_COLORS)))
    draw_bars(highlight_ax, "Làm nổi bật một đối tác", PARTNER_ORDER, EXPORTS, PARTNER_LABELS,
              highlight, mode, emphasis=selected)
    empty_ax.axis("off")
    fig.savefig(folder / f"charts_{name}.png")
    plt.close(fig)


def main():
    with apply_style():
        for name, mode in MODES.items():
            folder = OUTPUT / name
            folder.mkdir(exist_ok=True)
            save_palette(folder, name, mode)
            save_charts(folder, name, mode)


if __name__ == "__main__":
    main()
