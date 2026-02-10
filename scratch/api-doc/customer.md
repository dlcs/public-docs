

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



## deliveryChannelPolicies

/customers/15/deliveryChannelPolicies returns

```
{
    "@context": "http://www.w3.org/ns/hydra/context.jsonld",
    "@id": "https://api.dlcs-stage.digirati.io/customers/15/deliveryChannelPolicies",
    "@type": "Collection",
    "totalItems": 4,
    "member": [
        {
            "@id": "https://api.dlcs-stage.digirati.io/customers/15/deliveryChannelPolicies/iiif-img",
            "@type": "Collection",
            "title": "Policies for IIIF Image service delivery",
            "totalItems": 0
        },
        {
            "@id": "https://api.dlcs-stage.digirati.io/customers/15/deliveryChannelPolicies/thumbs",
            "@type": "Collection",
            "title": "Policies for thumbnails as IIIF Image Services",
            "totalItems": 0
        },
        {
            "@id": "https://api.dlcs-stage.digirati.io/customers/15/deliveryChannelPolicies/iiif-av",
            "@type": "Collection",
            "title": "Policies for Audio and Video delivery",
            "totalItems": 0
        },
        {
            "@id": "https://api.dlcs-stage.digirati.io/customers/15/deliveryChannelPolicies/file",
            "@type": "Collection",
            "title": "Policies for File delivery",
            "totalItems": 0
        }
    ]
}
```

but /customers/15/deliveryChannelPolicies/thumbs returns

```
{
    "@context": "http://www.w3.org/ns/hydra/context.jsonld",
    "@id": "https://api.dlcs-stage.digirati.io/customers/15/deliveryChannelPolicies/thumbs",
    "@type": "Collection",
    "totalItems": 1,
    "pageSize": 1,
    "member": [
        {
            "@context": "https://api.dlcs-stage.digirati.io/contexts/DeliveryChannelPolicy.jsonld",
            "@id": "https://api.dlcs-stage.digirati.io/customers/15/deliveryChannelPolicies/thumbs/default",
            "@type": "vocab:DeliveryChannelPolicy",
            "name": "default",
            "displayName": "A default thumbs policy",
            "channel": "thumbs",
            "policyData": "[\"!1024,1024\",\"!400,400\",\"!200,200\",\"!100,100\"]",
            "policyCreated": "2024-04-17T15:10:53.8550160Z",
            "policyModified": "2024-04-17T15:10:53.8550160Z"
        }
    ]
}
```

The first doesn't show the nested members - claims there are no nested members.


Delivery channel policies use `name` instead of `id` as the field for the slug - I had to change the documentation here.



## defaultDeliveryChannels

POST /customers/2/defaultDeliveryChannels
{
    "channel": "iiif-img",
    "policy": "https://api.dlcs.example/customers/{customer}/deliveryChannelPolicies/iiif-av/default-video",
    "mediaType": "application/mp4"
}

`policy` needed to be a FQ URL not just "default" - check.