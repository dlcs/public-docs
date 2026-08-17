# size-restrictions.mdx — parked material

This file was created in hygiene sprint session 2 (2026-08-12, card SPA-01). Until then
size-restrictions.mdx had no scratch twin (the page was written from behaviour tables, not
ported prose).

## openMaxWidth scenarios (SPA-01, ruled (b) 2026-08-12)

`openMaxWidth` and the substitute open image service are **not implemented** (no such
property on `Image.cs`; no substitute mechanism in Orchestrator). Ruling: docs describe
released behaviour only, so the openMaxWidth material below was removed from the live page
verbatim. The design work is now tracked as a protagonist ADR-writing ticket
([protagonist #1249](https://github.com/dlcs/protagonist/issues/1249)), companion to
[ADR 0010](https://github.com/dlcs/protagonist/blob/develop/docs/adr/0010-replace-maxunauthorised.md),
which deliberately scoped to `maxWidth`/`openFullMax` only — protagonist issue #306 promised
"`openMaxWidth` will be implemented in a future ticket", but that ticket was never created.
**Restore this material to the live page when the feature ships.** The companion prose
removed from asset.mdx at the same time is in [asset.md](./asset.md) (`## openMaxWidth`
section) — together these are the full as-written spec of the feature.

### Removed from the summary table

The table's `openMaxWidth` column (value `0` in rows 1–7) and these four rows:

```
| # | Has roles | maxWidth | openFullMax | openMaxWidth | Open (anonymous) access | Authenticated access | Thumbnails |
| 8 | Yes | 0 | 0 | 512 | Any region, up to 512px (substitute service) | Any region, up to platform limit | Up to 512px |
| 9 | Yes | 1000 | 0 | 512 | Any region, up to 512px (substitute service) | Any region, up to 1000px | Up to 512px |
| 10 | Yes | 0 | 400 | 512 | `/full/` up to 400px (main); any region up to 512px (substitute) | Any region, up to platform limit | Up to 512px |
| 11 | Yes | 2000 | 400 | 512 | `/full/` up to 400px (main); any region up to 512px (substitute) | Any region, up to 2000px | Up to 512px |
```

### Removed scenarios (verbatim)

### 8. Has roles, maxWidth=0, openFullMax=0, openMaxWidth=512

The image service has a probe and related IIIF Auth services. An unauthorised user receives `"status": 401` from the probe service, but the probe service response includes a `substitute` image service. The substitute image service has no access control and has a `maxWidth` of `openMaxWidth` (512px). Any user — including anonymous — can make requests of any region on the substitute service, up to the 512px bounding square.

An authorised user with a role can access the main image service with requests up to the platform limit (as `maxWidth` is 0).

Thumbnails are created up to the `openMaxWidth` limit (512px).

> [Aside note in original:] Scenario 8 above allows anonymous users to use tile-based deep zoom viewers up to the maximum resolution of the source image, but forbids anonymous users from downloading high resolution images above `openMaxWidth`. It differs from Scenario 2 in the first "No roles" section, because it allows authorised users to download much higher resolution images than the `openMaxWidth` limit, up to the platform limit.

### 9. Has roles, maxWidth=1000, openFullMax=0, openMaxWidth=512

The image service has a probe and related IIIF Auth services. An unauthorised user receives `"status": 401` from the probe service, but the probe service response includes a `substitute` image service. The substitute image service has no access control and has a `maxWidth` of `openMaxWidth` (512px). Any user — including anonymous — can make requests of any region on the substitute service, up to the 512px bounding square.

An authorised user with a role can access the main image service with requests up to `maxWidth` (1000px).

Thumbnails are created up to `min(maxWidth, openMaxWidth)` = 512px.

This is similar to the previous example except that even authorised users have a size restriction set below the platform default.

### 10. Has roles, maxWidth=0, openFullMax=400, openMaxWidth=512

The image service has a probe and related IIIF Auth services. An unauthorised user receives `"status": 401` from the probe service, but the probe service response includes a `substitute` image service. The substitute image service has no access control and has a `maxWidth` of `openMaxWidth` (512px). Any user — including anonymous — can make requests of any region on the substitute service, up to the 512px bounding square.

In addition, any user can make `/full/` region requests directly on the main image service up to the `openFullMax` bounding square (400px), without needing to interact with the probe or use the substitute service.

An authorised user with a role can access the main image service with requests up to the platform limit (as `maxWidth` is 0).

Thumbnails are created up to 512px. Both `openFullMax` (400px) and `openMaxWidth` (512px) allow thumbnail generation; the higher limit (`openMaxWidth` = 512px) applies, and since `maxWidth` is 0 it does not further constrain the thumbs limit.

### 11. Has roles, maxWidth=2000, openFullMax=400, openMaxWidth=512

The image service has a probe and related IIIF Auth services. An unauthorised user receives `"status": 401` from the probe service, but the probe service response includes a `substitute` image service. The substitute image service has no access control and has a `maxWidth` of `openMaxWidth` (512px). Any user — including anonymous — can make requests of any region on the substitute service, up to the 512px bounding square.

In addition, any user can make `/full/` region requests directly on the main image service up to the `openFullMax` bounding square (400px), without needing to interact with the probe or use the substitute service.

An authorised user with a role can access the main image service with requests up to `maxWidth` (2000px).

Thumbnails are created up to `min(maxWidth, openMaxWidth)` = 512px.

### Other removed phrasing

- Intro named three properties: "for the maxWidth, openFullMax and openMaxWidth properties" (now two).
- "No roles" intro: "`openFullMax` and `openMaxWidth` are ignored" (now just openFullMax).
- Scenario 3 heading/body covered "openFullMax or openMaxWidth != 0".
- "Has roles" intro: "the combination of `maxWidth`, `openFullMax`, and `openMaxWidth`".
- Thumbs Aside: "neither `openFullMax` nor `openMaxWidth` is set".
- Scenario headings 1–7 each ended ", openMaxWidth=0".
