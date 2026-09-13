# Recipes section — plan + spike state (2026-09-13)

> **⏸ PAUSED Sunday 2026-09-13 on the stage outage. RESUME Monday: check stage `/version`; if up, run
> `dlcs-docs-client/_rspike.py` (local, uncommitted) and work the "Blocked: wire spike" checklist below,
> then bring the page skeleton to the PO.**

Origin: `idea.md` (Slack transcript, Delft/DEL-131). Goal: new top-level **Recipes** docs section;
first recipe = images → OCR text (adjuncts) → managed manifest → search services + searchable PDF.

## PO decisions (2026-09-13)
- Recipe is written **PDF-first**, with a removable caution Aside explaining that the PDF link is not
  yet surfaced on the manifest (target: when surfacing ships, maybe 0.11). Gap summary goes to Jack to
  prioritise — especially PDF surfacing.
- Recipes = top-level sidebar group after The API.
- OCR engine: **tesseract** (native ALTO via `tesseract page.jpg out alto`); the invocation lives in a
  dedicated `ocr.py` exposing `generate_alto(image_path) -> alto_xml` — THE pluggable step, one function
  body to replace with any OCR/HTR/model.

## Done (wire-independent)
- Fixtures committed: `doc_fixtures/recipes/energy-index/` — 8 pages of Wellcome b3343136x at full/max
  (**Public Domain Mark 1.0**; attribution README) + pre-generated Tesseract 5.4 ALTO in `alto/`
  (pages 3–6 dense text; 7–8 near-empty — realistic). Pre-staged so the recipe is runnable (adjunct
  origins on gh-pages) while the live-OCR step is still shown.
- Code recon (iiif-presentation, confirmed present in the v0.10.0 tag):
  - **Adjuncts at manifest save**: `paintedResources[].asset.adjuncts: [...]` (validated via
    AdjunctValidator; ingested with the manifest; EMPTY array = delete all that asset's adjuncts).
    Manifest-level `"adjuncts": [...]` also exists → rides on a stub asset
    (`{customer}/{stub-space}/Manifest_{id}`). So Jack's "(4)-(6) combined" is real — wire-verify.
  - **The text pipeline already requests `JobServices.All`** (Search|Autocomplete|FullText|Annotations|
    **Pdf**|TextAugmented|Figures) — text-services should be PRODUCING the PDF today;
    `TextManifestAugmentor` only surfaces SearchService2(+autocomplete). PDF surfacing = the gap.
  - Text-services job id = `{customer}/iiif/{resourceId}`; public routes observed: `search/v2/{jobId}`,
    `autocomplete/v2/{jobId}` on the public host. PDF probe candidates: `pdf/v2/`, `fulltext/v2/`,
    `text/v2/`, `annotations/v2/`, `figures/v2/`, `textaugmented/v2/`.

## Blocked: wire spike (stage outage 2026-09-13 — ALL stage hosts 503 at the LB: presentation-api,
## api., and the public host; possibly weekend scale-down — PO checking)
Script ready in `dlcs-docs-client/_rspike.py` (local, not committed). Checklist when stage returns:
1. **Spike A**: create manifest with inline `asset.adjuncts` + pipeline in ONE call → adjuncts created?
   expressed? pipeline Completed? (slug hyg7-rspike; cleans page_01 adjuncts after)
2. **PDF probe**: on the indexed manifest, GET the route candidates above — is the PDF fetchable
   (unofficially) today? Either answer feeds the gap summary.
3. **Spike B**: adjunct added AFTER manifest exists → confirm stored manifest does NOT refresh; verify
   the minimal regeneration nudge (re-PUT placeholders + same paintedResources).
4. **Spike C**: Jules scenario — items-only manifest with DLCS image-service bodies: (a) confirm no
   asset recognition + pipeline = CompletedNoOperation even when the asset HAS text adjuncts ("doesn't
   run on items"); (b) ADOPTION: update with stripped canvases (authored ids kept) + paintedResources
   with canvasId = authored ids → public canvas ids preserved, NO reingest (batch unchanged), adjuncts
   expressed, pipeline then Completed.
5. Sweep stale asset.manifests refs afterwards (#672).

## Then
- Skeleton of `recipes/searchable-manifest.mdx` to PO for approval; section-at-a-time build; numbered
  step scripts in `dlcs-docs-client/recipes/searchable_manifest/` (01_register_assets … run_all) +
  recipe README (tesseract install). New conventions → CLAUDE.md.
- **Gap summary for Jack** at the end (PO 2026-09-13): PDF surfacing (top), byte-POST adjuncts (#1140),
  OCR-as-pipeline (private-protagonist #13), regeneration-on-adjunct-change, items→paintedResources
  adoption ergonomics, copy-back workflow, canvas-level adjuncts on external manifests.
