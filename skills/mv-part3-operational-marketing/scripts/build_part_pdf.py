#!/usr/bin/env python3
"""
build_part_pdf.py
Construye el PDF de una parte a partir del Markdown del análisis y la carpeta de gráficos.

Uso:
    python build_part_pdf.py --md part1_output.md --charts charts/ --output part1_output.pdf
"""

import argparse
import sys
from pathlib import Path


def md_to_pdf(md_path: Path, charts_dir: Path, pdf_path: Path) -> None:
    """Convertir markdown a PDF usando markdown + weasyprint."""
    try:
        import markdown
        from weasyprint import HTML, CSS
    except ImportError:
        sys.stderr.write("Faltan dependencias. Instalar: pip install markdown weasyprint\n")
        sys.exit(2)

    md_text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "attr_list"]
    )

    css = CSS(string="""
        @page {
            size: A4;
            margin: 2cm 2cm 2.2cm 2cm;
            @bottom-center {
                content: counter(page) " / " counter(pages);
                font-size: 9pt;
                color: #888;
            }
        }
        body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #1a1a1a;
        }
        h1 {
            font-size: 18pt;
            color: #0b3a6e;
            border-bottom: 2px solid #0b3a6e;
            padding-bottom: 4pt;
            margin-top: 22pt;
            page-break-before: auto;
        }
        h2 {
            font-size: 14pt;
            color: #0b3a6e;
            margin-top: 16pt;
            page-break-after: avoid;
        }
        h3 {
            font-size: 12pt;
            color: #2c3e50;
            margin-top: 12pt;
            page-break-after: avoid;
        }
        h4 {
            font-size: 10.5pt;
            color: #444;
            margin-top: 10pt;
            page-break-after: avoid;
        }
        p { margin: 6pt 0; text-align: justify; }
        table {
            border-collapse: collapse;
            width: 100%;
            font-size: 9pt;
            margin: 10pt 0;
            page-break-inside: avoid;
        }
        th, td {
            border: 1px solid #cfcfcf;
            padding: 5pt 7pt;
            text-align: left;
            vertical-align: top;
        }
        th {
            background-color: #eef2f7;
            font-weight: bold;
            color: #0b3a6e;
        }
        tr:nth-child(even) td { background-color: #fafbfc; }
        code {
            background-color: #f4f4f4;
            padding: 1pt 4pt;
            font-size: 9pt;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10pt;
            font-size: 8.5pt;
            white-space: pre-wrap;
            border-left: 3px solid #0b3a6e;
            page-break-inside: avoid;
        }
        blockquote {
            border-left: 3px solid #0b3a6e;
            padding-left: 12pt;
            color: #444;
            margin: 10pt 0;
            font-style: italic;
        }
        img {
            max-width: 100%;
            page-break-inside: avoid;
            display: block;
            margin: 10pt auto;
        }
        ul, ol { margin: 6pt 0; padding-left: 24pt; }
        li { margin: 3pt 0; }
        hr { border: none; border-top: 1px solid #ccc; margin: 16pt 0; }
    """)

    full_html = f"""
    <html><head><meta charset='utf-8'></head>
    <body>{html_body}</body></html>
    """

    base_url = str(md_path.parent)
    HTML(string=full_html, base_url=base_url).write_pdf(str(pdf_path), stylesheets=[css])
    print(f"PDF generado: {pdf_path}")


def main():
    parser = argparse.ArgumentParser(description="Construir PDF de una parte del análisis.")
    parser.add_argument("--md", required=True, type=Path, help="Ruta al archivo Markdown.")
    parser.add_argument("--charts", required=False, type=Path, default=None, help="Carpeta de gráficos (PNG).")
    parser.add_argument("--output", required=True, type=Path, help="Ruta de salida del PDF.")
    args = parser.parse_args()

    if not args.md.exists():
        sys.stderr.write(f"No se encuentra el Markdown: {args.md}\n")
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    md_to_pdf(args.md, args.charts, args.output)


if __name__ == "__main__":
    main()
