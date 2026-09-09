# Hygiene Sprint · Session 7 · The IIIF port (one arc)

> **Port log, not a card session.** The plan (PO-agreed 2026-09-09) and the opening slate live at the top
> of `session-6-iiif-auth.md`; the one register card ruled here is **IIIF-12** (card in the session-6
> file). This file records step status, wire findings, and in-room decisions made during the port.
> Started 2026-09-09 on branch `hygiene/session-7`. Slate outcomes recorded in the session-6 file.

## Step checklist

- [ ] **Step 0** — re-run IIIF-12 scenarios on v0.10.0; rule IIIF-12. *(wire work DONE 2026-09-09;
      findings below; ruling pending)*
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
| F5 | **Duplicate `canvasOrder` is not an error**: both assets share ONE canvas as a `Choice` body (`choiceOrder` stays null) — this is how a Choice is made | ✗ (predicted 400; cf. closed #649) |
| F6 | GET→PUT-unchanged of an asset-backed manifest → 400 type 21 — **#661 re-confirmed on v0.10.0**; the documented gotcha stands | ✓ |
| F7 | **Reorder recipe works**: PUT with `items` reversed + `paintedResources: []` → 200; canvas order changes and the public view is correct. BUT `paintedResources[].canvasId` values are **re-minted to fresh ids that match neither the items canvases nor anything else** — API-view internal inconsistency after any items-only update | recipe ✓ / inconsistency NEW (bug) |

## IIIF-12 ruling — ☐ pending

Presented 2026-09-09 with recommendation **(a″ as amended by F1–F7)**; see the in-room presentation.
New-issue question presented alongside: F7 (canvasId re-mint) and F3 (silent body discard) need homes —
recommendation: **one new iiif-presentation issue for F7**, **F3 as a comment on #661** (same merge-path
subject; #661 already carries the RFC 0005 drift checklist).

## Findings ledger (accumulates through the arc)

- 2026-09-09 · Step 0 · F1–F7 above.

## In-room decisions during the port

- (none yet)
