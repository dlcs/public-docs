# pdf and zip output types — ✅ PROMOTED 2026-08-19 (session 4, DIS-07 ruled (b))

> ⟳ DIS-07 ruled (b): `pdf`, `zip` AND `raw-resource` all documented in a new `## Output types`
> section of named-queries.mdx, with control files, 202+Retry-After, the pdf purge DELETE, and
> (PO wording) "PDF generation may not be enabled on all environments". New sample
> `named_query_outputs.py` proven end-to-end on stage (zip 200 + 744KB archive, raw-resource
> asset-id array, control files, purge). **Two corrections found while executing:**
> 1. The claim below that the zip contains the **largest available thumbnails is WRONG** (PO
>    correction, code-verified): both zip and pdf use `SizeClosestTo(ProjectionThumbsize)`,
>    default **1000px** (`OrchestratorSettings.cs:300-302`, `ImageThumbZipCreator.cs:139`,
>    `FireballPdfCreator.cs:123`). Doc says "closest to the platform's configured projection
>    size (1000 pixels by default)".
> 2. **RELEASE-GATED TWIN (XC-01 family):** the pdf purge DELETE returns **200 + {"success":true}**
>    on released v1.13.2 (wire-confirmed; `Ok(new { success = result })` in the v1.13.2 tag).
>    Our session-0 XC-01 change (develop-only) makes it **204 No Content**. When the carrying
>    release ships: update the purge sentence in named-queries.mdx#pdf-and-zip to 204, and the
>    `purge_pdf` expectation comment + body-print in `named_query_outputs.py`.
> Stage quirk (not documented): the FIRST pdf GET returns a 500 while kicking off generation,
> subsequent GETs 202+Retry-After:600; generation never completes on stage — Fireball
> presumed not deployed there. pdf works in production installations.
> (Old heading follows — kept for the historical verification notes.)

(was) # pdf and zip output types — ⟳ IMPLEMENTED, restore (verified 2026-08-03, DIS-07)

**Stale heading — these ARE implemented** (PDF: `Orchestrator\Features\PDF\PdfController.cs`;
ZIP: `Zip\ZipController.cs`; plus an undocumented `raw-resource` type, `Query\QueryController.cs`).
Restore-candidates. Zip verified end-to-end 2026-08-03: route → `GetZipFromNamedQueryHandler`
→ `ZipNamedQueryParser` → `ImageThumbZipCreator` (builds archive on disk, uploads to S3,
stored-projection lifecycle) with 16 integration tests (`Orchestrator.Tests/Integration/ZipTests.cs`)
covering 404s, **202 + Retry-After while generation is in process**, stale-control-file
regeneration and asset ordering. Two precision points for the eventual docs: (1) the zip
contains the **largest available thumbnails of image assets** (`ImageThumbZipCreator` /
`IThumbSizeProvider`), not original files — say so explicitly; (2) the 202+Retry-After
in-process behaviour is real today and worth documenting (it also matches where PR #1230
wants to take PDF). Still source+test verification only — a sample exercising pdf/zip
against a live deployment remains the DIS-07 punch item.
The output-type table in the page originally listed three values:

| output-type | |
|:---|:---|
| `iiif-resource` | Generates a IIIF Manifest |
| `pdf` | Generates a PDF |
| `zip` | Generates a zip file |

When restoring: also document the pdf purge endpoint
(`DELETE /customers/{c}/resources/pdf/{queryName}?args=...` — pdf only, no zip
equivalent), and per open PR #1230 (RFC 024, async Text-Services `/pdf/v2/`) do not
document synchronous first-request generation as contractual.


# PDF-specific template parameters — ✅ PROMOTED / DROPPED 2026-08-19 (session 4, DIS-08 ruled (a))

> ⟳ DIS-08 ruled (a): the three real params (`objectname` pdf+zip, `coverpage` pdf, `redactedmessage`
> pdf) documented in named-queries.mdx#output-types with the replacement-token list
> ({s1}{s2}{s3}{n1}{n2}{n3}, unmatched tokens removed); `sequence` and `roles` **dropped** from all
> examples — drop-disposition executed, they exist below only as a record of what the old docs
> wrongly claimed. Old "filename used when downloaded" wording NOT carried over: no
> Content-Disposition is wired from ObjectName — doc says "names the stored object (and, for pdf,
> sets the PDF document title); defaults to Untitled". Sample extended with `objectname={s1}.zip`
> and wire-proven: zip control-file key flipped from `/Untitled` to `/autumn-1985.zip`.

(was) # PDF-specific template parameters — ⟳ PARTLY implemented (verified 2026-08-03, DIS-08)

**Three of these are real, two are not:** `objectname` (pdf AND zip), `coverpage`,
`redactedmessage` are implemented (`StoredNamedQueryParser.cs`, `PdfNamedQueryParser.cs`)
— restore-candidates. **`roles` is NOT a template param** (it is an output field on the
control file; roles derive from the selected assets) and **`sequence` is parsed nowhere**
— both should be corrected out of the old examples, not restored (drop-disposition).

| `objectname` | The filename used when the result is downloaded | `&objectname={s1}_{n1}.pdf` |
| `coverpage` | URL of a cover page to prepend to a generated PDF | `&coverpage=https://example.org/cover/{s1}` |
| `redactedmessage` | Message to display for access-controlled pages in a PDF | `&redactedmessage=This page is restricted` |
| ~~`roles`~~ | ~~Restrict the named query result to a role~~ — not a template param | |

# Complex examples (use unimplemented PDF parameters)

```
manifest=s1&sequence=n1&canvas=n2&s1=p1&n1=p2&space=p3&#=5&objectname={s1}_{n1}.pdf&coverpage=http://wellcomelibrary.org/service/pdfcoverpageaspdf/{s1}/0&roles=https://api.dlcs.example/customers/2/roles/clickthrough&redactedmessage=This page is restricted and is not available in PDF downloads
```

```
manifest=s3&sequence=n1&canvas=n2&s3=p1&objectname={s3}&coverpage=http://wellcomelibrary.org/service/pdfcoverpage/{s3}/0&roles=https://api.dlcs.example/customers/4/roles/clickthrough
```

```
manifest=s3&canvas=n2&space=p1&s3=p2&objectname={s3}_{n2}.pdf&coverpage=https://iiif.wellcomecollection.org/pdf-cover/{s3}&roles=https://api.dlcs.example/customers/2/roles/clickthrough&redactedmessage=This page is restricted and is not available in PDF downloads
```

# manifest field — ⟳ answered 2026-08-03 (DIS-10)

Verify what the manifest id should look like in this query (currently "xxxx").
**Answer:** `manifest` sets `assetQuery.Manifests` (comma-separated membership
identifiers, filtering on the asset's own `manifests` list) — typically supplied via
`p1`; not "xxxx" and not a stored-Manifest entity id. NOTE the old docs meant
something different by `manifest` (*"How to group images"*, `&manifest=s1` — a
grouping key); that redefinition is PROV-08 and the room should confirm the new
meaning is the intended one before the docs table is finalised.

# global named queries — ⟳ answered 2026-08-03 (DIS-09)

should I be able to see other customer's NQs? **Answer:** yes for global ones —
customers can GET their own NQs or any `global` NQ; create/edit of a global NQ is
admin-only (403 otherwise); `global` is effectively settable only at create (PUT
persists only `template`); DELETE is own-customer only.

# sequence (PROV-07, captured 2026-08-03) — drop-disposition

The old docs' template-syntax table had a `sequence` row (*"Which sequence to use"*,
`&sequence=n1`). `sequence` is parsed nowhere in current code; the tokens survive
only inside the complex examples above. Preserved here so a reader of those examples
can know what it *was*; do not restore unless the feature returns.

