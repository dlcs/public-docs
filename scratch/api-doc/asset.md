# Asset - Scratch Notes

Notes on changes made while porting asset.mdx from the old documentation to the new site.

## Example JSON changes (2026-02-18)

When updating the example JSON to match the actual API response, the following changes were made:

### Added fields (present in actual API but not in old docs example)

- `imageService` - the IIIF Image Service URL (e.g., `https://dlcs.example/iiif-img/2/5/b2921371x_0001.jp2`)
- `thumbnailImageService` - the thumbnail service URL (e.g., `https://dlcs.example/thumbs/2/5/b2921371x_0001.jp2`)
- `manifests` - array of manifests this asset is used in (replaces `manifest` link)
- `family` - single character indicating asset family ("I" for image)

### Removed fields (in old docs but not in actual API response)

- `manifest` - single link to a IIIF Manifest. Old docs had: `"manifest": "https://dlcs.example/iiif-manifest/2/5/b2921371x_0001.jp2"`. Replaced by `manifests` array.
- `usedBy` - link to collection of Manifests using this asset. Old docs had: `"usedBy": "https://api.dlcs.example/customers/2/spaces/5/images/b2921371x_0001.jp2/usedBy"`

### HTTP status code corrections

- DELETE: Old docs said "200 OK", actual API returns "204 No Content" on success

### Fields present conditionally

- `batch` - link to the batch this image was ingested in. Only present on assets submitted via the queue, not on assets created directly via PUT.

### Fields documented as planned (not yet in actual API)

The following fields are documented as if implemented, but the actual API currently uses `maxUnauthorised: -1` instead:

- `maxWidth` - restricts maximum permitted pixel response
- `openFullMax` - open thumbnail sizes for role-protected images
- `openMaxWidth` - open tile sizes for role-protected images

The `@context` is documented as `https://dlcs.github.io/vocab/context/future.json` (the planned value) rather than the current API value of `https://api.dlcs.example/contexts/Image.jsonld`.

## Changes made while porting sections

### `## id` section

- Fixed typo: old docs had `/{channel}/{customer}/{space}>/{id}` (extra `>`), corrected to `/{channel}/{customer}/{space}/{id}`
- Removed mention of POST to space.images: The old docs said "you MAY supply `id` on a POST to space.images" and "The platform will mint a GUID `id` if not supplied on a POST to space.images". This feature is not currently implemented (returns HTTP 405 Method Not Allowed), so these references were removed.

### `## mediaType` section

- Removed reference to `[manifest](#manifest)`: The old docs said "and includes it in the output of the [manifest](#manifest) linked resource". This was removed because the `manifest` field has been replaced by `manifests` array in the current API.

### `## origin` section

- Fixed typo: "This is npt the default behaviour" → "This is not the default behaviour"

### `## batch` section

- Fixed URL path: Old docs had `/customers/{customer}/spaces/{spaceId}/images/{imageId}/{batchId}` which is incorrect. The batch link on an asset points directly to `/customers/{customer}/queue/batches/{batchId}`.
- Removed reference to POST to space.images: Old docs said "An asset created directly, with POST to the parent space.images or a direct PUT, will not have a batch link." POST to space.images is not implemented, so changed to just "An asset created directly with a direct PUT will not have a batch link."

### `## duration` section

- Removed unanswered questions from old docs:
  - "Is this only allowed on audio/* and video/* mediaType? Or is that too restrictive?"
  - "Is the customer allowed to specify it? Can we always determine it?"

### `## deliveryChannels` section

- Fixed typo: "Not that the value" → "Note that the value"

### `## roles` section

- Changed example domain from `api.dlcs.io` to `api.dlcs.example` for consistency
- Fixed JSON example: removed trailing comma, fixed indentation

### `## maxWidth`, `## openFullMax`, `## openMaxWidth` sections

- Changed `thumbnail` delivery channel references to `thumbs` to match actual API
- Changed example domains from `dlcs.io` to `dlcs.example` for consistency
- Fixed typo in openFullMax: "whether the use has" → "whether the user has"

### `## adjuncts` section

- Fixed typo: "for See [Adjuncts]" → "See [Adjuncts]"
- NOTE: This feature is not yet implemented. Python sample code created but not tested.

### `## metadata` section

- Added clarification: "For non-AV assets, this endpoint returns HTTP 400 Bad Request."
- Added 400 Bad Request to the HTTP status codes in the table (verified by testing)

### `## storage` section

- Removed internal note: "This needs to be generalised to report on usage per delivery channel."
- Verified endpoint works (tested with rusty boat asset, returns thumbnailSize, size, lastChecked, checkingInProgress)

### `## reingest` section

- Fixed lowercase "a" at start of sentence: "a POST to this resource" → "A POST to this resource"
- Added URL path that was missing from old docs: `/customers/{customer}/spaces/{spaceId}/images/{imageId}/reingest`
- Removed internal note: "Need to determine what happens when a thumbnail policy is updated."
- Verified endpoint works (tested with rusty boat asset, returns asset with ingesting: true)

### `## manifest` section

- NOT PORTED: This property is not yet implemented. The old docs described it as "A link to a IIIF Presentation 3 manifest that provides the URLs and additional information for all the _outputs_ of the delivery channels, and any [adjuncts](adjuncts) you have registered (or that the platform has created)."

### `## usedBy` section

- NOT PORTED: This property is not yet implemented. Full content from old docs:

```
## usedBy 🆕

This asset may be used by one or more Manifests that the platform is also managing and serving. Those manifests link to this asset, and this asset provides the reverse linking, allowing you to keep track of where the asset is being used.

Typically, an asset is used in only one Manifest, but not always.

> The returned collection cannot include Manifests that the platform doesn't know about! There could be many third party Manifests also referencing an image service generated from this asset, but you have no way of knowing about them.

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:Image | 🔗 iiif:Collection | True | False |

`/customers/{customer}/spaces/{spaceId}/images/{imageId}/{batchId}`

| Method | Label | Expects | Returns | Status |
|:---|:---|:---|:---|:---|
| GET | Retrieve a IIIF Collection of Manifests that this asset is used in | - | iiif:Collection | 200 OK |
```

## Sections not yet ported from old documentation

The following sections from the old asset.mdx remain to be ported:

