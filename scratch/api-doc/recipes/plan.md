# Recipes section — plan + spike state (2026-09-13)

> **✅ BUILD COMPLETE 2026-09-14**: page live at `recipes/searchable-manifest.mdx` (Recipes sidebar
> group in astro.config); five step scripts + `ocr.py` (pluggable) + README in
> `dlcs-docs-client/recipes/searchable_manifest/`; steps 1–4 ran green on stage; showcase manifest
> kept live at `/15/manifests/energy-index` (search "energy"=24, "pressure"=16, xywh targets);
> pipelines.mdx ALTO-only correction applied; CLAUDE.md Recipes conventions added; #672 sweep done.
> **NEW BUG found + raised: iiif-presentation #677** — see "Monday regression" below.

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


## SPIKE RESULTS (2026-09-14, stage v0.10.0, all fixtures cleaned + #672 sweep done)

1. **One-call flow WORKS (Spike A)**: a single PUT with `paintedResources[].asset.adjuncts` + `pipeline`
   → 202; adjuncts created on the asset; pipeline Completed; public manifest has seeAlso, the inline
   annotations page, and the search service. Jack's "(4)–(6) combined" confirmed. THE RECIPE CORE.
2. **THE PDF EXISTS AND IS FETCHABLE TODAY** — the probe found text-services' real public routes are
   **v1**: `pdf/v1/{c}/iiif/{manifestId}` → 200 application/pdf (real text layer, Tj ops present);
   also unsurfaced: `text/v1/…` (full plain text) and `annotations/manifest/v1/…` (W3C annos, JSON-LD),
   plus per-page `annotations/lines/v1/{n}/…` and `annotations/words/v1/{n}/…` and
   `identified/figures/…` (routes read from the dlcs/text-services repo, now cloned locally).
   **The gap is purely link-surfacing in TextManifestAugmentor** (it merges SearchService2 only, though
   the builder job already requests JobServices.All).
3. **Plain-text adjuncts are NOT indexed — ALTO only.** Search hits for ALTO words (chapter=4,
   Nutrition=1) but zero for words unique to an attached text/plain adjunct, across two runs.
   ⚠ CORRECTS pipelines.mdx ("their ALTO and plain-text Adjuncts") — fix on this branch. Recipe
   guidance: your pluggable OCR should emit ALTO for search/PDF; plain text still displays as an
   inline annotation but doesn't feed the index.
4. **Adjunct-after-save (Spike B)**: NOT expressed without a re-save (Tom's suspicion confirmed);
   the regeneration nudge = re-PUT with placeholder canvases + the same paintedResources (canvasId =
   items ids) → 200, adjunct expressed. Friction: no lightweight "regenerate" operation — full update dance.
5. **Jules pathway (Spike C) — fully proven**:
   - Items-only manifest with DLCS image-service bodies: the platform DID recognise the asset (derived
     PR carries `asset`) — but the pipeline is `CompletedNoOperation` ("No text resources found") even
     when the asset HAS an ALTO adjunct: text-services reads the STORED manifest's text links, and an
     authored items-only manifest has none. So "doesn't run on items" in effect.
   - **ADOPTION in one update**: stripped placeholder canvases (authored ids kept) + paintedResources
     with `canvasId` = the authored canvas ids + pipeline → 202; **no reingest** (asset batch
     unchanged); **public canvas ids preserved** (authored ids kept — annotations elsewhere stay
     valid); seeAlso expressed; search live; **pdf/v1 200**. This is the recipe's variant-2 script.

## Monday regression (2026-09-14): adoption path stopped indexing → iiif-presentation #677
Spike C's adoption indexed on Sunday (Completed, hits, pdf/v1 200). On Monday EVERY no-ingest
("built upfront") pipeline submission finishes **CompletedNoOperation** (zero words) with search 404,
despite seeAlso present on the public manifest. Six variants tried (plain adoption; restated inline
adjuncts; initial-save-with-pipeline→adopt/reprocess; adopt→second save; NEW adjunct inline during
adoption; asset-level adjunct first = Sunday's exact shape) — all NoOperation. Greenfield batch-ingest
path (deferred submission) still indexes fine. Code trail: ManifestWriteService.SaveToS3 submits
immediately after staging write on canBeBuiltUpfront; TextBuilderClient points text-services at the
STAGING S3 copy; TotalWordCount==0 → CompletedNoOperation. Likely staging/expression ordering race or
post-outage env change. **Raised as https://github.com/dlcs/iiif-presentation/issues/677**; step_05
and the page's adoption section carry honest caution notes citing it.

## Gap summary for Jack — FINAL (delivered 2026-09-14)
1. **Surface the text-services links on the manifest** (top priority per PO): PDF as `rendering`,
   full text + W3C annotations as canvas/manifest links — everything is already generated and served
   at `pdf/v1` / `text/v1` / `annotations/*/v1`; only TextManifestAugmentor needs extending. The
   recipe's "searchable PDF" section is written as-if-surfaced with a removable caution Aside.
2. **Adoption path can't be relied on for search today** (iiif-presentation #677): text pipeline
   completes NoOperation on the no-ingest path — this is THE Jules/DEL-131 scenario, so it sits just
   below (or beside) item 1 in priority.
3. Plain-text (text/plain) adjuncts not indexed by text-services — ALTO only (docs corrected; is
   plain-text indexing intended?).
4. **No lightweight manifest regeneration after asset-level adjunct changes.** A stored manifest is
   only enriched *when it is saved*: if a customer later adds or replaces an adjunct through the
   asset-level adjuncts API (e.g. re-running OCR with a better engine), the stored/public manifest
   does not change — no new `seeAlso`, no re-index — even though the asset now carries the new text
   (wire-proven, spike result 4). The only remedy today is a full manifest update: GET the manifest
   for its ETag, re-PUT the whole body (placeholder canvases + the same paintedResources + the
   pipeline again). That works but is a heavy dance for "my text changed, please refresh" — the
   client must reconstruct and resend a body that says nothing new. A lightweight nudge — e.g. a
   `POST {manifest}/regenerate`, or a pipeline action like `{"name": "text", "config": {"action":
   "Refresh"}}` accepted without a body change, or automatic re-expression when an adjunct on a
   manifest-tracked asset changes — would make OCR improvement a one-call operation. Matters most
   at scale: re-OCR of a whole collection means re-PUTting every manifest.
5. Byte-POST adjuncts (#1140) — recipes must pre-stage OCR output at an HTTP origin.
6. OCR-as-pipeline (the recipe's pluggable step is the placeholder for it).
7. Copy-back workflow (variant 3) remains awkward by design; adoption (variant 2) is smooth —
   once #677 is fixed.
