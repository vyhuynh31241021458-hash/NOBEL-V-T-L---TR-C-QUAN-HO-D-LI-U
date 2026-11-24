from pathlib import Path
from unittest import TestCase
import warnings

import matplotlib
from matplotlib import font_manager
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ft2font import FT2Font

from house_style import apply_style
from house_style.typography import (
    ANNOTATION, DIRECT_LABEL, EDITORIAL_FONTS, FONT_DIR, KPI, SANS_FONTS, SOURCE, SUBTITLE,
)

VIETNAMESE = (
    "aàáảãạăằắẳẵặâầấẩẫậeèéẻẽẹêềếểễệiìíỉĩị"
    "oòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵđ"
)
DATA_SYMBOLS = "0123456789%−+-.,:/()×₫–—"


class TypographyTests(TestCase):
    def test_font_roles_and_context(self):
        before = list(matplotlib.rcParams["font.family"])
        with apply_style():
            self.assertEqual(tuple(matplotlib.rcParams["font.family"]), SANS_FONTS)
            for role in (DIRECT_LABEL, KPI, SOURCE):
                self.assertEqual(role["fontfamily"], SANS_FONTS)
            for role in (SUBTITLE, ANNOTATION):
                self.assertEqual(role["fontfamily"], EDITORIAL_FONTS)
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
            fig.text(0.05, 0.95, "Giá khảo sát · 125,000 ₫", **SUBTITLE)
            fig.text(0.05, 0.02, "Nguồn: Dữ liệu minh họa", **SOURCE)
            canvas.draw()
