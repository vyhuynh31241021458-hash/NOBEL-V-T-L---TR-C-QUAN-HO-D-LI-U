from pathlib import Path
from unittest import TestCase
import warnings

import matplotlib
from matplotlib import font_manager
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ft2font import FT2Font

from house_style import apply_style
from house_style.theme import AXIS_LABEL_GAP
from house_style.typography import (
    ANNOTATION, AXIS_TEXT_COLOR, AXIS_TEXT_WEIGHT, DIRECT_LABEL, EDITORIAL_FONTS,
    FONT_DIR, KPI, SANS_FONTS, SOURCE, SUBTITLE,
)

VIETNAMESE = (
    "aàáảãạăằắẳẵặâầấẩẫậeèéẻẽẹêềếểễệiìíỉĩị"
    "oòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵđ"
)
DATA_SYMBOLS = "0123456789%−+-.,:/()×₫–—"


class TypographyTests(TestCase):
    def test_axis_labels_and_ticks_share_style_and_equal_gaps(self):
        with apply_style():
            fig = Figure(dpi=144)
            canvas = FigureCanvasAgg(fig)
            ax = fig.subplots()
            ax.set(
                xlabel="Năm", ylabel="Tỷ USD danh nghĩa",
                xlim=(0, 1), ylim=(100, 140), xticks=[0, 1], yticks=[100, 120, 140],
            )
            canvas.draw()
            renderer = canvas.get_renderer()
            gap = renderer.points_to_pixels(AXIS_LABEL_GAP)
            for axis, ticks in ((ax.xaxis, ax.get_xticklabels()), (ax.yaxis, ax.get_yticklabels())):
                for label in (axis.label, *ticks):
                    self.assertEqual(label.get_color(), AXIS_TEXT_COLOR)
                    self.assertEqual(label.get_fontweight(), AXIS_TEXT_WEIGHT)
                    self.assertEqual(tuple(label.get_fontfamily()), SANS_FONTS)

            x_ticks = [label.get_window_extent(renderer) for label in ax.get_xticklabels()]
            x_label = ax.xaxis.label.get_window_extent(renderer)
            y_ticks = [label.get_window_extent(renderer) for label in ax.get_yticklabels()]
            y_label = ax.yaxis.label.get_window_extent(renderer)
            self.assertAlmostEqual(ax.bbox.y0 - max(box.y1 for box in x_ticks), gap)
            self.assertAlmostEqual(min(box.y0 for box in x_ticks) - x_label.y1, gap)
            self.assertAlmostEqual(ax.bbox.x0 - max(box.x1 for box in y_ticks), gap)
            self.assertAlmostEqual(min(box.x0 for box in y_ticks) - y_label.x1, gap)

    def test_font_roles_and_context(self):
        before = list(matplotlib.rcParams["font.family"])
        with apply_style():
            self.assertEqual(tuple(matplotlib.rcParams["font.family"]), SANS_FONTS)
            self.assertEqual(matplotlib.rcParams["axes.titlelocation"], "center")
            for role in (DIRECT_LABEL, KPI, SOURCE):
                self.assertEqual(role["fontfamily"], SANS_FONTS)
            for role in (SUBTITLE, ANNOTATION):
                self.assertEqual(role["fontfamily"], EDITORIAL_FONTS)
            for role in (SUBTITLE, ANNOTATION, SOURCE):
                self.assertEqual(role["ha"], "center")
        self.assertEqual(matplotlib.rcParams["font.family"], before)

    def test_bundled_faces_and_glyph_coverage(self):
        cases = (
            (SANS_FONTS[0], "normal", "BricolageGrotesque-Regular.ttf"),
            (SANS_FONTS[0], "medium", "BricolageGrotesque-Medium.ttf"),
            (SANS_FONTS[0], "bold", "BricolageGrotesque-Bold.ttf"),
            (EDITORIAL_FONTS[0], "normal", "Platypi.ttf"),
        )
        required = VIETNAMESE + VIETNAMESE.upper() + DATA_SYMBOLS
        with apply_style():
            for family, weight, filename in cases:
                with self.subTest(family=family, weight=weight):
                    properties = font_manager.FontProperties(family=[family], weight=weight)
                    path = font_manager.findfont(properties, fallback_to_default=False)
                    self.assertEqual(Path(path).resolve(), (FONT_DIR / filename).resolve())
                    face = FT2Font(path)
                    missing = sorted({char for char in required if not face.get_char_index(ord(char))})
                    self.assertEqual(missing, [])

    def test_render_axes_and_editorial_text_without_missing_glyphs(self):
        with apply_style(), warnings.catch_warnings():
            warnings.filterwarnings("error", message=r"Glyph .* missing from font")
            fig = Figure()
            canvas = FigureCanvasAgg(fig)
            ax = fig.subplots()
            ax.plot([0, 1], [-2, 3], label="Xuất khẩu")
            ax.set(xlabel="Tháng", ylabel="Tỷ USD", title="Cán cân thương mại")
            ax.legend()
            ax.annotate("Chênh lệch −12.5%", (0, 0), **ANNOTATION)
            fig.text(0.5, 0.95, "Giá khảo sát · 125,000 ₫", **SUBTITLE)
            fig.text(0.5, 0.02, "Nguồn: Dữ liệu minh họa", **SOURCE)
            canvas.draw()
