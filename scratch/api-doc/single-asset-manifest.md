# Examples section

Added all six examples based on the documentation and observed image service URL patterns
from real platform output. The image service and thumbnail URL patterns are confirmed correct
(`iiif-img/v2/{customer}/{space}/{asset}` for ImageService2, `iiif-img/{customer}/{space}/{asset}`
for ImageService3, etc.). The AV and file delivery URL patterns are illustrative — verify
against real AV and file-channel assets when the platform is available.

# Manifest URL and asset.manifest

The asset doesn't yet expose a link to the single asset manifest:

```
"manifest": "https://dlcs.io/iiif-manifest/2/5/b2921371x_0001.jp2"
```

```
https://dlcs.example/iiif-manifest/{customer}/{space}/{assetId}
```

# Note on iiif-av Choice resource — ⟳ ANSWERED by code, and the docs are wrong (2026-08-03, DIS-25)

Line 17 of the original had `(?)` after the note that the iiif-av painting annotation body is "always a Choice resource, even if there is only one output". This was an open question from the original author — confirm whether this is intentional.

**Answer** (`ManifestV3Builder.HandleTimebasedAsset:303-309`): a single transcode gets
a **bare `Sound`/`Video` body**; `PaintingChoice` only when there is more than one.
The live page's prose AND its "Audio with iiif-av" example (Choice wrapping one
output) are wrong. Also undocumented anywhere: an iiif-av asset with **no** transcode
metadata gets **no canvas at all** (:283-287). See DIS-25 — fix docs, or rule
always-Choice is the intended contract and change code.

# Adjunct auth services (PROV-23, captured 2026-08-03) — restore-candidate for when adjunct access control lands

Old-doc clause dropped in the port, verified NOT implemented (adjunct entries carry
no `Service` — `ManifestV3Builder.CreateExternalResource:495-566`):

> "Any adjuncts are listed as seeAlso properties of the Canvas, _with auth services
> if they have them_."

Ties to ADJ-03 (adjunct roles unimplemented). When adjunct auth exists, the manifest
builder must express services on adjunct entries — this is the only record of that
requirement.

# Example scenario coverage narrowed (PROV-24, noted 2026-08-03) — folds into DIS-19

The old page's (empty) example headings promised: video + two adjuncts; image with
image service + thumbnail + **file outputs** + three adjuncts; Word document on file
channel + one adjunct. The new example set has no video+adjuncts case, no
channel-combination case (which exercises the rendering-alongside-painting path in
`GetCanvasForAsset`), and its file-only example has no adjunct. Low priority; part of
DIS-19's example-verification debt.

# Source reference

The behaviour for file-only assets (placeholder image, `placeholder` and `original` behaviors) was sourced from https://github.com/wellcomecollection/docs/pull/77


# dlcs:channelOutputs

removed from copy:

In addition to the above, the single asset manifest has an extension property `dlcs:channelOutputs`: an array of content resources and services, one per delivery channel output, each including the channel it belongs to. This is more consistent in structure than the regular manifest properties and can be used for quick programmatic access to channel outputs.
## Replaced prose preserved (DIS-25, session 0, 2026-08-06)

Original iiif-av bullet (single-asset-manifest.mdx:27), replaced per the DIS-25 ruling:

> For the `iiif-av` delivery channel, the body of the painting annotation is a `Choice` resource listing all the transcoded outputs.

And the audio-example prose:

> The painting body is a `Choice` wrapping the single transcoded output.

**Why changed:** ManifestV3Builder.HandleTimebasedAsset uses a bare `Sound`/`Video`
body when `transcodes.Length == 1` and `PaintingChoice` only for several; an asset
with no transcode metadata gets no canvas at all. The old doc's own "(?)" question
is answered by the code in the opposite direction. The audio example's `Choice`
wrapper was removed and its annotation id corrected to `.../page/image` (the
builder uses `{canvasId}/page/image` for timebased assets too).

**Disposition: probably-drop** (superseded by code reality). Restore only if
always-Choice is ever made the contract (the room chose not to).

## DIS-19 verification pass — all examples now real platform output (2026-09-07)

The AV / file-delivery / adjunct / no-channels examples, previously marked "based on expected
platform behaviour", were verified against stage (customer 15, space 98765) and replaced with
real captured output (hostname/customer/space/asset ids substituted). Capture files:
`scratch/hygiene-sprint/dis-19-manifests/`. Corrections made:

- Canvas/AnnotationPage/Annotation ids always use the `/iiif-img/` route prefix, and the
  annotation id always ends `/page/image`, for every asset type (old examples showed
  `/iiif-av/` and `/iiif-manifest/` prefixes and `/page/video`).
- AV bodies: id is the parameterised transcode path (`/full/max/default.mp3`,
  `/full/full/max/max/0/default.mp4`), no `label`, `format` is the transcode media type
  (`audio/mp3`), duration in decimal seconds. Old examples showed preset-named ids
  (`/mp3-320`), labels ("MP3 320kbps") and codec/profile info — none emitted.
- Video `Choice`: outputs must use different containers; same-extension outputs share one
  storage key and produce identical ids (protagonist **#970** — caution Aside added; evidence
  assets `dis19-video` (broken) / `dis19-video-2` (correct) left on stage).
- File-only: `@context` becomes an array incl. the Wellcome born-digital extension context;
  placeholder body is `/static/{type}/placeholder.png` with 1000×1000 + format; rendering
  label auto-generated `File {c}/{s}/{id}` (old example invented a custom label).
- No delivery channels: **no canvas at all** (no `items` property) — old example showed an
  empty canvas with source dimensions. Same for iiif-av with no transcodes.
- Adjuncts: `provides`/`fileSize`/annotations-page `language` not emitted; scalar
  motivation/body/target (protagonist **#1299**).

Old "expected behaviour" JSON is in git history at tag/branch `hygiene/session-6` if ever needed.

Not yet wire-verified (left as prose claims): auth services inlined on image services and file
renderings for role-bearing assets (needs auth-configured assets; #538 territory).

## PROV-24 scenarios verified — 2026-09-07 (same-day follow-up, PO-directed)

The three example scenarios the old docs promised but the new page dropped were wire-verified
(captures `prov24-combo.json`, `prov24-video-adjuncts.json`, `prov24-file-adjunct.json` in
`scratch/hygiene-sprint/dis-19-manifests/`):

- **Channel combination** (`prov24-combo`: iiif-img + thumbs + file, kept on stage as a fixture):
  file rendering DOES appear alongside the real painting body, carrying the image's full
  dimensions + generated label — but **without** `behavior: ["original"]` and **without** the
  born-digital `@context` (both are file-only extras). **PO confirmed 2026-09-07: this is the
  intended behaviour** (as is identical adjunct placement on AV/placeholder canvases) — no issue
  needed. New "Image with iiif-img, thumbs and file" example added to the page (elided jsonc —
  delta from example 1); prose clarified.
- **Adjuncts on a video canvas** (dis19-video-2 + seeAlso/rendering adjuncts, deleted after
  capture): identical placement to image canvases; an `externalId` adjunct's URL is used verbatim
  as the rendering id.
- **Adjunct on a file-only canvas** (dis19-file-txt + seeAlso adjunct, deleted after capture):
  coexists with the file rendering; placeholder behaviors unaffected.

One sentence added to the page's adjuncts paragraph ("works the same way on every kind of
canvas"). PROV-24's "scenario coverage narrowed" debt is now cleared — the old doc's promised
coverage is either on the page or wire-confirmed prose.

Persistent fixtures kept on stage in space 98765 so future re-verification needs no re-transcode:
`dis19-file-txt`, `dis19-no-channels`, `dis19-audio`, `dis19-video`, `dis19-video-2`, plus
customer-15 iiif-av policies `dis19-video-choice` (two-mp4, demonstrates #970) and
`dis19-video-choice2` (mp4+webm). The four adjuncts on `put-example-1-rusty-boat` were deleted
after capture (the p13 sample expects to create them).
