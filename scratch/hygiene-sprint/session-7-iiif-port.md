# Hygiene Sprint · Session 7 · The IIIF port (one arc)

> **Port log, not a card session.** The plan (PO-agreed 2026-09-09) and the opening slate live at the top
> of `session-6-iiif-auth.md`; the one register card ruled here is **IIIF-12** (card in the session-6
> file). This file records step status, wire findings, and in-room decisions made during the port.
> Started 2026-09-09 on branch `hygiene/session-7`. Slate outcomes recorded in the session-6 file.

## Step checklist

- [x] **Step 0** — re-run IIIF-12 scenarios on v0.10.0; rule IIIF-12. **DONE 2026-09-09 — RULED (a″)**;
      findings F1–F7 below; F3 comment posted on #661; register complete (last open card closed)
- [ ] **Step 1** — `iiif.mdx` (order 22) + ops table wire-checked + p22 samples
- [ ] **Step 2** — `iiif-collections.mdx` (order 23) incl. search + p23 samples
- [ ] **Step 3** — `iiif-manifests.mdx` (order 24), full page + p24 samples
- [ ] **Step 4** — close (sidebar, CLAUDE.md, register, `_issues-rfcs.md` pre-flight block, PR)

## Step 0 — IIIF-12 scenario results on stage v0.10.0 (2026-09-09)

Request dumps 10–22 in `iiif-12-requests/` (see its README). All test manifests deleted after capture.
The session-6 code-trace predictions marked ✓ (held) or ✗ (overturned on the wire):

| # | Finding | vs trace |
|---|---------|----------|
| F1 | Mixed additive create → **201**: match keyed on `canvasId`; PR `canvasOrder` authoritative; unmatched PR entries get minted canvases; a client-supplied canvas id is preserved as `/{c}/canvases/{clientId}` | ✓ (now provable — #660 fixed) |
| F2 | **Client canvas ids are customer-global unique**: reusing an id held by another manifest → 400 `InvalidCanvasId` "Id used in one of your other manifests" | NEW |
| F3 | **Create/update asymmetry on matched content canvases**: at CREATE, a matched `items` canvas WITH a painting annotation is **accepted (201)** — the supplied body is *silently discarded*, replaced by the asset painting, while the client's canvas dims are kept (4288×2848 kept though the asset is 2474×2922). At UPDATE the same shape → 400 type 21 "cannot contain an annotation body" | ✗ ("must be empty placeholder else 400" is update-only) |
| F4 | Matched canvas with differing `canvasLabel` → 400 `ErrorMergingPaintedResourcesWithItems` "does not have a matching canvas label" | ✓ |
| F5 | **Same `canvasOrder` = shared canvas as a `Choice`.** With explicit `choiceOrder` (1, 2, …) → 201, Choice items in choiceOrder order, values echoed (dump 23) — this is the form the docs teach. WITHOUT `choiceOrder`, v0.10.0 silently accepts (Choice, null choiceOrders) — **PO 2026-09-09: fixed per #649, will be REJECTED in 0.11** (not on stage yet) → the missing-choiceOrder 400 is a release-gated twin; do not document the sloppy acceptance | ✗ on the 400 timing; recipe ✓ |
| F6 | GET→PUT-unchanged of an asset-backed manifest → 400 type 21 — **#661 re-confirmed on v0.10.0**; the documented gotcha stands | ✓ |
| F7 | **Reorder recipe works**: PUT with `items` reversed + `paintedResources: []` → 200; canvas order changes and the public view is correct. `paintedResources[].canvasId` values are re-minted to fresh ids that match nothing — **room challenged "bug" 2026-09-09 ("prove us wrong"); challenge run, room PROVEN RIGHT on the substance** (dumps 24–26): public canvas ids stayed stable through reorder, failed edit, and second reorder; repeat items-only edits fine (E3 200). The one real consequence (E2): after an items-only update, GET's response is **not re-submittable verbatim** — PUT-back of the API view → 400 "canvas painting records conflict with the order from items" (the stale PR canvasIds can never match). Clean escape hatch (E1, 200): reference existing canvases by their **`items` ids** — the PR edit succeeds AND re-syncs the stored canvasIds. Verdict: not a bug in effect; an API-view reporting blemish = improvement-for-later + a docs rule ("identify canvases by their items ids; after items-only edits, ignore `paintedResources[].canvasId`"). E2's failed round-trip is #661-family evidence | recipe ✓ / "bug" withdrawn after challenge |

## IIIF-12 ruling — ✅ RULED (a″) 2026-09-09

PO ruled **(a″)** with the in-room amendments below; F3-only comment posted on #661
(https://github.com/dlcs/iiif-presentation/issues/661#issuecomment-5600079141). Register cell + card
status + counts updated — **every register card now carries a final status.**

Presented 2026-09-09 with recommendation **(a″ as amended by F1–F7)**. Amendments in-room:
**F5** — PO: #649 fix ships in 0.11; docs teach the explicit-`choiceOrder` Choice form only; the
missing-choiceOrder 400 is a release-gated twin. **F7** — room challenged the "bug" framing; challenge
experiments (dumps 24–26) proved the room right on public-id stability; "new issue" withdrawn. Escalation
now: **ONE comment on #661** carrying F3 (create/update asymmetry, silent body discard) + F7's E2 (API
view not re-submittable after items-only updates; items-ids escape hatch re-syncs) — same round-trip
family as #661 — plus the improvement suggestion (report canvasIds consistently / re-sync on write).
**⟳ PO 2026-09-09: the E2/re-mint behaviour was already discussed on #661 and WILL BE ADDRESSED** — so
E2 needs no comment. Escalation shrinks to at most a short F3-only comment on #661 (the create-side
asymmetry: matched content canvas silently accepted at create, supplied body discarded — dump 18 —
vs the 400 on update; input for the reconciliation design). Docs implication unchanged for now: the
round-trip gotcha + items-ids rule describe released v0.10.0 behaviour and carry the #661 caution;
when the #661 fix ships, both soften — note kept with the release-gated twins.

## Findings ledger (accumulates through the arc)

- 2026-09-09 · Step 0 · F1–F7 above.
- 2026-09-09 · Step 1 · **F8**: Show-Extras without auth is IGNORED (303 public behaviour), not the old
  page's promised 401; value case-sensitive; invalid values ignored. Live page corrected.
- 2026-09-09 · Step 1 · **F9**: `/{c}/collections` and `/{c}/manifests` listing URLs 404 on v0.10.0 — old
  "paged collections of all your resources" claim parked (same class as #656).
- 2026-09-09 · Step 1 · **F10** (to re-verify at the ops-table step): a storage-collection PUT-create
  returned **200**, where a manifest PUT-create returns 201 — possible create-status inconsistency.
- 2026-09-09 · Step 1 · Reserved slugs: case-insensitive ✓, enforced at every hierarchy level ✓, error
  400 `ValidationFailed` "'slug' cannot be one of prohibited terms" (verified verbatim).
- 2026-09-09 · Step 1 · **F11**: If-Match on a creating PUT → **412** on v0.10.0 (both types) — the
  session-6 "400 ETagNotAllowed" was v0.9.0 behaviour, since changed. All conditional violations
  uniformly 412 now.
- 2026-09-09 · Step 1 · **F12**: body `id` silently ignored on create AND update, both types — old
  "must match the request URL" claim disproven; URL is authoritative.
- 2026-09-09 · Step 1 · F10 CONFIRMED: collection PUT-create 200 vs manifest 201 — **PO: fixed in
  0.11 (uniform 201)**; no issue; release-gated twin recorded in scratch (same 0.11 watch-list as
  the #649 choiceOrder twin).
- 2026-09-09 · Step 1 · manifest_lifecycle.py moved to p24_iiif_manifests/ (final home; re-run green).
- 2026-09-09 · Step 1 · **F13**: error `instance` = bare API host on v0.10.0 (spec said request URL —
  corrected); 404 bodies minimal (no type/detail); unauthenticated write = bodyless 401; 412 type =
  `ETagNotMatched`.

## In-room decisions during the port

- (none yet)
