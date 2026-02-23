# COPIED WHOLESALE FROM OLD SITE

# Pipelines

import { Callout } from 'nextra/components'

<Callout type="warning" emoji="⚠️">
  DO NOT USE THIS PAGE. This is simply to salvage some useful text from the adjuncts page now that that page doesn't cover pipelines.
</Callout>

## (Ragbag from old adjuncts page)

While the above is an example of a GET returning an already-created adjunct, the resource would be the same if supplied as a POST to this collection (assuming the METS-ALTO adjunct had already been added):

```
POST https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts       
{
    "id": "b2921371x_0001.anno.json",
    "@type": "AnnotationPage",
    "label": { "en": [ "IIIF Annotations for b2921371x_0001.jp2" ] },
    "roles": [],
    "creator": "pipeline:annotationsFromOCR",
    "source": "b2921371x_0001.xml"
}
```

or a direct PUT:

```
PUT https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/b2921371x_0001.anno.json       
{
    "@type": "AnnotationPage",
    "label": { "en": [ "IIIF Annotations for b2921371x_0001.jp2" ] },
    "roles": [],
    "creator": "pipeline:annotationsFromOCR",
    "source": "b2921371x_0001.xml"
}
```

It's also possible to supply adjuncts _and_ specify pipeline operations on them in the same POST. For example, if that asset had no existing adjuncts the same result could be obtained with:

```
POST https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts     
[
    {
        "id": "b2921371x_0001.xml",
        "@type": "Dataset",
        "label": { "en": [ "METS-ALTO text for b2921371x_0001.jp2" ] },
        "mediaType": "text/xml",
        "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
        "origin": "https://s3-eu-west-1.amazonaws.com/example-bucket/digitised/b2921371x/v1/data/objects/alto/b2921371x_0001.xml",
        "roles": []
    },
    {
        "id": "b2921371x_0001.anno.json",
        "@type": "AnnotationPage",
        "label": { "en": [ "IIIF Annotations for b2921371x_0001.jp2" ] },
        "roles": [],
        "creator": "pipeline:annotationsFromOCR",
        "source": "b2921371x_0001.xml"
    }
]
```

The POST to the asset's [adjuncts](asset#adjuncts) collection can take a single adjunct, an array of adjuncts, or a Hydra Collection width an array of adjuncts as `member`.



## creator

This is used to identify the process that created the adjunct - or if it has not been created yet, the process you want to invoke to create it. If you are supplying the adjunct yourself, for the platform to store and serve, you may supply a `creator` field which should be a fully qualified URI. The platform doesn't make use of this information, it just stores it with the adjunct for your reference. The URI is an identifier for _your_ external pipelines and processes. 

If you are asking the platform to create the adjunct, you specify a value that matches one of the platform's known pipelines. On initial PUT or POST the platform enqueues the adjunct to be processed by that pipeline.

See [pipelines](pipelines) for more detail. You can ignore this property if supplying the content of adjuncts yourself.

Current defined pipelines are:

(only one of these is supported so far!)

| name | description |
|:-----|:------------|
| pipeline:test               | Generates a text file adjunct that contains the size of the asset file in bytes |
| pipeline:OCR                | Generates METS-ALTO XML from the asset (assuming the asset is an image) |
| pipeline:annotationsFromOCR | Generates IIIF (W3C) web annotations from a supported OCR format such as METS-ALTO or hOCR |
| more...                     |           |
| pipeline:AVTranscript       | ... |
| pipeline:HTR                | ... |
| pipeline:sentiment          | ... |
| pipeline:NER                | ... |
| pipeline:imageDescription   | ... |
| pipeline:paletteInfo        | ... |

### pipeline versions

The above examples are _unversioned_ - the intention is "use the latest version of this pipeline". Once the pipeline has processed, the `creator` value given to the new adjunct will include a version part:

```
{
    "creator": "pipeline:OCR/v0.9.1"
}
```

You can specify the full versioned pipeline in the initial call (e.g., to ensure consistency over time).

## source

Only valid when you are asking the platform to create the adjunct - and even then, only when you need to specify one of the other adjuncts. In most cases the platform can work out what source you mean. For many pipelines, the source is the asset itself (e.g., OCR) and for others there may only be one other adjunct that could be a suitable source (as in the `annotationsFromOCR` example above). 

If you are supplying the adjunct yourself, for the platform to store and serve, you may supply a `source` that makes sense to you, if some external process has been involved. If the platform is creating the adjunct it will always set the source field to either the asset `@id` or one of the other adjunct `@id` values, and return the value on subsequent GETs. Whenever the platform serves an adjunct, and there is a source, it will always appear as a full URL. When referring to one of the other adjuncts in a POST or PUT, you may supply either the full URL or the last path part, the implied `id` (as in the examples above). If specified at all, an adjunct's `source` can only be one of the other adjuncts, making this reference unambiguous.


# Adjunct creation field usage 

THIS TABLE IS OUT OF DATE, the one in adjuncts has been updated

See [pipeline](pipelines) for further clarification of how these fields are used when invoking a platform pipeline.

The following table assumes that you are responsible for the binary content of the adjunct.


| Field       | POST existing | PUT existing         | POST create | PUT create           | appears in IIIF  |
|:------------|---------------|----------------------|-------------|----------------------|------------------|
| `@id`       | not allowed   | optional, must match | not allowed | optional, must match | no               |
| `id`        | not allowed   | optional, must match | not allowed | optional, must match | as last path element if not external |
| `origin`    | optional      | optional             | not allowed | not allowed          | no               |
| `externalId`| optional      | optional             | not allowed | not allowed          | no               |
| `@type`     | required      | required             | not allowed | not allowed          | yes              |
| `mediaType` | required      | required             | not allowed | not allowed          | yes, as `format` |
| `profile`   | optional      | optional             | not allowed | not allowed          | yes              |
| `label`     | required      | required             | optional    | optional             | yes              |
| `language`  | optional      | optional             | optional    | optional             | yes              |
| `roles`     | optional      | optional             | optional    | optional             | as IIIF auth     |
| `creator`   | optional      | optional             | required    | required             | no               |
| `source`    | not allowed   | not allowed          | depends     | depends on pipeline  | no               |
| `publicId`  | not allowed   | not allowed          | not allowed | not allowed          | The IIIF `id`    |
| `size`      | not allowed   | not allowed          | not allowed | not allowed          | yes              |
| `content`   | not allowed   | not allowed          | not allowed | not allowed          | no               |


# More examples

The examples so far show a pipeline using an existing adjunct as source. However, that same pipeline could use an adjunct that itself had been created by a pipeline. In the following example, the platform is doing the OCR itself, and then using the OCR output to generate IIIF annotations.

Assume an image asset with _no_ adjuncts:

```
POST https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts     
[
    {
        "id": "b2921371x_0001.xml",
        "label": { "en": [ "METS-ALTO text for b2921371x_0001.jp2" ] },
        "creator": "pipeline:OCR"
    },
    {
        "id": "b2921371x_0001.anno.json",
        "label": { "en": [ "IIIF Annotations for b2921371x_0001.jp2" ] },
        "creator": "pipeline:annotationsFromOCR"
    }
]
```

This is enough information for the platform to process the pipelines in the correct order, assign `source` values, etc.

Once this process has finished, the result would be:

`GET https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts`

```json copy
{
    "@context": "https://dlcs.github.io/vocab/context/future.json",
    "@id": "https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts",
    "@type": "Collection",
    "totalItems": 2,
    "member": [
        {
            "@id": "https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/b2921371x_0001.xml",
            "@type": "Dataset",
            "label": { "en": [ "METS-ALTO text for b2921371x_0001.jp2" ] },
            "mediaType": "text/xml",
            "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
            "language": [ "en" ],
            "roles": [],
            "creator": "pipeline:OCR/v0.9.1",
            "source": "https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2",
            "publicId": "https://dlcs.io/adjuncts/2/5/b2921371x_0001.jp2/b2921371x_0001.xml",
            "size": 240563,
            "content": "https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/b2921371x_0001.xml/content"
        },
        {
            "@id": "https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/b2921371x_0001.anno.json",
            "@type": "AnnotationPage",
            "label": { "en": [ "IIIF Annotations for b2921371x_0001.jp2" ] },
            "mediaType": "application/json",
            "language": [ "en" ],
            "roles": [],
            "creator": "pipeline:annotationsFromOCR/v0.9.1",
            "source": "https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/b2921371x_0001.xml",
            "publicId": "https://dlcs.io/adjuncts/2/5/b2921371x_0001.jp2/b2921371x_0001.anno.json",
            "size": 390553,
            "content": "https://api.dlcs.io/customers/2/spaces/5/images/b2921371x_0001.jp2/adjuncts/b2921371x_0001.anno.json/content"
        }
    ]
}
```
