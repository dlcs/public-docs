
space has `maxUnauthorised` = 1

PUT ../spaces/123
{
    "id": 456,
    "name": "blah"
}

This works but ignores 456; space 123 is created.
Should it be a Bad Request?

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
