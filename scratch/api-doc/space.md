# maxUnauthorised (clarified 2026-08-03 — the line below was cryptic; see SPA-05, PROV-19) — **deprecation path, do NOT document as a feature**

The old page's example JSON included `"maxUnauthorised": -1` (no `##` section existed
for it in old OR new). The new page dropped it from the example without a note. The
property is real and live-settable today (`DLCS.HydraModel\Space.cs:57-58`; read on
create/patch/put) — but **PO intent (2026-08-03): it is to be REPLACED by the new
space-level default max properties** (`defaultMaxWidth` / `defaultOpenFullMax` /
`defaultOpenMaxWidth`, parked below in this file), mirroring the asset-level
`maxUnauthorised` → `maxWidth`/`openFullMax` migration (ADR
0010-replace-maxunauthorised; cf. SPA-03). So the docs should not adopt it; the
SPA-05 decision is about sequencing the deprecation/replacement, not about
documenting the legacy field.

Original cryptic note: "space has `maxUnauthorised` = 1"

# defaultRoles range rationale (PROV-20, captured 2026-08-03) — park (provenance)

Old editorial note dropped in the port — the reason the range is an array of string
URIs, and a warning that older Deliverator docs disagree:

> "NB deliverator readthedocs has this a Hydra collection of vocab:Role, which is
> wrong - they are default values for the assets, therefore an array of string URIs."

PUT ../spaces/123
{
    "id": 456,
    "name": "blah"
}

This works but ignores 456; space 123 is created.
Should it be a Bad Request?

*(⟳ SPA-14 ruling (a), session 2, 2026-08-14: YES — it becomes a Bad Request. Protagonist
draft PR **#1260** (`hygiene/spa-14`): space PUT/PATCH with a body `id` differing from the URL
→ 400 "The id in the request body does not agree with the request URL."; space POST with ANY
body `id` → 400 "An id cannot be supplied when creating a space; the platform assigns it."
(the POST half folds in session-1's ACC-13 finding that POSTing an existing id silently minted
a new space); asset PUT/PATCH mismatched body `id` → same 400 (legacy full-form
`{customer}/{space}/{id}` still accepted when it matches). **Release-gated doc change — apply
to space.mdx#id when the release carrying #1260 ships:** after "This is provided for read
convenience, you can't set it yourself", add: "If a request body includes an `id` that
conflicts with the request URL, the response is 400 Bad Request; on POST, where the platform
assigns the id, supplying one at all is a 400." Mirror on asset.mdx#id (see asset.md twin).
The PR also records the PO's ask for a centrally defined id-handling policy across all HTTP
operations.)*

*(⟳ SPA-07 ruling (a), session 2, 2026-08-14: the old section below is now partly resolved.
The **PATCH row and its no-reprocessing prose are restored to the live page** (space.mdx#images),
reworded and verified against develop@2f262b41 and live against staging (200 + 400 paths).
The **POST row stays parked** — no controller action exists (405 on the wire); the phantom POST
advertisement was removed from the Space Hydra vocab in protagonist PR #1258, which advertises
the implemented PATCH instead. The POST prose below (platform-minted GUID identifiers when no
model id is supplied) is the only written description of that unimplemented registration mode —
preserved here in case it is ever built. The cryptic allImages note below fed card ACC-20
(customer-level allImages PATCH is a different endpoint and body shape; see
session-1-account-access.md).)*

## images

> Same query but NOT POST id 2025 operations as customer/allImages - allImages

## images

All the assets (not just images) in the Space. This is presented as a [Hydra Collection](collections) of assets, and can take any [asset query](asset-queries) to filter the returned collection. You can also adjust the page size to suit your application needs (the default is 100).

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:Space | 🔗 hydra:Collection (of vocab:Image) | True | False |

`/customers/{customer}/spaces/{spaceId}/images`

| Method | Label | Expects | Returns | Status |
|:---|:---|:---|:---|:---|
| GET | (with optional [query parameter](asset-queries)). | - | hydra:Collection | 200 OK |
| POST | Add an Asset (vocab:Image) to a Space | vocab:Image | vocab:Image | 201 Image created., 400 Bad Request |
| PATCH | Update one *or more* assets | 🔗 hydra:Collection (of vocab:Image) | 🔗 hydra:Collection (of vocab:Image) | 200 OK, 400 Bad Request |

For full details, see [Registering Assets](registering-assets), which describes use of queues, and direct PUTs, for creating assets as well as POST to this collection. 

The POST mechanism on `space.images` is the only way to register an asset and have the platform assign it an identifier. This is generally not recommended, your asset identifiers should be based on asset file names, or some other identifier meaningful to you. If no _model id_ (see [Identifiers](identifiers)) is provided in the POST, the platform will mint a GUID.

The PATCH operation is only permitted for changes to assets that _do not require reprocessing_, because it updates the submitted assets synchronously. Therefore changes to metadata fields like [string1](asset#string1), or [roles](asset#roles) can be patched, but changes to the [origin](asset#origin) or [delivery channels](asset#deliveryChannels) are not permitted.




## defaultMaxWidth

If greater than zero, this value will be set for the [maxWidth](asset#maxWidth) property of any _newly created_ asset in the Space.

It does not have any effect on updates of assets.

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:Space | xsd:integer | False | False |


## defaultOpenFullMax

If greater than zero, this value will be set for the [openFullMax](asset#openFullMax) property of any _newly created_ asset in the Space.

It does not have any effect on updates of assets.

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:Space | xsd:integer | False | False |


## defaultOpenMaxWidth

If greater than zero, this value will be set for the [openMaxWidth](asset#openMaxWidth) property of any _newly created_ asset in the Space.

It does not have any effect on updates of assets.

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:Space | xsd:integer | False | False |


> Likely never implement metadata as not used

*(⟳ SPA-06 ruling (a), session 2, 2026-08-12: the phantom `metadata` link — emitted on every
space response but 404 on GET — is removed from the Hydra model in protagonist draft PR
#1255 (`hygiene/spa-06`). The broken sample `p06_space/space_metadata.py` (it followed the
link into the 404) is deleted. The distinct-query design below stays parked here; if a real
space-metadata home is ever needed (e.g. rehousing the Portal's `dlcs:manifestSpace` flag
from Tags), that belongs to the protagonist #1253 discussion.)*

## metadata

Returns information about the use of metadata ([string1](asset#string1), [number1](asset#number1) etc) fields on assets within the space. The returned vocab:SpaceMetadata resource provides further query endpoints.

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:Space | vocab:SpaceMetadata | False | False |

Currently only one further query endpoint is supported, _distinct_:

`customers/{{customer_id}}/spaces/2/metadata/distinct?field={{fieldName}}`

For example, 

`customers/{{customer_id}}/spaces/2/metadata/distinct?field=string3`

might return:

```
{
    "strings": [
        "",
        "s33",
        "test_string3"
    ]
}
```

This example query returns all the distinct values of the [string3](asset#string3) metadata field across all assets in the space.
