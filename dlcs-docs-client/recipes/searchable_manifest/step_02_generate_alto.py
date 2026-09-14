"""Step 2: generate METS-ALTO for each page - THE PLUGGABLE STEP.

This runs the OCR locally (see ocr.py to plug in your own engine) and writes
one ALTO file per page into out/. In your own workflow the next step is to
stage these files at any HTTP(S) location the platform can fetch from; this
recipe's later steps use the copies published with the documentation site.
"""
from pathlib import Path
from recipes.searchable_manifest.ocr import generate_alto
from recipes.searchable_manifest.recipe_settings import PAGES, LOCAL_FIXTURES

out_dir = Path(__file__).parent / "out"
out_dir.mkdir(exist_ok=True)

for page in PAGES:
    image = LOCAL_FIXTURES / f"{page}.jpg"
    alto_xml = generate_alto(image)
    out_file = out_dir / f"{page}.xml"
    out_file.write_text(alto_xml, encoding="utf-8")
    words = alto_xml.count("<String ")
    print(f"{image.name} -> {out_file.name} ({words} words)")
