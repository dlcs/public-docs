
# There are no such things as manifest batches yet:

A batch represents a submitted job of assets. [Collections](collections) of batches are returned from:

- `/customers/{customer}/iiif/<identifier>/queue/batches` 🆕
- `/customers/{customer}/iiif/<identifier>/queue/active` 🆕
- `/customers/{customer}/iiif/<identifier>/queue/recent` 🆕

# The `assets` property is missing from the batch object but the endpoint works

```json
    "assets": "https://api.dlcs.io/customers/2/queue/batches/875629/assets",
```

# Batch-size limit: old docs said 100, shipped default is 250 (PROV-05/PROV-18, resolved 2026-08-03)

The old docs stated a fixed limit: *"There is a limit of 100 assets per batch."*
Verified against code: `ApiSettings.MaxBatchSize = 250` (platform-configured).
registering-assets.mdx already says 250; batch.mdx says only "configurable";
collections.mdx still carries the old "e.g., 100" advice. Make all three agree on
"250 by default, platform-configured". The same limit applies to adjunct batches
(`AdjunctBatchPostValidator`).

