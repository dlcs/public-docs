# Hygiene sprint · Session 2 · Spaces & assets

Scope: cross-referenced the five "Spaces & assets" pages (`space.mdx`, `asset.mdx`,
`registering-assets.mdx`, `delivery-channels.mdx`, `origin-strategy.mdx`) and their parked
scratch notes against the protagonist API code (`API/Features/Space`, `Features/Image`,
`Features/DeliveryChannels`, `Features/OriginStrategies`) and the Hydra models
(`DLCS.HydraModel/Image.cs`, `Space.cs`, `DeliveryChannelPolicy.cs`, `CustomerOriginStrategy.cs`,
`OriginStrategy.cs`). Read-only; no docs/code/samples were changed. All seed items were verified
against current code (corrected where the seed was stale) and expanded with new findings. Status
codes/field claims are cited to `file:line`.

## Resolved (Category A — verified correct, no action)

- DeliveryChannelPolicy custom-policy channel restriction: doc says only `thumbs` and `iiif-av`
  accept customer policies — **correct**; `HydraDeliveryChannelPolicyValidator.cs:14-18`
  allows only `Thumbnails` and `Timebased`.
- AV vs image ingest sync/async: doc says images sync, AV async — **correct**;
  `ImageController.cs:62-64` ("Image + File assets are ingested synchronously. Timebased assets
  are ingested asynchronously").
- Asset DELETE returns 204 No Content — **correct**; `ImageController.cs:185,201` (`NoContent()`).
- CustomerOriginStrategy DELETE returns 204, origin-strategy.mdx agrees — `CustomerOriginStrategiesController.cs:188`.
- POST-to-Space is not implemented (405): `ImagesController.cs` exposes only GET (`:61`) and PATCH
  (`:107`) — live `registering-assets.mdx` correctly lists three registration methods.
- `thumbs`/`default` channel labels, simplified delivery-channel registration forms (string array,
  no `@type`, no policy), and the `none`/`default` marker channels read consistently with code intent.
- `maxWidth` and `openFullMax` ARE now present in `Image.cs:87-88,93-94` (the old scratch note
  claiming the API only has `maxUnauthorised` is stale on these two — but see SPA-01 re openMaxWidth).

---

### SPA-01 · openMaxWidth and the substitute/open image service are not in code
- **Theme:** Spaces & assets
- **Surfaces:** asset.mdx#openmaxwidth (lines 319-358) · size-restrictions.mdx scenarios 8-11 · `DLCS.HydraModel/Image.cs:75-94`
- **Type:** CODE-MISSING
- **Docs say:** `openMaxWidth` (writeonly) caps deep-zoom tile delivery for role-protected images; the `iiif-img` channel emits a probe with a `substitute` open image service (maxWidth = openMaxWidth) per IIIF Auth 2.0.
- **Original-doc nuance:** "the `iiif-img` delivery channel provides an info.json with a probe service ... but will also offer a `substitute` as defined in the IIIF Authorization Flow specification" — preserve the full probe JSON and substitute prose; it is the only written spec for the feature.
- **Code does:** `Image.cs` has `maxWidth` (`:87`) and `openFullMax` (`:93`) but **no `openMaxWidth` property at all**; no substitute/open image-service mechanism found. The obsolete `maxUnauthorised` (`:75-81`) is the only legacy size-gate.
- **Issues/RFCs:** to check (protagonist issues for IIIF Auth probe/substitute)
- **Decision needed:** Should openMaxWidth + substitute service be built, dropped, or turned into an RFC, and should the docs be marked "planned" until then?
- **Options:** (a) build it and keep docs (b) mark the asset.mdx/size-restrictions sections "not yet implemented" and move prose to scratch (c) write an RFC and link it
- **Possible outputs:** doc / code / RFC
- **Who's needed:** API/eng lead + IIIF auth owner
- **Status:** ☐ undecided

### SPA-02 · asset `family` shown in examples but has no documented section
- **Theme:** Spaces & assets
- **Surfaces:** asset.mdx (example JSON line 58 `"family": "I"`; no `## family` section) · registering-assets.mdx (omits family) · `Image.cs:197-200` · `ImageController.cs:76-80`
- **Type:** DOC-MISSING
- **Docs say:** `family` appears only in the asset example JSON; it is never defined.
- **Original-doc nuance:** —
- **Code does:** `Image.cs:197-200` exposes `family` (`AssetFamily`, "I for Image, T for time-based, F for File"), `ReadOnly = true`. But the PUT sample in `ImageController.cs:76-80` shows `"family": "I"` in a request body, implying it is settable — conflicting signal about whether family is user-supplied or derived from `mediaType`.
- **Issues/RFCs:** to check
- **Decision needed:** Document `family` as a read-only derived field, or as a settable registration hint? Resolve the readonly-vs-PUT-sample contradiction.
- **Options:** (a) add a read-only `## family` section, note values I/T/F (b) document it as optional-on-registration if code actually honours it (c) leave undocumented and drop from example
- **Possible outputs:** doc / code
- **Who's needed:** API owner
- **Status:** ☐ undecided

### SPA-03 · obsolete `maxUnauthorised` still emitted on assets, undocumented
- **Theme:** Spaces & assets
- **Surfaces:** asset.mdx (not documented) · asset.md scratch lines 30-36 · `Image.cs:75-81`
- **Type:** DESIGN / STALE-SCRATCH
- **Docs say:** Nothing (deliberately omitted in favour of maxWidth/openFullMax/openMaxWidth).
- **Original-doc nuance:** scratch asset.md: "the actual API currently uses `maxUnauthorised: -1` instead" — now partially stale, since maxWidth/openFullMax exist in code.
- **Code does:** `Image.cs:75-81` keeps `maxUnauthorised` with `[Obsolete("Use openFullMax and/or maxWidth instead")]`; still serialised, default -1.
- **Issues/RFCs:** to check
- **Decision needed:** Keep emitting the obsolete field, document it as deprecated, or remove it from the Hydra model? Update the stale scratch note either way.
- **Options:** (a) remove from model once migration confirmed (b) document as deprecated/back-compat (c) leave and just refresh scratch
- **Possible outputs:** code / doc / sample
- **Who's needed:** API owner
- **Status:** ☐ undecided

### SPA-04 · asset `manifest` (singular) vs `manifests` (array) vs possible `scopes` rename
- **Theme:** Spaces & assets
- **Surfaces:** asset.mdx (example line 56 `"manifests": []`; no property section) · registering-assets.mdx#assets-as-iiif-cs-api-resources (line 114) · single-asset-manifest.mdx · asset.md scratch lines 102-108 · `Image.cs:241-244`
- **Type:** DESIGN / CODE-MISSING
- **Docs say:** `manifests` is "any IIIF Presentation Manifests this asset is used in"; the single-asset-manifest URI *should* become a `manifest` (singular) property but is not yet a property.
- **Original-doc nuance:** scratch: "the single-asset manifest exists, and its URI _should_ become the value of a `manifest` property — but it is not yet implemented _as a property_"; "possible rename of `manifests` -> `scopes`. Not present in protagonist `main` or `develop`."
- **Code does:** `Image.cs:241-244` has only `Manifests` (`string[]`, readonly, Range `vocab:Manifests`). **No `manifest` singular and no `scopes`** in current code — the rename is still hypothetical/unmerged. `manifests` is undocumented as a property (appears in example only).
- **Issues/RFCs:** to check (unmerged PR for scopes?)
- **Decision needed:** What is the intended model — keep `manifests` array, add a singular `manifest` (single-asset-manifest link), and/or rename to `scopes`? Add a property section once decided.
- **Options:** (a) document `manifests` now, defer manifest/scopes (b) add singular `manifest` property in code + docs (c) hold for the scopes PR and write an RFC
- **Possible outputs:** doc / code / RFC
- **Who's needed:** API owner + IIIF presentation owner
- **Status:** ☐ undecided

### SPA-05 · `space.maxUnauthorised` present in code but undocumented
- **Theme:** Spaces & assets
- **Surfaces:** space.mdx (not documented) · space.md scratch line 2 · `Space.cs:55-58` · `SpaceController.cs:101,175,215`
- **Type:** DOC-MISSING
- **Docs say:** Nothing; space.mdx documents defaultRoles/defaultTags/defaultDeliveryChannels but not maxUnauthorised.
- **Original-doc nuance:** scratch space.md also parks unimplemented `defaultMaxWidth`/`defaultOpenFullMax`/`defaultOpenMaxWidth` (correctly absent from `Space.cs`).
- **Code does:** `Space.cs:55-58` exposes `maxUnauthorised` ("Default size at which role-based authorisation will be enforced. -1=open, 0=always require auth"); it is read in Create/Patch/Put (`SpaceController.cs:101,175,215`), so it is a live, settable space default.
- **Issues/RFCs:** to check
- **Decision needed:** Document `space.maxUnauthorised`, or is it superseded by the planned default size fields (so deprecate)?
- **Options:** (a) add a `## maxUnauthorised` section to space.mdx (b) document it as deprecated alongside the planned defaults (c) leave undocumented if slated for removal
- **Possible outputs:** doc / code
- **Who's needed:** API owner
- **Status:** ☐ undecided

### SPA-06 · stray `metadata` link on Space model, undocumented, "likely never implement"
- **Theme:** Spaces & assets
- **Surfaces:** space.mdx (not documented) · space.md scratch lines 75-106 · `Space.cs:82-85,118-137`
- **Type:** STALE-SCRATCH / DESIGN
- **Docs say:** Nothing.
- **Original-doc nuance:** scratch: "Likely never implement metadata as not used"; describes a `distinct` query endpoint for metadata fields.
- **Code does:** `Space.cs:82-85` still declares a `metadata` HydraLink and `SpaceClass:118-137` defines a GET operation for it (Hydra advertises an endpoint), even though the feature is considered dead. Model comment itself: "TOOD- what exactly?".
- **Issues/RFCs:** to check
- **Decision needed:** Remove `metadata` from the Space Hydra model (and the advertised operation), or keep and document the distinct-values query?
- **Options:** (a) remove from model (b) implement + document distinct query (c) leave as-is, note in scratch
- **Possible outputs:** code / doc
- **Who's needed:** API owner
- **Status:** ☐ undecided

### SPA-07 · `space.images` bulk PATCH is implemented but absent from live docs; Hydra advertises a non-existent POST
- **Theme:** Spaces & assets
- **Surfaces:** space.mdx#images (HTTP table lines 98-100, GET only) · space.md scratch lines 26-37 · `ImagesController.cs:61,107` · `Space.cs:112-113`
- **Type:** DOC-MISSING / CODE-WRONG
- **Docs say:** `space.images` supports only GET.
- **Original-doc nuance:** scratch space.md retains a PATCH row ("Update one *or more* assets") and a POST row; the PATCH is real, the POST is not.
- **Code does:** `ImagesController.cs:107` implements bulk `PATCH /customers/{c}/spaces/{s}/images` (synchronous, non-reprocessing fields only) — undocumented in the live page. Meanwhile `Space.cs:112-113` (SpaceClass) still advertises a POST operation on the images collection that the controller does not implement (405).
- **Issues/RFCs:** to check
- **Decision needed:** Add the bulk-PATCH row to space.mdx#images (with the "no reprocessing fields" constraint), and remove the phantom POST operation from the Space Hydra model?
- **Options:** (a) document PATCH + sample, strip POST from model (b) document PATCH only (c) defer until POST-to-Space lands and document both together
- **Possible outputs:** doc / code / sample
- **Who's needed:** API owner + docs
- **Status:** ☐ undecided

### SPA-08 · DeliveryChannelPolicy DELETE annotation says 202, code returns 204
- **Theme:** Spaces & assets
- **Surfaces:** delivery-channels.mdx#deliverychannelpolicy (table line 381, "204 No Content") · `DeliveryChannelPoliciesController.cs:268,279` · `HydraController.cs:164-174`
- **Type:** CODE-WRONG (annotation only)
- **Docs say:** DELETE returns 204 No Content (already correct).
- **Original-doc nuance:** —
- **Code does:** `DeliveryChannelPoliciesController.cs:268` annotates `[ProducesResponseType(StatusCodes.Status202Accepted)]`, but `HandleDelete` -> `ConvertDeleteToHttp` returns `NoContent()` = 204 (`HydraController.cs:174`). The Swagger annotation is wrong; published doc is right.
- **Issues/RFCs:** to check
- **Decision needed:** Fix the annotation to 204 (purely a code/Swagger correction)?
- **Options:** (a) change annotation to `Status204NoContent` (b) leave (doc already correct)
- **Possible outputs:** code
- **Who's needed:** API dev
- **Status:** ☐ undecided

### SPA-09 · Space DELETE annotation says 200 + Space body, code returns 204 No Content
- **Theme:** Spaces & assets
- **Surfaces:** space.mdx (table line 37, "204 No Content, 404 Not found") · `SpaceController.cs:113-122` · `HydraController.cs:164-174`
- **Type:** CODE-WRONG (annotation only)
- **Docs say:** DELETE returns 204 No Content (already correct).
- **Original-doc nuance:** —
- **Code does:** `SpaceController.cs:115` annotates `[ProducesResponseType(StatusCodes.Status200OK, Type = typeof(Space))]`, but `DeleteSpace` (`:121`) calls `HandleDelete` -> `NoContent()` = 204. Annotation (and implied response body) is wrong; published doc is right. Note: a space can only be deleted when empty — surfaces a possible `409 Conflict` (`ConvertDeleteToHttp` maps `DeleteResult.Conflict` -> 409) that the doc does not list.
- **Issues/RFCs:** to check
- **Decision needed:** Fix annotation to 204, and add `409 Conflict` (space not empty) to the doc status list?
- **Options:** (a) fix annotation + add 409 to doc (b) fix annotation only (c) leave
- **Possible outputs:** code / doc
- **Who's needed:** API dev + docs
- **Status:** ☐ undecided

### SPA-10 · PUT to an asset "always triggers reingest" per code, but docs imply reprocessing only on origin change
- **Theme:** Spaces & assets
- **Surfaces:** asset.mdx#origin (line 143), asset.mdx#reingest (lines 489-499) · registering-assets.mdx · `ImageController.cs:62`
- **Type:** DOC-MISSING / to-check
- **Docs say:** "If an update of an asset modifies the value of `origin`, the asset will be re-processed"; the `reingest` endpoint is "for cases the platform has no way of knowing an asset needs re-processing" — implying ordinary PUTs do not always reingest.
- **Original-doc nuance:** —
- **Code does:** `ImageController.cs:62` XML doc: "PUT requests always trigger reingesting of asset - in general batch processing should be preferred." If literally true, every PUT reingests regardless of which fields changed — broader than the docs suggest.
- **Issues/RFCs:** to check (does CreateOrUpdateImage short-circuit when nothing reprocess-worthy changed?)
- **Decision needed:** Confirm actual PUT reingest behaviour and align the docs (PUT = always reingest vs PATCH = field-dependent)?
- **Options:** (a) verify in `CreateOrUpdateImage`, then add a note to asset.mdx/registering-assets (b) clarify the PUT-vs-PATCH distinction in docs (c) no change if comment is stale
- **Possible outputs:** doc / code
- **Who's needed:** API owner
- **Status:** ☐ undecided

### SPA-11 · readonly/writeonly Hydra flags on asset disagree with the doc domain/range tables
- **Theme:** Spaces & assets
- **Surfaces:** asset.mdx tables (id line 107; mediaType 115; error 209) · `Image.cs:35-38,116-119,192-195`
- **Type:** STYLE
- **Docs say:** `id` readonly=True; `mediaType` readonly=False; `error` readonly=True.
- **Original-doc nuance:** —
- **Code does:** `Image.cs` flags disagree: `id`/ModelId `ReadOnly = false` (`:36`); `mediaType` `ReadOnly = true` (`:193`); `error` `ReadOnly = false` (`:117`). These RdfProperty flags drive the generated Hydra ApiDocumentation, so the machine vocab and the human tables contradict each other for at least these three fields.
- **Issues/RFCs:** to check
- **Decision needed:** Which is authoritative per field, and should the Hydra attributes or the doc tables be corrected to match? (e.g., mediaType is required at create but readonly thereafter — the binary flag can't express that.)
- **Options:** (a) align Hydra flags to documented intent (b) align doc tables to code (c) introduce a "settable at create only" convention for id/mediaType/space
- **Possible outputs:** code / doc
- **Who's needed:** API owner + docs
- **Status:** ☐ undecided

### SPA-12 · stray readonly/writeonly flags on origin-strategy Hydra models
- **Theme:** Spaces & assets
- **Surfaces:** origin-strategy.mdx tables (requiresCredentials line 76; strategy 120; credentials 162) · `CustomerOriginStrategy.cs:45-55` · `OriginStrategy.cs:39-42`
- **Type:** STYLE
- **Docs say:** `requiresCredentials` readonly=True; `strategy` readonly=False; `credentials` writeonly=True.
- **Original-doc nuance:** —
- **Code does:** `OriginStrategy.cs:39-42` `requiresCredentials` `ReadOnly = false` (doc says True). `CustomerOriginStrategy.cs:45-48` `strategy` is a `HydraLink` with `ReadOnly = true` (doc says False). `CustomerOriginStrategy.cs:51-55` `credentials` is a `HydraLink` (Range String) with `ReadOnly = false, WriteOnly = false` (doc says writeonly True) — and modelling a write-only secret as a link looks wrong.
- **Issues/RFCs:** to check
- **Decision needed:** Correct the Hydra attributes (credentials -> RdfProperty WriteOnly; strategy ReadOnly=false; requiresCredentials ReadOnly=true) to match the documented contract?
- **Options:** (a) fix model attributes to match docs (b) adjust docs to match code (c) leave (cosmetic, low risk)
- **Possible outputs:** code / doc
- **Who's needed:** API dev
- **Status:** ☐ undecided

### SPA-13 · CustomerOriginStrategy Hydra model advertises PATCH that the controller doesn't implement
- **Theme:** Spaces & assets
- **Surfaces:** origin-strategy.mdx (table lines 102-106, GET/PUT/DELETE only) · `CustomerOriginStrategy.cs:80-82` · `CustomerOriginStrategiesController.cs`
- **Type:** CODE-WRONG (Hydra operations)
- **Docs say:** Customer origin strategy supports GET, PUT, DELETE (no PATCH) — correct.
- **Original-doc nuance:** —
- **Code does:** `CustomerOriginStrategyClass.DefineOperations` (`CustomerOriginStrategy.cs:80-82`) advertises `"GET","PUT","PATCH","DELETE"`, but `CustomerOriginStrategiesController` implements no PATCH on `{strategyId}` (only GET/PUT/DELETE; POST on the collection). Hydra over-advertises PATCH.
- **Issues/RFCs:** to check
- **Decision needed:** Drop PATCH from the advertised operations (or implement it)?
- **Options:** (a) remove PATCH from DefineOperations (b) implement PATCH (c) leave
- **Possible outputs:** code
- **Who's needed:** API dev
- **Status:** ☐ undecided

### SPA-14 · PUT to a space silently ignores a body `id` that differs from the URL
- **Theme:** Spaces & assets
- **Surfaces:** space.mdx#id (lines 45-54) · space.md scratch lines 4-12 · `SpaceController.cs:204-224`
- **Type:** DESIGN
- **Docs say:** "This is provided for read convenience, you can't set it yourself"; PUT to a particular space URL sets the id from the URL.
- **Original-doc nuance:** scratch: "PUT ../spaces/123 { id: 456, name } ... This works but ignores 456; space 123 is created. Should it be a Bad Request?"
- **Code does:** `PutSpace` (`SpaceController.cs:204-224`) never reads `space.ModelId`; the URL path wins and any body `id` is silently dropped. No validation/409/400 for a mismatch.
- **Issues/RFCs:** to check
- **Decision needed:** Should a body `id` that conflicts with the URL be a 400, or is silent-ignore acceptable (and should the doc state it)?
- **Options:** (a) reject mismatched id with 400 (matches asset behaviour, which validates id against the path) (b) keep silent-ignore and document it explicitly (c) leave undocumented
- **Possible outputs:** code / doc
- **Who's needed:** API owner
- **Status:** ☐ undecided

### SPA-15 · registering-assets returns `imageService`; scratch says this should become the `manifest` property
- **Theme:** Spaces & assets
- **Surfaces:** registering-assets.mdx#http-put (lines 166-178) · registering-assets.md scratch lines 4-22 · single-asset-manifest.mdx
- **Type:** DESIGN / STALE-SCRATCH
- **Docs say:** After a PUT, an image asset gains an `imageService` property the user can open in a viewer.
- **Original-doc nuance:** scratch registering-assets.md: "THIS NEEDS TO BE REPLACED BY THE `manifest` PROPERTY of asset"; also parks the "four ways / first-two" wording to restore when POST-to-Space lands.
- **Code does:** see SPA-04 — no `manifest` property exists yet; `imageService` is the current real field (`Image.cs:43-46`). Tightly coupled to SPA-04.
- **Issues/RFCs:** to check
- **Decision needed:** Once the single-asset `manifest` property exists, should registering-assets steer users to the manifest (viewer-openable) instead of the bare `imageService`?
- **Options:** (a) keep `imageService` guidance for now (b) add manifest guidance after SPA-04 ships (c) document both
- **Possible outputs:** doc
- **Who's needed:** docs + API owner
- **Status:** ☐ undecided

### SPA-16 · sample-code DELETE status comments are wrong (200/202 vs actual 204)
- **Theme:** Spaces & assets
- **Surfaces:** `dlcs-docs-client/p07_asset/get_put_patch_delete_asset.py:75` · `dlcs-docs-client/p11_delivery_channels/get_put_patch_delete_policy.py:66`
- **Type:** DOC-WRONG (sample comment)
- **Docs say:** asset sample comment "DELETE 200 OK"; policy sample comment "DELETE 202 Accepted".
- **Original-doc nuance:** —
- **Code does:** both endpoints return 204 No Content (`ImageController.cs:201`; `HydraController.cs:174`). The inline comments mislead.
- **Issues/RFCs:** —
- **Decision needed:** Correct both comments to "DELETE 204 No Content"?
- **Options:** (a) fix both comments (b) leave
- **Possible outputs:** sample
- **Who's needed:** docs
- **Status:** ☐ undecided

### SPA-17 · several legacy asset properties are serialised but undocumented
- **Theme:** Spaces & assets
- **Surfaces:** asset.mdx (none documented) · `Image.cs:49-53,60-63,98-104,202-211,231-244`
- **Type:** DESIGN / STALE-SCRATCH
- **Docs say:** Nothing.
- **Original-doc nuance:** —
- **Code does:** `Image.cs` still declares numerous undocumented fields that serialise into asset responses when set: `degradedInfoJson` (`:52`), `thumbnail400` (`:62`), `queued`/`dequeued` (`:98,103`), `text`/`textType` (`:205,210`, the latter flagged TODO replace with issue #148), and the legacy Deliverator links `imageOptimisationPolicy`/`thumbnailPolicy` (`:233,238`). These clutter the asset contract and aren't in the docs.
- **Issues/RFCs:** protagonist#148 (text) — to check others
- **Decision needed:** For each legacy field, decide document / deprecate / remove-from-model, so the published asset shape matches the docs.
- **Options:** (a) prune dead fields from the Hydra model (b) document the ones still in use (e.g., text/textType per #148) (c) leave and add a "legacy/undocumented fields" note
- **Possible outputs:** code / doc
- **Who's needed:** API owner
- **Status:** ☐ undecided
