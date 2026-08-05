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
