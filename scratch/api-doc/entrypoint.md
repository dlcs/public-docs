# Notes (clarified 2026-08-03)

- **`queue`:** the API response is missing a `queue` link — even though the global
  `/queue` **endpoint** exists (`QueueController.cs:17`). The EntryPoint model simply
  has no `queue` property to emit (`DLCS.HydraModel/EntryPoint.cs:18-55`). So the fix,
  if wanted, is cheap: add the link property (DIS-14 option b). *(An earlier
  verification note misread this as a false claim about the model — the intended
  meaning, endpoint-present/link-missing, is correct.)*
- **Remove `imageOptimisationPolicies` and `thumbnailPolicies`** (DIS-15; emitted,
  legacy, undocumented — and `thumbnailPolicies`' description string is a copy-paste
  of the `portalRoles` text).
- The model DOES emit `portalRoles`, undocumented (DIS-16).

# Old-doc prose preserved by the 2026-08-03 provenance re-audit

## `deliveryChannelPolicies` (PROV-01) — **probably to be dropped, not restored**

The API does **not** return a `deliveryChannelPolicies` link, and it probably should
not be documented (the old section header was itself `## DELETE
deliveryChannelPolicies`, wrapped in a Callout questioning whether the global set
should exist). The live entrypoint.mdx JSON example still shows the property and
should lose it (DIS-14). The old prose is preserved here **only** in case the room
decides the feature is wanted after all:

> "A link to a paged [Collection](collections) of further collections of [delivery
> channel policies](delivery-channels). This is a rare example of a Collection of
> Collections, where the returned collections are like sub-folders, for organisational
> use. / These _Delivery Channel policies_ are common settings you can re-use for your
> own assets, as further explained in [Delivery Channels](delivery-channels)."

## "Hardcoded" non-dereferenceable policies (PROV-02) — **restore-candidate**

Real behaviour worth documenting somewhere (delivery-channels page?): `use-original`,
`none` and `default` are valid policy references that exist as hardcoded values
rather than dereferenceable resources.

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
