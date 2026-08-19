# Current state (rewritten 2026-08-19, session 4, DIS-17 ruled (a) — all EntryPoint cards resolved)

**EntryPoint emitted links:**
- **Released (v1.13.2) wire:** `customers`, `originStrategies`, `portalRoles`,
  `imageOptimisationPolicies`, `thumbnailPolicies`, `storagePolicies` — six links, three of
  them dead or dying (see below).
- **develop** (after XC-07 #1237, DIS-14 #1282, DIS-16 #1284 all merge): `customers`,
  `originStrategies`, `storagePolicies`, `queue` — every advertised link reachable.
- **Live doc** (entrypoint.mdx) documents: customers, originStrategies, storagePolicies as
  links, plus the `## queue` section describing the (released, unlinked) `GET /queue` endpoint.

**How each question resolved:**
- `queue` link missing → **DIS-14 ruled (b′) 2026-08-19**: link added in draft PR #1282;
  release-gated twin below restores the doc's JSON key/table/sample when it ships.
- `imageOptimisationPolicies` + `thumbnailPolicies` (legacy, undocumented) → **DIS-15 resolved
  by XC-07 cascade (session 0, PR #1237)**: removed on develop; still on released wire until
  the carrying release; docs never showed them — nothing gates.
- `portalRoles` → **DIS-16 ruled (a) 2026-08-19**: was a DEAD link (endpoint never existed,
  always 404); removed with its orphaned vocab class in draft PR #1284; docs correctly silent.
- `deliveryChannelPolicies` (docs-only phantom) → **DIS-14**: dropped from the doc example;
  not planned (PROV-01 below closed).

# Old-doc prose preserved by the 2026-08-03 provenance re-audit

## `deliveryChannelPolicies` (PROV-01) — ✅ CLOSED: dropped (DIS-14 ruling, 2026-08-19)

The room decided: no global `deliveryChannelPolicies` set — the JSON key is gone from
the doc example, no route exists (wire-confirmed 404), not planned. The old prose stays
below purely as history:

> "A link to a paged [Collection](collections) of further collections of [delivery
> channel policies](delivery-channels). This is a rare example of a Collection of
> Collections, where the returned collections are like sub-folders, for organisational
> use. / These _Delivery Channel policies_ are common settings you can re-use for your
> own assets, as further explained in [Delivery Channels](delivery-channels)."

## "Hardcoded" non-dereferenceable policies (PROV-02) — ✅ CLOSED: already documented (checked 2026-08-19)

The restore-candidate flag is satisfied: the three preset policies (`use-original`,
`default`, `none`) are fully documented in the live **delivery-channels.mdx** (the
policy-reference sentence and the "out-of-the-box policies" section with per-channel
applicability). Nothing to restore; the original prose stays below as history:

> "You get some default Delivery Channel **Policies** when your customer is created.
> For thumbs and AV. / You can also refer to \"hardcoded\" but not dereferenceable
> policies use-original, none and default. So what would be in here?"

# DIS-14 — ✅ RULED (b′) 2026-08-19 (session 4): queue link added in code; deliveryChannelPolicies dropped

> Split treatment. **`deliveryChannelPolicies`**: JSON key removed from the example — no global
> route exists (wire-confirmed 404; per-customer only), the old docs had already flagged the
> global set for deletion. Dropped, not parked — not planned.
> **`queue`**: `GET /queue` is real, anonymous, released (wire-confirmed 200 QueueSummary with
> incoming/priority/timebased/transcodeComplete/file counts + obsolete failed/success compat
> keys). Only the LINK was missing — added by draft PR **protagonist #1282** (PRO-01/XC-07
> "advertise the reachable surface" family; Order 14, Range vocab:QueueSummary, GET operation,
> test asserts link).
>
> **RELEASE-GATED TWIN — apply when the #1282-carrying release ships:**
> 1. entrypoint.mdx example JSON: re-add `"queue": "https://api.dlcs.example/queue"` after
>    storagePolicies.
> 2. entrypoint.mdx `## queue`: replace "It is not currently linked from the entry point body —
>    request it directly at the API root plus `/queue`" with "The entry point provides a link to
>    this global queue resource." and restore the domain/range table:
>    `| vocab:EntryPoint | 🔗 vocab:QueueSummary | True | False |`
> 3. p04_entrypoint/entrypoint.py: swap to `api_root["queue"]` (un-comment, drop the hand-built
>    URL and the PR annotation).
>
> Removed original section wording (for the record): "The entry point also provides a link to
> this global queue, to report on the current workload of the platform." + the domain/range
> table shown in point 2. The queues.mdx back-link (`../entrypoint#queue`) stays valid — the
> section remains.

# DIS-16 — ✅ RULED (a) 2026-08-19 (session 4): dead portalRoles link removed in code; docs stay silent

> Card premise overturned at presentation: `portalRoles` is emitted by the released EntryPoint
> but `GET /portalRoles` has ALWAYS 404'd — no controller or route exists anywhere in
> protagonist; the vocab class was `[Unstable("Under consideration.")]` and referenced by
> nothing else. PRO-07/XC-07 dead-link family. Draft PR **protagonist #1284** removes the
> EntryPoint link + operations AND deletes the orphaned PortalRole vocab class (PO: both in
> one PR); breaking, signposted (response loses a never-followable property).
> Deprecation context: portal-users is already marked "will be deprecated" in the live docs
> (session 1) — portal roles exist solely for portal users, so implementing the endpoint was
> rejected. **No live-doc change**: entrypoint.mdx never documented portalRoles, which this
> ruling retroactively makes the correct state — nothing to gate on release either (the doc
> is silent both before and after #1284 ships).
