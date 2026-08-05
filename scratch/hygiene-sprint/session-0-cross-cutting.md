# Hygiene Sprint · Session 0 — Cross-cutting conventions

**Scope.** This is the backbone file. It ratifies house rules that all other theme sessions (per-resource pages, error handling, identifiers) defer to. Findings come from a sweep of every `API/Features/**/*Controller*.cs`, the shared base `API/Infrastructure/HydraController.cs` + `API/Infrastructure/ControllerBaseX.cs`, the Hydra models in `DLCS.HydraModel`, and the docs in `public-docs/src/src/content/docs/api-doc/*.mdx`. These are SYSTEMIC patterns, not one-off bugs: each card proposes a convention plus the list of sites that violate it.

**How the framework decides status codes (context for every status card).** Most write endpoints funnel through `HydraController.HandleUpsert` / `HandleDelete`, which call `ControllerBaseX.ModifyResultToHttpResult` (`ControllerBaseX.cs:139`) and `ConvertDeleteToHttp` (`HydraController.cs:164`). The mapping is: `WriteResult.Updated → 200 Ok`, `WriteResult.Created → 201 (HydraCreated, Location header)`, `DeleteResult.Deleted → 204 NoContent`. So a verb's status is determined by which `WriteResult`/`DeleteResult` the *request handler* returns, NOT by the controller — which is why a handler returning the wrong `WriteResult` silently produces the wrong code while the `[ProducesResponseType]` annotation says otherwise. Errors everywhere go through `HydraProblem` (`ControllerBaseX.cs:74`) which builds a Hydra `Error` body. The outliers below are endpoints that bypass this machinery.

**⟳ Verified 2026-08-03** against protagonist develop@8341d780. All framework claims above re-confirmed; cards below carry inline corrections and three new cards (XC-11..13) from the second pass. Two data points for the room:
- **The new AdjunctQueues controller (July 2026) is a model citizen for these rules**: POST annotates 201 and the handler returns `WriteResult.Created` (annotation and handler agree — `CustomerAdjunctQueueController.cs:186`, `CreateAdjunctBatch.cs:103`); all errors flow through the standard machinery. The conventions being ratified here are ones current development already follows when nothing legacy is in the way.
- **PUT/POST standardisation is ALREADY IN-FLIGHT on the iiif-presentation side.** Jack (JackLewis-digirati) is implementing consistent PUT/POST semantics in open PR dlcs/iiif-presentation#641 (re-implementing #503, for issue #464; updated 2026-08-03): hierarchical PUT with If-Match, type-sniffing POST, everything routed through the `WriteResult.Created/Updated` mapping. **When the room ratifies XC-02/XC-03, hand the rulings to Jack's in-flight work rather than minting a parallel convention** — iiif-presentation has a single choke point where the ruling can land. We'll see in the process how the two codebases converge.

---

### XC-01 · DELETE must return 204 No Content
- **Theme:** Cross-cutting
- **Axis:** status-codes
- **Surfaces:** all controllers with a `[HttpDelete]`; `HydraController.cs:164-177` (canonical path)
- **Issues:** https://github.com/dlcs/protagonist/issues/1050
- **Type:** CODE-WRONG (annotations) + DESIGN (two legacy outliers)
- **Current state:** The canonical `ConvertDeleteToHttp` returns `204` (`HydraController.cs:174`). Nearly every DELETE is correct and annotated `204`: ApiKeys (`ApiKeysController.cs:95,107`), CustomHeaders (`CustomHeadersController.cs:156`), OriginStrategies (`CustomerOriginStrategiesController.cs:188`), PortalUsers (`PortalUsersController.cs:166,176`), NamedQueries (`NamedQueriesController.cs:162`), DefaultDeliveryChannels (`DefaultDeliveryChannelsController.cs:156`), Adjuncts (`AdjunctsController.cs:115`), CustomerAdjuncts (`CustomerAdjunctsController.cs:41,68`), Asset/Image (`ImageController.cs:185,201`). ~~Three~~ **Five** diverge *(tally corrected 2026-08-03)*.
- **Proposed house rule:** Every DELETE returns `204 No Content` with an empty body on success, `404` (Hydra Error) if absent, `409`/`500` (Hydra Error) on conflict/failure. No 2xx-with-body deletes. Annotate exactly `[ProducesResponseType(Status204NoContent)]`.
- **Violation sites:**
  - `DeliveryChannels/DeliveryChannelPoliciesController.cs:268` — annotated `Status202Accepted` but `HandleDelete` actually returns `204`. Annotation is a lie; fix annotation to 204.
  - `Customer/CustomerImagesController.cs:175,203` — bulk DELETE returns `200 OK` with `{ message = "images deleted" }` (explicit Deliverator back-compat note at `:202`). Non-standard.
  - `Space/SpaceController.cs:115` *(added 2026-08-03)* — DELETE annotated `Status200OK, Type = typeof(Space)` but uses `HandleDelete` → actual 204 empty body. Swagger promises a Space body that never arrives — a worse annotation lie than the 202 case.
  - `NamedQueries/CustomerResourcesController.cs:37-57` *(added 2026-08-03)* — DELETE `pdf/{queryName}` annotated 200 and returns `Ok(new { success = result })` ("backwards compat" TODO at `:56`). Fourth genuine DELETE-with-200-body.
  - `Customer/CustomerAdjunctsController.cs` is fine on success (204) — but its `404, Type=typeof(Error)` annotation (`:42`) lies: the not-found path actually returns **400** (`:65`, `HydraProblem(..., 400, ...)`) *(added 2026-08-03; XC-05 family)*.
- **Decision needed:** Ratify 204 rule? Fix `DeliveryChannelPoliciesController.cs:268` and `SpaceController.cs:115` annotations (code, trivial). Decide whether the bulk-image delete and pdf-purge keep their legacy 200 bodies (DESIGN/back-compat) or migrate — affects asset.mdx / queues / named-queries docs.
- **Possible outputs:** code + doc
- **Who's needed:** API maintainer + docs owner
- **Status:** ✅ RULED (session 0, 2026-08-06): **rule ratified** — every DELETE returns 204 empty on success (404/409/500 as Hydra Error), annotated exactly 204; no 2xx-with-body deletes, no exceptions. **Option (a): migrate both legacy endpoints** (`CustomerImagesController` bulk deleteImages 200+message; `CustomerResourcesController` pdf-purge 200+success) **to 204** — a BREAKING wire change, to be signposted in the PR (repo PR template, breaking-change section) for release notes. Owner: Donald. Outputs: protagonist hygiene/session-0 commit + comment on #1050. Doc updates for the migrated endpoints are release-gated (main = released behaviour). The two annotation lies were already fixed in PR #1234

### XC-02 · create-POST must return 201 Created
- **Theme:** Cross-cutting
- **Axis:** status-codes
- **Surfaces:** every resource-creating `[HttpPost]`
- **Type:** DESIGN + DOC-WRONG
- **Current state:** Resource creates correctly return `201` via `HydraCreated`: CustomHeaders (`:65`), CustomerOriginStrategies (`:72`), Customer (`:74`), PortalUsers (`:91,114`), NamedQueries (`:65`), DefaultDeliveryChannels (`:84`), Adjuncts (`:72`), AdjunctQueue (`CustomerAdjunctQueueController.cs:185-186` — was `:55`, five GET endpoints added above it July 2026), CustomerQueue batches (`:96,134`), Space (`:78`), DeliveryChannelPolicies (`:112`). Two POSTs that *do* mint something return `200`: API-key creation (`ApiKeysController.cs:76,83 Ok(...)`) and application setup (`ApplicationController.cs:28`). *(2026-08-03: see the Jack/#641 note in the preamble — iiif-presentation is standardising exactly this right now; hand the ruling over.)*
- **Proposed house rule:** A POST that creates a server-addressable resource returns `201` + `Location`. A POST that performs an *action* returning a transient/secret payload with no canonical URL (API key+secret, app bootstrap) may return `200` — but this exception must be named explicitly in the rule so it isn't copied accidentally.
- **Violation sites (or sanctioned exceptions to document):**
  - `Customer/ApiKeysController.cs:76,83` — key creation returns `200` (key/secret has no GET-able URL). Likely sanctioned exception.
  - `Application/ApplicationController.cs:28,36` — setup returns `200`. Likely sanctioned exception.
- **Decision needed:** Ratify 201 rule and explicitly carve out the "action POST returning ephemeral payload" exception, or force these to 201? Doc owners then state the exception on customer.mdx (keys section, `customer.mdx:477`).
- **Possible outputs:** RFC (carve-out) + doc
- **Who's needed:** API maintainer + docs owner
- **Status:** ✅ RULED (session 0, 2026-08-06): option (a) — **rule ratified**: a POST that creates a server-addressable resource returns 201 + Location. **Named exceptions (exactly two):** API-key creation and application setup are *action POSTs* returning an ephemeral payload with no canonical URL — they return 200, and this exception must not be copied to new endpoints. Cascades: ACC-14 resolves as "wire 200 is canonical" (ApiKey.cs Hydra metadata 201→200, on hygiene/session-0); customer.mdx#keys gains a sentence naming the exception; ruling handed to Jack's iiif-presentation PR #641 together with XC-03 once that is ruled

### XC-03 · PUT upsert: 201 on create, 200 on replace — handler must report the right WriteResult
- **Theme:** Cross-cutting
- **Axis:** status-codes
- **Surfaces:** PUT upsert endpoints + their request handlers
- **Type:** CODE-WRONG
- **Current state:** The framework returns `201` for `WriteResult.Created` and `200` for `WriteResult.Updated` (`ControllerBaseX.cs:146-147`). Handlers that correctly branch: `PutSpace.cs:61` (`Created` vs `Updated`), Image upsert (`CreateOrUpdateImage.cs:166`), DefaultDeliveryChannel update. Controllers that annotate both codes: Image (`ImageController.cs:82-83`), DeliveryChannelPolicies PUT (`:180-181`). One handler hard-codes `Created` on the update path.
- **Proposed house rule:** An upsert handler MUST return `WriteResult.Updated` when it replaced an existing row and `WriteResult.Created` only when it inserted; the PUT controller annotates BOTH `200` and `201`. Never hard-code `Created` on a known-update branch.
- **Violation sites:**
  - `CustomHeaders/Requests/UpdateCustomHeader.cs:50` — returns `WriteResult.Created` after updating an *existing* custom header → emits `201` for a replace. Controller annotates only `200` (`CustomHeadersController.cs:126`), so code and annotation disagree and the code is wrong.
- **Decision needed:** Ratify rule. Fix `UpdateCustomHeader.cs:50` to `WriteResult.Updated` (code). Audit other `*Update*` handlers for the same copy-paste (`UpdateCustomHeader` is the confirmed one; `UpsertDeliveryChannelPolicy.cs:74` and the create handlers correctly use Created only on insert paths). *(2026-08-03: `UpdateCustomHeader.cs:50` verified unchanged since 2023 — live PUT-update really does return 201 today; see ACC-15. And see the Jack/#641 preamble note: the same 201-create/200-replace mapping is what iiif-presentation's in-flight work funnels through.)*
- **Possible outputs:** code
- **Who's needed:** API maintainer
- **Status:** ✅ RATIFIED (session 0, 2026-08-06), with an addition: an upsert handler returns `Updated` on replace / `Created` only on insert, and a true-upsert PUT controller annotates BOTH 200 and 201; an **update-only PUT** (e.g. custom-header, which 404s rather than creates) annotates exactly what it does — 200/400/404. The sole violation (ACC-15) already fixed on hygiene/session-0; audit of other Update handlers found no second instance. Cascade: CustomHeadersController PUT annotation gains 404 (hygiene/session-0). Ruling handed with XC-02 to Jack's iiif-presentation PR #641

### XC-04 · All error responses must be a Hydra Error body — no bare status, no ad-hoc JSON
- **Theme:** Cross-cutting
- **Axis:** error-model
- **Surfaces:** all controllers
- **Type:** CODE-WRONG
- **Current state:** Errors are overwhelmingly produced by `HydraProblem` (`ControllerBaseX.cs:74`), giving a consistent Hydra `Error` (status/title/detail/instance). A handful of endpoints break the shape.
- **Proposed house rule:** Every non-2xx response carries a Hydra `Error` produced via `HydraProblem`/`HydraNotFound`/`ValidationFailed`. Never return bare `BadRequest()` / `NotFound()` (empty body) and never return ad-hoc anonymous success/diagnostic objects.
- **Violation sites:**
  - `DeliveryChannels/DefaultDeliveryChannelsController.cs:114` — `return BadRequest();` (empty, no Hydra Error) in the catch-all of the create POST.
  - `NamedQueries/CustomerResourcesController.cs:57` — `Ok(new { success = result })` (ad-hoc, non-Hydra success body).
  - `Queues/CustomerQueueController.cs:309` — `Ok(new { success = response })` (ad-hoc).
  - `Customer/CustomerImagesController.cs:203` — `Ok(new { message = "images deleted" })` (ad-hoc; see XC-01).
  - `DeliveryChannels/DeliveryChannelPoliciesController.cs:308` — `return Ok()` empty-body sentinel *(2026-08-03: was two sites, `:308,325`; now one, inside the merged private helper `TryValidateHydraDeliveryChannelPolicy` `:285-309`)*.
- **Decision needed:** Ratify "Hydra Error for all failures". Replace `BadRequest()` at `DefaultDeliveryChannelsController.cs:114` with `HydraProblem` (code). Decide whether the `{ success = ... }` action responses are acceptable success shapes or should become Hydra (DESIGN — touches queues/named-query docs).
- **Possible outputs:** code + RFC
- **Who's needed:** API maintainer + docs owner
- **Status:** ✅ RATIFIED (session 0, 2026-08-06): every non-2xx carries a Hydra Error via HydraProblem/HydraNotFound/ValidationFailed. Rulings: (1) bare `BadRequest()` at DefaultDeliveryChannelsController.cs:114 → HydraProblem (hygiene/session-0); (2) the batch `/test` `Ok({success})` is **kept and documented** as that endpoint's success shape (batch.mdx, docs hygiene/session-0) — the other two ad-hoc shapes were already removed by XC-01; (3) the internal `Ok()` sentinel in `TryValidateHydraDeliveryChannelPolicy` gets a tidy-up commit (no wire change). Owner: Donald (code) / PO (doc)

### XC-05 · ProducesResponseType error type must be `Error`, not `ProblemDetails`
- **Theme:** Cross-cutting
- **Axis:** error-model
- **Surfaces:** `Image/ImageController.cs`
- **Type:** CODE-WRONG (annotation only)
- **Current state:** Almost all controllers annotate error responses as `Type = typeof(Error)` (e.g. `CustomHeadersController.cs:35`, `NamedQueriesController.cs:36`). `ImageController` instead annotates `Type = typeof(ProblemDetails)` for its 4xx/5xx (`ImageController.cs:84-89,156-161`) even though the runtime body is a Hydra `Error` via `HydraProblem` (`ImageController.cs:108,308,317`). The OpenAPI/Swagger contract therefore advertises the wrong error schema for the asset endpoints.
- **Proposed house rule:** Error `[ProducesResponseType]` annotations always use `typeof(Error)` to match the actual `HydraProblem` body. `ProblemDetails` is never the documented error type.
- **Violation sites:**
  - `Image/ImageController.cs:84,85,86,87,88,89` (PUT) and `:156,157,158,159,160,161` (**PATCH** — mislabelled "POST/legacy" in the first pass) — `typeof(ProblemDetails)`.
  - `Image/ImageController.cs:244` *(added 2026-08-03)* — the actual legacy POST (`PostImageWithFileBytes`) carries a 13th `ProblemDetails` annotation. Repo-wide these 13 lines are the only `ProblemDetails` annotations in API.
- **Sub-pattern to fold in** *(added 2026-08-03)*: bare `Status404NotFound` annotations without `Type = typeof(Error)` are scattered (`SpaceController.cs:116,130`, `DeliveryChannelPoliciesController.cs:269`, `CustomerAdjunctQueueController.cs:35`, `ImageController.cs:186,215-216`, …) while sibling endpoints include the type; the rule could cover error annotations having *both* the right status and the `Error` type. Also `CustomerAdjunctsController.cs:42` annotates 404 where the code path returns 400 (see XC-01).
- **Decision needed:** Ratify; fix ImageController annotations to `Error` (code, trivial); decide whether the bare-404 sub-pattern is in scope for the same sweep.
- **Possible outputs:** code
- **Who's needed:** API maintainer
- **Status:** ✅ RATIFIED (session 0, 2026-08-06), sub-pattern in scope: error `[ProducesResponseType]` annotations always carry **both** the status and `Type = typeof(Error)`; `ProblemDetails` never appears. The 13 ImageController annotations were fixed in PR #1234; the repo-wide bare-error-status sweep is a hygiene/session-0 commit. Owner: Donald

### XC-06 · Hydra property names must not have trailing spaces
- **Theme:** Cross-cutting
- **Axis:** hydra-cleanliness
- **Surfaces:** `DLCS.HydraModel/Customer.cs`; docs that render these fields
- **Type:** CODE-WRONG (with downstream DOC-WRONG)
- **Current state:** `Customer` serializes three properties with a trailing space in the wire key: `"administrator "` (`Customer.cs:135`), `"created "` (`Customer.cs:140`), `"acceptedAgreement "` (`Customer.cs:145`). Clients must literally request `obj["created "]`. The docs hide this: `customer.mdx:19` shows `"created"` (clean) and the property section heading is `## created` (`customer.mdx:95` as of 2026-08-03) — so the published JSON example does not match what the API emits. *(2026-08-03: repo-wide regex re-run — these three remain the only whitespace-suffixed property names.)*
- **Proposed house rule:** No `JsonProperty(PropertyName=...)` may contain leading/trailing whitespace. Add a unit/reflection test asserting every Hydra property name `== name.Trim()`.
- **Violation sites:**
  - `DLCS.HydraModel/Customer.cs:135` — `"administrator "`
  - `DLCS.HydraModel/Customer.cs:140` — `"created "`
  - `DLCS.HydraModel/Customer.cs:145` — `"acceptedAgreement "`
- **Decision needed:** Ratify. This is a breaking wire change — fixing the code (trim the names) is correct but may affect existing consumers/portal; needs API maintainer sign-off. Until fixed, customer.mdx is arguably *wrong* to show clean names (DOC-WRONG); decide whether docs document the bug or wait for the fix.
- **Possible outputs:** code + doc + RFC (breaking-change call)
- **Who's needed:** API maintainer + docs owner
- **Status:** ✅ RULED (session 0, 2026-08-06): rule ratified + reflection test added (no Hydra JsonProperty name may differ from its Trim()); the three spaced names are **fixed now** on hygiene/session-0 — BREAKING, signposted in PR #1236 alongside the XC-01 changes; Donald to confirm the portal reads clean keys before merge. Docs stay clean (they already show the post-fix names)

### XC-07 · Legacy / unmanageable Hydra links should not be advertised in entry-point & customer
- **Theme:** Cross-cutting
- **Axis:** hydra-cleanliness
- **Surfaces:** `DLCS.HydraModel/EntryPoint.cs`, `DLCS.HydraModel/Customer.cs`; entrypoint.mdx, customer.mdx
- **Issues:** https://github.com/dlcs/protagonist/issues/899, https://github.com/dlcs/protagonist/issues/738
- **Type:** DESIGN / DOC-WRONG
- **Current state:** `EntryPoint` still emits `imageOptimisationPolicies` (`EntryPoint.cs:40-42`, ops `:115-125`) and `thumbnailPolicies` (`EntryPoint.cs:48-49`, ops `:127-137`) — legacy policy concepts superseded by delivery channels. `Customer` still emits `authServices` (`Customer.cs:83-84`), `roles` (`Customer.cs:96-97`) and `roleProviders` (`Customer.cs:89-90`) — the IIIF-Auth subsystem (iiif-auth-v2) that, per project notes, cannot yet be managed via the REST API. These links appear in live responses and are partly reflected in docs.
- **Proposed house rule:** The API only advertises Hydra links to resources that are actually reachable/manageable through the current API. Links to deprecated subsystems (image/thumbnail policies) or not-yet-API-backed subsystems (auth services/roles/roleProviders) are either removed or explicitly flagged as not-yet-available; docs must agree with whatever is emitted.
- **Violation sites:**
  - `DLCS.HydraModel/EntryPoint.cs:40-42,48-49` — imageOptimisationPolicies, thumbnailPolicies
  - `DLCS.HydraModel/Customer.cs:83-84,89-90,96-97` — authServices, roleProviders, roles
- **Decision needed:** Ratify "advertise only reachable links". For each link: remove (code) vs keep+document-as-unavailable (doc). Coordinates with the not-yet-ported roles/auth-service/access-control pages.
- **Possible outputs:** code or doc (per link) + RFC
- **Who's needed:** API maintainer + docs owner + auth subsystem owner
- **Status:** ☐ undecided

### XC-08 · Identifier policy: id everywhere, with a named exception register
- **Theme:** Cross-cutting
- **Axis:** identifier-policy
- **Surfaces:** all resources; `identifiers.mdx`
- **Type:** DESIGN (documentation of an accepted inconsistency)
- **Current state:** Most resources are addressed by their minted `id`. `DeliveryChannelPolicy` is keyed by `name` (its URL path element is the policy name; route `{deliveryChannelName}/{deliveryChannelPolicyName}`, e.g. `DeliveryChannelPoliciesController.cs:267`). `NamedQuery` carries a `name` property but is addressed by a minted GUID `id` (`NamedQueriesController.cs` get/patch by id). `identifiers.mdx` already documents this divergence and `CLAUDE.md` conventions echo it.
- **Proposed house rule:** Resources are addressed by `id` unless explicitly listed in an "identifier exception register" in identifiers.mdx. Exactly two registered exceptions today: (a) `DeliveryChannelPolicy` addressed by `name`; (b) `NamedQuery` has a human `name` but is still addressed by `id`. Any new name-addressed resource must be added to the register in the same PR.
- **Violation sites:** none in code today — this card ratifies the existing exceptions and makes the register authoritative so future drift is caught in review.
- **Decision needed:** Ratify the register concept; confirm identifiers.mdx is the canonical home and lists exactly these two cases.
- **Possible outputs:** doc
- **Who's needed:** docs owner + API maintainer
- **Status:** ☐ undecided

### XC-09 · domain/range tables: fixed format + flags derived from the model, not hand-typed
- **Theme:** Cross-cutting
- **Axis:** table-convention
- **Surfaces:** every property section in api-doc/*.mdx
- **Type:** STYLE + DOC-WRONG (trust)
- **Current state:** The `| domain | range | readonly | writeonly |` table format is applied consistently across pages (customer.mdx has 14 such tables as of 2026-08-03, space.mdx ~9, similar elsewhere). Good. BUT the flags are hand-transcribed from the model's `RdfProperty`/`HydraLink` `ReadOnly`/`WriteOnly` attributes, so their trustworthiness depends on manual sync — and XC-06 already shows the docs diverging from the model (clean vs trailing-space names, `customer.mdx:19`). There is no automated check that a table row matches the underlying attribute.
- **Proposed house rule:** (a) Keep the canonical 4-column format. (b) The readonly/writeonly values are authoritative *only if* they match the model's `ReadOnly`/`WriteOnly` attribute for that property; treat the model as source of truth. (c) Add a verification pass (script or checklist) cross-referencing each table against `DLCS.HydraModel`, run during the per-resource sessions.
- **Violation sites:** systemic — no single line; flagged because the other sessions will rely on these flags. Confirmed concrete mismatch: customer.mdx renders the trailing-space props with clean names (XC-06).
- **Decision needed:** Ratify "model is source of truth for flags"; agree a lightweight verification step the per-resource sessions must run.
- **Possible outputs:** doc + (optional) sample/script
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### XC-10 · Docs and Python samples move together (sample-parity rule + coverage)
- **Theme:** Cross-cutting
- **Axis:** samples-coverage
- **Current state:** Most published pages ship a Python sample in `dlcs-docs-client/p{N}_…/`
  (overview, registering, entrypoint, customer, space, asset, queues, batch, delivery-channels,
  origin-strategy, adjuncts, asset-queries, named-queries, single-asset-manifest, storage,
  custom-headers). Conceptual pages deliberately have none (collections, identifiers,
  size-restrictions). BUT there is no rule binding a doc change to its sample, so coverage drifts:
  several real, documented (or about-to-be-documented) operations have **no** sample, and at
  least one sample is an orphan demoing an unbuilt feature.
- **Proposed house rule:** Any user-facing feature change/add/removal updates the matching
  Python sample in the SAME unit of work (add for new, edit for changed, retire for removed).
  A doc-only card must record why no sample is needed. New pages ship with a sample unless
  conceptual. Make this part of the per-item definition-of-done (README principle 6).
- **Known coverage gaps (sample missing / stale / orphan) — re-checked 2026-08-03; several closed since June:**
  - ~~Portal Users~~ **partially closed**: `p05_customer/portal_users.py` now exists (list GET, POST, DELETE); GET-single and PATCH still unsampled (ACC-10).
  - ~~API-key DELETE~~ **closed**: `p05_customer/keys.py` now includes it (ACC-12). Still open: priority-queue GET (PRO-05); asset `reingest` POST (asset.mdx:499).
  - Bulk `POST /customers/{c}/deleteImages` and `/deleteAdjuncts` (XC-01, ADJ-11) — still no sample.
  - `space.images` bulk PATCH (SPA-07) — implemented, still no sample (`p06_space/space_images.py:49-52` still commented out).
  - named-query PDF/ZIP generation + params (DIS-07/08) — promote-from-scratch needs a sample.
  - asset-query ordering (DIS-01) — **half-closed**: `get_images_ordered` example now exists (`p15_asset_queries/asset_queries.py:97`, invoked `:156`) but its docstring still says "NOT yet supported - ordering is ignored" — docstring fix outstanding. `manifests` filter / `include=adjuncts` (DIS-02/03) docstrings still stale.
  - **New since June**: an adjunct-queue sample suite exists (`p08_queue/get_adjunct_*` ×3, `get_and_post_adjunct_queue.py`; `p09_batch/adjunct_batch_operations.py`; `p13_adjuncts/get_adjunct_batch.py`; `p07_asset/get_asset_batch.py`, `asset_adjuncts.py`) — three of these are broken against the actual API (wrong/missing `asset` field, un-emitted links): see PRO-08/PRO-11.
  - Origin-strategy `update_credentials.py` — still ORPHAN: no `/credentials` route anywhere in current API (delete/rewrite).
  - Adjunct `content_adjunct.py` — still ORPHAN: no `content` route (ADJ-01).
  - `p02_registering/post.py` / `space_images.py` — intentional orphans demoing the 405 POST-to-space (keep, but label).
  - Unported pages will each need a sample on porting: `iiif` (feasible now), `pipelines` (defer), and the auth cluster (blocked until a management API exists — AUTH-01).
- **Decision needed:** Ratify the sample-parity rule + DoD addition; agree that each themed
  session, when it rules on a feature card, also assigns the sample work; triage the coverage
  gaps above into the relevant sessions.
- **Possible outputs:** doc + sample + process
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### XC-11 · Adjunct PUT annotation wrong on both status and type *(added 2026-08-03 verification pass)*
- **Theme:** Cross-cutting
- **Axis:** status-codes / annotations
- **Surfaces:** `Adjuncts/AdjunctsController.cs:92-94` · `AdjunctsController.cs:150-162` (`BuildHydraResponse`)
- **Type:** CODE-WRONG (annotation)
- **Current state:** PUT `/adjuncts/{id}` annotates only `200, Type = typeof(HydraCollection<Adjunct>)`. But (a) the handler is an upsert that can return `WriteResult.Created` → actual **201** for a new adjunct; (b) PUT deliberately returns a **single `Adjunct`**, never a collection (`adjuncts.Single().ToHydra(...)`). Annotation wrong twice.
- **Decision needed:** Fix annotation to `200 + 201, Type = typeof(Adjunct)` (code, trivial); feeds the XC-03 audit list.
- **Possible outputs:** code
- **Who's needed:** API maintainer
- **Status:** ☑ mechanical — merged in protagonist PR #1234 (2026-08-06, donaldgray)

### XC-12 · Batch upserts collapse per-member Created/Updated into one WriteResult *(added 2026-08-03 verification pass)*
- **Theme:** Cross-cutting
- **Axis:** status-codes
- **Surfaces:** `Adjuncts/Requests/CreateOrUpdateAdjunct.cs:52,70,122` (single `anyUpdates` trip-flag)
- **Type:** DESIGN
- **Current state:** A multi-member POST/PUT that mixes new and existing members reports one status for the whole batch: the `anyUpdates` flag means a mixed batch reports 200/Updated even though some members were created. No per-member semantics anywhere.
- **Decision needed:** Convention ruling for ALL batch upserts: is whole-batch 200-if-any-update acceptable (document it), or should mixed batches report 201-if-any-create, or per-member status in the body? Applies to any future bulk endpoint too.
- **Possible outputs:** RFC (small) + doc
- **Who's needed:** API maintainer + docs owner
- **Status:** ☐ undecided

### XC-13 · Advertise what exists: live `/adjunctQueue` has no Customer link; AdjunctBatch links commented out against reality *(added 2026-08-03 verification pass)*
- **Theme:** Cross-cutting
- **Axis:** hydra-cleanliness (inverse of XC-07)
- **Surfaces:** `DLCS.HydraModel/Customer.cs` (no `adjunctQueue` property) · `DLCS.HydraModel/AdjunctBatch.cs:54-65` (links commented out) · `DlcsResource.cs:55` (link URL generation)
- **Type:** CODE-WRONG / DESIGN
- **Current state:** XC-07's mirror image: the Customer model advertises links to *unreachable* subsystems while NOT advertising the live `/customers/{id}/adjunctQueue` resource (develop). And `AdjunctBatch`'s `CurrentAdjuncts`/`Adjuncts` HydraLinks are commented out with a TODO saying "not implemented yet" — but the routes ARE now implemented (PR #1226), so the TODO is stale in the opposite direction. Trap for the reinstating PR: auto-generation emits `{@id}/{jsonPropertyName}` → `.../currentAdjuncts`, which does NOT match the implemented `/current` route — needs `SetManually` + converter wiring (batch.mdx:180 documents the `/current` form).
- **Decision needed:** One rule covering both directions: the model advertises exactly the reachable surface. Add `adjunctQueue` link to Customer; reinstate the two AdjunctBatch links with correct manual URLs. Ties to protagonist #1166.
- **Possible outputs:** code
- **Who's needed:** API maintainer
- **Status:** ☐ undecided
