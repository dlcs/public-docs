

> Actual JSON response for non admin should not have `administrator`, `acceptedAgreement` fields.

> for admin, they should come back *without* trailing spaces!!!


GET is only operation supported on Customer - how do I edit name and displayName?


## spaces

A link to a paged [Collection](collections) of all the [Space](space) resources associated with your customer. A space allows you to organise assets (like folders), and specify different default [roles](space#defaultroles), [tags](space#defaulttags) and [delivery channels](space#deliverychannels) per space.

### HTTP operations

> Three new fields - defaults

```
POST /customers/{customer}/spaces
{ "name": "My new space" }
```

| field | |
|:---|:---|
| [name](space#name) | REQUIRED |
| [defaultTags](space#defaulttags) | OPTIONAL |
| [defaultRoles](space#defaultroles) | OPTIONAL |
| [maxUnauthorised](space#maxunauthorised) | OPTIONAL |


> If you POST to /customers/{customer}/spaces and DO supply an `id` that already exists, a new space is created with a new `id`. This feels wrong. See code sample.






## iiif 🆕

A link to the root API Storage Collection for IIIF Manifests and Collections. When you make new IIIF Presentation API resources, they get created here.

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:EntryPoint | iiif:Collection | True | False |

### HTTP operations

| Method | Label | Expects | Returns | Status |
|:---|:---|:---|:---|:---|
| GET | The root Storage Collection | - | iiif:Collection | 200 OK |
| POST | Add a new IIIF Collection or Manifest | iiif:Collection or iiif:Manifest | iiif:Collection or iiif:Manifest | 201 Created, 400 Bad Request |

See [IIIF Manifests and Collections](iiif).



> allImages in the dos is a merge of these. We can PATCH atm but only the `manifests` property which is not something a customer should do anyway.

### allImages

A query endpoint for retrieving full assets from any of your spaces, using [asset query syntax](asset-queries). It's unlikely you would use this endpoint without additional query data, but if you do it will simply return a paged hydra:Collection of all your assets across all spaces.

### HTTP operations

| Method | Label | Expects | Returns | Status |
|:---|:---|:---|:---|:---|
| GET | Append a [query parameter](asset-queries) to return matching assets across all spaces. | (no body, but usually a query string) | hydra:Collection | 200 OK |
| PATCH | Make partial update to all matching values | (see below) | hydra:Collection | 200 OK |

Note that the items to be updated with `PATCH` can be specified either by the `"member"` property or [query parameter](asset-query) syntax

```
PATCH /customers/2/allImages
{
    "@type": "Collection",
    "member": [ 
        {"id": "2/36/PHOTO.2.22.36.2.tif"},
        {"id": "2/17/my-image.jpg"} 
    ],
    "field": "manifests",
    "operation": "add"
    "value": ["manuscripts"]
}
```

```
PATCH /customers/2/allImages?q={"number": 101}
{
    "@type": "Collection",
    "field": "manifests",
    "operation": "replace"
    "value": ["manuscripts"]
}
```




## originStrategies

On stage, the root /originStrategies doesn't list anything.
Compare with https://deploy-preview-2--dlcs-docs.netlify.app/api-doc/origin-strategy

Also when POSTing, "basic-http-authentication" works but an expanded URI does not.