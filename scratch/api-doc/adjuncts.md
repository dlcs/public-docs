# Adjuncts — scratch notes

## Creating an adjunct by supplying content separately (not yet implemented)

This section was removed from adjuncts.mdx because the content endpoint cannot currently be POSTed to or read from.

The third mechanism creates the API resource for the adjunct, and then supplies the binary content in a separate step. Again, the adjunct can be created by PUT or POST:

```
POST https://api.dlcs.example/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts
{
    "id": "mets-from-content.xml",
    "@type": "Dataset",
    "mediaType": "text/xml",
    "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
    "label": { "en": [ "METS-ALTO XML" ] },
    "iiifLink": "seeAlso"
}
```

or by PUT (`id` is optional but if present, must match the PUT URL):

```
PUT https://api.dlcs.example/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/mets-from-content.xml
{
    "@type": "Dataset",
    "mediaType": "text/xml",
    "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
    "label": { "en": [ "METS-ALTO XML" ] },
    "iiifLink": "seeAlso"
}
```

In both these cases the response is HTTP 201 Created, and the adjunct API resource is available immediately and looks like this:

```
GET https://api.dlcs.example/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/mets-from-content.xml
```
returns:

```json
{
    "@id": "https://api.dlcs.example/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/mets-from-content.xml",
    "@type": "Dataset",
    "mediaType": "text/xml",
    "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
    "label": { "en": [ "METS-ALTO XML" ] },
    "iiifLink": "seeAlso",
    "motivation": null,
    "provides": null,
    "size": 0,
    "ingesting": false,
    "error": null,
    "created": "2025-09-22T16:49:29+00:00",
    "finished": "2025-09-22T16:49:29+00:00",
    "roles": [],
    "content": "https://api.dlcs.example/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/mets-from-content.xml/content"
}
```

The adjunct has no `publicId` property, and has a `size` of 0.

To change this we need to POST the content to the URL given by the adjunct's `content` property:

```
POST https://api.dlcs.example/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/mets-from-content.xml/content
<binary body>
```

This is a synchronous operation. Requesting the adjunct immediately will result in HTTP 200 OK, but the `ingesting` property is likely to be `true`. Once the POSTed content has been stored and measured and the adjunct record updated, the `ingesting` property will be `false`. Any error encountered will be recorded in the `error` property.

LinkCard: 💻 Create an adjunct by supplying content separately
→ dlcs-docs-client/p13_adjuncts/content_adjunct.py

---

## content field (not yet implemented)

This section was removed from adjuncts.mdx because the content endpoint cannot currently be POSTed to or read from.

`/customers/{customer}/spaces/{space}/images/{assetId}/adjuncts/{adjunctId}/content`

A link to the adjunct content. Assuming the adjunct has been processed, an HTTP GET request will return the same bytes as the `publicId`, but without using any IIIF Auth via roles. If you have an API key to see the API adjunct, the same key will let you access the content at this URL.

The other use of `content` is to _supply_ the bytes of an adjunct, via HTTP POST. If created without an `origin` (or without a creating pipeline specified), the adjunct will have no content and size 0, _until_ the bytes of the adjunct are POSTed to this URL.

---

## No iiifLink / otherAdjuncts (not yet implemented)

Removed from the iiifLink section and the single-asset-manifest examples. When implemented:

- `iiifLink` will accept a no or null value
- Adjuncts without `iiifLink` will appear in a non-standard `otherAdjuncts` property on the Canvas (defined in the single-asset-manifest @context)
- As `otherAdjuncts` is not a valid IIIF property, users should process and remove it when turning platform-generated IIIF into public-facing IIIF

The fifth adjunct in the iiifLink example (before removal):

```json
{
    "id": "link-unspecified-from-external.xml",
    "externalId": "https://dlcsstage-public-test-objects.s3.eu-west-1.amazonaws.com/images-with-text/b29820947_0014.jp2.xml",
    "@type": "Text",
    "mediaType": "text/xml",
    "label": { "en": [ "A link to a resource without a IIIF expression" ] }
}
```

The corresponding canvas output (before removal):

```jsonc
"otherAdjuncts": [     // new property (defined in single-asset-manifest @context)
    {
        "id": "https://dlcsstage-public-test-objects.s3.eu-west-1.amazonaws.com/images-with-text/b29820947_0014.jp2.xml",
        "type": "Text",
        "format": "text/xml",
        "label": { "en": ["A link to a resource without a IIIF expression"]}
    }
]
```
