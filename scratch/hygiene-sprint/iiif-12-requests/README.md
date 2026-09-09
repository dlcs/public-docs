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

## Re-run on v0.10.0 — Session 7 Step 0 (2026-09-09)

Stage `/version` = 0.10.0; #660 fixed. Dumps 10–22, slugs `hyg7-iiif12-*`, all deleted after capture.
Full findings table (F1–F7): `../session-7-iiif-port.md`.

| file | scenario | result |
|---|---|---|
| 10 | A: mixed additive create (dump-01 shape, matched empty c1 + appended page_02) | **201** — F1: canvasId match, PR canvasOrder wins, client id kept as `/15/canvases/c1` |
| 11 | B1: matched canvas WITH content, id `c1` | 400 `InvalidCanvasId` "Id used in one of your other manifests" — masked by F2 (c1 held by manifest from 10); see 18 |
| 12 | B2: duplicate canvasOrder (first pass) | **201** (not the predicted 400) — inspected properly in 20 |
| 13 | B3: differing canvasLabel, id `c1` | 400 `InvalidCanvasId` — masked by F2; see 19 |
| 14/15 | C: create + GET→PUT-unchanged round-trip | create 201; PUT back **400 type 21** — #661 re-confirmed (F6) |
| 16 | D: reversed `items` + `paintedResources: []` | **200** — reorder recipe works (F7) |
| 18 (+RESULT) | B1u: matched content canvas, unique id | **201** — supplied body silently replaced by asset painting; client canvas dims kept (F3) |
| 19 | B3u: differing canvasLabel, unique id | **400** `ErrorMergingPaintedResourcesWithItems` "does not have a matching canvas label" (F4) |
| 20 (+RESULT) | B2u: duplicate canvasOrder, inspected | **201** — one canvas, `Choice` body, choiceOrder null (F5) |
| 21/22 | D′: reorder inspected, API + public views | order sticks, public view correct; **PR canvasIds re-minted, match nothing** (F7 bug half) |
