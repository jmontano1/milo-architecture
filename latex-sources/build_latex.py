#!/usr/bin/env python3
"""Build single-column LaTeX PDFs for the 5 MILO architectural manuscripts."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

PUB = Path("/Users/jorgemontano/Desktop/MILO/Publications")
WORK = Path("/tmp/singlecol-latex")
FIG_DIR = WORK / "figures"
SRC_DIR = WORK / "sources"
OUT_DIR = WORK / "outputs"
SRC_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

PANDOC = str(Path.home() / "bin" / "pandoc")
TECTONIC = str(Path.home() / "bin" / "tectonic")

ARTICLES = [
    (1, "MILO_Article_01_ThermalEntropy_DRAFT.md", "article1-singlecol"),
    (2, "MILO_Article_02_LatencyAuth_DRAFT.md", "article2-singlecol"),
    (3, "MILO_Article_03_SupervisoryPrimacy_DRAFT.md", "article3-singlecol"),
    (4, "MILO_Article_04_GoverningPrinciples_DRAFT.md", "article4-singlecol"),
    (5, "MILO_Article_05_AdaptiveResilience_DRAFT.md", "article5-singlecol"),
]


def parse_front_matter(text):
    front = {}
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            front = yaml.safe_load(text[4:end])
            body = text[end + 5:]
    # Cut to start from "## Abstract"
    idx = body.find("## Abstract")
    if idx >= 0:
        body = body[idx:]
    return front, body


def postprocess_latex(tex: str, fig_filename: str) -> str:
    """Tweak pandoc-emitted LaTeX for our single-column template."""
    # Drop pandoc's auto-numbering of headings (we use real numbering in text)
    # Convert \subsection{Abstract} -> abstract environment
    m = re.search(r"\\subsection\{Abstract\}\\label\{abstract\}\s*", tex)
    if m:
        # Find the abstract body and Keywords block
        kw_m = re.search(r"\\textbf\{Keywords:\}\s*(.+?)(?:\.\s*)?\n\n", tex, re.DOTALL)
        if kw_m:
            abs_body = tex[m.end():kw_m.start()].strip()
            kw = kw_m.group(1).strip().rstrip(".")
            kw = re.sub(r"\\emph\{(.*?)\}", r"\1", kw)
            replacement = (
                "\\begin{abstract}\n\\noindent " + abs_body + "\n\\end{abstract}\n\n"
                "\\noindent\\textbf{Keywords:} " + kw + "\\par\n\n"
            )
            tex = tex[:m.start()] + replacement + tex[kw_m.end():]

    # Strip pandoc-emitted bold-paragraph metadata that duplicates the title page
    for prefix in ("Subtitle:", "Author:", "Publication date:"):
        tex = re.sub(
            r"\\textbf\{" + re.escape(prefix) + r"\}.*?\n\n",
            "",
            tex,
            flags=re.DOTALL,
        )
    tex = re.sub(
        r"\\textbf\{\\textasciitilde MILO\\texttrademark\{\}\}.*?\n\n",
        "",
        tex,
        flags=re.DOTALL,
    )

    # Replace any surviving FIGURE_1 marker (we usually replace it in the
    # markdown before pandoc runs, but this is a fallback)
    fig_pattern = re.compile(r"\{?\[FIGURE\\?_1\]?\}?", re.IGNORECASE)
    fig_block = (
        "\\begin{figure}[!t]\n"
        "\\centering\n"
        "\\includegraphics[width=\\linewidth]{" + fig_filename + "}\n"
        "\\end{figure}\n"
    )
    tex = fig_pattern.sub(lambda m: fig_block, tex)

    # Replace pandoc-style citations {[}N{]} with \cite{refN}
    # First, anchor references in the bibliography section
    # Find each [N] entry as a paragraph leading with {[}N{]}
    ref_section_pattern = re.compile(r"(\\section\{References\}.*?)(?=\\section\{|\Z)", re.DOTALL)
    rm = ref_section_pattern.search(tex)
    if rm:
        ref_block = rm.group(1)
        # Convert "[N] ..." paragraphs into thebibliography
        entries = re.findall(r"\{\[\}(\d+)\{\]\}\s*(.+?)(?=\n\n\{\[\}|\Z)", ref_block, re.DOTALL)
        if entries:
            new_ref_block = "\\section*{References}\n\\begin{thebibliography}{99}\n"
            for num, content in entries:
                content = re.sub(r"\s+", " ", content).strip()
                new_ref_block += f"\\bibitem{{ref{num}}} {content}\n"
            new_ref_block += "\\end{thebibliography}\n"
            tex = tex.replace(ref_block, new_ref_block)

    # Replace inline {[}N{]} with \cite{refN}
    tex = re.sub(r"\{\[\}(\d+)\{\]\}", r"\\cite{ref\1}", tex)

    # Tables: pandoc emits longtable; convert simple longtables to regular table
    # For Article 2's latency table we already injected raw LaTeX in the markdown
    # (article2 uses our pre-built \begin{table*}...) so it should pass through.

    # Strip pandoc-emitted \hypertarget anchors (we use hyperref directly)
    tex = re.sub(r"\\hypertarget\{[^}]+\}\{%\n", "", tex)
    tex = re.sub(r"^\}\n", "", tex, flags=re.MULTILINE)

    # Clean any leftover {} pairs from removed anchors
    tex = re.sub(r"^\}\s*$\n?", "", tex, flags=re.MULTILINE)

    return tex


def build_one(article_num, md_filename, output_stem):
    print(f"\n=== Building {output_stem} ===")
    text = (PUB / md_filename).read_text(encoding="utf-8")
    front, body = parse_front_matter(text)

    # Hand-replace the FIGURE_1 marker BEFORE pandoc — we will inject raw LaTeX
    # for the figure. Pandoc passes raw LaTeX through unchanged.
    fig_name = f"figures/article{article_num}-fig1.pdf"
    body = body.replace(
        "[FIGURE_1]",
        f"\\begin{{figure}}[t]\n\\centering\n\\includegraphics[width=\\linewidth]{{{fig_name}}}\n\\end{{figure}}",
    )

    # For Article 2, replace the markdown latency table with hand-written LaTeX
    # (same approach used for the IEEEtran build).
    if article_num == 2:
        latex_table = (
            "\n\\begin{table}[t]\n"
            "\\caption{Operational Latency Budgets in Industrial Domains and Authentication Compatibility.}\n"
            "\\label{tab:latency}\n"
            "\\centering\n"
            "\\renewcommand{\\arraystretch}{1.2}\n"
            "\\begin{tabular}{p{0.28\\linewidth} p{0.20\\linewidth} p{0.44\\linewidth}}\n"
            "\\toprule\n"
            "\\textbf{Industrial Domain} & \\textbf{Typical Latency Budget} & \\textbf{Authentication Compatibility} \\\\\n"
            "\\midrule\n"
            "Motion control (servo loops) & 100 $\\mu$s -- 1 ms per loop & No authentication compatible per loop; session-level only with structural override \\\\\n"
            "PLC scan cycle (logic execution) & 1--10 ms per scan & Lightweight pre-execution log compatible; cryptographic handshake incompatible \\\\\n"
            "Machine vision inspection (high-speed line) & 5--50 ms per item & Lightweight gate compatible; full MFA incompatible \\\\\n"
            "HMI operator interaction & 100--2000 ms per action & Full MFA / human-perceptible challenge compatible \\\\\n"
            "Supervisory control / SCADA reconfiguration & 1--10 s per action & Deliberate authorization gate compatible; full MFA with audit trail \\\\\n"
            "Production schedule / recipe change & 10--60 s per action & Multi-party authorization gate compatible; institutional review \\\\\n"
            "\\bottomrule\n"
            "\\end{tabular}\n"
            "\\end{table}\n\n"
        )
        body = re.sub(
            r"^\| Industrial Domain.*?\n(?:\|.*?\n)+",
            lambda m: latex_table,
            body,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )

    # Write the cleaned markdown to a temp file
    md_path = WORK / "body.md"
    md_path.write_text(body, encoding="utf-8")

    # Build dir for this article (so we don't share figures/ symlinks)
    build_dir = WORK / f"build-{output_stem}"
    build_dir.mkdir(exist_ok=True)
    # Copy figures into the build dir
    fig_dst = build_dir / "figures"
    fig_dst.mkdir(exist_ok=True)
    shutil.copy(FIG_DIR / f"article{article_num}-fig1.pdf", fig_dst / f"article{article_num}-fig1.pdf")

    # Run pandoc
    body_tex = build_dir / "body.tex"
    subprocess.run(
        [PANDOC, "-f", "markdown", "-t", "latex", "-o", str(body_tex), str(md_path)],
        check=True,
    )

    # Post-process body.tex
    body_tex.write_text(postprocess_latex(body_tex.read_text(), fig_name))

    # Build the main.tex by substituting macros in template.tex
    template = (WORK / "template.tex").read_text()
    title = front.get("title", "")
    subtitle = front.get("subtitle", "")
    description = front.get("description", "")
    keywords = front.get("keywords", [])
    if isinstance(keywords, list):
        keywords_str = ", ".join(keywords)
    else:
        keywords_str = str(keywords)
    # Truncate title for running header
    header = title[:80] + ("..." if len(title) > 80 else "")
    main_tex = (
        template
        .replace("\\newcommand{\\milotitle}{TITLE}", "\\newcommand{\\milotitle}{" + title.replace("&", r"\&") + "}")
        .replace("\\newcommand{\\milosubtitle}{SUBTITLE}", "\\newcommand{\\milosubtitle}{" + subtitle.replace("&", r"\&") + "}")
        .replace("PDFTITLE", title.replace("&", r"\&"))
        .replace("PDFKEYWORDS", keywords_str.replace("&", r"\&"))
        .replace("PDFSUBJECT", description.replace("&", r"\&"))
        .replace("HEADTITLE", header.replace("&", r"\&"))
    )
    (build_dir / "main.tex").write_text(main_tex)

    # Compile via tectonic
    result = subprocess.run(
        [TECTONIC, "-X", "compile", "main.tex"],
        cwd=build_dir, capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  COMPILE FAILED:\n{result.stdout[-1500:]}\n{result.stderr[-500:]}")
        return None

    # Copy the output PDF to OUT_DIR
    out_pdf = OUT_DIR / f"{output_stem}.pdf"
    shutil.copy(build_dir / "main.pdf", out_pdf)
    # Also stage the LaTeX source bundle
    src_bundle = SRC_DIR / output_stem
    src_bundle.mkdir(exist_ok=True)
    shutil.copy(build_dir / "main.tex", src_bundle / "main.tex")
    shutil.copy(build_dir / "body.tex", src_bundle / "body.tex")
    shutil.copytree(build_dir / "figures", src_bundle / "figures", dirs_exist_ok=True)

    # Count pages
    from pypdf import PdfReader
    pages = len(PdfReader(str(out_pdf)).pages)
    print(f"  → {out_pdf}  ({pages} pages)")
    return out_pdf


def main():
    for article_num, md_name, stem in ARTICLES:
        build_one(article_num, md_name, stem)


if __name__ == "__main__":
    main()
