

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