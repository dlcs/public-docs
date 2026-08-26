# Adjuncts — scratch notes

## Creating an adjunct by supplying content separately (not yet implemented)

> ⟳ ADJ-01 ruled (a) 2026-08-26 (hygiene session 5): stays parked. Tracking ticket is protagonist **#1140** ("Adjuncts consisting of binary content"). Restore this section, the `content` field section below, and the PROV-15 fragments when #1140 ships; the validator's exactly-one-of `origin`/`externalId` rule must relax first.

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

> ⟳ ADJ-06 ruled (a) 2026-08-26 (hygiene session 5): stays parked. Tracking ticket is protagonist **#1142** ("Handle `otherAdjuncts` iiifLink" — API + Orchestrator + extra `@context`), which depends on **digirati-co-uk/iiif-net #62**. Restore this section, the fifth example adjunct in `iiif_link_adjuncts.py`, and the canvas output in single-asset-manifest.mdx when #1142 ships; the validator's `iiifLink` NotEmpty rule must relax first.

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

---

## label requirement (open question, 2026-06-24)

The adjunct creation field-usage table originally marked `label` as **required** in all four columns (POST/PUT external, POST/PUT from origin), and the `### label` prose said it "is required when supplying the adjunct yourself". The validator (`API/Features/Adjuncts/Validation/HydraAdjunctValidator.cs`) does **not** enforce `label`, so the docs were softened to "recommended" to match current behaviour.

Open question: should the API require `label` when the user supplies the adjunct (the four scenarios above)? If so, add a `Label` NotEmpty rule to the validator and restore "required" in the table and prose. Original prose clause removed:
> It is recommended to always supply this, and is required when supplying the adjunct yourself.

---

## Old-doc prose preserved by the 2026-08-03 provenance re-audit

### `iiifLink` expression semantics (PROV-14) — **restore-candidate**

Explains what the field is *for*; dropped in the port, absent from the new `iiifLink`
section:

> "This property is used when the adjunct is _expressed_ by the platform in the IIIF
> Presentation API, either in the [single asset manifest](asset#manifest) or in a
> [Named Query](named-queries)."

### Content-POST fragments (PROV-15) — **park with the ADJ-01 `content` material**

Small fragments dropped without capture; they belong with the parked content-supply
workflow above (only meaningful if/when the `content` endpoint is built):

- rationale: "removing the need to manage the origin"
- on `publicId`: "or by POSTing binary content to the adjunct's ../content URI"
- field-usage table footnote: "** assumes you will provide content later by binary POST"
- field-usage table row: `content | ignored` (×4 columns)

## roles — ⏸ PARKED 2026-08-26 (hygiene session 5, ADJ-03 ruled (a))

> Removed from adjuncts.mdx because adjunct access control is not implemented: no `roles` column,
> Hydra property, validator rule or converter mapping exists; the Orchestrator serves hosted
> adjuncts openly (`OrchestrationAdjunct.RequiresAuth => false`, "Currently adjuncts are not
> auth-covered"; `AdjunctRequestHandler.cs` `// TBD - AUTH`). Tracking ticket: protagonist
> **#1141** "Adjuncts can be access-controlled". A live caution now states that adjuncts are served
> openly. Restore the passages below (and `"roles": []` in the example payloads + the field-usage
> table row) when #1141 ships — and re-decide the **parent-role inheritance rule** ("unless you
> explicitly provide `roles` as an empty array…") at that point; it is design intent, not shipped
> behaviour.

Paragraph after the externalId example:

> While `roles` can be specified when creating an adjunct via `externalId`, and will be stored on the adjunct, the platform will ignore them when serving the adjunct as it has no means of enforcing them.

Paragraph + Aside in "Registering multiple adjuncts":

> If an adjunct needs to be access-controlled, it specifies [roles](../asset#roles) in the same way assets do, and the platform will emit IIIF Auth services when referencing the adjunct in a manifest.
> 
> <Aside type="caution">
> For auth, adjuncts behave like assets on the File [delivery channel](../delivery-channels). Access control is enforced in _exactly_ the same way.
> </Aside>
>

Field section:

### roles

Works in the same way as [asset.roles](../asset#roles) and accepts the same values. If specified, it will result in the platform enforcing access control. IIIF Authorisation Flow 2.0 services will be emitted on the adjunct in any generated manifests.

Unless you explicitly provide `roles` as an empty array, adjuncts will be assigned the roles of their parent asset.

Clause removed from `### publicId`: "…e.g., `https://dlcs.example/adjuncts/2/5/b2921371x_0001.jp2/mets-from-origin.xml`, and access will be subject to any `roles` the adjunct has."

Field-usage table row:

| `roles`     | optional      | optional     | optional         | optional        | as IIIF auth                         |

## creator — ⏸ PARKED 2026-08-26 (hygiene session 5, ADJ-04 ruled (c): defer with pipelines)

> Not implemented (no Hydra property / column / validator / converter — dropped on input, never
> emitted). Deferred with the pipelines feature; tracked on the **dlcs/private-protagonist #13**
> "Adjunct-producing pipeline" epic (docs note posted there 2026-08-26) — no separate issue. The
> open design question (should the store-only half exist independently of pipelines?) is recorded
> in that comment. Restore the section, the `### profile` sentence, the field-usage row and the
> intro example's `creator` line when the epic delivers. (The intro example + narrative at
> adjuncts.mdx ~:63/:80 are rewritten under ADJ-16.)

Field section:

### creator

This is used to identify the process that created the adjunct — or if it has not been created yet, the process you want to invoke to create it. If you are supplying the adjunct yourself, for the platform to store and serve, you may supply a `creator` field which should be a fully qualified URI. The platform doesn't make use of this information, it just stores it with the adjunct for your reference. The URI is an identifier for _your_ external pipelines and processes.

If you are asking the platform to create the adjunct, you specify a value that matches one of the platform's known pipelines. On initial PUT or POST the platform enqueues the adjunct to be processed by that pipeline.

See [pipelines](../pipelines) for more detail. You can ignore this property if supplying the content of adjuncts yourself.

Sentence removed from `### mediaType`: "…you must supply a `mediaType`. If you are asking the platform to create the adjunct, by specifying a `creator` that matches one of the platform's known pipelines, you should _not_ supply `mediaType` because the platform will set this itself."

Sentence removed from `### profile`: "…sometimes not relevant or possible. If you are asking the platform to create the adjunct, by specifying a `creator` that matches one of the platform's known pipelines, you should _not_ supply `profile` because the platform will set this itself."

Field-usage table row:

| `creator`   | optional      | optional     | optional         | optional        | no                                   |

## source — ⏸ PARKED 2026-08-26 (hygiene session 5, ADJ-05 ruled (c): defer with pipelines)

> Not implemented (dropped on input, never emitted). Deferred with pipelines alongside `creator`;
> docs note posted on **dlcs/private-protagonist #13** 2026-08-26 (second comment) — no separate
> issue. Restore the section, the field-usage row and the intro example's `source` line when the
> epic delivers (intro example/narrative rewritten under ADJ-16).

Field section:

### source

Only valid when you are asking the platform to create the adjunct via a pipeline — and even then, only when you need to specify one of the other adjuncts. In most cases the platform can work out what source you mean. For many pipelines, the source is the asset itself (e.g., OCR) and for others there may only be one other adjunct that could be a suitable source (as in the `annotationsFromOCR` example above).

If you are supplying the adjunct yourself, for the platform to store and serve, you may supply a `source` that makes sense to you, if some external process has been involved. If the platform is creating the adjunct it will always set the source field to either the asset `@id` or one of the other adjunct `@id` values, and return the value on subsequent GETs. Whenever the platform serves an adjunct, and there is a source, it will always appear as a full URL.

Field-usage table row:

| `source`    | optional      | optional     | optional         | optional        | no                                   |
