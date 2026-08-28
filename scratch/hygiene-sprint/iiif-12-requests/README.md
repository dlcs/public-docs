# IIIF-12 stage verification requests (2026-08-28)

Target: `PUT https://presentation-api.dlcs-stage.digirati.io/15/manifests/{slug}` on stage (`/version` = 0.9.0), headers:
`Authorization: Basic …`, `X-IIIF-CS-Show-Extras: All`, `Content-Type: application/json`, no `If-Match` (create).
Asset shape follows the released model: `"asset": {"id": "page_01", "space": 98765}` (a full path `15/98765/page_01`
is rejected 400 "AssetId '15/-10/15/98765/page_01' is invalid" — first attempt, not dumped).

| file | result |
|---|---|
| 01 | **500** `{"title":"Operation failed","detail":"Unknown error"}` — DB row + asset links created, S3 write missing |
| 02 | **500** same, paintedResources-only, no items — so the failure is not the mixed payload |
| 03–06 | **412** "ETag does not match" — slug now exists from 02 (create refused without If-Match) |

Afterwards: flat `GET /15/manifests/hyg-iiif12-a|x` → 500 `Unable to read and deserialize manifest from storage`;
hierarchical `GET /15/hyg-iiif12-a` → 303 to flat; root collection lists both; protagonist `page_01.manifests` =
[hyg-iiif12-a, hyg-iiif12-x]; no new batch. DELETE → 412 with no / `"*"` If-Match (no ETag obtainable). Orphans need DB/S3 cleanup.
Scenarios B (conflict), C (round-trip), D (reorder) were never reached.
