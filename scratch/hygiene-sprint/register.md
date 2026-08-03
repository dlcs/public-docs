# Hygiene sprint — master decision register

> **Status: DRAFT.** Theme files hold one decision card per item; this file is the index +
> triage table that ties them together. See `README.md` for the plan and the decision
> taxonomy. Prepared 2026-06-25.
>
> **⟳ Refreshed 2026-08-03** against protagonist `main` (v1.13.2) and `develop` + open PRs.
> Biggest change: the adjunct-queue API that queues.mdx/batch.mdx describe has largely been
> **built** (PR #1228, develop-only, unreleased) — **PRO-08** flipped from "docs overstate the
> implementation" to "docs now nearly right, pending release; residual gaps in the card".
> Adjunct size/storage accounting was reworked (PR #1220, on main; new internal `Optimised`
> flag) — inline updates on **ACC-06** and **ADJ-13**; session-5 has a dated development-update
> section. Issues #1157/#1158/#1160/#1218 closed. One open PR: #1230 proposes RFC 024
> (Text-Services PDF generation — bears on DIS-07/PRO-09 territory). `_issues-rfcs.md` updated.
>
> **⟳ Full independent verification pass, 2026-08-03 (second refresh).** Seven parallel
> fresh-eyes audits re-verified every card's claims against protagonist develop@8341d780,
> iiif-presentation develop@ac3dcf45, iiif-auth-v2@494e373, the old Nextra docs and the
> samples. Outcome: **no card was wrong in direction**; ~105 confirmed exactly as written,
> the rest corrected inline (marked ⟳). One register self-error found and fixed — session 1's
> Resolved list had trusted an annotation (custom-header PUT actually returns **201** on
> update → new ACC-15). **21 new cards added** from misses: XC-11..13, ACC-15..19, SPA-18..21,
> PRO-11..13, ADJ-17..18, DIS-22..24, IIIF-14. `_provenance-nuance.md` revised: the "14/19
> clean" claim did not survive — now ~18 lost-nuance items (PROV-11..18) plus a new
> "silent normative changes" category. Strategic: **Jack is already standardising PUT/POST in
> iiif-presentation PR #641** — hand the XC-02/XC-03 rulings to that in-flight work (see
> session-0 preamble and session-6 scope note); and the **main = released behaviour** policy
> (PO decision, README) makes the published adjunct-queue sections ahead-of-policy until
> protagonist releases.

## Headline findings (read me first)

A one-screen orientation for the room. Full detail + file:line citations live in the cards.

- **Cross-cutting is the unlock.** The single most useful discovery: in protagonist, HTTP
  status is decided by the *request handler's* `WriteResult`/`DeleteResult`, **not the
  controller** — so `[ProducesResponseType]` annotations actively lie (e.g. DeliveryChannelPolicy
  DELETE is annotated `202` but returns `204`). Session 0's ten rulings (DELETE→204, POST→201,
  error-body shape, **no trailing-space property names**, identifier policy, table-flag trust,
  **docs-and-samples-move-together**) each retire a whole cluster of per-resource cards. Settle
  those first; the rest go fast.
- **The Customer resource is leaking.** Trailing-space JSON keys (`"created "`,
  `"administrator "`, `"acceptedAgreement "`), admin-only fields emitted to every caller, and
  links to subsystems with no REST API. A coordinated — and partly *breaking* — code cleanup.
- **EntryPoint docs are materially wrong.** They document `queue` / `deliveryChannelPolicies`
  links the model doesn't emit, while it *does* emit undocumented `portalRoles` plus legacy
  policy links.
- **Several "scratch = not built yet" notes are now stale.** Asset-query ordering,
  `include=adjuncts`, and named-query PDF/ZIP all shipped → promote to docs. Conversely,
  **`openMaxWidth` + the substitute service genuinely don't exist** anywhere — a real
  build-or-drop decision, not a doc fix.
- **(2026-08-03) The adjunct-queue docs caught up from the other direction.** The code moved to
  meet the docs: nearly all of the documented `/adjunctQueue` surface now exists on `develop`
  (PRO-08). Remaining gaps: `completedAdjuncts`/`errorAdjuncts` (parallel of PRO-02) and the
  `AdjunctBatch` link properties, deliberately commented out pending a follow-up PR — with a
  latent link-name-vs-route mismatch flagged in the card.
- **The nuance worry — now answered completely (all 19 pages deep-audited, 2026-08-03).**
  Final: 24 lost-nuance items (PROV-01..24); verifiably clean: overview, collections,
  identifiers, custom-headers (+ size-restrictions clean on losses); 9 pages had uncaptured
  losses. The **silent normative changes** category proved the productive one: most were
  deliberate-but-unrecorded *corrections* of old-doc errors, and two were genuinely wrong in
  the NEW docs → cards DIS-25 (single-asset-manifest Choice claim vs code) and SPA-22
  (origin-strategy credentials "must"). Plus a previously-untracked unported page:
  `curl-examples.mdx`.
- **Auth is a design project, not a doc task.** `iiif-auth-v2` has no management API at all
  (configured by raw SQL); the whole 12-card cluster is gated on protagonist #538 / an RFC.
  Correctly scoped DESIGN-only, sequenced last.

## How to read this

- Each **decision card** lives in a per-session theme file (linked below) and has a stable ID
  (`ACC-01`, `SPA-03`, `XC-02`, …). Cross-cutting rulings (`XC-*`) are decided **first**;
  other cards reference them.
- The **triage table** below is the scannable in-room view: one line per open card. Work top
  to bottom within a session. Fill the **Ruling** and **Track** columns live.
- **Type** legend: `DOC-WRONG` · `CODE-WRONG` · `CODE-MISSING` · `DOC-MISSING` ·
  `STALE-SCRATCH` · `STYLE` · `DESIGN` (see README).
- **Track** (decided in session): `doc` · `code` · `sample` · `rfc` · `defer` · `close`.

## Theme files

| Session | File | Theme |
|:--|:--|:--|
| 0 | [session-0-cross-cutting.md](./session-0-cross-cutting.md) | Conventions: status codes, error model, Hydra cleanliness, identifiers |
| 1 | [session-1-account-access.md](./session-1-account-access.md) | Customer, custom-headers, storage, keys, portal users |
| 2 | [session-2-spaces-assets.md](./session-2-spaces-assets.md) | Space, asset, registering, delivery-channels, origin-strategy |
| 3 | [session-3-processing.md](./session-3-processing.md) | Queues, batch, pipelines |
| 4 | [session-4-discovery-delivery.md](./session-4-discovery-delivery.md) | Named-queries, asset-queries, manifests, identifiers, size-restrictions, entrypoint |
| 5 | [session-5-adjuncts.md](./session-5-adjuncts.md) | Adjuncts |
| 6 | [session-6-iiif-auth.md](./session-6-iiif-auth.md) | IIIF Presentation, roles, auth-service, access-control |
| — | [_provenance-nuance.md](./_provenance-nuance.md) | Lost-nuance diff (old Nextra → new Starlight) |
| — | [_issues-rfcs.md](./_issues-rfcs.md) | Open GitHub issues + RFCs, tagged by theme |

## By the numbers

**137 open decision cards** across 7 sessions (XC 13, ACC 19, SPA 22, PRO 13, DIS 26, ADJ 18,
IIIF 14 + AUTH 12 — 24 added by the 2026-08-03 verification + completion passes, marked
*(added 2026-08-03)* in the theme files), plus 24 lost-nuance items (`_provenance-nuance.md`,
PROV-01..24 — **all 19 ported pages now deep-audited**)
and the external index (`_issues-rfcs.md`: 143 open protagonist issues, 67 iiif-presentation,
8 iiif-auth-v2 as of 2026-08-03; 29 RFCs + 15 ADRs, +1 RFC proposed in open PR #1230, +1 in
iiif-presentation PR #228).
Already-resolved Category A items are listed (not as cards) at the top of each theme file.

Rough split by primary track (many cards are composite — see the card for the full option set):

| Primary track | ~Count | Nature |
|:--|:--|:--|
| **Doc / sample only** (quick wins) | ~32 | docs or samples wrong/stale; no code or design needed |
| **protagonist / iiif code change** | ~35 | model omissions, wrong annotations, leaked fields, cleanup |
| **Design / RFC** | ~26 | feature questions; whole auth cluster (12) + adjunct fields + manifest model |
| **Verify-first** (flagged "to check") | ~10 | claims read from source, not confirmed against a running API |
| **Python sample fixes** | 6 | see companion punch-list below |

## Recommended sequencing

1. **Session 0 (cross-cutting) first.** Its 9 rulings (DELETE→204, POST→201, error model,
   trailing-space property names, identifier policy, table-flag trust) cascade into dozens of
   per-resource cards — settle the principle once, then the rest become mechanical.
2. **Verify-first sweep.** Before the themed sessions, run the ~10 "to check" cards against a
   live/staging API (or have a dev confirm) so the room argues from facts, not source-reading.
   (2026-08-03: add the newly-built adjunct-queue endpoints — PRO-08 — to this sweep, noting
   they exist on `develop` only, not the v1.13.2 release.)
3. **Then themed sessions 1→5** (account · spaces/assets · processing · discovery · adjuncts).
4. **Session 6 (IIIF & Auth) last.** IIIF is mostly a *porting* job (the feature shipped);
   Auth is *design-led* (no management API exists — gated on protagonist #538 / an RFC).

## Triage table

> One sub-table per session. Work top-to-bottom. **Type** legend in README. **Track**: the
> card's suggested output(s) — `doc`·`code`·`sample`·`rfc`·`defer`. Fill **Ruling** live; record
> the owner and full reasoning in the card itself (theme file).

### Session 0 · Cross-cutting conventions — [file](./session-0-cross-cutting.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| XC-01 | DELETE must return 204 No Content | CODE-WRONG / DESIGN | code + doc | |
| XC-02 | create-POST must return 201 Created | DESIGN / DOC-WRONG | rfc + doc | |
| XC-03 | PUT upsert: 201 create / 200 replace, honestly | CODE-WRONG | code | |
| XC-04 | All errors must be a Hydra Error body | CODE-WRONG | code + rfc | |
| XC-05 | ProducesResponseType error type = `Error` not `ProblemDetails` | CODE-WRONG | code | |
| XC-06 | No trailing spaces in Hydra property names | CODE-WRONG | code + doc + rfc | |
| XC-07 | Don't advertise legacy/unmanageable Hydra links | DESIGN / DOC-WRONG | code/doc + rfc | |
| XC-08 | Identifier policy: id everywhere + exception register | DESIGN | doc | |
| XC-09 | domain/range tables: flags derived from the model | STYLE / DOC-WRONG | doc + sample | |
| XC-10 | Docs & Python samples move together (parity rule + coverage) | STYLE / process | doc + sample | |
| XC-11 | *(new 08-03)* Adjunct PUT annotation wrong on status and type | CODE-WRONG | code | |
| XC-12 | *(new 08-03)* Batch upserts collapse per-member Created/Updated | DESIGN | rfc + doc | |
| XC-13 | *(new 08-03)* Advertise what exists: no adjunctQueue link; stale AdjunctBatch TODO | CODE-WRONG / DESIGN | code | |

### Session 1 · Account & access — [file](./session-1-account-access.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| ACC-01 | Customer JSON property names have trailing spaces | CODE-WRONG | code / rfc | |
| ACC-02 | Customer emits authServices / roleProviders / roles links | CODE-WRONG | code / rfc / doc | |
| ACC-03 | administrator / acceptedAgreement leak to non-admins | CODE-WRONG / DOC-MISSING | code / doc / rfc | |
| ACC-04 | CustomHeader `role` carries stray readonly attr | STYLE | code | |
| ACC-05 | CustomHeader validator message says "named query" | STYLE | code | |
| ACC-06 | Storage exposes undocumented adjunct fields | DOC-MISSING | doc | |
| ACC-07 | ImageStorage: 3 properties share JsonProperty Order 55 | STYLE | code | |
| ACC-08 | Customer storage @id shown as .../spaces/0/storage | DOC-WRONG ⚠verify | doc / sample | |
| ACC-09 | storagePolicy on space-level storage: 3-way contradiction | DESIGN ⚠verify | doc / code / sample | |
| ACC-10 | Portal Users sub-resource under-documented | DOC-MISSING | doc / sample | |
| ACC-11 | API-key creation "administrator" claim vs no code guard | DOC-WRONG ⚠verify | doc / code / rfc | |
| ACC-12 | Operations tables miss real status codes | DOC-MISSING | doc / code | |
| ACC-13 | Customer space-creation POST defaults undocumented | DOC-MISSING ⚠verify | doc / code / rfc | |
| ACC-14 | API-key POST status: 200 (controller) vs 201 (metadata) | STYLE / CODE | code / doc | |
| ACC-15 | *(new 08-03)* Custom-header PUT returns 201 on successful update | CODE-WRONG + DOC-WRONG | code / doc | |
| ACC-16 | *(new 08-03)* customer.mdx example advertises `iiif` link not emitted | DOC-WRONG | doc / code | |
| ACC-17 | *(new 08-03)* Space 0 / stub-asset storage semantics undocumented | DOC-MISSING | doc | |
| ACC-18 | *(new 08-03)* Bulk POST /deleteImages completely undocumented | DOC-MISSING | doc / sample | |
| ACC-19 | *(new 08-03)* Doc/vocab cosmetics sweep (LinkCards, typos, example bugs) | STYLE | doc + code | |

### Session 2 · Spaces & assets — [file](./session-2-spaces-assets.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| SPA-01 | openMaxWidth + substitute/open service not in code | CODE-MISSING | doc / code / rfc | |
| SPA-02 | asset `family` in examples, no documented section | DOC-MISSING | doc / code | |
| SPA-03 | obsolete `maxUnauthorised` still emitted on assets | DESIGN / STALE-SCRATCH | code / doc / sample | |
| SPA-04 | asset `manifest` vs `manifests` vs possible `scopes` rename | DESIGN / CODE-MISSING | doc / code / rfc | |
| SPA-05 | `space.maxUnauthorised` in code, undocumented | DOC-MISSING | doc / code | |
| SPA-06 | stray `metadata` link on Space model | STALE-SCRATCH / DESIGN | code / doc | |
| SPA-07 | space.images bulk PATCH undoc'd; advertises non-existent POST | DOC-MISSING / CODE-WRONG | doc / code / sample | |
| SPA-08 | DeliveryChannelPolicy DELETE annotation 202 vs actual 204 | CODE-WRONG (annotation) | code | |
| SPA-09 | Space DELETE annotation 200+body vs actual 204 | CODE-WRONG (annotation) | code / doc | |
| SPA-10 | PUT to asset "always reingests" vs docs imply origin-change only | DOC-MISSING ⚠verify | doc / code | |
| SPA-11 | readonly/writeonly flags on asset disagree with doc tables | STYLE | code / doc | |
| SPA-12 | stray readonly/writeonly flags on origin-strategy models | STYLE | code / doc | |
| SPA-13 | CustomerOriginStrategy advertises PATCH the controller lacks | CODE-WRONG | code | |
| SPA-14 | PUT to a space silently ignores body `id` ≠ URL | DESIGN | code / doc | |
| SPA-15 | registering returns `imageService`; scratch wants `manifest` prop | DESIGN / STALE-SCRATCH | doc | |
| SPA-16 | sample-code DELETE comments wrong (200/202 vs 204) | DOC-WRONG (sample) | sample | |
| SPA-17 | several legacy asset properties serialised but undocumented *(⟳ corrected: vocab-only, not serialised)* | DESIGN / STALE-SCRATCH | code / doc | |
| SPA-18 | *(new 08-03)* imageService / thumbnailImageService undocumented | DOC-MISSING | doc | |
| SPA-19 | *(new 08-03)* Phantom Hydra credentials PUT op on CustomerOriginStrategy | CODE-WRONG | code / sample | |
| SPA-20 | *(new 08-03)* asset/space ops tables: wrong/missing codes + false id claim | DOC-WRONG | doc | |
| SPA-21 | *(new 08-03)* maxWidth upper bound (default 5000) undocumented | DOC-MISSING | doc | |
| SPA-22 | *(new 08-03)* origin-strategy "credentials must be supplied on POST" is wrong | DOC-WRONG | doc / code | |

### Session 3 · Processing — [file](./session-3-processing.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| PRO-01 | Batch model omits `assets` link although `/assets` works | CODE-WRONG | code / doc | |
| PRO-02 | `completedImages` / `errorImages` links emitted but 404 | CODE-WRONG | code / doc / rfc | |
| PRO-03 | `errors` field present in API + example but undocumented | DOC-MISSING | doc | |
| PRO-04 | `estCompletion` in model, undocumented and never populated | DOC-MISSING / CODE-WRONG | code / doc / defer | |
| PRO-05 | Doc says GET priority queue "not supported" — but it is | DOC-WRONG | doc / code | |
| PRO-06 | `test` endpoint does more than update `superseded` | DOC-WRONG | doc | |
| PRO-07 | CustomerQueue advertises `images` link, endpoint 404s | DOC-WRONG | doc / code | |
| PRO-08 | Adjunct queue/batch endpoints — largely **built on develop** since 2026-07 (see card ⟳ update) | ⚠verify (was DOC-MISSING / DESIGN) | doc / sample / code | |
| PRO-09 | Pipelines page unported; no implementation exists | DESIGN / defer | rfc / defer | |
| PRO-10 | `QueueSummaryClass` vocab wiring copy-paste bug | CODE-WRONG | code | |
| PRO-11 | *(new 08-03)* Adjunct-queue POST `asset` field undocumented; both samples 400 | DOC-MISSING + sample | doc / sample | |
| PRO-12 | *(new 08-03)* "active" batch semantics wrong (asset + adjunct queues) | DOC-WRONG | doc | |
| PRO-13 | *(new 08-03)* GET /queue + /adjunctQueue can 404; tables say 200 only | DOC-MISSING | doc / code | |

### Session 4 · Discovery & delivery — [file](./session-4-discovery-delivery.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| DIS-01 | asset-query ordering now works — promote from scratch | STALE-SCRATCH | doc / sample | |
| DIS-02 | `include=adjuncts` implemented — Aside & sample stale | STALE-SCRATCH | doc / sample | |
| DIS-03 | `manifests` filter supported but undocumented | DOC-MISSING | doc / sample | |
| DIS-04 | tags / roles / id filters not implemented — keep or design? | DESIGN | code / rfc / defer | |
| DIS-05 | multi-value string arrays unsupported (only `manifests`) | STALE-SCRATCH | rfc / defer | |
| DIS-06 | `orderBy` has no field whitelist — invalid name 500s | CODE-WRONG | doc / code | |
| DIS-07 | named-query PDF & ZIP output implemented — promote | STALE-SCRATCH | doc / sample | |
| DIS-08 | objectname/coverpage/redactedmessage real; sequence/roles not params | STALE-SCRATCH | doc / sample | |
| DIS-09 | named-query `global` field undocumented | DOC-MISSING | doc | |
| DIS-10 | `manifest` template key — placeholder value & broken `iiif` link | DOC-WRONG / DOC-MISSING | doc | |
| DIS-11 | `canvas` is obsolete alias for `assetOrder` — docs lead with it | DESIGN / STYLE | doc | |
| DIS-12 | named-query syntax table `s3` row example typo | DOC-WRONG (STYLE) | doc | |
| DIS-13 | named-query model carries `[Unstable]`/`[Obsolete]` | CODE-WRONG (cleanup) | code | |
| DIS-14 | EntryPoint docs show `queue` & `deliveryChannelPolicies`; model emits neither | DOC-WRONG / CODE-MISSING | doc / code / rfc | |
| DIS-15 | EntryPoint emits legacy imageOptimisation/thumbnailPolicies | CODE-WRONG (cleanup) | code | |
| DIS-16 | EntryPoint emits `portalRoles` — undocumented | DOC-MISSING | doc / code | |
| DIS-17 | EntryPoint scratch note is stale/incorrect | STALE-SCRATCH | doc (scratch) | |
| DIS-18 | size-restrictions documents openMaxWidth + substitute (absent) | DOC-WRONG | doc / rfc | |
| DIS-19 | single-asset-manifest examples partly unverified | DESIGN | doc / sample | |
| DIS-20 | broken `../iiif` links (page not yet ported) | DOC-MISSING (link) | doc | |
| DIS-21 | collections.mdx host inconsistency in example JSON | STYLE | doc | |
| DIS-22 | *(new 08-03)* Batch endpoints support asset-query syntax — page omits them | DOC-MISSING | doc | |
| DIS-23 | *(new 08-03)* Versioned iiif-resource paths + Accept negotiation undocumented | DOC-MISSING | doc | |
| DIS-24 | *(new 08-03)* entrypoint.mdx uses production hostname in examples | STYLE | doc | |
| DIS-25 | *(new 08-03)* single-asset-manifest "always a Choice" wrong; no-transcode AV = no canvas | DOC-WRONG | doc / code | |
| DIS-26 | *(new 08-03)* "thumbs channel serves only open content" — unsourced claim | DOC-WRONG? ⚠verify | doc | |

### Session 5 · Adjuncts — [file](./session-5-adjuncts.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| ADJ-01 | `content` sub-resource (POST/GET binary) not implemented | CODE-MISSING | code / rfc / defer | |
| ADJ-02 | Live mdx still shows `content` in example GET responses | DOC-WRONG | doc | |
| ADJ-03 | `roles` field not implemented | CODE-MISSING | doc / code / rfc / defer | |
| ADJ-04 | `creator` field not implemented | CODE-MISSING | doc / code / defer | |
| ADJ-05 | `source` field not implemented | CODE-MISSING | doc / code / defer | |
| ADJ-06 | null `iiifLink` / `otherAdjuncts` not implemented | CODE-MISSING | code / defer | |
| ADJ-07 | `label` required vs recommended (parked design Q) | DESIGN | code / doc | |
| ADJ-08 | `asset` back-link emitted but undocumented | DOC-MISSING | doc / code | |
| ADJ-09 | `mediaType` required, but example + sample omit it on AnnotationPage | DOC-WRONG + sample | doc / sample | |
| ADJ-10 | `@type` must be AnnotationPage when iiifLink=annotations — undoc'd | DOC-MISSING | doc / code | |
| ADJ-11 | Bulk-delete `POST /customers/{c}/deleteAdjuncts` undocumented | DOC-MISSING | doc / sample | |
| ADJ-12 | DELETE `?deleteFrom=` query parameter undocumented | DOC-MISSING | doc | |
| ADJ-13 | `size = -1` while unprocessed — code uses null | DOC-WRONG (low conf) | doc / code | |
| ADJ-14 | POST of single adjunct returns a HydraCollection | DOC-MISSING (clarify) | doc / sample / code | |
| ADJ-15 | Samples flagged "not implemented" though they now work | STALE-SCRATCH / STYLE | sample | |
| ADJ-16 | Intro example + pipeline narrative aspirational | DOC-WRONG (composite) | doc | |
| ADJ-17 | *(new 08-03)* New `### batch` section carries asset-page copy-paste bugs | DOC-WRONG | doc | |
| ADJ-18 | *(new 08-03)* Adjunct POST 409 / PUT-update 200 undocumented | DOC-MISSING | doc | |

### Session 6 · IIIF & Auth — [file](./session-6-iiif-auth.md) — *DESIGN-only for auth; sequence last*

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| IIIF-01 | Port iiif.mdx at all (and what gets samples) | STALE-SCRATCH | doc / sample / rfc | |
| IIIF-02 | PATCH documented but not implemented (PUT+If-Match only) | DOC-WRONG | doc / code / rfc | |
| IIIF-03 | `/configuration` + IIIFConfiguration resource not implemented | STALE-SCRATCH | doc / rfc / defer | |
| IIIF-04 | Reserved slugs — port verbatim (verified match) | STALE-SCRATCH | doc | |
| IIIF-05 | Manifest `assets` & `queue` link properties absent from model | CODE-MISSING | doc / code / rfc | |
| IIIF-06 | Collection `totals` / descendant counts missing in code | DOC-WRONG | doc / code | |
| IIIF-07 | ETag vs `If-Match` for optimistic updates | DOC-WRONG | doc | |
| IIIF-08 | `ingesting` object shape differs (gains `errors`) | DOC-WRONG | doc | |
| IIIF-09 | canvasPainting `duration` field undocumented | DOC-MISSING | doc | |
| IIIF-10 | Item ordering now implemented (`itemsOrder`) | STALE-SCRATCH | doc | |
| IIIF-11 | Placeholder JSON-LD `@context` URL (tbc.org) | DOC-WRONG | doc / code / rfc | |
| IIIF-12 | "JSON is King" update semantics — verify | DESIGN | doc / rfc | |
| IIIF-13 | Python samples for IIIF page (different host + auth) | DESIGN | sample | |
| IIIF-14 | *(new 08-03)* New surface shipped since June: search-across, manifest pipelines, error conventions | DOC-MISSING | doc / sample | |
| AUTH-01 | No management REST API exists — core design gap | DESIGN | rfc / doc / defer | |
| AUTH-02 | Naming: `AuthService` (docs) vs `AccessService` (code) | DESIGN | doc / code / rfc | |
| AUTH-03 | IP-address Role Provider documented but not implemented | DOC-WRONG | doc / rfc | |
| AUTH-04 | Design: AccessService management CRUD | DESIGN | rfc / doc / sample | |
| AUTH-05 | Design: RoleProvider management + host-keyed JSONB config | DESIGN | rfc / doc | |
| AUTH-06 | Design: Role management + auto-create clickthrough role | DESIGN | rfc / code / doc | |
| AUTH-07 | Undocumented entity: CustomerCookieDomain | DOC-MISSING | rfc / doc / defer | |
| AUTH-08 | Where the auth management API lives (protagonist vs auth-v2) | DESIGN | rfc | |
| AUTH-09 | OIDC provider configuration rich but undocumented | DOC-MISSING | doc / rfc | |
| AUTH-10 | Appointments-based / dynamic roles — future design | DESIGN | defer / rfc | |
| AUTH-11 | Synthesise the three access-control RFCs into the page | STALE-SCRATCH | doc | |
| AUTH-12 | `customer.authServices` link — verify and reconcile | DOC-WRONG | doc / code | |

## Companion artefacts (separate punch-lists)

### Python sample fixes (factual, low-controversy — can be applied once decisions ratified)
1. `p13_adjuncts/iiif_link_adjuncts.py` — AnnotationPage adjunct missing required `mediaType`.
2. `p12_origin_strategies/get_put_delete_origin_strategy.py` — `put_origin_strategy` docstring wrongly says credentials are not updated (full-object PUT does update; basic-http/sftp only).
3. `p12_origin_strategies/update_credentials.py` — orphan describing a non-existent `/credentials` sub-resource; delete or rewrite to full-object PUT.
4. `p15_asset_queries/asset_queries.py` — `get_images_ordered` docstring "ordering not supported" is stale (ordering works); pairs with the asset-queries doc promotion (DIS theme).
5. `p07_asset/get_put_patch_delete_asset.py:75` — `# Expected: DELETE 200 OK` → **204 No Content** (`ImageController.cs:201`).
6. `p11_delivery_channels/get_put_patch_delete_policy.py:66` — `# Expected: DELETE 202 Accepted` → **204 No Content** (`HandleDelete`→`NoContent()`).

> Items 5 & 6 also feed cross-cutting card(s) on DELETE status semantics (see session-0).
