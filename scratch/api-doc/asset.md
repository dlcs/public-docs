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

*(⟳ refreshed session 2, 2026-08-12 — SPA-03 ruling (b). The original note below was written when none of the three replacement fields existed; `maxWidth` and `openFullMax` have since shipped (v1.13.x, with a data migration from `MaxUnauthorised`), and `maxUnauthorised` itself is now documented in asset.mdx as deprecated, including the mutual-exclusion 400 (`HydraImageValidator.cs:41-44`). Only `openMaxWidth` remains unimplemented — see SPA-01.)*

The following fields are documented as if implemented, but the actual API currently uses `maxUnauthorised: -1` instead:

- ~~`maxWidth` - restricts maximum permitted pixel response~~ (shipped)
- ~~`openFullMax` - open thumbnail sizes for role-protected images~~ (shipped)
- `openMaxWidth` - open tile sizes for role-protected images (still not in code — SPA-01)

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

*(⟳ SPA-04 ruling, session 2, 2026-08-12: the `manifest` property is now implemented in
protagonist draft PR #1251 (`hygiene/spa-04`) — every asset response will carry the
single-asset manifest URL. The scopes question is settled: `manifests` stays live-documented
(with a do-not-edit caution) and will later be renamed `scopes` alongside a new `usedBy`
property — design ticket protagonist #1250. The doc section below is **release-gated**: apply
it to asset.mdx when the release carrying #1251 ships.)*

- Old docs described it as "A link to a IIIF Presentation 3 manifest that provides the URLs and additional information for all the _outputs_ of the delivery channels, and any [adjuncts](adjuncts) you have registered (or that the platform has created)."
- Confirmed (2026-06-24): the single-asset manifest exists, and its URI _should_ become the value of a `manifest` property — ~~but it is not yet implemented _as a property_~~ (implemented in #1251).

Need to make bigger use of this feature and encourage linking to it in a viewer - provide a link to viewer in the API? Maybe not that far.

#### RELEASE-GATED: `## manifest` section to add to asset.mdx (before `## manifests`) when #1251 ships

```mdx
## manifest

A link to the [single-asset manifest](../single-asset-manifest) for this asset: a IIIF Presentation Manifest generated by the platform, presenting the outputs of the asset's delivery channels.

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:Image | iiif:Manifest | True | False |

The URL is on the public host, not the API host, and needs no authentication (subject to the asset's access control):

​```
{public-host}/iiif-manifest/{customer}/{space}/{asset-id}
​```
```

Also when applying:
- add `"manifest": "https://dlcs.example/iiif-manifest/2/5/b2921371x_0001.jp2",` to the example JSON in asset.mdx (after `imageService`/`thumbnailImageService` block, matching wire order near `manifests`), and the registering-assets.mdx example likewise;
- update the p17_single_asset_manifest sample to read the manifest URL from the asset's `manifest` property instead of constructing it by hand (sample parity, XC-10);
- remove the escaping (`​`) from the nested code fence above.

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

---

## "(First draft) Version 1" `max` / `maxBehaviour` design block (PROV-03, captured 2026-08-03) — **park (design history)**

The old page's trailing design discussion — superseded by the `maxWidth` /
`openFullMax` / `openMaxWidth` three-property model but the only record of *why* that
design exists, and of one unresolved combination case:

> "The effect of setting `max` depends on what you set `maxBehaviour` to: `maxWidth`:
> this is independent of roles... `substitute`: the effect is 'Anyone can see a request
> up to maxWidth but you need a role to see higher'... `thumbnail`: this only applies
> to images with roles... Note that for this choice it's not a width, it's a bounding
> box - like maxUnauthorised."

And the open question:

> "What about the scenario where you want to allow full thumbs up to 400 px, but still
> impose a maxWidth of 512 even for authed users?... Or have a fourth behaviour:
> `maxWidthWithOpenThumbs`..."

Relevant when SPA-01/DIS-18 decide the fate of `openMaxWidth` + substitute.


## Replaced prose preserved (SPA-20, mechanical track, 2026-08-05)

Original `## id` validation sentence in asset.mdx:101, replaced on the hygiene
mechanical track:

> You can't update `id` for an existing asset (via PATCH), and if you create or update an asset via PUT, it is not required (if present, the platform will validate that it matches the last path element of the PUT URL).

**Why changed:** a body `id` on PUT is silently ignored (the URL path wins,
AssetConverter.cs:278-281); only `@id` is validated against the URL (400 on
mismatch). The old sentence claimed `id` itself is validated.

**Disposition: probably-drop** (superseded by code reality). Restore only if the
platform starts validating body `id` against the PUT URL.

## openMaxWidth section (SPA-01, removed from asset.mdx 2026-08-12 — ruled (b))

The feature is not implemented (`Image.cs` has no `openMaxWidth` property; no
substitute/open-image-service mechanism exists). Removed verbatim below — this, with the
scenarios preserved in [size-restrictions.md](./size-restrictions.md), is the only written
spec of the feature. Design work tracked as protagonist ADR-writing ticket [#1249](https://github.com/dlcs/protagonist/issues/1249) (companion to
[ADR 0010](https://github.com/dlcs/protagonist/blob/develop/docs/adr/0010-replace-maxunauthorised.md);
issue #306 promised a future openMaxWidth ticket that was never minted).
**Restore when the feature ships.**

---

## openMaxWidth

Only applies when an image has roles, and for any region, including `/full/`.

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:Image | xsd:integer | False | True |

This setting allows Image API tiles for deep zoom to be served to any user - anonymous, or without a matching role. An anonymous user can deep zoom, but not download a high resolution image. For this reason it is recommended that the value of this setting is a power of 2, e.g., 512, so that it matches an optimised tile size for deep zoom.

This setting does not (and cannot) prevent a user from stitching multiple individual image tiles into a single large image, or taking a screen grab of rendered tiles in a viewer, but does prevent sharing of single IIIF Image API URLs for large images.

When an image has roles and has a value greater than zero for `openMaxWidth`, the `iiif-img` delivery channel provides an info.json with a probe service. The probe service will return `"status": 401` for a user without any matching role, but will also offer a `substitute` as defined in the [IIIF Authorization Flow specification](https://iiif.io/api/auth/2.0/).

If the image has an Image Service endpoint of `https://dlcs.example/iiif-img/2/99/my-image`, the probe response for an unauthorised user is:

```json
{
  "@context": "http://iiif.io/api/auth/2/context.json",
  "id": "https://dlcs.example/probe/2/99/my-image",
  "type": "AuthProbeResult2",
  "status": 401,
  "substitute": {
    "id": "https://dlcs.example/iiif-img/2/99/my-image/substitute",
    "type": "ImageService3"
  }
}
```

The _substitute_ image service at `https://dlcs.example/iiif-img/2/99/my-image/substitute` is for the same source image, but has no access control. However, it does have a maxWidth of `openMaxWidth` (e.g., 512).

The expected behaviour of a IIIF client is to show the substitute, and offer the user the option to log in to access the original image service.

If an image has both `maxWidth` and `openMaxWidth`, the first, access controlled image has a `maxWidth` of `maxWidth` and the second, open image service has a `maxWidth` of `openMaxWidth`. This feature doesn't make much sense unless `maxWidth` is either 0 or is greater than `openMaxWidth`, but it's not an error if `maxWidth <= openMaxWidth` (again, you may be updating different things at different times).

On the `thumbs` delivery channel, thumbnails will be created up to the limit defined by `maxWidth` or `openMaxWidth`, whichever is _lower_ (unless maxWidth is 0).

The value of `openMaxWidth` must either be `0`, indicating unset, or a positive integer equal to or greater that `256`. Values between 0 and 256 exclusive are disallowed.

See [Size Restrictions](../size-restrictions) for examples of the effects of the [maxWidth](#maxwidth), [openFullMax](#openfullmax) and [openMaxWidth](#openmaxwidth) properties.
