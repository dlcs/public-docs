# Recipe: from images to a searchable Manifest

The runnable code for the [searchable-manifest recipe](https://dlcs.github.io/public-docs/recipes/searchable-manifest/).
Run each step from the `dlcs-docs-client` directory:

```
python -m recipes.searchable_manifest.step_01_register_assets
python -m recipes.searchable_manifest.step_02_generate_alto
python -m recipes.searchable_manifest.step_03_create_manifest
python -m recipes.searchable_manifest.step_04_inspect_results
python -m recipes.searchable_manifest.step_05_adopt_existing_manifest
```

Step 2 needs **Tesseract** (the recipe's swappable OCR engine — see `ocr.py`):

- Windows: `winget install UB-Mannheim.TesseractOCR` (then set `TESSERACT` to
  `C:\Program Files\Tesseract-OCR\tesseract.exe` if it is not on your PATH)
- macOS: `brew install tesseract`
- Debian/Ubuntu: `apt install tesseract-ocr`

The fixture images and pre-generated ALTO live in the docs site at
`doc_fixtures/recipes/energy-index/` — steps 1 and 3 fetch them from the
published site, so the recipe runs without you having to stage anything.
When you adapt it, your images and your OCR output need to be at HTTP(S)
locations the platform can fetch from.
