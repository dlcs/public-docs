# Hygiene Sprint · Session 6 · IIIF & Auth

## Scope

This session covers the **largest design-gap cluster** in the API documentation: the IIIF
Presentation pages and the IIIF Auth (roles / auth-service / access-control) pages. None of
these pages have been ported to the new Starlight site yet — `iiif.mdx`, `roles.mdx`,
`auth-service.mdx` and `access-control.mdx` are all linked from existing pages but will 404
until created. So the whole cluster is a set of **porting decisions**, not in-place fixes.

Two parts, with very different shapes:

1. **IIIF Presentation** (`iiif.mdx`). The old Nextra page is ~1,940 lines of rich, detailed
   prose (storage collections, IIIF collections, manifests, `paintedResources`,
   flat-vs-hierarchical URIs, the `X-IIIF-CS-Show-Extras` header, configuration, "JSON is
   King" update semantics). The corresponding feature is **substantially implemented today**
   in the `iiif-presentation` repo — controllers, routes, models and reserved-slug validation
   all exist. So most IIIF cards are STALE-SCRATCH → port (the doc largely matches the code),
   with a handful of DOC-WRONG / CODE-MISSING divergences where the prose describes things the
   code doesn't do (PATCH, the `configuration` endpoint, manifest `assets`/`queue` links,
   descendant counts).

2. **Auth** (`roles` / `auth-service` / `access-control`). The old `access-control.mdx` is a
   stub ("still under development"), and there is no `roles.mdx` or `auth-service.mdx` in the
   old docs at all. The runtime is implemented in `iiif-auth-v2`, but it has **no management
   REST API** — roles, access services and role providers are configured by inserting rows
   directly into Postgres tables (see `scripts/sql/bootstrap.sql`). The big work here is
   **DESIGN**: what should the management REST API look like? These cards map the DB model and
   frame the design questions, leaning on the open issues (protagonist #538 "Manage Auth
   Services via API", iiif-auth-v2 #46 "auto create clickthrough role").

Note: for IIIF, the old Nextra `iiif.mdx` and `scratch/api-doc/iiif.md` are essentially the
**same content** — the whole live page was copied verbatim into scratch ("THIS WHOLE PAGE IS
COPIED TO SCRATCG"), so the rich prose is preserved in scratch already.

**⟳ Verified 2026-08-03** against iiif-presentation develop@ac3dcf45 and iiif-auth-v2 HEAD
494e373 (2026-03-31 — auth repo has NOT moved; all 12 AUTH cards re-verified unchanged). The
IIIF side HAS moved substantially — inline updates below, new card IIIF-14, and two strategic
notes for the room:
1. **Jack (JackLewis-digirati) is standardising PUT/POST semantics right now** in open PR
   **#641** "hierarchical consistent PUT/POST" (updated 2026-08-03; re-implements stale #503,
   for issue #464 "Consistent API PUT and POST behaviour", also resolves #291). It lands:
   hierarchical POST that type-sniffs Manifest-vs-Collection from the body, a NEW hierarchical
   PUT (create-or-update at path, carries If-Match), Show-Extras **not** required on
   hierarchical writes (vanilla IIIF bodies; responses cleaned by `PresentationIIIFCleaner`),
   and hierarchical DELETE deliberately dropped. Everything funnels through the
   `WriteResult.Created/Updated` mapping (refactored in merged #639, `PresentationResult`).
   **We'll see in the process how this converges with the XC-02/XC-03 rulings — hand them to
   Jack's in-flight work rather than minting a parallel convention.** Treat #503 as the design
   record, #641 as what will merge; IIIF-02/IIIF-12 walkthroughs should target #641's branch.
2. **PR #228 (open since 2025-10) adds RFC 0020 "collection containment vs membership"** —
   `containedItems` (extras) + independently-editable `items` (vanilla IIIF), server-maintained
   membership; it muses about dissolving the Storage-vs-IIIF-Collection distinction asserted
   above. Do not port the collections prose as settled while it is open (affects IIIF-01,
   IIIF-06, IIIF-12).

---

**⟳ SESSION 6 PRE-FLIGHT 2026-08-26.** Repos synced. Branch `hygiene/session-6` cut from the `hygiene/session-5`
head because docs **PR #17** (session 5) is still open — retarget/rebase onto main when #17 merges. Protagonist:
develop unchanged since the session-5 baseline (1a77352a); **#1292 merged**; release still **v1.13.2**; **#538
"Manage Auth Services via API" still OPEN** (the auth-cluster gate) and #284 "Manage role-provider configuration"
likewise — so the AUTH cards remain DESIGN-only as planned. **iiif-auth-v2 has NOT moved** (HEAD 086011f; only two
dependabot bumps since 494e373; #46 open; all 12 AUTH cards' premises stand unchanged).

**iiif-presentation HAS moved — twice over.** (1) **Release v0.10.0 shipped 2026-08-04** ("Search services": stored
incoming payloads, Text-Services integration, search-within + **search-across (#635)**, manifest **pipelines**
(#623/#625/#633), error-URI fixes (#638), #639 housekeeping) — everything IIIF-14 describes is now *released*, not
develop-only. (2) develop is **41 commits past v0.10.0**: **PR #641 "Hierarchical consistent PUT/POST" MERGED
2026-08-12** (closes #464/#291; #503 closed as superseded) — `StorageController` now has `[HttpPut("{*slug}")]`
(:124-125) alongside hierarchical POST (:101-102), both `[Authorize]` without `RequireShowExtras`; slugs may no
longer contain slashes/FQDNs (8baa210a); space must be a positive integer (31561863/34a71c38); choice without
`choiceOrder` rejected (#649 closed); empty adjunct arrays dropped from responses (#612 closed, a4942d62); **.NET 10**
(#652 merged 08-24). Open PRs: #655 (iiif-net bump / deserialisation fixes, 08-25), #228 (RFC 0020 collections
containment — still open, still the reason not to port the collections prose as settled), #93 (2024 prototype).
New issues: **#654** legacy host setting + **#653** legacy redirects (`presentation-api.*` → `iiif.*` hostname
migration per an ADR — affects every URL example the port will contain; find the ADR before IIIF-01), #579 (missing
`type` → 500, open since 03-31), #540 (error-message tidy).

**Card-cite freshness:** cited files that changed since the 08-03 baseline: `ManifestController.cs`,
`CollectionController.cs`, `StorageController.cs`, `ManifestConverter.cs`, `HttpRequestX.cs`, both validators.
Re-derived on develop 94713c79: Manifest routes GET :31 / POST :66 / PUT :83 / DELETE :99 (no PATCH); Collection
GET :34 / search :65 / POST :92 / PUT :104 / DELETE :147 (no PATCH); Storage GET :37 / POST :102 / **PUT :125 (new)**.
`HttpRequestX` Show-Extras :7/:16; `CustomHttpHeaders.ShowExtras` :8; `SpecConstants.ProhibitedSlugs` unchanged
(11 slugs, IIIF-04 ✓); `PresentationManifest` props unchanged from the 08-03 inventory (pipeline :54,
finishedPipelines :59, reingest :76, duration :91); `PresentationCollection` itemsOrder :30, totals :36, view :38;
`Collection.IsStorageCollection` :58; `DescendantCounts` = three child counts (IIIF-06 ✓). Other line numbers
in the cards drift by a few lines only.

**Read-only released-wire sweep (stage presentation API — `/version` reports 0.9.0, i.e. stage is one release
BEHIND the v0.10.0 tag):** hierarchical `GET /{c}` with auth+extras → **303** to `/{c}/collections/root`; without
auth → 200 vanilla IIIF (`@context,id,label,type`) — flat-vs-hierarchical and the extras gate both as documented.
Flat root emits `behavior, created, createdBy, flatId, id, label, modified, publicId, seeAlso, slug, totalItems,
totals {childStorageCollections, childIIIFCollections, childManifests}, type, view {@id,@type,page,pageSize,
totalPages}` — no `itemsOrder` key (null omitted), **no `service` (search) block** and `/collections/root/search`
→ 404 (v0.10 not deployed); `@context` is still the placeholder `http://tbc.org/iiif-repository/1/context.json`
(IIIF-11 ✓); `/configuration` → 404 (IIIF-03 ✓); `OPTIONS /manifests/{id}` → `Allow: DELETE, GET, POST, PUT`
(**no PATCH** — IIIF-02 ✓); missing manifest → 404 problem-details `{instance,status,title}`; `/manifests` list
→ 404 (no list route — matches code). **Consequence for the room:** IIIF-14's search/pipelines surface is
released (tag) but not wire-verifiable on stage today; the PO needs to say whether "released" means tagged or
deployed for the iiif.mdx port, and whether the port waits for a stage deploy of v0.10.0 (or for the #653/#654
hostname change, which will alter every example URL).

**PO rulings at pre-flight (2026-08-26):** (1) **"released" = TAGGED** — v0.10.0 is in scope for the port even
though stage runs 0.9.0; verify search/pipelines from the tagged code + tests (or any v0.10.0 deployment) and say
so on the card. (2) **The port does NOT wait for #653/#654** — document the new `iiif.*` hostname in all example
URLs now, even while wire checks run against the old `presentation-api.*` name; note the substitution where it
matters. Both recorded in README "Decisions made by the product owner".

**Session shape:** 26 cards — IIIF-01..14 (IIIF-12 status line says XC-07 cascade resolved AUTH-12; check
IIIF-02/12 against merged #641 rather than the card's "PR in flight" framing) + AUTH-01..12 (AUTH-12 ✅ by cascade;
11 to rule, all DESIGN). Mutating checks left for in-room: hierarchical PUT (develop-only), manifest create
with pipelines, search (needs v0.10 on stage). No hydra-model-dump involvement (protagonist unchanged).

---

## iiif-presentation: implemented today (verified)

Repo: `C:\git\dlcs\iiif-presentation`. Confirmed by code inspection:

- **Controllers / verbs** *(line refs updated 2026-08-03 to develop@ac3dcf45)*:
  - `ManifestController` (`src/IIIFPresentation/API/Features/Manifest/ManifestController.cs`,
    route `/{customerId:int}`): GET `/manifests/{id}` (:31), POST `/manifests` (:66),
    PUT `/manifests/{id}` (:83), DELETE `/manifests/{id}` (:99). **No PATCH.**
  - `CollectionController` (`src/IIIFPresentation/API/Features/Storage/CollectionController.cs`):
    GET `/collections/{id}` (:34, supports page/pageSize/orderBy), **GET
    `/collections/{id}/search` (:65 — NEW, #635: `[Authorize]` + `[RequireShowExtras]`,
    root-collection-only MVP, `?label=` terms + paging + ordering; see IIIF-14)**, POST
    `/collections` (:92), PUT `/collections/{id}` (:104), DELETE `/collections/{id}` (:146).
    **No PATCH.**
  - `StorageController` (`src/IIIFPresentation/API/Features/Storage/StorageController.cs:26`):
    GET `/{*slug}` (:36, hierarchical resolution), POST `/{*slug}` (:98).
- **Flat + hierarchical URLs both exist.** Hierarchical GET with auth + extras header returns
  303 redirect to flat form (StorageController.cs:52-56, 75-79).
- **`X-IIIF-CS-Show-Extras` header is real**, constant in
  `src/IIIFPresentation/API/Infrastructure/Http/CustomHttpHeaders.cs:8`; required value `"All"`
  (`HttpRequestX.cs:7`, `.HasShowExtraHeader()` :13).
- **Storage vs IIIF Collection distinction is real:** `Collection.IsStorageCollection`
  (`Models/Database/Collections/Collection.cs:58`), behavior string `"storage-collection"`
  (`Core/Infrastructure/Behavior.cs:7`), root must be a storage collection
  (`RootCollectionValidator.cs:21`).
- **Reserved slugs match the docs exactly** — `SpecConstants.ProhibitedSlugs`
  (`Models/API/General/SpecConstants.cs:7-21`): collections, manifests, paintedResources,
  canvases, annotations, adjuncts, pipelines, queue, assets, configuration, publish.
  Root id `"root"` (`KnownCollections.cs:8`).
- **Models match the doc shape closely** *(inventory updated 2026-08-03 — the model has GROWN)*:
  `PresentationManifest` (`Models/API/Manifest/PresentationManifest.cs`) has slug, publicId,
  parent, created/modified/By, flatId, `paintedResources` (:33), `space` (:35), `adjuncts`
  (:40), `ingesting` (:45), **`pipeline` (:54) and `finishedPipelines` (:59) — NEW, see
  IIIF-14**. `PaintedResource` also has a **`reingest`** bool (:76) not mentioned anywhere in
  this register. `CanvasPainting` API model with canvasId, canvasOriginalId, canvasOrder,
  choiceOrder, thumbnail, label, canvasLabel, target, staticWidth, staticHeight, plus
  `duration` (:91, was :84). `PresentationCollection` has totals (`DescendantCounts`), view,
  totalItems, `itemsOrder` (:30, was :23), `tags`.
- **NOT implemented:** PATCH on either controller; a `/configuration` endpoint /
  `IIIFConfiguration` resource (the slug is reserved but no endpoint exists); standalone
  `/canvases` or `/paintedResources` routes (both are nested in the manifest model only).
- **Async ingest:** manifest write ingests via the IIIF-CS queue and can return 202 while
  batches complete (RFC `docs/rfcs/0002-manifest-write-mvp.md`); ETag/optimistic concurrency
  uses the **`If-Match`** request header + `Manifest.etag` Guid, not an `ETag` request header.

## iiif-auth-v2: state today

Repo: `C:\git\dlcs\iiif-auth-v2`. Runtime implementation of IIIF Authorization Flow 2.0.
**No management REST API** — all configuration is direct SQL insert.

- **Entities** (`src/IIIFAuth2/IIIFAuth2.API/Data/Entities/`):
  - `RoleProvider` (`RoleProvider.cs:8`): Guid Id, `RoleProviderConfiguration` (JSONB),
    list of AccessServices.
  - `AccessService` (`AccessService.cs:8`): Guid Id, Customer, RoleProviderId?, Name (unique
    per customer), Profile ("active"/"kiosk"/"external"), and IIIF Auth 2.0 language-map fields:
    Label, Heading, Note, ConfirmLabel, LogoutLabel, AccessTokenErrorHeading, AccessTokenErrorNote.
  - `Role` (`Role.cs:6`): string Id (role URI) + Customer composite PK, AccessServiceId, Name.
  - `SessionUser`, `RoleProvisionToken`, `CustomerCookieDomain` (runtime/session state).
- **Role providers — only TWO implemented:** Clickthrough
  (`Infrastructure/Auth/RoleProvisioning/ClickThroughProviderHandler.cs:10`) and OIDC
  (`.../Oidc/OidcRoleProviderHandler.cs:12`, supporting Auth0 + Microsoft Entra). The
  **IP-address provider described in the docs does not exist.**
- **Config model:** `RoleProviderConfiguration` is a `Dictionary<string,IProviderConfiguration>`
  keyed by host ("default" fallback) (`Models/Domain/RoleProviderConfiguration.cs:11,19`),
  stored as JSONB. OIDC config: provider, domain, clientId/secret, scopes, claimType,
  unknownValueBehaviour, fallbackMapping, mapping (claim-value → role URIs).
- **Separate database** from protagonist; roles are passed in at runtime as query params
  (`?roles=...`) to probe/verifyaccess/services endpoints.
- **Runtime endpoints only** (no CRUD): ProbeController, AccessTokenController, AccessController
  (`/access/{customerId}/{accessServiceName}`, `/gesture`, `/oauth2/callback`, `/logout`),
  ServicesController, VerifyAccessController.
- **Setup today:** `scripts/sql/bootstrap.sql` inserts a role_provider, an access_service and
  a role row to create a clickthrough role. `readme.md` documents this manual process.

---

# Part 1 — IIIF Presentation cards

### IIIF-01 · Port iiif.mdx at all (and decide what gets samples)
- **⟳ Session-1 note (2026-08-10, ACC-16):** the phantom `iiif` link was removed from the customer.mdx example; building it for real is protagonist **issue #1245**, with the PO caveat that emission must be config-gated (some deployments omit iiif-presentation). When this page is ported, coordinate the customer-side link story with that issue; parked prose + provenance in scratch/api-doc/customer.md `## iiif`.
- **Theme:** IIIF & Auth
- **Surfaces:** `src/src/content/docs/api-doc/iiif.mdx` (does not exist; linked, 404s) · `scratch/api-doc/iiif.md` (~1,940 lines, full copy of old page) · old `C:\git\dlcs\docs\pages\api-doc\iiif.mdx` · code: `C:\git\dlcs\iiif-presentation` (whole repo)
- **Type:** STALE-SCRATCH
- **Docs say:** The entire IIIF Presentation feature is documented in scratch but published nowhere; multiple ported pages link to `../iiif` and 404.
- **Original-doc nuance:** Page header: _"IIIF Manifests and Collections 🆕"_ and _"This will need rewriting for public consumption, there's no need be 'historic'"_.
- **Code does:** Feature is substantially implemented (controllers, models, reserved slugs all present in `iiif-presentation`); the page can be written against real behaviour, not speculation. *(⟳ 2026-08-03: but NOT stable — the repo moves weekly. New shipped surface since these cards were written: search-across (RFC 0008), manifest pipelines/text-services incl. Content Search 2 on public manifests (RFC 0007, #633/#634), error-URI conventions (#638) — see IIIF-14. And the write path is being rebuilt in open PR #641. Scope the port accordingly; the write-semantics chapter should wait for #641.)*
- **Issues/RFCs:** `iiif-presentation/docs/rfcs/0002-0006` **+ 0007 (text-services), 0008 (search-across MVP), and pending 0020 (PR #228, containment vs membership)**; to check whether host is `iiif.dlc.services` in deployment config.
- **Decision needed:** Whether to port `iiif.mdx` in this sprint, and how to split the very long source (one mega-page vs several: storage collections, IIIF collections, manifests/paintedResources).
- **Options:** (a) Port as a single large page mirroring the old structure. (b) Split into 2–4 sibling pages under an "IIIF" section. (c) Defer until the divergence cards below are resolved.
- **Possible outputs:** doc / sample / RFC
- **Who's needed:** docs owner + iiif-presentation dev
- **Status:** ✅ RULED (session 6, 2026-08-26): option **(b) shape, (c) sequence** — the port produces **sibling pages under an IIIF sidebar group** (working split: `iiif.mdx` parent = concepts, two concerns, flat/hierarchical URIs, Show-Extras, reserved slugs, error conventions, write semantics incl. If-Match and "JSON is King", the HTTP-operations table; `iiif-collections.mdx` = storage vs IIIF collections, paging/totals, itemsOrder, containment marked as under RFC 0020; `iiif-manifests.mdx` = manifests, paintedResources/canvasPainting, adjuncts, ingesting/202, pipelines, search), written **after** IIIF-02..14 are ruled, by the PO-scheduled port job, against tagged v0.10.0 (released = tagged). **PO note: much is shared between manifests and collections** — everything common (URI forms, headers, auth, write/update semantics, error shapes, the operations table) lives ONCE on the parent page; child pages carry only resource-specific content and link up. Hierarchical PUT (#641) release-gated in scratch. Samples: one runnable set per page on `IIIF_CS_PRESENTATION_HOST` (new `p22_iiif*` dirs, sidebar 22–24); examples show `iiif.*`, verification on the old host. **PO note on the HTTP-operations table → new card IIIF-15.** Card premise correction: no live page links to `../iiif` any more (DIS-20 neutralised them) — the driver is an undocumented released product, not 404s.

### IIIF-02 · PATCH is documented but not implemented
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` §"HTTP Operations" table + §"Example: PATCHing a Storage Collection" · code: `ManifestController.cs` / `CollectionController.cs` (no PATCH action)
- **Type:** DOC-WRONG
- **Docs say:** The operations tables list `PATCH ... partial iiif:Collection ... 202` for both flat and hierarchical routes, with a worked PATCH example modifying a Collection `label`.
- **Original-doc nuance:** _"PATCH: Modify only some properties, e.g., `behavior` and/or `label` properties."_ and _"The PATCH operation returns the updated resource."_
- **Code does:** No PATCH verb on either controller — only GET/POST/PUT/DELETE (`ManifestController.cs:31-99`, `CollectionController.cs:34-146`). Updates are done via full PUT with `If-Match`. *(⟳ 2026-08-03: PR #641 adds hierarchical PUT but still no PATCH — PUT + If-Match is what the team is actively doubling down on; option (a) is effectively decided by the direction of travel.)*
- **Issues/RFCs:** issue #464 "Consistent API PUT and POST behaviour"; PR #503 (stale design record); **PR #641 (active, Jack — see scope note)**
- **Decision needed:** Document PUT-only updates now, or hold the PATCH prose for when/if PATCH lands.
- **Options:** (a) Port without PATCH; describe updates as PUT + If-Match. (b) Keep PATCH in scratch only. (c) File an issue to add PATCH and port the doc as "planned".
- **Possible outputs:** doc / code / RFC
- **Who's needed:** iiif-presentation dev
- **Status:** ✅ RULED (session 6, 2026-08-26): option **(a)** — the port documents updates as **full PUT with `If-Match`** and carries no PATCH. Port spec for the parent page: `If-Match` optional on create, checked on update (412 on mismatch — `UpsertErrorHelper.EtagNotRequired`/`EtagNonMatching`); **DELETE also honours `If-Match`** (`ManifestController.cs:102`, `HierarchyResourceDeleter.cs:26`) — new detail, folds into IIIF-07 and the IIIF-15 table. Wire-confirmed: `OPTIONS /manifests/{id}` → `Allow: DELETE, GET, POST, PUT`. PATCH material (table rows :191-192, HTML row :292, worked example :644-666, :848 verb list, :1007 configuration) stays in `scratch/api-doc/iiif.md` as design history — no issue filed; #641's direction (PUT + If-Match) is the team's chosen shape.

### IIIF-03 · `/configuration` endpoint + IIIFConfiguration resource not implemented
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` §"Configuration - default URLs for public URLs" · code: `SpecConstants.cs:19` (slug reserved), no controller/model found
- **Type:** STALE-SCRATCH
- **Docs say:** `GET/PATCH https://iiif.dlc.services/99/configuration` returns an `IIIFConfiguration` with `publicUriStructure`, `defaultStorageCollectionBehavior`, `publicStorageCollectionMaxItems`, `paintingAssetThumbnailSize`, `imageServices`.
- **Original-doc nuance:** _"The endpoint `.../99/configuration` returns the following resource, which you can patch to change behaviour"_ — and `imageServices` controls whether ImageService2/3 are emitted.
- **Code does:** `"configuration"` is a reserved/prohibited slug (`SpecConstants.cs:19`) but **no configuration endpoint, controller, or `IIIFConfiguration` model exists**. Several doc behaviours (`publicUriStructure`, `imageServices`) therefore have no runtime control surface.
- **Issues/RFCs:** to check
- **Decision needed:** Omit configuration from the ported page, or document as planned and keep design in scratch.
- **Options:** (a) Cut configuration prose from the port; keep in scratch. (b) Port as an explicitly "not yet implemented" callout. (c) RFC the configuration resource before porting.
- **Possible outputs:** doc / RFC / defer
- **Who's needed:** iiif-presentation dev + docs owner
- **Status:** ☐ undecided

### IIIF-04 · Reserved slugs — port verbatim (verified match)
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` §"Reserved names" · code: `SpecConstants.cs:7-21`
- **Type:** STALE-SCRATCH
- **Docs say:** Reserved slugs: collections, manifests, paintedResources, canvases, annotations, adjuncts, pipelines, queue, assets, configuration, publish.
- **Original-doc nuance:** _"Should we better avoid the risk of users wanting these slugs by naming them `_collections`, `_manifests` …?"_ (open question).
- **Code does:** `ProhibitedSlugs` lists exactly these 11 strings (`SpecConstants.cs:10-20`), case-insensitive, enforced in `PresentationValidator.cs`. The doc list is accurate.
- **Issues/RFCs:** —
- **Decision needed:** Confirm we port the list as-is and drop the `_`-prefix open question (code shows it was not adopted).
- **Options:** (a) Port verbatim, remove the open question. (b) Port and keep the question as a footnote.
- **Possible outputs:** doc
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### IIIF-05 · Manifest `assets` and `queue` link properties absent from the model
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` §"Assets property" / §"Queue property" / §"Assets and Spaces" · code: `Models/API/Manifest/PresentationManifest.cs:13-52`
- **Type:** CODE-MISSING
- **Docs say:** The API Manifest exposes `assets` (a Hydra Collection alias for the manifest's on-demand Space) and `queue` (POST assets for async ingest), plus a `space` property; assets can be POSTed to `.../manifests/{id}/queue` and `.../assets`.
- **Original-doc nuance:** _"`assets`: 'https://iiif.dlc.services/99/manifests/t454knmf/assets'"_ and _"this `assets` property works exactly like space.images because it is in fact an alias for a Space"_; the on-demand space created via the `Link: <…#Space>; rel="DCTERMS.requires"` header.
- **Code does:** `PresentationManifest` exposes `space` (string, :35) but the inventory found **no `assets` or `queue` link properties**, and there is no `/manifests/{id}/queue` or `/manifests/{id}/assets` route. Ingest happens through `paintedResources` + batches (`Manifest.batches`, RFC 0002). *(⟳ 2026-08-03: the on-demand-Space part of the old prose IS implemented — the `Link: <https://dlcs.io/vocab#Space>;rel="DCTERMS.requires"` request header (`API/Infrastructure/Helpers/HttpRequestX.cs:8,22`, wired into manifest POST/PUT via `Request.HasCreateSpaceHeader()`) creates the space on demand. Only the `assets`/`queue` aliases are missing — the card previously implied the whole section was unimplemented.)*
- **Issues/RFCs:** `iiif-presentation/docs/rfcs/0002-manifest-write-mvp.md`
- **Decision needed:** Does the manifest expose `assets`/`queue` today (re-verify), and if not, port without them?
- **Options:** (a) Port only `space` + `paintedResources`; drop `assets`/`queue` prose to scratch. (b) Confirm with dev whether these links exist and document accordingly. (c) RFC the queue/assets aliases.
- **Possible outputs:** doc / code / RFC
- **Who's needed:** iiif-presentation dev
- **Status:** ☐ undecided

### IIIF-06 · Collection `totals` — descendant counts missing in code
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` §"Paging" (totals block) · code: `Models/API/Collection/DescendantCounts.cs:6`, `PresentationCollection.cs:39`
- **Type:** DOC-WRONG
- **Docs say:** `totals` has six fields: `childStorageCollections`, `childIIIFCollections`, `childManifests`, `descendantStorageCollections`, `descendantIIIFCollections`, `descendantManifests`.
- **Original-doc nuance:** worked example shows `"descendantManifests": 3412` etc.
- **Code does:** `DescendantCounts` record exposes only the three **child** counts (ChildStorageCollections, ChildIIIFCollections, ChildManifests); no `descendant*` fields found.
- **Issues/RFCs:** to check
- **Decision needed:** Port with child-only totals, or treat descendant counts as planned.
- **Options:** (a) Document only the three child counts. (b) Keep descendant counts as "planned" callout. (c) File issue to add descendant counts.
- **Possible outputs:** doc / code
- **Who's needed:** iiif-presentation dev
- **Status:** ☐ undecided

### IIIF-07 · ETag vs `If-Match` for optimistic updates
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` §"Example: PATCHing a Storage Collection" (ETag header) · code: `ManifestController.cs:83` (If-Match), `Manifest.etag` Guid (`Models/Database/Collections/Manifest.cs:56`), RFC 0004
- **Type:** DOC-WRONG
- **Docs say:** Updates must carry an `ETag` request header acquired on a previous GET (`ETag: "33a64df…"`).
- **Original-doc nuance:** _"As this an update of an existing resource, it must be accompanied by an ETag acquired on a previous GET. If the ETag doesn't match the latest GET the request will be rejected."_
- **Code does:** PUT upsert requires the **`If-Match`** request header when the resource exists (`ManifestController.cs:83` comment), with a `Guid etag`. The semantics match but the header name differs (`ETag` is a response header; `If-Match` is the conditional request header).
- **Issues/RFCs:** `iiif-presentation/docs/rfcs/0004-etag-changes.md`
- **Decision needed:** Standardise the ported prose on `If-Match` (and `ETag` for the response).
- **Options:** (a) Rewrite examples to use `If-Match`. (b) Keep `ETag` and add a note. 
- **Possible outputs:** doc
- **Who's needed:** iiif-presentation dev
- **Status:** ☐ undecided

### IIIF-08 · `ingesting` object shape differs
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` (manifest examples: `"ingesting": { "finished": 1, "total": 1 }`) · code: `Models/API/Manifest/PresentationManifest.cs:89` (`IngestingAssets`)
- **Type:** DOC-WRONG
- **Docs say:** `ingesting` is `{ finished, total }` (and elsewhere `null` when idle).
- **Original-doc nuance:** _"`ingesting` is now `false` on the individual asset, and the `ingesting` property of the Manifest shows all completed."_
- **Code does:** `IngestingAssets` has **`total`, `finished`, `errors`** (:91-93) — the doc omits `errors`.
- **Issues/RFCs:** —
- **Decision needed:** Add `errors` to documented `ingesting` examples.
- **Options:** (a) Update examples to include `errors`. (b) Document `errors` only in the field table.
- **Possible outputs:** doc
- **Who's needed:** iiif-presentation dev
- **Status:** ☐ undecided

### IIIF-09 · canvasPainting `duration` field undocumented
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` §"canvasPainting" field table · code: `PresentationManifest.cs:84` (`duration`)
- **Type:** DOC-MISSING
- **Docs say:** The `canvasPainting` field table lists canvasId … staticWidth/staticHeight but not `duration`.
- **Original-doc nuance:** `staticWidth`/`staticHeight` described "For images"; nothing for time-based media duration.
- **Code does:** API `CanvasPainting` has `double? duration` (:84) — needed for AV assets (the doc promises AV support but the table predates it).
- **Issues/RFCs:** —
- **Decision needed:** Add `duration` to the canvasPainting field table when porting.
- **Options:** (a) Add `duration` row. (b) Defer until AV examples are written.
- **Possible outputs:** doc
- **Who's needed:** iiif-presentation dev
- **Status:** ☐ undecided

### IIIF-10 · Item ordering in storage collections — now implemented (`itemsOrder`)
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` ("The default ordering … is by their `slug` value" + open question about future ordering) · code: `PresentationCollection.cs:23` (`itemsOrder`)
- **Type:** STALE-SCRATCH
- **Docs say:** Ordering of items in a storage collection is by slug; explicit ordering is flagged as a future feature.
- **Original-doc nuance:** _"Later we will look at ways of ordering items in Storage Collections. This is analogous to ordering directory listings in a file system…"_
- **Code does:** `PresentationCollection.itemsOrder` (int?, :30 as of 2026-08-03) exists — the "later" feature appears to have landed. *(⟳ 2026-08-03: the ordering story is now bigger than `itemsOrder` — collection GET and the new search endpoint also accept `orderBy`/`orderByDescending` query params (commit 20dae303). Document both when porting.)*
- **Issues/RFCs:** to check (collection ordering RFC)
- **Decision needed:** Document `itemsOrder` as a shipped feature rather than a future one.
- **Options:** (a) Port with `itemsOrder` documented. (b) Verify semantics with dev first.
- **Possible outputs:** doc
- **Who's needed:** iiif-presentation dev
- **Status:** ☐ undecided

### IIIF-11 · Placeholder JSON-LD `@context` URL
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` §"JSON-LD @context" (and every extended example) · code: to check (context serialization in `iiif-presentation`)
- **Type:** DOC-WRONG
- **Docs say:** Extended resources carry `"http://tbc.org/iiif-repository/1/context.json"` alongside the IIIF presentation 3 context.
- **Original-doc nuance:** literal `tbc.org` ("to be confirmed") placeholder host appears throughout the examples.
- **Code does (⟳ answered 2026-08-03, unhappily):** the code emits the placeholder **itself** — `Core/IIIF/PresentationJsonLdContext.cs:8` hard-codes `public static readonly string Context = "http://tbc.org/iiif-repository/1/context.json"`, applied in `ManifestConverter.cs:98` and `CollectionConverter.GenerateContext()`. Doc and code agree on a URL that must not ship. This is now a **CODE+DOC** issue — a real context must be minted and published before the port; option (a) "find the real URL in code" is dead.
- **Issues/RFCs:** to check
- **Decision needed:** Mint and publish the canonical extras `@context` (code change + hosted document), then port.
- **Options:** (b) Hold extended-form examples until the context is published. (c) Mint/publish the context as part of the port (code + doc + possibly RFC).
- **Possible outputs:** doc / code / RFC
- **Who's needed:** iiif-presentation dev
- **Status:** ☐ undecided

### IIIF-12 · "JSON is King" update semantics — verify against implementation
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/iiif.md` §'"JSON is King" - handling complex update scenarios' · code: `iiif-presentation/docs/rfcs/0005-mixed-manifests.md`, `docs/notes/canvas-paintings.md`
- **Type:** DESIGN
- **Docs say:** When both `items` and `paintedResources` are supplied, JSON wins; additive `paintedResources` are merged, conflicting ones are a 400; reorder/delete must go through `items` with empty `paintedResources`.
- **Original-doc nuance:** _"a round trip of requesting a Flat/API Manifest and then saving it back without changes would be a no-op"_ and _"Getting this right will be hard!"_ (author's own flag).
- **Code does:** RFC 0005 ("mixed manifests") and the canvas-paintings notes describe the reconciliation; `Services/Manifests/ManifestMerger.cs` is still present, so the walkthrough plan stands. *(⟳ 2026-08-03: but the write path is being rebuilt RIGHT NOW — merged #639 refactored handler results (`PresentationResult`), and open #641 rewrites create/upsert dispatch with type-sniffing and vanilla-IIIF bodies. Do the RFC-0005-vs-code walkthrough against **#641's branch**, not current develop, or it will be immediately stale. PR #228's `items`-editing proposal is explicitly another JSON-is-King property.)*
- **Issues/RFCs:** `iiif-presentation/docs/rfcs/0005-mixed-manifests.md` · PR #641 (Jack) · PR #228/RFC 0020
- **Decision needed:** Confirm the conflict/merge rules as implemented, then port (this is the highest-risk prose to get wrong).
- **Options:** (a) Port after a dev walkthrough of RFC 0005 vs **#641's branch** (Jack in the room). (b) Port a reduced version (additive-only) and defer the complex cases. (c) Defer the section.
- **Possible outputs:** doc / RFC
- **Who's needed:** iiif-presentation dev + docs owner
- **Status:** ☐ undecided

### IIIF-13 · Python samples for the IIIF page (different host + auth)
- **Theme:** IIIF & Auth
- **Surfaces:** `dlcs-docs-client/` conventions (`CLAUDE.md`) · code: `iiif-presentation` runs on `iiif.dlc.services`, not `api.dlc.services`
- **Type:** DESIGN
- **Docs say:** Convention: each ported page gets Python samples under `dlcs-docs-client/p{N}_{page}/` using `iiif_cs.py` helpers against `IIIF_CS_API_HOST` (the `api.` host).
- **Original-doc nuance:** — (CLAUDE.md conventions)
- **Code does:** IIIF Presentation CRUD targets the `iiif.` host with the same Bearer/Basic auth; the helper module derives the public host by stripping `api.`. Samples will need a new base host and likely the `X-IIIF-CS-Show-Extras` header baked into a helper.
- **Issues/RFCs:** —
- **Decision needed:** How to extend the sample client to address the `iiif.` host and the extras header.
- **Options:** (a) Add an `iiif_host` setting + a `get/post/put_iiif_resource` helper. (b) Parameterise existing helpers with a base-URL argument. (c) Defer samples until the page lands.
- **Possible outputs:** sample
- **Who's needed:** docs owner
- **Status:** ☐ undecided

### IIIF-14 · New API surface shipped since 2026-06-25 — the future iiif.mdx must cover it *(added 2026-08-03 verification pass)*
- **Theme:** IIIF & Auth
- **Surfaces:** iiif-presentation develop@ac3dcf45 · no docs anywhere (old or new site)
- **Type:** DOC-MISSING (net-new features, no old prose exists to port)
- **Code does:**
  1. **Search-across** (#635, RFC 0008): `GET /{customerId}/collections/root/search?label={terms}&page&pageSize&orderBy|orderByDescending` — auth + Show-Extras, root-storage-collection-only MVP (404 elsewhere), min-length validation → 400 `InvalidSearchQuery`. Returns a *synthetic* `PresentationCollection` (`CollectionConverter.ToSearchCollection`: id = search URL, generated label, `seeAlso` back-link, items/totalItems/paging; no slug/parent/etag). The root flat collection now advertises `service: [{ "IIIFCS-Search" / "level0" }]`.
  2. **Pipelines on the Manifest** (RFC 0007 + #633, implements issue #620): authenticated manifest GET now carries `pipeline` and `finishedPipelines` (`List<PipelineItem>`: `{ name, config: { action }, status, error, warning, created, finished }`). Only recognised pipeline: `name: "text"`, `config.action: "Index"`; unknown pipelines silently stripped on write (`PipelineHelper.RemoveInvalidPipelines`). Public manifests with text get an **IIIF Content Search 2** service injected (`TextManifestAugmentor`). This is the first shipped piece of the pipelines theme (cross-ref PRO-09 — the reserved `pipelines` slug still has no endpoint, but pipelines-as-manifest-property is live).
  3. **deleteTextServices** (#634): behaviour only — deleting a manifest also removes its text-pipeline artefacts.
  4. **Error conventions** (#638): problem-details `instance` = request URL without query params; error `type` = generated URI `{host}/errors/{EnumType}/{value}`.
- **Decision needed:** Scope the iiif.mdx port to include these (search, pipelines, errors get sections; deleteTextServices a sentence) — they have no old-doc prose, so this is net-new writing with samples (extends IIIF-13's sample scope: search endpoint, pipeline polling, create-space Link header).
- **Possible outputs:** doc / sample
- **Who's needed:** docs owner + iiif-presentation dev
- **Status:** ☐ undecided

### IIIF-15 · The IIIF HTTP-operations table must be re-designed for Starlight *(minted 2026-08-26, session 6, PO note on IIIF-01)*
- **Theme:** IIIF & Auth
- **Surfaces:** old `iiif.mdx:179-194` (markdown table with `Method<br/>Headers` cells: 14 rows × GET/POST/PUT/PATCH/DELETE × hierarchical/flat × header combinations) and `iiif.mdx:201-…` (a second, HTML `<table>` rendering of the same matrix); also the mini request/response table at `:615-618`. Both are carried verbatim in `scratch/api-doc/iiif.md`.
- **Type:** STYLE (+ DOC-WRONG content: the PATCH rows and 202 codes — see IIIF-02, IIIF-12)
- **Docs say:** Two versions of the same operations matrix, one markdown-with-`<br/>` and one raw HTML; neither renders legibly in the Starlight template (the `<br/>` cells wrap badly, the HTML table ignores the site's table styling), and they have drifted from each other.
- **Code does:** the real matrix on v0.10.0 is smaller and cleaner than either table: hierarchical GET (public → IIIF; auth+extras → 303 to flat), flat GET (auth+extras → API view), POST hierarchical + flat, PUT flat (+If-Match), DELETE flat; no PATCH; search GET on the root collection. (#641 adds hierarchical PUT on develop.)
- **Decision needed:** one authoritative, easy-to-read operations table for the parent IIIF page, in a form that renders well in Starlight — plain markdown with one row per (verb, URL form) and the header requirements in their own column, or a small HTML table only if markdown genuinely cannot express it. Never two copies.
- **Options:** (a) single markdown table, one row per verb × URL form, columns: Method · URL form · Required headers · Expects · Returns · Status; per-resource differences (collection vs manifest bodies) as footnotes (b) a Starlight `<Tabs>` component with one tab per URL form (c) keep HTML
- **Possible outputs:** doc
- **Who's needed:** docs owner (PO)
- **Status:** ☐ undecided — to be designed when the parent page is written (IIIF-01 sequence); content rows come from IIIF-02/07/12/14 rulings

---

# Part 2 — Auth cards (roles / auth-service / access-control)

> **⟳ Verified 2026-08-03:** iiif-auth-v2 HEAD is 494e373 (2026-03-31) — the repo has not
> moved since these cards were written. All 12 AUTH cards re-verified and stand unchanged:
> entities as listed, only Clickthrough + OIDC provider handlers (no IP provider — AUTH-03
> holds), `bootstrap.sql` manual setup (AUTH-01 holds), runtime-only controllers. AUTH-12
> (`customer.authServices` link in protagonist) remains open as stated — cross-ref ACC-02.

### AUTH-01 · No management REST API exists — the core design gap
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/access-control.md` ("Write the full auth docs as a PR … this will have to come later") · old `access-control.mdx` (stub, "still under development") · code: `iiif-auth-v2` (runtime endpoints only; `scripts/sql/bootstrap.sql`)
- **Type:** DESIGN
- **Docs say:** Access control is configured around Roles, AuthServices and RoleProviders, but the page is a stub; there is no documented way to create them via API.
- **Original-doc nuance:** scratch: _"this will have to come later though"_; old page Callout: _"These features are still under development."_
- **Code does:** `iiif-auth-v2` has **no CRUD endpoints** — only runtime probe/token/access/services/verifyaccess controllers. Configuration is manual SQL (`scripts/sql/bootstrap.sql`, `readme.md`).
- **Issues/RFCs:** protagonist #538 "Manage Auth Services via API"; iiif-auth-v2 #46 "auto create clickthrough role"; RFCs 005, 008, 012.
- **Decision needed:** Whether to design the management REST API now (RFC) before any auth pages can be ported with working samples.
- **Options:** (a) Write an RFC for the full auth management API and block doc porting on it. (b) Document the current SQL-bootstrap reality as an interim "advanced setup" page. (c) Defer the whole cluster.
- **Possible outputs:** RFC / doc / defer
- **Who's needed:** platform architect + auth dev + docs owner
- **Status:** ☐ undecided

### AUTH-02 · Naming: `AuthService` (docs) vs `AccessService` (code)
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/access-control.md` ("Should we introduce a new API class, vocab:AccessService? Or stick with AuthService?") · `customer.mdx` (`authServices`) · code: `Data/Entities/AccessService.cs:8`
- **Type:** DESIGN
- **Docs say:** Docs use `AuthService` (Customer has `authServices`, "A Role has an AuthService", "An AuthService has a RoleProvider"); scratch explicitly asks whether to switch to `vocab:AccessService`.
- **Original-doc nuance:** scratch: _"Should we introduce a new API class, vocab:AccessService? Or stick with AuthService?"_
- **Code does:** The implementation already names the entity **`AccessService`** (`AccessService.cs:8`), with IIIF Auth 2.0 profile/label/heading/note/confirmLabel/logoutLabel fields — i.e. the code has effectively chosen `AccessService`.
- **Issues/RFCs:** RFC 012-auth-service.md
- **Decision needed:** Align the public vocabulary on `AccessService` (matching code + IIIF Auth 2.0) or keep `AuthService` for continuity, and reconcile `customer.authServices`.
- **Options:** (a) Adopt `AccessService` everywhere; update `customer.mdx`. (b) Keep `AuthService` as the API term, map to AccessService internally. (c) RFC the vocabulary.
- **Possible outputs:** doc / code / RFC
- **Who's needed:** platform architect + docs owner
- **Status:** ☐ undecided

### AUTH-03 · IP-address Role Provider documented but not implemented
- **Theme:** IIIF & Auth
- **Surfaces:** old `access-control.mdx` §"The IP-address Role Provider" + "three Role Providers" · `scratch/api-doc/access-control.md` (IP / appointments) · code: `Infrastructure/Auth/RoleProvisioning/` (only ClickThrough + Oidc handlers)
- **Type:** DOC-WRONG
- **Docs say:** _"There are three Role Providers included with the platform at present"_ — OIDC, Clickthrough, and IP-address.
- **Original-doc nuance:** §"The IP-address Role Provider" exists as a heading with no body; scratch points at external `dynamic-roles.md` / `appointments-app.md` for background.
- **Code does:** Only **two** providers exist — `ClickThroughProviderHandler.cs:10` and `OidcRoleProviderHandler.cs:12` (Auth0/Entra). **No IP-address provider.**
- **Issues/RFCs:** uol-dlip `dynamic-roles.md`, `appointments-app.md` (external design)
- **Decision needed:** Drop IP-address from "providers available today" (document only Clickthrough + OIDC) and move IP-address to a future/roadmap note.
- **Options:** (a) Document two providers; IP-address as "planned". (b) Keep three with a "not yet implemented" callout on IP-address. (c) RFC the IP-address provider.
- **Possible outputs:** doc / RFC
- **Who's needed:** auth dev + docs owner
- **Status:** ☐ undecided

### AUTH-04 · Design: AccessService management CRUD
- **Theme:** IIIF & Auth
- **Surfaces:** future `auth-service.mdx` (not ported) · RFC 012 · code: `Data/Entities/AccessService.cs:8`, migration `20230718101853_simplify access_service`
- **Type:** DESIGN
- **Docs say:** Nothing yet — `auth-service.mdx` doesn't exist; the AccessService concept is only described indirectly via the role chain.
- **Original-doc nuance:** old chain: _"A Customer has authServices … A Role has an AuthService … An AuthService has a RoleProvider."_
- **Code does:** `AccessService` fields: Customer, RoleProviderId?, Name (unique per customer), Profile (active/kiosk/external), Label/Heading/Note/ConfirmLabel/LogoutLabel/AccessTokenErrorHeading/AccessTokenErrorNote (all LanguageMaps). The parent/child hierarchy was removed in migration `20230718101853`.
- **Issues/RFCs:** protagonist #538; RFC 012
- **Decision needed:** Shape of CRUD for access services (route, identifier, which fields are writable, how `Profile` is validated).
- **Options:** (a) `/customers/{c}/accessServices/{id}` REST resource keyed by Guid. (b) Key by `Name` (already unique per customer). (c) Nest under role provider. 
- **Possible outputs:** RFC / doc / sample
- **Who's needed:** auth dev + platform architect
- **Status:** ☐ undecided

### AUTH-05 · Design: RoleProvider management + host-keyed JSONB config
- **Theme:** IIIF & Auth
- **Surfaces:** future `auth-service.mdx`/`access-control.mdx` · code: `Data/Entities/RoleProvider.cs:8`, `Models/Domain/RoleProviderConfiguration.cs:11,19`, `scripts/sql/bootstrap.sql`
- **Type:** DESIGN
- **Docs say:** Role providers are described conceptually (OIDC/Clickthrough) but there is no documented config schema or management surface.
- **Original-doc nuance:** old OIDC section: _"use configuration to define endpoints, and mappings between OIDC claims and the role URIs"_ — exactly the JSONB config in code, undocumented in detail.
- **Code does:** `RoleProvider` = Guid + `RoleProviderConfiguration` (JSONB), a `Dictionary<host,IProviderConfiguration>` with a "default" fallback (`RoleProviderConfiguration.cs:11,19`). One provider feeds many access services.
- **Issues/RFCs:** protagonist #538; RFC 008-more-access-control-oidc-oauth.md
- **Decision needed:** How to expose a per-host JSON config object through REST (and how to handle the `clientSecret` / `secretsmanager:` indirection safely).
- **Options:** (a) PUT the whole JSONB config object per role provider. (b) Structured sub-resources per host. (c) Defer; document SQL bootstrap as interim.
- **Possible outputs:** RFC / doc
- **Who's needed:** auth dev + platform architect
- **Status:** ☐ undecided

### AUTH-06 · Design: Role management + auto-create clickthrough role
- **Theme:** IIIF & Auth
- **Surfaces:** `asset.mdx` §roles (roles on assets) · future `roles.mdx` (not ported) · code: `Data/Entities/Role.cs:6`, `scripts/sql/bootstrap.sql`
- **Type:** DESIGN
- **Docs say:** Assets carry opaque role URIs; "A Role has an AuthService". No way to create a Role via API is documented.
- **Original-doc nuance:** access-control: _"Assets can have roles. These are usually opaque URIs … An asset might have many roles; if the user has any of them, they can see the asset."_
- **Code does:** `Role` = (Id role-URI + Customer) composite PK, `AccessServiceId`, `Name`. Created today only via SQL insert. Issue #46 asks for **auto-creation of the clickthrough role**.
- **Issues/RFCs:** iiif-auth-v2 #46 "auto create clickthrough role"; protagonist #538
- **Decision needed:** REST shape for roles, the role-URI minting convention, and whether common roles (clickthrough) are auto-provisioned.
- **Options:** (a) `/customers/{c}/roles/{role}` CRUD with server-minted URIs. (b) Auto-create well-known roles (clickthrough) on customer setup (#46), explicit CRUD for the rest. (c) Defer.
- **Possible outputs:** RFC / code / doc
- **Who's needed:** auth dev + platform architect
- **Status:** ☐ undecided

### AUTH-07 · Undocumented entity: CustomerCookieDomain
- **Theme:** IIIF & Auth
- **Surfaces:** (no doc) · code: `Data/Entities/CustomerCookieDomain.cs:7`, migration `20230920144949_add customerCookieDomains`
- **Type:** DOC-MISSING
- **Docs say:** Nothing — this entity is absent from all docs.
- **Original-doc nuance:** —
- **Code does:** `CustomerCookieDomain` (Customer PK + `List<string> Domains`) controls which additional domains receive auth cookies — operationally important for multi-domain deployments, and a likely management-API resource.
- **Issues/RFCs:** —
- **Decision needed:** Whether cookie-domain configuration is in scope for the auth docs / management API.
- **Options:** (a) Include in the management API + docs. (b) Treat as deployment config, document separately. (c) Defer.
- **Possible outputs:** RFC / doc / defer
- **Who's needed:** auth dev
- **Status:** ☐ undecided

### AUTH-08 · Where does the auth management API live — protagonist vs iiif-auth-v2?
- **Theme:** IIIF & Auth
- **Surfaces:** `customer.mdx` (`authServices` under `api.dlc.services`) · code: `iiif-auth-v2` (separate service + separate DB) · protagonist #538
- **Type:** DESIGN
- **Docs say:** The customer entity (on `api.dlc.services`) links `authServices`, implying auth management belongs to the main protagonist API.
- **Original-doc nuance:** old chain places `authServices` on the Customer resource, i.e. in the protagonist API surface.
- **Code does:** Auth config lives in **`iiif-auth-v2`**, a standalone service with its **own database**, decoupled from protagonist; roles flow in at runtime via `?roles=` query params. Issue #538 is filed in **protagonist**.
- **Issues/RFCs:** protagonist #538
- **Decision needed:** Should the management API be served by protagonist (`api.dlc.services/customers/{c}/...`) proxying iiif-auth-v2, or directly by iiif-auth-v2? This determines URLs in every auth page + sample.
- **Options:** (a) Protagonist owns the management API and writes to the auth DB. (b) iiif-auth-v2 exposes its own admin API; protagonist links to it. (c) Shared/federated. 
- **Possible outputs:** RFC
- **Who's needed:** platform architect + auth dev
- **Status:** ☐ undecided

### AUTH-09 · OIDC provider configuration is rich but undocumented
- **Theme:** IIIF & Auth
- **Surfaces:** old `access-control.mdx` §"The OIDC Role Provider" (prose only) · code: `Models/Domain/RoleProviderConfiguration.cs:72-109`, `Oidc/OidcRoleProviderHandler.cs`
- **Type:** DOC-MISSING
- **Docs say:** OIDC bridges the platform to your user store via OAuth2/OIDC with claim→role mappings, but no concrete config fields are listed.
- **Original-doc nuance:** _"use configuration to define endpoints, and mappings between OIDC claims and the role URIs … greatly simplified with commercial services like Auth0."_
- **Code does:** OIDC config supports `provider` (auth0 | entra), domain, clientId/clientSecret (with `secretsmanager:` indirection, `OidcRoleProviderHandler.cs:96`), scopes, claimType, unknownValueBehaviour, fallbackMapping, and a claim-value→role-URIs `mapping` dictionary.
- **Issues/RFCs:** RFC 008
- **Decision needed:** Document the OIDC config schema (and Auth0/Entra specifics) as part of the auth-service page once the management API shape is set.
- **Options:** (a) Document the full config schema now (even if SQL-only). (b) Wait for the management API design. (c) Provide an Auth0 worked example.
- **Possible outputs:** doc / RFC
- **Who's needed:** auth dev + docs owner
- **Status:** ☐ undecided

### AUTH-10 · Appointments-based / dynamic roles — future design
- **Theme:** IIIF & Auth
- **Surfaces:** `scratch/api-doc/access-control.md` §"Appointments-based roles" + §"The IP-address Role Provider" (external file refs) · code: none in iiif-auth-v2
- **Type:** DESIGN
- **Docs say:** Scratch references appointments-based and dynamic roles, pointing at `C:\git\uol-dlip\design\access-control\RFCs\dynamic-roles.md` and `appointments-app.md`.
- **Original-doc nuance:** scratch headings _"## The IP-address Role Provider"_ and _"## Appointments-based roles…"_ with only external-file pointers.
- **Code does:** No appointments/dynamic-role implementation in `iiif-auth-v2` (no IP provider, no appointments entity).
- **Issues/RFCs:** uol-dlip `dynamic-roles.md`, `appointments-app.md`
- **Decision needed:** Keep appointments/dynamic roles entirely out of the ported docs (roadmap only) for now.
- **Options:** (a) Defer; leave in scratch. (b) Add a brief roadmap mention. (c) RFC if uol-dlip work is firm.
- **Possible outputs:** defer / RFC
- **Who's needed:** platform architect
- **Status:** ☐ undecided

### AUTH-11 · Synthesise the three access-control RFCs into the ported page
- **Theme:** IIIF & Auth
- **Surfaces:** old `access-control.mdx` (lists RFCs to synthesise) · `scratch/api-doc/access-control.md` (same) · protagonist RFCs 005, 008, 012
- **Type:** STALE-SCRATCH
- **Docs say:** The page is a placeholder that says it must synthesise RFC 005 (Access Control), 008 (more access control OIDC/OAuth), and 012 (auth-service).
- **Original-doc nuance:** _"Need to synthesise … 005-Access-Control.md … 008-more-access-control-oidc-oauth.md … 012-auth-service.md."_
- **Code does:** The implemented model (`AccessService`, two providers, JSONB config) is the concrete result of those RFCs — the page can be written from code + RFCs rather than from scratch speculation.
- **Issues/RFCs:** protagonist RFCs 005, 008, 012
- **Decision needed:** Whether to write the conceptual access-control page now (concepts are stable) even while the management API (AUTH-01) is undesigned.
- **Options:** (a) Port the conceptual page now (sessions, roles, providers) with no management examples. (b) Hold until the management API exists. (c) Split: concepts now, management later.
- **Possible outputs:** doc
- **Who's needed:** auth dev + docs owner
- **Status:** ☐ undecided

### AUTH-12 · `customer.authServices` link — verify and reconcile
- **Theme:** IIIF & Auth
- **Surfaces:** `customer.mdx` (`authServices` property) · access-control chain · code: `AccessService.Customer` field, no protagonist `authServices` endpoint confirmed
- **Type:** DOC-WRONG
- **Docs say:** The Customer resource exposes an `authServices` collection link (per the role chain "A Customer has authServices").
- **Original-doc nuance:** access-control: _"A Customer has authServices"_, linking `customer#authservices`.
- **Code does:** `AccessService` rows are scoped by `Customer` in the **iiif-auth-v2** DB; whether the protagonist Customer resource actually serves an `authServices` link/collection today is unconfirmed (likely not, given no management API). Needs verification against the protagonist Customer model.
- **Issues/RFCs:** protagonist #538
- **Decision needed:** Confirm whether `customer.authServices` resolves today; if not, mark it planned in `customer.mdx`.
- **Options:** (a) Verify in protagonist; if absent, annotate as not-yet-implemented. (b) Leave until the management API lands. 
- **Possible outputs:** doc / code
- **Who's needed:** protagonist dev + docs owner
- **Status:** ✅ RESOLVED by XC-07 cascade (session 0, 2026-08-06): `customer.authServices` (with `roleProviders` and `roles`) never resolved — no route exists — and the links are removed from the Customer model in protagonist PR #1237. customer.mdx never showed them. The links return when the auth management API exists (AUTH-01/AUTH-08)
