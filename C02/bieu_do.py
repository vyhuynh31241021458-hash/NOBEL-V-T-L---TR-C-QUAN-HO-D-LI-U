"""Reusable Matplotlib figure constructors for C02. Import from the repository root."""

from matplotlib import rcParams
from matplotlib.colors import to_rgb
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter, MaxNLocator, MultipleLocator

from notebooks.house_style.house_style import (
    BAR_WIDTH, COUNTRY_COLORS, DIRECT_LABEL, HS_COLORS, HS_LABELS, SOURCE, SUBTITLE,
    TRADE_FLOW_COLORS, TRADE_FLOW_LABELS, TRADE_FLOW_LINESTYLES, TRADE_FLOW_MARKERS,
    TRADE_FLOW_ORDER, apply_style, format_number, format_percent, format_year, grayscale,
)

from .du_lieu import CHAPTERS, MILESTONES, YEARS

# Redundant symbols distinguish HS lines and stack segments independently of colour.
HS_MARKS = ("o", "s", "^", "D", "P", "x")
HS_HATCHES = ("/", chr(92), "x", ".", "-", "")


def heading(fig, title, scope, source):
    fig.suptitle(title, y=.98)
    fig.text(.5, .925, "Việt Nam · " + scope, va="top", **{**SUBTITLE, "color": COUNTRY_COLORS["VNM"]})
    fig.text(.5, .027, f"Nguồn · CEPII BACI HS2002 V202601 · {source}", **SOURCE)


def add_table(ax, headings, rows):
    ax.set_axis_off()
    table = ax.table(cellText=rows, colLabels=headings, cellLoc="center", bbox=(0, 0, 1, 1))
    table.auto_set_font_size(False)
    table.set_fontsize(rcParams["legend.fontsize"])
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor(rcParams["axes.edgecolor"])
        cell.set_linewidth(rcParams["axes.linewidth"] / 2)
        if row == 0:
            cell.get_text().set_weight(rcParams["figure.titleweight"])


def section_heading(code):
    return HS_LABELS[code].split(" · ")[0]


def legend_above(ax):
    ax.legend(ncols=3, loc="lower center", bbox_to_anchor=(.5, 1.01))


def composition(data, flow, title):
    fig = Figure(figsize=(11, 7))
    ax, table = fig.subplots(2, gridspec_kw={"height_ratios": (3, 1.5)})
    fig.subplots_adjust(left=.09, right=.94, bottom=.09, top=.79, hspace=.44)
    heading(fig, title, "5 mốc năm từ 2005 đến 2024", "section_year.csv")
    groups = data.import_groups if flow == "Import" else data.groups
    positions = list(range(len(MILESTONES)))
    bottoms = [0.] * len(positions)
    for group, hatch in zip(groups, HS_HATCHES):
        color = HS_COLORS[group]
        dark = float(grayscale(to_rgb(color))[0]) < .55
        ink = rcParams["axes.facecolor"] if dark else rcParams["text.color"]
        shares = [float(data.share(year, flow, group)) for year in MILESTONES]
        ax.bar(positions, shares, bottom=bottoms, width=BAR_WIDTH, color=color,
               edgecolor=ink, linewidth=0, hatch=hatch, label=HS_LABELS[group])
        for x, bottom, share in zip(positions, bottoms, shares):
            if share >= .085:
                ax.text(x, bottom + share / 2, format_percent(share),
                        ha="center", va="center", color=ink,
                        bbox={"facecolor": color, "edgecolor": "none", "pad": 1}, **DIRECT_LABEL)
        bottoms = [bottom + share for bottom, share in zip(bottoms, shares)]
    ax.set(ylim=(0, 1), xlabel="Năm", ylabel=f"Tỷ trọng {TRADE_FLOW_LABELS[flow].lower()} (%)")
    ax.set_xticks(positions, [format_year(year) for year in MILESTONES])
    ax.yaxis.set_major_locator(MultipleLocator(.25))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: format_percent(value, 0)))
    legend_above(ax)
    rows = [[section_heading(code), *[format_percent(float(data.share(y, flow, code))) for y in MILESTONES]]
            for code in groups]
    add_table(table, ["Phần HS", *map(format_year, MILESTONES)], rows)
    return fig


def format_value(usd):
    return format_number(float(usd / 1_000_000_000), 1)


def value_axis(ax, limit, ylabel):
    ax.set(xlim=(YEARS[0], YEARS[-1]), ylim=(0, limit), xlabel="Năm", ylabel=ylabel)
    ax.set_xticks(MILESTONES, [format_year(year) for year in MILESTONES])
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: format_number(value)))


def section_trends(data, flow, title):
    fig = Figure(figsize=(11, 10))
    ax, table = fig.subplots(2, gridspec_kw={"height_ratios": (3, 3.7)})
    fig.subplots_adjust(left=.09, right=.94, bottom=.075, top=.83, hspace=.31)
    heading(fig, title, "2005–2024", "section_year.csv")
    groups, values = (data.groups, data.sections) if flow == "Export" else (data.import_groups, data.import_sections)
    export_peak = max(v for (_, direction, _), v in data.sections.items() if direction == "Export")
    limit = float(max(export_peak, max(data.import_sections.values())) / 1_000_000_000) * 1.08
    for group, marker in zip(groups, HS_MARKS):
        ax.plot(YEARS, [float(values[y, flow, group] / 1_000_000_000) for y in YEARS],
                color=HS_COLORS[group], marker=marker, label=HS_LABELS[group])
    value_axis(ax, limit, f"{TRADE_FLOW_LABELS[flow]} (tỷ USD)")
    legend_above(ax)
    rows = [[format_year(y), *[format_value(values[y, flow, code]) for code in groups]] for y in YEARS]
    add_table(table, ["Năm", *map(section_heading, groups)], rows)
    return fig


def plot_c02a(data):
    """Return the 100% stacked export composition figure."""
    with apply_style():
        return composition(data, "Export", "C02A · Cơ cấu xuất khẩu theo phần HS")


def plot_c02b(data):
    """Return the 100% stacked import composition figure."""
    with apply_style():
        return composition(data, "Import", "C02B · Cơ cấu nhập khẩu theo phần HS")


def plot_c02c(data):
    """Return the six-series export figure."""
    with apply_style():
        return section_trends(data, "Export", "C02C · Kim ngạch xuất khẩu theo phần HS")


def plot_c02d(data):
    """Return the six-series import figure."""
    with apply_style():
        return section_trends(data, "Import", "C02D · Kim ngạch nhập khẩu theo phần HS")


def plot_c02e(data):
    """Return the two-panel trade-flow figure for HS84 and HS85."""
    with apply_style():
        fig = Figure(figsize=(11, 12))
        axes = fig.subplots(2, 2, sharey="row", gridspec_kw={"height_ratios": (3, 4.2)})
        fig.subplots_adjust(left=.09, right=.94, bottom=.085, top=.79, hspace=.35, wspace=.2)
        heading(fig, "C02E · Kim ngạch xuất nhập khẩu HS84 và HS85", "2005–2024", "product_year.csv")
        limit = float(max(v for (_, _, code), v in data.products.items() if code in CHAPTERS) / 1_000_000_000) * 1.08
        for code, ax, table in zip(CHAPTERS, *axes):
            ax.set_title(f"HS{code}")
            for flow in TRADE_FLOW_ORDER:
                ax.plot(YEARS, [float(data.products[y, flow, code] / 1_000_000_000) for y in YEARS],
                        color=TRADE_FLOW_COLORS[flow], linestyle=TRADE_FLOW_LINESTYLES[flow],
                        marker=TRADE_FLOW_MARKERS[flow], label=TRADE_FLOW_LABELS[flow])
            value_axis(ax, limit, "Kim ngạch (tỷ USD)" if code == CHAPTERS[0] else "")
            rows = [[format_year(y), *[format_value(data.products[y, flow, code]) for flow in TRADE_FLOW_ORDER]] for y in YEARS]
            add_table(table, ["Năm", *[TRADE_FLOW_LABELS[f] for f in TRADE_FLOW_ORDER]], rows)
        handles, labels = axes[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, ncols=2, loc="upper center", bbox_to_anchor=(.5, .88))
        return fig
