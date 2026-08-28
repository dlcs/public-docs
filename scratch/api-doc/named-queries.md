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

# manifest field — ✅ ROW PARKED 2026-08-19 (session 4, DIS-10 ruled (d))

> ⟳ DIS-10 ruled (d): the `manifest` row REMOVED from the live template-syntax table for
> **DIS-03 consistency** — the manifests-membership concept (asset-query `manifests` filter AND
> this NQ template key are the same underlying data) stays out of the published surface until
> the iiif page promotes the whole concept. **Promote this row when iiif.mdx lands** (with
> DIS-03's parked filter material), using the corrected form below.
>
> Removed row (original, with its two defects — placeholder value + doubly-broken link):
> `| manifest | Select assets that are part of a stored [IIIF Manifest](iiif) | &manifest=xxxx |`
>
> Promotion-ready corrected row:
> `| manifest | Select assets that are part of a stored [IIIF Manifest](../iiif) — the value is the stored manifest's id, as minted by the IIIF Presentation API | &manifest=p1 |`
>
> Value semantics (code-verified 2026-08-19 @develop 92fa2661): `manifest` sets
> `assetQuery.Manifests` (comma-split array, `BaseNamedQueryParser.cs:149-152`), filtering on
> the asset's own `manifests` membership list (`NamedQueryRepository.cs:110-113`); the values
> are iiif-presentation **flat manifest ids**, written onto assets when a Manifest stores
> painted resources (`DlcsManifestCoordinator.cs:399`). Stage's global `manifest-query` NQ
> (`template: manifest=p1`) is a live example.

(original 2026-08-03 note:)
Verify what the manifest id should look like in this query (currently "xxxx").
**Answer:** `manifest` sets `assetQuery.Manifests` (comma-separated membership
identifiers, filtering on the asset's own `manifests` list) — typically supplied via
`p1`; not "xxxx" and not a stored-Manifest entity id. NOTE the old docs meant
something different by `manifest` (*"How to group images"*, `&manifest=s1` — a
grouping key); that redefinition is PROV-08 and the room should confirm the new
meaning is the intended one before the docs table is finalised.

# global named queries — ✅ PARTIALLY PROMOTED 2026-08-19 (session 4, DIS-09 ruled (b))

> ⟳ DIS-09 ruled (b): a minimal `## global` section is live in named-queries.mdx (available to
> all customers; appears in every customer's collection; admin-only to create; read-only
> otherwise). The FULL semantics below stay here because they will change when protagonist
> **#566** ("Customers can view Global NamedQueries") lands — the write-up below is drafted on
> the #566 assumption that a customer can FOLLOW the link to another customer's global named
> query. **Promote the full table when #566 ships in a release**, updating the `@id` rows to
> whatever form #566 delivers (planned: `@id` omits the customer id; new `GET /namedQueries`
> and `GET /namedQueries/{id}` global endpoints).

## Full `global` contract — code-verified @develop 92fa2661, every row wire-confirmed on released v1.13.2 (2026-08-19, non-admin)

| behaviour | today (v1.13.2, wire-confirmed) | after #566 (planned) |
|:---|:---|:---|
| visibility in collections | global NQs appear in **every** customer's `namedQueries` collection alongside their own | unchanged; plus a dedicated `GET /namedQueries` listing all global NQs |
| single GET | 200 via **any** customer's path (`/customers/{you}/namedQueries/{id}`) | plus `GET /namedQueries/{id}` |
| `@id` in the response body | points at the **owning** customer (e.g. `/customers/26/...`) — **not followable** with your own credentials: basic-auth rejects the other customer's path | `@id` omits the customer id, so the advertised link is followable (same fix family as #525) |
| create with `global: true` | **403** "Only admins are allowed to create global Named Queries" for non-admins | unchanged |
| PUT carrying `"global": true` | **403** for non-admins — the gate checks the *body*, not the effect. Trap: echoing a GETted global NQ body back into a PUT hits this | unchanged (unless #566 revisits) |
| PUT (any body, own NQ) | persists **only `template`** — `global` is never updated, even for admins; effectively set-at-create, delete-and-recreate to change (like `name`) | unchanged |
| PUT / DELETE a foreign global NQ | **404** — write paths match own customer only; non-owners cannot modify or delete | unchanged |
| vocab flags | `global`: readonly False, writeonly False (settable at create by admins — consistent) | unchanged |

(original 2026-08-03 note, superseded by the table above:)
should I be able to see other customer's NQs? **Answer:** yes for global ones —
customers can GET their own NQs or any `global` NQ; create/edit of a global NQ is
admin-only (403 otherwise); `global` is effectively settable only at create (PUT
persists only `template`); DELETE is own-customer only.

# sequence (PROV-07, captured 2026-08-03) — drop-disposition

The old docs' template-syntax table had a `sequence` row (*"Which sequence to use"*,
`&sequence=n1`). `sequence` is parsed nowhere in current code; the tokens survive
only inside the complex examples above. Preserved here so a reader of those examples
can know what it *was*; do not restore unless the feature returns.


# canvas vs assetOrder emphasis — ✅ SWAPPED 2026-08-19 (session 4, DIS-11 ruled (a))

> ⟳ DIS-11 ruled (a): docs now lead with `assetOrder` everywhere (syntax table, worked example,
> all five example templates + results table, n1-n3 row examples, all three p16 samples);
> `canvas` presented as "Legacy alias for `assetOrder`, kept for backwards compatibility" —
> matching the code's `[Obsolete]` marking (`BaseNamedQueryParser.cs:30-31`; both keys set
> AssetOrdering identically, so the asc/desc/`;` syntax works with either). Wire-proven: outputs
> sample re-run green with `assetOrder=n1`. Original table emphasis (replaced):
> `| canvas | The metadata field used to order canvases in the projection | &canvas=n2 |`
> `| assetOrder | Alias for canvases, more generic when the project is not a IIIF manifest | &assetOrder=n2 |`
> Note: existing NQs in the wild (incl. stage globals `manifest`, `manifest-query`) still use
> `canvas` — permanent wire surface, hence alias documented rather than dropped.

> ⟳ DIS-11 addendum (2026-08-19, PO instruction): the trailing h1 "# More on assetOrder" section
> REMOVED — its content (asc/desc modifiers, multi-field `;` syntax) promoted into the syntax
> section: mentioned in the assetOrder table row and shown in a code block directly under the
> table, where readers will see it. Wire-verified via iiif-resource projections:
> `assetOrder=n1 desc` reverses canvas order (nq_03→01); `assetOrder=s1;n1 desc` (tie on s1,
> secondary decides) also reverses — modifiers and multi-field both real on v1.13.2.
> **Discovery during verification: `raw-resource` IGNORES assetOrder** (same desc template
> returned ascending ids) — the DIS-07 sentence "in query order" was corrected to "assetOrder
> does not apply to this output type; treat the array as unordered". Also: manifest canvas
> labels are positional ("Canvas 1/2/3"), a non-discriminating signal for ordering tests —
> use the painted asset ids.

# raw-resource ordering — ⏳ RELEASE-GATED twin (added 2026-08-26, session-5 pre-flight; DIS-11 follow-up)

> ⟳ Protagonist **PR #1289** (merged to develop 2026-08-24, fixes **#1285**) makes `raw-resource`
> honour `assetOrder`: `GetNamedQueryAssetIds.cs:44` now applies `.OrderByNamedQuery(parsedQuery)`
> (new `Orchestrator/Infrastructure/NamedQueries/NamedQueryOrderingX.cs:28-68`, OrderBy/ThenBy per
> field with asc/desc), and all NQ ordering moved from in-memory to the database query. Not in any
> release yet (latest v1.13.2, 2026-07-17); docs main keeps the released "unordered" sentence.
>
> **Apply when the release carrying #1289 ships.** In `named-queries.mdx` `### raw-resource` (currently
> line 267), replace:
>
> > Note that `assetOrder` does not apply to this output type; treat the array as unordered:
>
> with:
>
> > The array is returned in `assetOrder` order (the same ordering, modifiers and multi-field
> > syntax as the other output types):
>
> Verification at release: re-run the DIS-11 addendum experiment — a raw-resource projection of a
> template with `assetOrder=n1 desc` must return the asset ids in reverse n1 order (on v1.13.2 it
> returned ascending ids, which is what produced the current sentence). The p16 outputs sample needs
> no change (it reads the array, does not assert order) — add an ordering assertion only if the
> sample-parity rule's owner wants one. Null handling note from the PR: DB ordering vs in-memory
> ordering differ on nulls, but all orderable metadata fields are non-null in the DB, so no
> documented behaviour change beyond raw-resource gaining ordering.
