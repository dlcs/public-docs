# Hygiene Sprint · Session 0 — Cross-cutting conventions

**Scope.** This is the backbone file. It ratifies house rules that all other theme sessions (per-resource pages, error handling, identifiers) defer to. Findings come from a sweep of every `API/Features/**/*Controller*.cs`, the shared base `API/Infrastructure/HydraController.cs` + `API/Infrastructure/ControllerBaseX.cs`, the Hydra models in `DLCS.HydraModel`, and the docs in `public-docs/src/src/content/docs/api-doc/*.mdx`. These are SYSTEMIC patterns, not one-off bugs: each card proposes a convention plus the list of sites that violate it.

**How the framework decides status codes (context for every status card).** Most write endpoints funnel through `HydraController.HandleUpsert` / `HandleDelete`, which call `ControllerBaseX.ModifyResultToHttpResult` (`ControllerBaseX.cs:139`) and `ConvertDeleteToHttp` (`HydraController.cs:164`). The mapping is: `WriteResult.Updated → 200 Ok`, `WriteResult.Created → 201 (HydraCreated, Location header)`, `DeleteResult.Deleted → 204 NoContent`. So a verb's status is determined by which `WriteResult`/`DeleteResult` the *request handler* returns, NOT by the controller — which is why a handler returning the wrong `WriteResult` silently produces the wrong code while the `[ProducesResponseType]` annotation says otherwise. Errors everywhere go through `HydraProblem` (`ControllerBaseX.cs:74`) which builds a Hydra `Error` body. The outliers below are endpoints that bypass this machinery.

---

### XC-01 · DELETE must return 204 No Content
- **Theme:** Cross-cutting
- **Axis:** status-codes
- **Surfaces:** all controllers with a `[HttpDelete]`; `HydraController.cs:164-177` (canonical path)
- **Type:** CODE-WRONG (annotations) + DESIGN (two legacy outliers)
- **Current state:** The canonical `ConvertDeleteToHttp` returns `204` (`HydraController.cs:174`). Nearly every DELETE is correct and annotated `204`: ApiKeys (`ApiKeysController.cs:95,107`), CustomHeaders (`CustomHeadersController.cs:156`), OriginStrategies (`CustomerOriginStrategiesController.cs:188`), PortalUsers (`PortalUsersController.cs:166,176`), NamedQueries (`NamedQueriesController.cs:162`), DefaultDeliveryChannels (`DefaultDeliveryChannelsController.cs:156`), Adjuncts (`AdjunctsController.cs:115`), CustomerAdjuncts (`CustomerAdjunctsController.cs:41,68`), Asset/Image (`ImageController.cs:185,201`). Three diverge.
- **Proposed house rule:** Every DELETE returns `204 No Content` with an empty body on success, `404` (Hydra Error) if absent, `409`/`500` (Hydra Error) on conflict/failure. No 2xx-with-body deletes. Annotate exactly `[ProducesResponseType(Status204NoContent)]`.
- **Violation sites:**
  - `DeliveryChannels/DeliveryChannelPoliciesController.cs:268` — annotated `Status202Accepted` but `HandleDelete` actually returns `204`. Annotation is a lie; fix annotation to 204.
  - `Customer/CustomerImagesController.cs:175,203` — bulk DELETE returns `200 OK` with `{ message = "images deleted" }` (explicit Deliverator back-compat note at `:202`). Non-standard.
  - `Customer/CustomerAdjunctsController.cs` is fine (204) — listed only to contrast with the bulk-image outlier.
- **Decision needed:** Ratify 204 rule? Fix `DeliveryChannelPoliciesController.cs:268` annotation (code, trivial). Decide whether the bulk-image delete keeps its legacy 200 body (DESIGN/back-compat) or migrates — affects asset.mdx / queues docs.
- **Possible outputs:** code + doc
- **Who's needed:** API maintainer + docs owner
- **Status:** ☐ undecided

### XC-02 · create-POST must return 201 Created
- **Theme:** Cross-cutting
- **Axis:** status-codes
- **Surfaces:** every resource-creating `[HttpPost]`
- **Type:** DESIGN + DOC-WRONG
- **Current state:** Resource creates correctly return `201` via `HydraCreated`: CustomHeaders (`:65`), CustomerOriginStrategies (`:72`), Customer (`:74`), PortalUsers (`:91,114`), NamedQueries (`:65`), DefaultDeliveryChannels (`:84`), Adjuncts (`:72`), AdjunctQueue (`CustomerAdjunctQueueController.cs:55`), CustomerQueue batches (`:96,134`), Space (`:78`), DeliveryChannelPolicies (`:112`). Two POSTs that *do* mint something return `200`: API-key creation (`ApiKeysController.cs:76,83 Ok(...)`) and application setup (`ApplicationController.cs:28`).
- **Proposed house rule:** A POST that creates a server-addressable resource returns `201` + `Location`. A POST that performs an *action* returning a transient/secret payload with no canonical URL (API key+secret, app bootstrap) may return `200` — but this exception must be named explicitly in the rule so it isn't copied accidentally.
- **Violation sites (or sanctioned exceptions to document):**
  - `Customer/ApiKeysController.cs:76,83` — key creation returns `200` (key/secret has no GET-able URL). Likely sanctioned exception.
  - `Application/ApplicationController.cs:28,37` — setup returns `200`. Likely sanctioned exception.
- **Decision needed:** Ratify 201 rule and explicitly carve out the "action POST returning ephemeral payload" exception, or force these to 201? Doc owners then state the exception on customer.mdx (keys section, `customer.mdx:477`).
- **Possible outputs:** RFC (carve-out) + doc
- **Who's needed:** API maintainer + docs owner
- **Status:** ☐ undecided

### XC-03 · PUT upsert: 201 on create, 200 on replace — handler must report the right WriteResult
- **Theme:** Cross-cutting
- **Axis:** status-codes
- **Surfaces:** PUT upsert endpoints + their request handlers
- **Type:** CODE-WRONG
- **Current state:** The framework returns `201` for `WriteResult.Created` and `200` for `WriteResult.Updated` (`ControllerBaseX.cs:146-147`). Handlers that correctly branch: `PutSpace.cs:61` (`Created` vs `Updated`), Image upsert (`CreateOrUpdateImage.cs:166`), DefaultDeliveryChannel update. Controllers that annotate both codes: Image (`ImageController.cs:82-83`), DeliveryChannelPolicies PUT (`:180-181`). One handler hard-codes `Created` on the update path.
- **Proposed house rule:** An upsert handler MUST return `WriteResult.Updated` when it replaced an existing row and `WriteResult.Created` only when it inserted; the PUT controller annotates BOTH `200` and `201`. Never hard-code `Created` on a known-update branch.
- **Violation sites:**
  - `CustomHeaders/Requests/UpdateCustomHeader.cs:50` — returns `WriteResult.Created` after updating an *existing* custom header → emits `201` for a replace. Controller annotates only `200` (`CustomHeadersController.cs:126`), so code and annotation disagree and the code is wrong.
- **Decision needed:** Ratify rule. Fix `UpdateCustomHeader.cs:50` to `WriteResult.Updated` (code). Audit other `*Update*` handlers for the same copy-paste (`UpdateCustomHeader` is the confirmed one; `UpsertDeliveryChannelPolicy.cs:74` and the create handlers correctly use Created only on insert paths).
- **Possible outputs:** code
- **Who's needed:** API maintainer
- **Status:** ☐ undecided

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
  - `DeliveryChannels/DeliveryChannelPoliciesController.cs:308,325` — `return Ok()` / `Ok()` empty bodies used as sentinels.
- **Decision needed:** Ratify "Hydra Error for all failures". Replace `BadRequest()` at `DefaultDeliveryChannelsController.cs:114` with `HydraProblem` (code). Decide whether the `{ success = ... }` action responses are acceptable success shapes or should become Hydra (DESIGN — touches queues/named-query docs).
- **Possible outputs:** code + RFC
- **Who's needed:** API maintainer + docs owner
- **Status:** ☐ undecided

### XC-05 · ProducesResponseType error type must be `Error`, not `ProblemDetails`
- **Theme:** Cross-cutting
- **Axis:** error-model
- **Surfaces:** `Image/ImageController.cs`
- **Type:** CODE-WRONG (annotation only)
- **Current state:** Almost all controllers annotate error responses as `Type = typeof(Error)` (e.g. `CustomHeadersController.cs:35`, `NamedQueriesController.cs:36`). `ImageController` instead annotates `Type = typeof(ProblemDetails)` for its 4xx/5xx (`ImageController.cs:84-89,156-161`) even though the runtime body is a Hydra `Error` via `HydraProblem` (`ImageController.cs:108,308,317`). The OpenAPI/Swagger contract therefore advertises the wrong error schema for the asset endpoints.
- **Proposed house rule:** Error `[ProducesResponseType]` annotations always use `typeof(Error)` to match the actual `HydraProblem` body. `ProblemDetails` is never the documented error type.
- **Violation sites:**
  - `Image/ImageController.cs:84,85,86,87,88,89` (PUT) and `:156,157,158,159,160,161` (POST/legacy) — `typeof(ProblemDetails)`.
- **Decision needed:** Ratify; fix ImageController annotations to `Error` (code, trivial).
- **Possible outputs:** code
- **Who's needed:** API maintainer
- **Status:** ☐ undecided

### XC-06 · Hydra property names must not have trailing spaces
- **Theme:** Cross-cutting
- **Axis:** hydra-cleanliness
- **Surfaces:** `DLCS.HydraModel/Customer.cs`; docs that render these fields
- **Type:** CODE-WRONG (with downstream DOC-WRONG)
- **Current state:** `Customer` serializes three properties with a trailing space in the wire key: `"administrator "` (`Customer.cs:135`), `"created "` (`Customer.cs:140`), `"acceptedAgreement "` (`Customer.cs:145`). Clients must literally request `obj["created "]`. The docs hide this: `customer.mdx:19` shows `"created"` (clean) and the property section heading is `## created` (`customer.mdx:97`) — so the published JSON example does not match what the API emits.
- **Proposed house rule:** No `JsonProperty(PropertyName=...)` may contain leading/trailing whitespace. Add a unit/reflection test asserting every Hydra property name `== name.Trim()`.
- **Violation sites:**
  - `DLCS.HydraModel/Customer.cs:135` — `"administrator "`
  - `DLCS.HydraModel/Customer.cs:140` — `"created "`
  - `DLCS.HydraModel/Customer.cs:145` — `"acceptedAgreement "`
- **Decision needed:** Ratify. This is a breaking wire change — fixing the code (trim the names) is correct but may affect existing consumers/portal; needs API maintainer sign-off. Until fixed, customer.mdx is arguably *wrong* to show clean names (DOC-WRONG); decide whether docs document the bug or wait for the fix.
- **Possible outputs:** code + doc + RFC (breaking-change call)
- **Who's needed:** API maintainer + docs owner
- **Status:** ☐ undecided

### XC-07 · Legacy / unmanageable Hydra links should not be advertised in entry-point & customer
- **Theme:** Cross-cutting
- **Axis:** hydra-cleanliness
- **Surfaces:** `DLCS.HydraModel/EntryPoint.cs`, `DLCS.HydraModel/Customer.cs`; entrypoint.mdx, customer.mdx
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
- **Current state:** The `| domain | range | readonly | writeonly |` table format is applied consistently across pages (customer.mdx has ~17 such tables, space.mdx ~9, similar elsewhere). Good. BUT the flags are hand-transcribed from the model's `RdfProperty`/`HydraLink` `ReadOnly`/`WriteOnly` attributes, so their trustworthiness depends on manual sync — and XC-06 already shows the docs diverging from the model (clean vs trailing-space names, `customer.mdx:19`). There is no automated check that a table row matches the underlying attribute.
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
- **Known coverage gaps (sample missing / stale / orphan) — seeds, not exhaustive:**
  - Portal Users lifecycle GET-single / PATCH / DELETE (ACC-10) — no sample.
  - API-key DELETE (ACC-12); priority-queue GET (PRO-05); asset `reingest` POST (asset.mdx:499) — no samples.
  - Bulk `POST /customers/{c}/deleteImages` and `/deleteAdjuncts` (XC-01, ADJ-11) — no sample.
  - `space.images` bulk PATCH (SPA-07) — implemented, no sample.
  - named-query PDF/ZIP generation + params (DIS-07/08) — promote-from-scratch needs a sample.
  - asset-query ordering / `manifests` filter / `include=adjuncts` (DIS-01/02/03) — `p15` sample needs the ordering example added; `get_images_ordered` docstring stale.
  - Origin-strategy `update_credentials.py` — ORPHAN describing a non-existent `/credentials` sub-resource (delete/rewrite).
  - Adjunct `content_adjunct.py` — ORPHAN demoing the unimplemented `/content` endpoint.
  - `post.py` / `space_images.py` — intentional orphans demoing the 405 POST-to-space (keep, but label).
  - Unported pages will each need a sample on porting: `iiif` (feasible now), `pipelines` (defer), and the auth cluster (blocked until a management API exists — AUTH-01).
- **Decision needed:** Ratify the sample-parity rule + DoD addition; agree that each themed
  session, when it rules on a feature card, also assigns the sample work; triage the coverage
  gaps above into the relevant sessions.
- **Possible outputs:** doc + sample + process
- **Who's needed:** docs owner
- **Status:** ☐ undecided
