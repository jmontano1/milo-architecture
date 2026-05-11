#!/usr/bin/env python3
"""Render the 5 architectural figures (defined in build_pdfs.py) to standalone
PDFs for inclusion in the single-column LaTeX template via \\includegraphics.
"""
import sys
from pathlib import Path

# Make build_pdfs.py importable
sys.path.insert(0, "/tmp")
import build_pdfs  # registers fonts as a side-effect of make_styles, but we call directly

from reportlab.graphics import renderPDF
from reportlab.lib.units import inch

# LaTeX content width with 1-inch margins on US letter = 6.5 inches = 468 pt
TARGET_WIDTH = 6.5 * inch

FIG_DIR = Path("/tmp/singlecol-latex/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def render_one(article_num: int, builder, output: Path):
    flowable = builder(TARGET_WIDTH)
    drawing = flowable.drawing
    out_path = str(output)
    renderPDF.drawToFile(drawing, out_path)
    return out_path


def main():
    build_pdfs.register_fonts()
    for n, builder in [
        (1, build_pdfs._fig_article_1),
        (2, build_pdfs._fig_article_2),
        (3, build_pdfs._fig_article_3),
        (4, build_pdfs._fig_article_4),
        (5, build_pdfs._fig_article_5),
    ]:
        out = FIG_DIR / f"article{n}-fig1.pdf"
        path = render_one(n, builder, out)
        print(f"  → {path}")


if __name__ == "__main__":
    main()
