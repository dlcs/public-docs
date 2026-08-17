
# There are no such things as manifest batches yet:

A batch represents a submitted job of assets. [Collections](collections) of batches are returned from:

- `/customers/{customer}/iiif/<identifier>/queue/batches` 🆕
- `/customers/{customer}/iiif/<identifier>/queue/active` 🆕
- `/customers/{customer}/iiif/<identifier>/queue/recent` 🆕

# The `assets` property is missing from the batch object but the endpoint works

```json
    "assets": "https://api.dlcs.io/customers/2/queue/batches/875629/assets",
```

# Old volatility caveat on `images` — resolved (PROV-21, logged 2026-08-03)

The old page prefixed the images/batch-membership paragraph with *"The following
information will likely change"*. It did change: the images/assets split landed
(current-members vs at-creation members), and the new page's settled prose matches
code (`GetBatchImages.cs:10` — current batch members only). Caveat retired; nothing
to restore.

# Batch-size limit: old docs said 100, shipped default is 250 (PROV-05/PROV-18, resolved 2026-08-03)

The old docs stated a fixed limit: *"There is a limit of 100 assets per batch."*
Verified against code: `ApiSettings.MaxBatchSize = 250` (platform-configured).
registering-assets.mdx already says 250; batch.mdx says only "configurable";
collections.mdx still carries the old "e.g., 100" advice. Make all three agree on
"250 by default, platform-configured". The same limit applies to adjunct batches
(`AdjunctBatchPostValidator`).


# Release-gated sample twin: assets link (PRO-01, ruled 2026-08-17)

PRO-01 ruled (a): the `Batch` model now advertises the `assets` HydraLink
(protagonist PR #1272, merged to develop only). batch.mdx needed no change — its
example and #assets section already describe the link. When the release carrying
#1272 ships, apply the sample swap in `p09_batch/batch_operations.py`
`get_batch_assets`: replace the constructed URL with `assets_url = batch["assets"]`
and remove the TODO comment — the link will then be on the released wire.
