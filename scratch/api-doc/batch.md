
# There are no such things as manifest batches yet:

A batch represents a submitted job of assets. [Collections](collections) of batches are returned from:

- `/customers/{customer}/iiif/<identifier>/queue/batches` 🆕
- `/customers/{customer}/iiif/<identifier>/queue/active` 🆕
- `/customers/{customer}/iiif/<identifier>/queue/recent` 🆕

# The `assets` property is missing from the batch object but the endpoint works

```json
    "assets": "https://api.dlcs.io/customers/2/queue/batches/875629/assets",
```

