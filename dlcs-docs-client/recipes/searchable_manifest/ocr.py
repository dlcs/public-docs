"""THE PLUGGABLE STEP.

This module is the recipe's only contact with an OCR engine. To use your own
text-generating process - a different OCR engine, HTR, a vision model, an
existing METS-ALTO archive - replace the body of generate_alto() with anything
that returns METS-ALTO XML for a page image.

ALTO is what feeds the platform's text pipeline: search, autocomplete and the
searchable PDF are built from ALTO word positions. (A plain-text adjunct will
display as an annotation, but is not indexed.)

As written, this uses Tesseract, which emits ALTO natively:

    tesseract page.jpg output_base alto

Install: https://tesseract-ocr.github.io/tessdoc/Installation.html
(Windows: winget install UB-Mannheim.TesseractOCR; macOS: brew install tesseract;
Debian/Ubuntu: apt install tesseract-ocr). If the binary is not on your PATH,
set the TESSERACT environment variable to its full location.
"""
import os
import subprocess
import tempfile
from pathlib import Path

TESSERACT = os.environ.get("TESSERACT", "tesseract")


def generate_alto(image_path) -> str:
    """Return METS-ALTO XML for the page image at image_path.

    Replace this implementation to plug in your own OCR/HTR/model.
    """
    with tempfile.TemporaryDirectory() as working_dir:
        output_base = Path(working_dir) / "page"
        subprocess.run(
            [TESSERACT, str(image_path), str(output_base), "alto"],
            check=True, capture_output=True
        )
        return (output_base.with_suffix(".xml")).read_text(encoding="utf-8")
