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
