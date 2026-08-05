# Hygiene sprint — Session 4: Discovery & delivery

**Scope.** Decision cards for the "Discovery & delivery" theme: asset queries, named queries, single-asset manifest, collections, identifiers, size restrictions, entry point, overview. Each card was produced by cross-referencing the live Starlight docs (`src/src/content/docs/api-doc/*.mdx`), the scratch notes (`scratch/api-doc/*.md`), the Python samples (`dlcs-docs-client/`), the old Nextra docs (`C:\git\dlcs\docs\pages\api-doc`) and the protagonist API code (`C:\git\dlcs\protagonist`). Code claims are cited to `file:line`. Decisions are stated neutrally — nothing here has been actioned; no docs/code/samples were edited.

Seed items were verified against code: asset-query **ordering** and **include=adjuncts** are genuinely implemented (promote from scratch); **tags/roles/id** filters and **multi-value string arrays** are genuinely absent (scratch accurate); named-query **PDF/ZIP** output and **objectname/coverpage/redactedmessage** params are implemented (promote), but **sequence/roles** are *not* template params (scratch partly wrong); the EntryPoint model emits **neither** `queue` **nor** `deliveryChannelPolicies` (docs wrong), and **does** emit `portalRoles`/`imageOptimisationPolicies`/`thumbnailPolicies`.

**⟳ Verified 2026-08-03** against protagonist develop@8341d780: **all 21 cards confirmed** as
written (line-drift only; refinements inline on DIS-06/07/09/13/14). New cards DIS-22..24 added.
External development note: open protagonist PR **#1230** proposes RFC 024 (Text-Services PDF
generation) — it authoritatively confirms DIS-07's four projection types and the pdf purge
endpoint, and proposes an async `/pdf/v2/...` (202 + Retry-After) replacing Fireball; when
promoting pdf/zip, avoid documenting synchronous first-request generation as contractual.

## Resolved / no action (verified correct)

- **NamedQuery addressed by minted GUID `id`, not `name`** (identifiers.mdx, named-queries.mdx) — CONFIRMED. Management API routes are `[Route("{namedQueryId}")]` and look up by `nq.Id` (`API\Features\NamedQueries\NamedQueriesController.cs:97,127,160`; `...\Requests\GetNamedQuery.cs:33-36`). (Note: the *public* delivery URL resolves by `name` via `DLCS.Repository\Assets\NamedQueryRepository.cs:GetByName` L32-53 — both statements are true and already reflected in the docs.)
- **DeliveryChannelPolicy uses `name` as path element** (identifiers.mdx#resources-that-use-name-instead-of-id) — CONFIRMED, unchanged.
- **single-asset-manifest correctly omits `dlcs:channelOutputs`** — the old Nextra doc described a `dlcs:channelOutputs` extension; it exists nowhere in protagonist (grep: 0 hits). New doc rightly drops it.
- **asset-query shortcut params `string1-3` / `number1-3` and the `q` object** — CONFIRMED accurate (`API\Features\Assets\Query\AssetQueryConverter.cs:67-115`; `DLCS.HydraModel\ImageQuery.cs:25-47`).

---

### DIS-01 · asset-query ordering now works — promote from scratch
- **Theme:** Discovery & delivery
- **Surfaces:** asset-queries.mdx#permitted-queries (caution Aside L10-12) · scratch/api-doc/asset-queries.md ("Ordering not yet implemented", "More examples") · dlcs-docs-client/p15_asset_queries/asset_queries.py:97-107 (`get_images_ordered` docstring "Not yet supported - ordering is ignored")
- **Type:** STALE-SCRATCH
- **Docs say:** Aside: "ordering … not yet supported." Sample docstring: ordering is ignored. Ordering examples are held back in scratch.
- **Original-doc nuance:** old Nextra had a live `### Ordering` section: *"You can order by the value of a field of an asset: `?orderByDescending=width` / `?orderBy=height`. If no ordering is provided the order is undefined. (or is it created?)"*
- **Code does:** Ordering is implemented. `API\Features\Assets\Query\AssetQueryX.cs:21-37` (`AsOrderedAssetQuery`); default sort is **Created** when `orderBy` is empty (`AssetQueryX.cs:39-58`, `GetPropertyName` returns `"Created"`). Image endpoints read `?orderBy`/`?orderByDescending` via `API\Infrastructure\HydraController.cs:373-385` (`SetOrderBy`), applied in `HandlePagedFetch` L240-243. `orderBy` accepts hydra aliases (`string1`→`Reference1`, `number1`→`NumberReference1`) or any Asset property (e.g. `width`, `height`).
- **Issues/RFCs:** resume-audit-fixes memory, Category D — already flagged.
- **Decision needed:** Promote ordering to live docs and de-list it from the "not supported" Aside; confirm the documented default order ("undefined") should become "Created".
- **Options:** (a) restore an `### Ordering` section + remove "ordering" from the Aside + state default = `Created`; (b) also fix the sample docstring (DIS-06 covers the no-whitelist nuance); (c) defer.
- **Possible outputs:** doc / sample
- **Who's needed:** docs owner
- **Status:** ✅ RULED (session 0, 2026-08-06): options (a) + (b). Owner: PO. Output: public-docs hygiene/session-0 commit — restore `### Ordering`, de-list from the Aside, document default order = `Created`. The sample-docstring half of (b) already landed in PR #7 (2026-08-05)

### DIS-02 · `include=adjuncts` is implemented — Aside & sample stale
- **Theme:** Discovery & delivery
- **Surfaces:** asset-queries.mdx (caution Aside L11 lists `include` as unsupported; but body #include-children L50-56 documents it as accepted) · dlcs-docs-client/p15_asset_queries/asset_queries.py:123-136 (`get_images_with_adjuncts` docstring "Not yet supported - the include parameter is currently ignored")
- **Type:** STALE-SCRATCH (internal contradiction)
- **Docs say:** Aside says `include` not yet supported; the page body says `include=adjuncts` is the only accepted value. The sample says it is ignored.
- **Original-doc nuance:** —
- **Code does:** `include=adjuncts` works. `API\Features\Assets\Query\AssetQueryModel.cs:55-60` (`AllowedFields = [Adjuncts]`); parsed in `AssetQueryConverter.cs:36-42`; eager-load in `AssetQueryX.cs:133-145` (`IncludeRelated` → `.Include(a => a.Adjuncts!)`); passed through `ImagesController.cs:77` and `CustomerImagesController.cs:70,99`. Unknown include values are silently discarded, not errored.
- **Issues/RFCs:** —
- **Decision needed:** Reconcile the contradiction — the body is correct, the Aside and sample are wrong.
- **Options:** (a) remove `include` from the Aside's not-supported list and fix the sample docstring; (b) leave Aside, weaken body (not recommended — contradicts code); (c) defer.
- **Possible outputs:** doc / sample
- **Who's needed:** docs owner
- **Status:** ✅ RULED (session 0, 2026-08-06): option (a). Owner: PO. Output: public-docs hygiene/session-0 commit — remove `include` from the Aside's not-supported list. The sample docstring already fixed in PR #7 (2026-08-05)

### DIS-03 · `manifests` filter is supported but undocumented
- **Theme:** Discovery & delivery
- **Surfaces:** asset-queries.mdx#shortcut-metadata-fields (L25-41, lists only string/number) · code `AssetQueryX.cs:116-120`, `AssetQueryModel.cs:20-30`, `AssetQueryConverter.cs:106-110`
- **Type:** DOC-MISSING
- **Docs say:** "Only the 6 built-in string and number fields are supported." No mention of `manifests`.
- **Original-doc nuance:** —
- **Code does:** `manifests` is filterable both as a shortcut param `?manifests=a,b` (`AssetQueryConverter.cs:106-110`, comma-split array) and in `q` (`ImageQuery.Manifests` is `string[]`, `ImageQuery.cs:25-47`). Filter: `AssetQueryX.cs:116-120` `a.Manifests!.Any(m => assetFilter.Manifests.Contains(m))`. It is the **only** field that accepts multiple values. (Aligns with the earlier `manifest`→`manifests` rename, memory A6.)
- **Issues/RFCs:** resume-audit-fixes A6.
- **Decision needed:** Document the `manifests` filter (and that it is the lone multi-value field).
- **Options:** (a) add a `manifests` row/section to permitted queries; (b) leave undocumented; (c) defer.
- **Possible outputs:** doc / sample
- **Who's needed:** docs owner
- **Status:** ✅ RULED (session 0, 2026-08-06): option (b) — deliberately left undocumented (no-op / close). The `manifests` filter stays out of the published surface for now; revisit if/when the iiif page and manifests feature are promoted

### DIS-04 · tags / roles / id filters not implemented — keep, or design?
- **Theme:** Discovery & delivery
- **Surfaces:** asset-queries.mdx (Aside L11) · scratch/api-doc/asset-queries.md L1-10 · sample `asset_queries.py:61-94` (`get_images_by_tags/roles/id`, "Not yet supported")
- **Issues:** https://github.com/dlcs/protagonist/issues/753
- **Type:** DESIGN (docs currently accurate)
- **Docs say:** tags / roles / id queries not yet supported.
- **Original-doc nuance:** old Nextra `### Query object` listed `q={"tags":[…]}`, `q={"roles":[…]}`, `q={"id":"…"}` as if available, with the caveat *"We will need a full set of query features for portal use."*
- **Code does:** `AssetFilter` has no tags/roles/id properties (`AssetQueryModel.cs:20-30`); `ApplyAssetFilter` only handles Reference1-3 / NumberReference1-3 / Manifests / Space (`AssetQueryX.cs:83-128`). Docs and sample are accurate.
- **Issues/RFCs:** to check (portal requirements).
- **Decision needed:** Are these filters wanted? If yes this is a code feature request; if no, prune the speculative examples from scratch.
- **Options:** (a) leave as documented-future; (b) raise an RFC/issue to add tags/roles/id filtering; (c) discard the scratch examples as not-planned.
- **Possible outputs:** code / RFC / defer
- **Who's needed:** product + protagonist dev
- **Status:** ☐ undecided

### DIS-05 · multi-value string arrays not supported (only `manifests`)
- **Theme:** Discovery & delivery
- **Surfaces:** scratch/api-doc/asset-queries.md#multiple-values (L32-50) · code `ImageQuery.cs:25-47`, `Parse` L37-47
- **Type:** STALE-SCRATCH (mostly accurate)
- **Docs say:** scratch holds `q={"string1":["a","b"]}` / `q={"tags":["a","b"]}` / `q={"id":[…]}` as "not yet implemented".
- **Original-doc nuance:** —
- **Code does:** `ImageQuery.String1/2/3` are scalar `string?`; an array deserialises to failure → `Parse` returns null → controller 400 "Could not parse query" (e.g. `ImagesController.cs:69-72`). Only `manifests` (`string[]`) accepts multiple values. So the scratch note is correct **except** that one multi-value field already exists.
- **Issues/RFCs:** —
- **Decision needed:** When (if) multi-value filtering is generalised, note that `manifests` is the existing precedent; until then leave in scratch.
- **Options:** (a) keep in scratch, annotate the `manifests` exception; (b) raise feature request to generalise; (c) defer.
- **Possible outputs:** RFC / defer
- **Who's needed:** product
- **Status:** ☐ undecided

### DIS-06 · `orderBy` has no field whitelist — invalid name errors at runtime
- **Theme:** Discovery & delivery
- **Surfaces:** asset-queries.mdx (when ordering is promoted, DIS-01) · code `AssetQueryX.cs:21-58`, `HydraController.cs:373-385`, `ControllerBaseX.cs:20-36`
- **Type:** CODE-WRONG (robustness) / DOC
- **Docs say:** (nothing yet — to be written with DIS-01).
- **Original-doc nuance:** —
- **Code does:** `orderBy`/`orderByDescending` are passed through unvalidated; `GetPropertyName` PascalCases the value and feeds `Expression.PropertyOrField` (`AssetQueryX.cs:60-80`). A name that is not an Asset property throws at runtime rather than returning a clean 400. *(⟳ 2026-08-03 refinement: the exception is caught by `HydraExceptionFilter` (`API\Infrastructure\HydraExceptionFilter.cs:40-48`, registered `Startup.cs:117-119`) and surfaces as a well-formed Hydra Error, status **500**, title "Unexpected error" — a handled 500, not a raw crash; still not a 400. `PropertyOrField` matches case-insensitively, so `orderBy=WIDTH` works; ordering by a collection property like `manifests` also fails at EF translation → 500. Values shorter than 2 chars silently default to Created (`AssetQueryX.cs:42-45`).)*
- **Issues/RFCs:** to check.
- **Decision needed:** Should docs advertise only the safe set (string1-3/number1-3 + a few like width/height/created), and/or should the code validate the field and 400 on unknown?
- **Options:** (a) docs list a supported subset only; (b) add server-side validation → 400; (c) both; (d) defer.
- **Possible outputs:** doc / code
- **Who's needed:** docs owner + protagonist dev
- **Status:** ☐ undecided

### DIS-07 · named-query PDF & ZIP output types are implemented — promote
- **Theme:** Discovery & delivery
- **Surfaces:** named-queries.mdx#L37 (output-type table lists only `iiif-resource`) · scratch/api-doc/named-queries.md L1-12 ("pdf and zip output types not yet implemented")
- **Type:** STALE-SCRATCH
- **Docs say:** "Currently `iiif-resource` is supported." pdf/zip rows held in scratch.
- **Original-doc nuance:** old Nextra: *"Permitted values are `iiif-resource`, `pdf`, `zip`."* and intro *"This can generate IIIF Manifests, PDFs, zip files and other multi-asset results."*
- **Code does:** PDF route `Orchestrator\Features\PDF\PdfController.cs:29-31` (`pdf/{customer}/{namedQueryName}/{**args}`, `application/pdf`); ZIP route `Orchestrator\Features\Zip\ZipController.cs:29-31` (`application/zip`); IIIF route `Orchestrator\Features\Manifests\NamedQueryController.cs:16,37-39`; plus a `raw-resource` route `Orchestrator\Features\Query\QueryController.cs:15,32-33`. Control files: `pdf-control` / `zip-control`.
- **Issues/RFCs:** resume-audit-fixes Category D.
- **Decision needed:** Restore `pdf` and `zip` (and possibly `raw-resource`) to the output-type table. *(⟳ 2026-08-03: when doing so, also document the existing purge endpoint `DELETE /customers/{customerId}/resources/pdf/{queryName}?args=...` — deletes control-file + PDF, `CustomerResourcesController.cs:37-58`; pdf only, no zip equivalent — see DIS-23. And per open PR #1230/RFC 024, avoid promising synchronous generation.)*
- **Options:** (a) restore pdf/zip rows; (b) also document `raw-resource`; (c) defer pending a sample that exercises them.
- **Possible outputs:** doc / sample
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### DIS-08 · objectname / coverpage / redactedmessage implemented; sequence & roles are NOT template params
- **Theme:** Discovery & delivery
- **Surfaces:** scratch/api-doc/named-queries.md L14-37 ("PDF-specific template parameters not yet implemented") · code in `DLCS.Repository\NamedQueries\Parsing\`
- **Type:** STALE-SCRATCH (partly wrong)
- **Docs say:** scratch claims `objectname`, `coverpage`, `redactedmessage`, `roles` (and `sequence` in examples) are "likely not yet supported".
- **Original-doc nuance:** old Nextra examples used all of these inline, e.g. *"…&objectname={s1}_{n1}.pdf&coverpage=…&roles=…&redactedmessage=This page is restricted…"*.
- **Code does:** `objectname` → `StoredNamedQueryParser.cs:18,32-34` (`ObjectNameFormat`, PDF **and** ZIP). `coverpage` → `PdfNamedQueryParser.cs:15,30-32` (`CoverPageFormat`/`CoverPageUrl`). `redactedmessage` → `PdfNamedQueryParser.cs:16,33-35`. **`sequence`** is parsed nowhere (no constant/case in any parser). **`roles`** is not a template key — it appears only as an output field on the control file (`DLCS.Repository\NamedQueries\Models\ControlFile.cs:52-53`); roles are derived from the selected assets.
- **Issues/RFCs:** resume-audit-fixes Category D.
- **Decision needed:** Promote `objectname`/`coverpage`/`redactedmessage` to live docs (with pdf/zip applicability) and explicitly drop `sequence`/`roles` as template params (correct the old examples).
- **Options:** (a) promote the three real params, remove `sequence`/`roles` from examples; (b) keep all in scratch until a PDF sample exists; (c) defer.
- **Possible outputs:** doc / sample
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### DIS-09 · named-query `global` field is undocumented
- **Theme:** Discovery & delivery
- **Surfaces:** named-queries.mdx (property sections cover only `name` L93 and `template` L101; no `global`) · scratch/api-doc/named-queries.md L44-46 ("global named queries / should I be able to see other customer's NQs?") · code `DLCS.Model\Assets\NamedQueries\NamedQuery.cs:10`, `DLCS.HydraModel\NamedQuery.cs:52-55`
- **Type:** DOC-MISSING
- **Docs say:** nothing about `global`.
- **Original-doc nuance:** —
- **Code does:** `NamedQuery.Global` (`bool`) exists and is serialised as `"global"` ("available to all customers", `DLCS.HydraModel\NamedQuery.cs:52-55`). GET is global-aware: a customer can fetch their own NQ **or** any global NQ by id (`API\Features\NamedQueries\Requests\GetNamedQuery.cs:33-36`). Create/edit of a global NQ is admin-only (403 otherwise — `NamedQueriesController.cs:75-76,140-141,173-174`). This answers the scratch question: yes, customers see global NQs (read-only unless admin). *(⟳ 2026-08-03: **PUT never persists `global`** — `UpdateNamedQuery.cs:44` writes only `Template` (even for admins; matches the controller remark "only the template can be modified"), so `global` is effectively settable only at create. DELETE matches own-customer only (`DeleteNamedQuery.cs:32-35`) — non-owners cannot delete a global NQ. Whatever prose this card produces should say "set at create; not changeable via PUT" — or that's a code gap to raise.)*
- **Issues/RFCs:** resume-audit-fixes Category E.
- **Decision needed:** Document the `global` property + read/visibility/admin-write semantics.
- **Options:** (a) add a `## global` section + domain/range table; (b) document read-only for non-admins; (c) defer.
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### DIS-10 · `manifest` template key — placeholder value & broken `iiif` link
- **Theme:** Discovery & delivery
- **Surfaces:** named-queries.mdx#named-query-template-syntax L120 (`manifest` row, example `&manifest=xxxx`, links to `iiif`) · scratch/api-doc/named-queries.md L39-41 ("Verify what the manifest id should look like (currently xxxx)")
- **Type:** DOC-WRONG / DOC-MISSING
- **Docs say:** `manifest` "Select assets that are part of a stored IIIF Manifest" `&manifest=xxxx`; links to `iiif` (page not yet ported → 404).
- **Original-doc nuance:** old Nextra described `manifest` as *"How to group images"* `&manifest=s1` — a different (grouping) meaning.
- **Code does:** `manifest` sets `assetQuery.Manifests` (comma-separated string list) — `BaseNamedQueryParser.cs:47,149-152`. It filters on the asset's own `Manifests` membership list (`DLCS.Model\Assets\Asset.cs:150-153` "manifest identifiers that this asset is associated with"; filtered in `NamedQueryRepository.cs:110-113`). So the value is a manifest-membership identifier (typically supplied via `p1`), not "xxxx" and not a stored-manifest entity id.
- **Issues/RFCs:** depends on iiif.mdx being ported (see DIS-20).
- **Decision needed:** Replace the `xxxx` placeholder with a real example, confirm the membership-identifier semantics, and fix/relink `iiif`.
- **Options:** (a) example `&manifest=p1` + prose on membership; (b) cross-link to a future iiif/manifests page once ported; (c) defer until iiif.mdx exists.
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### DIS-11 · `canvas` is an obsolete alias for `assetOrder` — docs lead with `canvas`
- **Theme:** Discovery & delivery
- **Surfaces:** named-queries.mdx (all examples use `canvas=…`; `assetOrder` only mentioned L118 & L179-185) · code `BaseNamedQueryParser.cs:31` (`canvas` marked `[Obsolete]` "backwards compat with Deliverator. Favour assetOrder")
- **Type:** DESIGN / STYLE
- **Docs say:** `canvas` is the primary ordering key; `assetOrder` is "alias for canvases, more generic".
- **Original-doc nuance:** old Nextra described `canvas` as *"Ordering to apply to each image on canvas"*.
- **Code does:** `canvas` and `assetOrder` both set `AssetOrdering` (`BaseNamedQueryParser.cs:113-116`); code comment marks `canvas` obsolete and prefers `assetOrder`. The richer asc/desc/`;` syntax (DIS-shown) is documented under `assetOrder`.
- **Issues/RFCs:** —
- **Decision needed:** Should the docs lead with `assetOrder` and present `canvas` as the legacy alias (reversing current emphasis)?
- **Options:** (a) swap emphasis to `assetOrder`, mark `canvas` legacy; (b) keep `canvas` for familiarity but note it is obsolete; (c) defer.
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### DIS-12 · named-query syntax table — `s3` row example typo
- **Theme:** Discovery & delivery
- **Surfaces:** named-queries.mdx#named-query-template-syntax L123 (`s3` row example `&manifest=s3`)
- **Type:** DOC-WRONG (STYLE)
- **Docs say:** `s3` | "Alias for the `string3` metadata field" | example `&manifest=s3` — the example is a copy-paste error (a `manifest=` example, not an `s3=` one).
- **Original-doc nuance:** old Nextra had the same `&manifest=s3` example for `s3`.
- **Code does:** `s3` maps to `String3` (`BaseNamedQueryParser.cs:43,130-132`); a correct example would be `&s3=p2`.
- **Issues/RFCs:** —
- **Decision needed:** Fix the example cell.
- **Options:** (a) change to `&s3=p2`; (b) leave; (c) defer.
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☑ mechanical — merged in public-docs PR #6 (2026-08-05)

### DIS-13 · named-query Hydra model carries `[Unstable]`/`[Obsolete]` despite working API
- **Theme:** Discovery & delivery
- **Surfaces:** code `DLCS.HydraModel\NamedQuery.cs:26` (`[Unstable(Note = "Currently the named query implementation is a placeholder,")]`) · `BaseNamedQueryParser.cs:31` (`canvas` `[Obsolete]`)
- **Type:** CODE-WRONG (cleanup, low priority)
- **Docs say:** n/a (code-only).
- **Original-doc nuance:** —
- **Code does:** The management API (GET/PUT/DELETE/POST) and all output projections are fully implemented, yet the Hydra surface model is still annotated "placeholder". Misleading metadata. *(⟳ 2026-08-03: same family — `NamedQueryClass.DefineOperations` (`NamedQuery.cs:71-76`) advertises a **PATCH** operation the controller doesn't implement; the docs table correctly omits it. Fold into the same cleanup PR.)*
- **Issues/RFCs:** to check.
- **Decision needed:** Remove/refresh the `[Unstable]` placeholder annotation (and decide whether `canvas` should stay only as a documented legacy alias).
- **Options:** (a) protagonist PR to drop the stale annotation; (b) leave; (c) defer.
- **Possible outputs:** code
- **Who's needed:** protagonist dev
- **Status:** ☑ mechanical — merged in protagonist PR #1235 (2026-08-06, donaldgray): `[Unstable]` dropped and phantom PATCH removed. (The `canvas` legacy-alias question remains parked with the named-query promotion cards)

### DIS-14 · EntryPoint docs show `queue` & `deliveryChannelPolicies` — model emits neither
- **Theme:** Discovery & delivery
- **Surfaces:** entrypoint.mdx (example JSON L17-22 lists `deliveryChannelPolicies` + `queue`; `## queue` section L112-126) · queues.mdx (links to `../entrypoint#queue`, per memory) · scratch/api-doc/entrypoint.md · code `DLCS.HydraModel\EntryPoint.cs:18-55`, `API\Features\HomeController.cs:26-32` · *(added 2026-08-03)* `dlcs-docs-client/p04_entrypoint/entrypoint.py:26-28` (manually constructs the `/queue` URL, comment "TODO: add this property")
- **Type:** DOC-WRONG (or CODE-MISSING, if intended)
- **Docs say:** EntryPoint includes `queue` (link to global QueueSummary) and `deliveryChannelPolicies`.
- **Original-doc nuance:** old Nextra had a full `## queue` section *and* a `## DELETE deliveryChannelPolicies` section already flagged for deletion (*"Do we actually need this global set? How would you refer to it?"* … "DELETE").
- **Code does:** `EntryPoint` has exactly six links — `customers`, `originStrategies`, `portalRoles`, `imageOptimisationPolicies`, `thumbnailPolicies`, `storagePolicies` (`EntryPoint.cs:18-55`). **No** `queue`, **no** `deliveryChannelPolicies`, no `spaces`. `HomeController.Index` just returns `new EntryPoint(baseUrl)`; links auto-populate from the model only (`DlcsResource.cs:44-63`). So the documented links are not emitted. *(⟳ 2026-08-03: a global `/queue` endpoint DOES exist (`API\Features\Queues\QueueController.cs:17`), so option (b) only needs the EntryPoint link property added.)*
- **Issues/RFCs:** resume-audit-fixes Category C; integration test asserts only `@type` (`API.Tests\Integration\BasicApiTests.cs:24-33`).
- **Decision needed:** Either remove `queue` + `deliveryChannelPolicies` from the docs (and fix the `queues.mdx` back-link), or add them to the model/controller if they are intended. *(⟳ PO leaning, 2026-08-03: `deliveryChannelPolicies` is not returned and probably should NOT be documented — drop it from the example; `queue` is different — the endpoint exists, only the link is missing, so adding the link property is a cheap option b.)*
- **Options:** (a) docs: delete both sections + the JSON keys + fix queues.mdx link; (b) code: add `queue`/`deliveryChannelPolicies` to EntryPoint; (c) defer pending product intent.
- **Possible outputs:** doc / code / RFC
- **Who's needed:** docs owner + protagonist dev
- **Status:** ☐ undecided — ⟳ session-0 cascade note (2026-08-06): XC-07 (PR #1237) removed `imageOptimisationPolicies` + `thumbnailPolicies` from EntryPoint — post-merge the emitted set is customers / originStrategies / portalRoles / storagePolicies. This card's `queue`-link question (option b: add the EntryPoint.queue property) remains open; note XC-13 added Customer.adjunctQueue, not EntryPoint.queue

### DIS-15 · EntryPoint emits legacy `imageOptimisationPolicies` & `thumbnailPolicies`
- **Theme:** Discovery & delivery
- **Surfaces:** entrypoint.mdx (these are NOT documented) · scratch/api-doc/entrypoint.md ("Remove imageOptimisationPolicies and thumbnailPolicies") · code `EntryPoint.cs:37-49`
- **Type:** CODE-WRONG (cleanup) + a description bug
- **Docs say:** nothing (correctly omitted from docs).
- **Original-doc nuance:** —
- **Code does:** `EntryPoint.cs:37-42` emits `imageOptimisationPolicies`; L45-49 emits `thumbnailPolicies` — both legacy (delivery-channel policies superseded them). Additionally `thumbnailPolicies`' `[Description]` (L45-46) is a copy-paste of the `portalRoles` text. The live API therefore returns two undocumented legacy links.
- **Issues/RFCs:** resume-audit-fixes Category B.
- **Decision needed:** Remove the two legacy links from the model (and fix the stray description), or document them if still load-bearing.
- **Options:** (a) protagonist PR to remove both properties; (b) keep + document as deprecated; (c) defer.
- **Possible outputs:** code / doc
- **Who's needed:** protagonist dev
- **Status:** ☐ undecided

### DIS-16 · EntryPoint emits `portalRoles` — undocumented
- **Theme:** Discovery & delivery
- **Surfaces:** entrypoint.mdx (no `portalRoles`) · code `EntryPoint.cs:30-35`
- **Type:** DOC-MISSING
- **Docs say:** nothing.
- **Original-doc nuance:** —
- **Code does:** `EntryPoint.cs:30-35` emits `portalRoles` (auto-populated `{baseUrl}/portalRoles`). It is a real, returned link.
- **Issues/RFCs:** resume-audit-fixes Category E.
- **Decision needed:** Document `portalRoles` or decide it is internal/portal-only and should be hidden.
- **Options:** (a) add a `## portalRoles` section; (b) suppress from the public EntryPoint if portal-internal; (c) defer.
- **Possible outputs:** doc / code
- **Who's needed:** docs owner + protagonist dev
- **Status:** ☐ undecided

### DIS-17 · EntryPoint scratch note is stale/incorrect
- **Theme:** Discovery & delivery
- **Surfaces:** scratch/api-doc/entrypoint.md (whole file)
- **Type:** STALE-SCRATCH
- **Docs say:** scratch asserts *"API response is missing `queue` property - even though it's present"* and *"Remove `imageOptimisationPolicies` and `thumbnailPolicies`"*.
- **Original-doc nuance:** —
- **Code does:** ~~The `queue` claim is **false**~~ *(⟳ corrected 2026-08-03 per PO clarification: the note's intended meaning was "the `/queue` **endpoint** exists but the response carries no link" — which is TRUE: `QueueController.cs:17` exists, the model has no `queue` property to emit. The scratch note was right, just terse.)* The `imageOptimisationPolicies`/`thumbnailPolicies` removal note is a code action, now captured in DIS-15. Scratch file rewritten 2026-08-03 with the clarified meaning + PROV-01/02 prose with dispositions.
- **Issues/RFCs:** —
- **Decision needed:** Rewrite the scratch note to reflect actual model state once DIS-14/15/16 are decided.
- **Options:** (a) correct/replace the scratch note; (b) delete it once cards land; (c) defer.
- **Possible outputs:** doc (scratch)
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### DIS-18 · size-restrictions documents `openMaxWidth` + substitute service that don't exist in code
- **Theme:** Discovery & delivery
- **Surfaces:** size-restrictions.mdx (the `openMaxWidth` column + scenarios 8-11 L96-136; intro link to `../asset#openmaxwidth` L10) · asset.mdx#openmaxwidth (companion, also unimplemented) · no `scratch/api-doc/size-restrictions.md` exists yet
- **Type:** DOC-WRONG (documents unimplemented behaviour)
- **Docs say:** `openMaxWidth` drives a probe "substitute image service" (anonymous access up to N px while authed users go higher); scenarios 8-11 detail it.
- **Original-doc nuance:** preserve the scenario prose verbatim when moving — it is a coherent spec worth keeping.
- **Code does:** No `OpenMaxWidth` property on `Image`/asset, and no `substitute` image-service handling anywhere in protagonist (per memory openmaxwidth-unimplemented; asset model has only `maxWidth` and `openFullMax`, plus `[Obsolete] maxUnauthorised`). Scenarios 1-7 (roles/`maxWidth`/`openFullMax`) should be re-verified but appear plausible; 8-11 describe absent behaviour.
- **Issues/RFCs:** resume-audit-fixes Category C; memory openmaxwidth-unimplemented.
- **Decision needed:** Move `openMaxWidth`/substitute content out of live docs (to a new `scratch/api-doc/size-restrictions.md`) or keep it explicitly flagged as a not-yet-built spec for the protagonist team.
- **Options:** (a) move scenarios 8-11 + the `openMaxWidth` column to scratch, preserving prose; (b) keep but wrap in a "not yet implemented" Aside; (c) treat as a build spec / RFC; (d) defer.
- **Possible outputs:** doc / RFC
- **Who's needed:** docs owner + protagonist dev
- **Status:** ☐ undecided

### DIS-19 · single-asset-manifest examples are partly unverified ("expected behaviour")
- **Theme:** Discovery & delivery
- **Surfaces:** single-asset-manifest.mdx#examples (L49 disclaimer; AV/file/adjunct example blocks L390-588) · caution Aside L10-12
- **Type:** DESIGN (verification debt)
- **Docs say:** image + thumbnail patterns are "confirmed from real platform output"; AV, file-delivery and adjunct URL patterns are "based on expected platform behaviour". Aside: the manifest "does not yet represent … everything the platform knows".
- **Original-doc nuance:** old Nextra left all example blocks empty (` ```json ``` `) and added the AV note *"it is always a Choice resource, even if there is only one output. (?)"* and the `dlcs:channelOutputs` extension (the latter confirmed absent and rightly dropped).
- **Code does:** Single-asset-manifest generation lives in the Orchestrator/manifest builder (not yet line-cited here). The image/thumbnail JSON matches real output; AV `Choice`, `file`/placeholder and adjunct (`seeAlso`/`rendering`/`annotations`/inline) shapes need validation against the generator and a live asset.
- **Issues/RFCs:** to check (run a real AV/file/adjunct asset through the manifest endpoint).
- **Decision needed:** Validate the AV/file/adjunct example JSON against actual platform output (and confirm whether the caution Aside is still warranted).
- **Options:** (a) verify against live output and mark confirmed; (b) cite the manifest-builder code to confirm shapes; (c) leave disclaimed; (d) defer.
- **Possible outputs:** doc / sample
- **Who's needed:** docs owner + protagonist dev
- **Status:** ☐ undecided

### DIS-20 · broken `../iiif` links across discovery pages (page not yet ported)
- **Theme:** Discovery & delivery
- **Surfaces:** collections.mdx:11 (`../iiif`) · named-queries.mdx:120 (`iiif`) · overview.mdx:96 (`../iiif`) · single-asset-manifest references stored manifests · (iiif.mdx not yet created — listed as "Pages not yet ported")
- **Type:** DOC-MISSING (link target)
- **Docs say:** several pages link to an IIIF Manifests/Collections page that 404s until ported.
- **Original-doc nuance:** —
- **Code does:** The IIIF Manifests/Collections feature is implemented in the `iiif-presentation` repo (per CLAUDE.md); the docs page just hasn't been ported.
- **Issues/RFCs:** CLAUDE.md "Pages not yet ported".
- **Decision needed:** Prioritise porting `iiif.mdx`, or temporarily soften the links so they don't 404.
- **Options:** (a) port iiif.mdx (unblocks DIS-10 too); (b) stub the page; (c) remove/neutralise links until ported; (d) defer.
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### DIS-21 · collections.mdx host inconsistency in example JSON
- **Theme:** Discovery & delivery
- **Surfaces:** collections.mdx (page-1 example uses `api.dlcs.example` L38-72; page-2 example uses `api.dlcs.digirati.io` L80-113)
- **Type:** STYLE
- **Docs say:** two consecutive paged-collection examples use different hostnames for the same resource.
- **Original-doc nuance:** —
- **Code does:** n/a (doc consistency). The convention (overview.mdx#api-hostname) is `dlcs.example` / `api.dlcs.example`.
- **Issues/RFCs:** —
- **Decision needed:** Normalise the second example to `api.dlcs.example`. *(⟳ 2026-08-03: block is now L78-115, hostname hits at L82,88,97,107-110. See also DIS-24 — entrypoint.mdx has the same class of problem with the production hostname.)*
- **Options:** (a) replace `digirati.io` with `example`; (b) leave; (c) defer.
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☑ mechanical — merged in public-docs PR #6 (2026-08-05)

### DIS-22 · Batch endpoints support the full asset-query syntax — asset-queries.mdx omits them *(added 2026-08-03 verification pass)*
- **Theme:** Discovery & delivery
- **Surfaces:** asset-queries.mdx#applicable-endpoints (L16-19, lists only `/allImages` and `/spaces/{space}/images`) · `CustomerQueueController.cs:211-233, 257-279` · `GetBatchAssetsBase.cs:17`
- **Type:** DOC-MISSING
- **Code does:** `GET /customers/{c}/queue/batches/{batchId}/images` and `.../batches/{batchId}/assets` accept `?q=`, the shortcut params, `orderBy`/`orderByDescending`, paging, and `include=adjuncts` — the full asset-query surface.
- **Decision needed:** Add both batch endpoints to the applicable-endpoints list (coordinates with DIS-01/02/03 promotions and the batch.mdx cards PRO-01..03).
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### DIS-23 · Versioned `iiif-resource` paths and Accept negotiation undocumented *(added 2026-08-03 verification pass)*
- **Theme:** Discovery & delivery
- **Surfaces:** named-queries.mdx URL-pattern breakdown (L24-39) · `Orchestrator\Features\Manifests\NamedQueryController.cs:37-63`
- **Type:** DOC-MISSING
- **Code does:** `/iiif-resource/v2/{customer}/{nq}/{args}` and `/v3/...` exist, plus Accept-header version negotiation on the unversioned path. PR #1230's RFC writes the general syntax as `/{type}/{?version}/{customer}/{nq-name}/{**nq-params}`.
- **Decision needed:** Document the optional version segment + Accept negotiation when promoting the named-query material (DIS-07/08).
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### DIS-25 · single-asset-manifest: "always a Choice" for iiif-av is wrong; no-transcode AV assets get no canvas *(added 2026-08-03 completion pass)*
- **Theme:** Discovery & delivery
- **Surfaces:** single-asset-manifest.mdx:27 ("the body of the painting annotation is a `Choice` resource listing all the transcoded outputs") + the "Audio with iiif-av" example (a Choice wrapping a *single* output) · old doc's own "(?)" flag (preserved in scratch) · `Orchestrator\...\ManifestV3Builder.HandleTimebasedAsset` (:303-309), `:283-287`
- **Type:** DOC-WRONG (verified against code)
- **Code does:** a single transcode gets a **bare `Sound`/`Video` body**; `PaintingChoice` is used only when `transcodes.Length > 1`. The old author's open question is answered by the code in the opposite direction from both old and new prose. Additionally: an iiif-av asset with **no** transcode metadata gets **no canvas at all** — documented nowhere.
- **Decision needed:** Fix the prose + audio example (bare body for one output, Choice for several; document the no-canvas case) — or rule that always-Choice is the *intended* contract and file a code change.
- **Possible outputs:** doc / code
- **Who's needed:** docs owner + API dev
- **Status:** ✅ RULED (session 0, 2026-08-06): fix the docs — bare `Sound`/`Video` body for a single transcode, `Choice` only for several; AND document that an AV asset with no transcodes (or only the `file` delivery channel) gets **no canvas at all**. Owner: PO. Output: public-docs hygiene/session-0 commit (verify exact wording against ManifestV3Builder before drafting)

### DIS-26 · size-restrictions: "thumbs channel only serves openly-accessible content" — unsourced, unverified *(added 2026-08-03 completion pass)*
- **Theme:** Discovery & delivery
- **Surfaces:** size-restrictions.mdx "Has roles" Aside · no old-doc source (added at port time)
- **Type:** DOC-WRONG? ⚠verify
- **Docs say:** "The `thumbs` delivery channel only serves content that is accessible without authentication." Plausible (matches old scenarios 4-5 "No thumbnails are produced, whatever the policy") but the general claim about thumbs-channel auth behaviour has not been traced through Orchestrator/Engine.
- **Decision needed:** Verify against the thumbs-channel code (or a live role-protected asset) before treating as authoritative; add to the verify-first sweep.
- **Possible outputs:** doc (confirm or correct)
- **Who's needed:** API dev
- **Status:** ☐ undecided

### DIS-24 · entrypoint.mdx examples use the production hostname `api.dlc.services` *(added 2026-08-03 verification pass)*
- **Theme:** Discovery & delivery
- **Surfaces:** entrypoint.mdx JSON examples (L15-21, L50-75) · overview.mdx#api-hostname (convention: `api.dlcs.example`)
- **Type:** STYLE (DIS-21 family)
- **Docs say:** Both examples use the real production host instead of the documented example convention.
- **Decision needed:** Normalise to `api.dlcs.example` (mechanical; same sweep as DIS-21).
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☑ mechanical — merged in public-docs PR #6 (2026-08-05); hostnames only, the phantom-links question stays with DIS-14

### DIS-27 · NamedQuery `global` and `template` share JsonProperty Order 11 *(minted in session 0, 2026-08-06)*
- **Theme:** Discovery & delivery
- **Surfaces:** `DLCS.HydraModel/NamedQuery.cs` (`global` Order 11 at :54, `template` Order 11 at :59; line numbers pre-#1235)
- **Type:** STYLE (ACC-07 defect class)
- **Docs say:** n/a (serialisation ordering only).
- **Code does:** Both properties declare `[JsonProperty(Order = 11)]`, so their emission order is undefined — the exact defect ACC-07 fixed for ImageStorage/ApiKey/PortalUser (protagonist PR #1235). Observed during the DIS-13 cleanup in the same PR; deliberately not fixed there because it wasn't on the ratified mechanical list.
- **Issues/RFCs:** —
- **Decision needed:** Renumber to 11/12 (shifting `template` to 12).
- **Options:** (a) renumber; (b) leave (cosmetic).
- **Possible outputs:** code (mechanical-track candidate — verified, obvious fix, no design question)
- **Who's needed:** protagonist dev
- **Status:** ☐ undecided
