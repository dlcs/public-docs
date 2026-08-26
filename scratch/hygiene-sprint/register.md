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

- **⟳ 2026-08-19: Session 4 (Discovery & delivery) is DONE — all 27 DIS cards carry final
  statuses** (10 pre-closed by earlier sessions/mechanical/cascade; 16 ruled today; DIS-19
  deferred to the PO outside the sprint with a feasibility scout preserved). Named-queries got
  the biggest lift: a wire-proven **Output types** section (pdf/zip/raw-resource, control files,
  202+Retry-After, purge, "PDF generation may not be enabled on all environments"), the three
  real pdf/zip template params (sequence/roles dropped as phantoms), `## global` documented,
  and docs now lead with **assetOrder** (canvas = legacy alias). Versioned iiif-resource /
  iiif-manifest paths + Accept negotiation documented on two pages. EntryPoint cluster settled:
  `deliveryChannelPolicies` dropped, `queue` link added (**PR #1282**), **`portalRoles`
  revealed as a dead link that always 404'd** — removed with its orphaned vocab class
  (**PR #1284**, breaking). Four protagonist draft PRs (**#1281** orderBy 400 whitelist,
  breaking; #1282; #1284; **#1286** NamedQuery Order fix), two issues (**#1279** tags/roles/id
  + multi-value RFC for the portal team; **#1280** orderBy 500→400), comments on #960/#566
  territory. Evidence lessons: two code-reading predictions overturned on the wire
  (`orderBy=manifests` 200s; raw-resource IGNORES assetOrder), one of my own issue claims
  corrected (#1279 `space` — only batch endpoints honour it), and the DIS-26 thumbs claim was
  half-false (auth-location thumbs ARE generated, never served — live ingest experiment).
  Release-gated twins added: PRO-01-style queue-link restoration (entrypoint), XC-01 purge-204
  (named-queries), #566-gated global contract table. Docs on branch `hygiene/session-4`
  (PR at close).

- **⟳ 2026-08-17: Session 3 (Processing) is DONE — all 15 PRO cards carry final statuses**
  (7 pre-closed by session 0 / mechanical track / cascade; 8 ruled today, incl. **PRO-15**
  minted and ruled same-day). Five per-card protagonist draft PRs: **#1272** (Batch gains the
  `assets` link), **#1273** (estCompletion phantom pruned), **#1274** (dead CustomerQueue
  `images` link removed — breaking, never followable), **#1276** (Adjunct + AdjunctBatch get
  real vocab classes — the Adjunct twin found at presentation; last self-referencing
  HydraClass attrs gone), **#1277** (priority queue response gets its own @id, links
  deliberately shared — breaking). Doc work: batch.mdx `test` = full reconciliation +
  `success` semantics; dead `completedAdjuncts`/`errorAdjuncts` and queue `images` example
  lines removed; broken `get_queue_images.py` deleted; pipelines stays deferred with an
  annotated seed. Session context: all six session-2 PRs + #1268 (Hydra flags→OpenAPI) +
  #1269 merged same morning — vocab flags are now operational in Swagger, raising the stakes
  of every flags ruling. One evidence correction logged mid-session (sweep display artefact
  claimed no `test` link; full re-GET disproved). Docs on branch `hygiene/session-3`
  (PR at close).

- **⟳ 2026-08-14: Session 2 (Spaces & assets) is DONE — all 25 SPA cards + ACC-20 carry final
  statuses** (ran 08-12, paused, resumed 08-14). 16 cards ruled in-room; 2 minted mid-session
  and ruled same-session (SPA-25, ACC-20); SPA-24 (minted from SPA-22's work) resolved
  upstream by Donald between sittings (`96868fc5`, verified). Per-card protagonist PRs:
  **#1246/#1247/#1251/#1255 MERGED**; drafts open **#1258–#1260, #1262, #1263, #1266**
  (#1260 breaking — body-id-vs-URL 400s). New issues **#1248–#1250, #1252/#1253**,
  **#1261 (SEVERE bug: any asset PATCH silently wipes omitted roles/tags — released
  behaviour, wire-verified; response masks the wipe)**, **#1264** (family deprecation
  intent). New docs page **reprocessing.mdx** (which field changes trigger reprocessing, per
  operation — PO-directed, consistency-verified, v1.13.2==develop on all cited files). Room
  challenges twice overturned the sprint's own claims (space maxUnauthorised premise;
  maxUnauthorised-never-reprocesses — the ADR-0010 shim translates it to openFullMax), and
  the SPA-10 `finished`-timestamp wire evidence was retracted (MarkAsFinished bumps it on the
  no-reingest path too). Docs on branch `hygiene/session-2` (PR at close).

- **⟳ 2026-08-10: Session 1 (Account & access) is DONE — all 19 ACC cards now carry final
  statuses.** Ten cards handled in-room: 6 rulings executed (ACC-03/06/08/09/10/11), 2 closed
  as already-landed or overtaken (ACC-12/13), 2 deferred with artefacts (ACC-17 → public-docs
  issue #12; ACC-18 → release-gated twin in scratch). Per-card protagonist draft PRs
  #1241–#1244 (rule: per-card PRs, established session 0). New issues: protagonist #1240
  (per-space storage policies), #1245 (customer→iiif-presentation link, config-gated);
  public-docs #12. New card SPA-23 (space defaultTags/defaultRoles verified non-functional —
  space.mdx documents unimplemented behaviour). **Security fix en route:** portal-user PATCH
  lacked the customer-ownership check (cross-tenant password change by GUID) — fixed in #1243,
  prompt-release candidate. Docs-side changes on public-docs branch `hygiene/session-1`.

- **⟳ 2026-08-06: Session 0 is DONE.** All 13 XC conventions ratified and *executed* (not just
  minuted): protagonist PRs #1236 (session branch, 4 breaking changes signposted), #1237
  (unreachable links), #1238 (closes #899) + public-docs PR #9; the whole mechanical track
  (#5-#7, #1234-#1235) merged. Roughly 30 cards across sessions 1-5 are now fully resolved,
  partially done, or cascade-annotated — check each card's Status line before spending room
  time on it. The bullets below predate session 0 and stand as written *except* where a card
  Status says otherwise (e.g. Customer trailing spaces + auth links: fixed in the PRs above).

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
- **⟳ 2026-08-06:** session 0 is complete. Card **Status lines are authoritative**; the
  triage tables' Ruling column is back-filled for every session-0 outcome (rulings,
  mechanical merges, cascades). Keep the column in sync as later sessions rule.
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
| — | [_mechanical-track.md](./_mechanical-track.md) | Mechanical-track candidate list (session-0 veto pass; batches → draft PRs) |
| — | [_worked-example.md](./_worked-example.md) | Fictionalised end-to-end walkthrough of one session — read this first if new |

## By the numbers

**144 decision cards** (⟳ 08-19: **session 4 complete** — its 17 open cards ruled (DIS-19 by
deferral to the PO outside the sprint), all 27 DIS cards now closed, **85 closed
register-wide**; ⟳ 08-17: session 3 complete — all 15 PRO closed, 68 register-wide;
⟳ 08-14: sessions 0, 1 and 2 complete — 60 cards closed; ⟳ 08-06: session 0 closed its 13 XC
cards and resolved or part-resolved ~30 more — see Status lines)
across 7 sessions (XC 13, ACC 20, SPA 25, PRO 15, DIS 27, ADJ 18,
IIIF 14 + AUTH 12 — 24 added by the 2026-08-03 verification + completion passes, marked
*(added 2026-08-03)* in the theme files; SPA-24/SPA-25/ACC-20 minted mid-sprint in session 2,
PRO-15 in session 3), plus 24 lost-nuance items (`_provenance-nuance.md`,
PROV-01..24 — **all 19 ported pages now deep-audited**)
and the external index (`_issues-rfcs.md`: 150 open protagonist issues (+#1279/#1280 raised in
session 4), 65 iiif-presentation, 8 iiif-auth-v2 as of 2026-08-19; 29 RFCs + 15 ADRs, +1 RFC
proposed in open PR #1230, +1 in iiif-presentation PR #228).
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
| XC-01 | DELETE must return 204 No Content | CODE-WRONG / DESIGN | code + doc | RATIFIED; both legacy DELETEs migrated to 204 (#1236, breaking) |
| XC-02 | create-POST must return 201 Created | DESIGN / DOC-WRONG | rfc + doc | RATIFIED (a): 201 + two named 200 action-POST exceptions; doc PR #9 |
| XC-03 | PUT upsert: 201 create / 200 replace, honestly | CODE-WRONG | code | RATIFIED + update-only-PUT rule; ACC-15 fixed (#1236); handed to iiif-p #641 |
| XC-04 | All errors must be a Hydra Error body | CODE-WRONG | code + rfc | RATIFIED; bare 400 fixed + sentinel tidied (#1236); /test body kept, documented (PR #9) |
| XC-05 | ProducesResponseType error type = `Error` not `ProblemDetails` | CODE-WRONG | code | RATIFIED; 13 fixed (#1234) + 24-annotation typed-Error sweep (#1236) |
| XC-06 | No trailing spaces in Hydra property names | CODE-WRONG | code + doc + rfc | RATIFIED; 3 names trimmed + guard test (#1236, breaking) |
| XC-07 | Don't advertise legacy/unmanageable Hydra links | DESIGN / DOC-WRONG | code/doc + rfc | RATIFIED (reachable-surface rule); 5 links removed (#1237) |
| XC-08 | Identifier policy: id everywhere + exception register | DESIGN | doc | RATIFIED; identifiers.mdx = exception register (PR #9) |
| XC-09 | domain/range tables: flags derived from the model | STYLE / DOC-WRONG | doc + sample | RATIFIED; hydra-model-dump tool + _hydra-model-flags.md delivered |
| XC-10 | Docs & Python samples move together (parity rule + coverage) | STYLE / process | doc + sample | RATIFIED main-only (samples educational; Playwright = regression); runner parked as issue #11 |
| XC-11 | *(new 08-03)* Adjunct PUT annotation wrong on status and type | CODE-WRONG | code | mechanical, merged #1234 |
| XC-12 | *(new 08-03)* Batch upserts collapse per-member Created/Updated | DESIGN | rfc + doc | (a) aggregate status, RFC 9110 framing; documented (PR #9 + scratch) |
| XC-13 | *(new 08-03)* Advertise what exists: no adjunctQueue link; stale AdjunctBatch TODO | CODE-WRONG / DESIGN | code | links added/removed per rule (#1238, closes #899); docs half PR #9 |

### Session 1 · Account & access — [file](./session-1-account-access.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| ACC-01 | Customer JSON property names have trailing spaces | CODE-WRONG | code / rfc | RESOLVED by XC-06 (#1236, option c exactly) |
| ACC-02 | Customer emits authServices / roleProviders / roles links | CODE-WRONG | code / rfc / doc | RESOLVED by XC-07 (#1237) |
| ACC-03 | administrator / acceptedAgreement leak to non-admins | CODE-WRONG / DOC-MISSING | code / doc / rfc | RULED: drop acceptedAgreement; administrator only-when-true (breaking; draft PR #1241) |
| ACC-04 | CustomHeader `role` carries stray readonly attr | STYLE | code | mechanical, merged #1235 |
| ACC-05 | CustomHeader validator message says "named query" | STYLE | code | mechanical, merged #1235 |
| ACC-06 | Storage exposes undocumented adjunct fields | DOC-MISSING | doc | RULED (c): brief sections + cross-link to adjuncts; applied session-1 branch |
| ACC-07 | ImageStorage: 3 properties share JsonProperty Order 55 | STYLE | code | mechanical, merged #1235 (incl. ApiKey/PortalUser) |
| ACC-08 | Customer storage @id shown as .../spaces/0/storage | DOC-WRONG ⚠verify | doc / sample | RULED (a): example fixed, live-verified; applied session-1 branch |
| ACC-09 | storagePolicy on space-level storage: 3-way contradiction | DESIGN ⚠verify | doc / code / sample | RULED (b): space-level emission dropped (breaking, draft PR #1242); docs release-gated (scratch twin); per-space design → #1240 |
| ACC-10 | Portal Users sub-resource under-documented | DOC-MISSING | doc / sample | RULED (b)+deprecation notice: portal-users.mdx + lifecycle sample (staging-verified); msg split + PATCH ownership security fix + XC-07 cascade (draft PR #1243, prompt-release candidate) |
| ACC-11 | API-key creation "administrator" claim vs no code guard | DOC-WRONG ⚠verify | doc / code / rfc | RULED (a): reworded to "authenticated as this customer" — docs session-1 branch + vocab draft PR #1244 |
| ACC-12 | Operations tables miss real status codes | DOC-MISSING | doc / code | CLOSED (session 1): all parts landed via PRs #5/#9/#1236 |
| ACC-13 | Customer space-creation POST defaults undocumented | DOC-MISSING ⚠verify | doc / code / rfc | CLOSED (session 1): defaultTags/defaultRoles verified non-functional -> do NOT document; finding minted as SPA-23; ignored-id folded into SPA-14 |
| ACC-14 | API-key POST status: 200 (controller) vs 201 (metadata) | STYLE / CODE | code / doc | RESOLVED via XC-02: metadata 201→200 (#1236) |
| ACC-15 | *(new 08-03)* Custom-header PUT returns 201 on successful update | CODE-WRONG + DOC-WRONG | code / doc | handler → Updated/200 (#1236, minor breaking); docs row fixed (PR #9) |
| ACC-16 | *(new 08-03)* customer.mdx example advertises `iiif` link not emitted | DOC-WRONG | doc / code | RULED (a): example line removed (session-1 branch); build-the-link → issue #1245 (config-gated, not all deployments have iiif-presentation) |
| ACC-17 | *(new 08-03)* Space 0 / stub-asset storage semantics undocumented | DOC-MISSING | doc | RULED (b): not customer-facing yet, no doc now; public-docs issue #12 holds the design questions + doc task |
| ACC-18 | *(new 08-03)* Bulk POST /deleteImages completely undocumented | DOC-MISSING | doc / sample | RULED (a): full doc+sample twin drafted, release-gated in scratch (home: customer.mdx); apply with ADJ-11 when #1236's release ships |
| ACC-19 | *(new 08-03)* Doc/vocab cosmetics sweep (LinkCards, typos, example bugs) | STYLE | doc + code | CLOSED (PR #6 + #1235) |
| ACC-20 | *(minted 08-14 in session 2, from SPA-07 discussion)* allImages PATCH undocumented-by-design (unrecorded); Customer vocab misadvertises collection ops | DOC-MISSING / CODE-WRONG | doc / code | RULED (a)+Swagger-exclusion (session 2, 08-14): vocab POST now describes real id-list retrieval; internal manifests PATCH hidden from Swagger — draft PR #1259; undocumented-PATCH porting decision ratified |

### Session 2 · Spaces & assets — [file](./session-2-spaces-assets.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| SPA-01 | openMaxWidth + substitute/open service not in code | CODE-MISSING | doc / code / rfc | RULED (session 2): openMaxWidth/substitute prose → scratch verbatim (incl. new scratch size-restrictions.md); ADR-writing ticket #1249 (the unfulfilled #306 promise); examples fixed |
| SPA-02 | asset `family` in examples, no documented section | DOC-MISSING | doc / code | RULED (a) (session 2, 08-14): family documented — derived/immutable + legacy-mode-reacts note; Swagger sample fix #1263; PO deprecation intent → issue #1264 |
| SPA-03 | obsolete `maxUnauthorised` still emitted on assets | DESIGN / STALE-SCRATCH | code / doc / sample | RULED (b) (session 2): documented as deprecated (0/-1 semantics, mutual-exclusion 400, migration guidance); see also SPA-25 discovery re the ADR-0010 shim |
| SPA-04 | asset `manifest` vs `manifests` vs possible `scopes` rename | DESIGN / CODE-MISSING | doc / code / rfc | RULED (a+b) (session 2): manifests documented live w/ do-not-edit caution; `manifest` link added, PR #1251 MERGED; scopes+usedBy design ticket #1250; manifest doc twin release-gated |
| SPA-05 | `space.maxUnauthorised` in code, undocumented | DOC-MISSING | doc / code | RULED (d) (session 2 — room overturned premise): verified VESTIGIAL, removed from model, PR #1247 MERGED (breaking); space-level replacements issue #1248 |
| SPA-06 | stray `metadata` link on Space model | STALE-SCRATCH / DESIGN | code / doc | RULED (a) (session 2): phantom link removed, PR #1255 MERGED; broken sample space_metadata.py deleted |
| SPA-07 | space.images bulk PATCH undoc'd; advertises non-existent POST | DOC-MISSING / CODE-WRONG | doc / code / sample | RULED (a) (session 2, 08-14): bulk PATCH documented + sample (staging-verified 200/400); vocab POST→PATCH swap draft PR #1258; discussion minted ACC-20 |
| SPA-08 | DeliveryChannelPolicy DELETE annotation 202 vs actual 204 | CODE-WRONG (annotation) | code | mechanical, merged #1234 |
| SPA-09 | Space DELETE annotation 200+body vs actual 204 | CODE-WRONG (annotation) | code / doc | RULED (a) (session 2): 409 row added w/ PO wording ("If the space is not empty…"); annotation half merged #1234 |
| SPA-10 | PUT to asset "always reingests" vs docs imply origin-change only | DOC-MISSING ⚠verify | doc / code | RULED (a) (session 2, 08-14): new reprocessing.mdx page ratified as payload (PUT/PATCH distinction, trigger tables, none-channel, mediaType-on-every-PUT); finished-timestamp wire evidence retracted — ruled on code trace |
| SPA-11 | readonly/writeonly flags on asset disagree with doc tables | STYLE | code / doc | RULED (a)+space-vocab (session 2, 08-14): five flags aligned to wire truth (doc tables were right in all five), space gains missing RdfProperty — draft PR #1262; deliveryChannels deferred to SPA-17 |
| SPA-12 | stray readonly/writeonly flags on origin-strategy models | STYLE | code / doc | attrs fixed to documented contract (#1236) |
| SPA-13 | CustomerOriginStrategy advertises PATCH the controller lacks | CODE-WRONG | code | PATCH removed (#1236) |
| SPA-14 | PUT to a space silently ignores body `id` ≠ URL | DESIGN | code / doc | RULED (a) (session 2, 08-14): conflicting body id → 400 on space POST/PUT/PATCH + asset PUT/PATCH (ACC-13 fold-in honoured) — draft PR #1260, BREAKING; carries PO-requested central id-policy recommendation; doc twins release-gated |
| SPA-15 | registering returns `imageService`; scratch wants `manifest` prop | DESIGN / STALE-SCRATCH | doc | RULED (b) (session 2): manifest-as-hub; imageService guidance swap release-gated; imageService/thumbnailImageService deprecation intent → issue #1252 |
| SPA-16 | sample-code DELETE comments wrong (200/202 vs 204) | DOC-WRONG (sample) | sample | mechanical, merged PR #7 |
| SPA-17 | several legacy asset properties serialised but undocumented *(⟳ corrected: vocab-only, not serialised)* | DESIGN / STALE-SCRATCH | code / doc | RULED (session 2, 08-14): six phantoms pruned incl. degradedInfoJson (descriptions parked in scratch); iop/tp [Obsolete] + doc note; deliveryChannels vocab entry fixed — draft PR #1266 |
| SPA-18 | *(new 08-03)* imageService / thumbnailImageService undocumented | DOC-MISSING | doc | mechanical, merged PR #6 |
| SPA-19 | *(new 08-03)* Phantom Hydra credentials PUT op on CustomerOriginStrategy | CODE-WRONG | code / sample | op removed (#1236); orphan sample deleted (PR #9) |
| SPA-20 | *(new 08-03)* asset/space ops tables: wrong/missing codes + false id claim | DOC-WRONG | doc | mechanical, merged PR #5; the id claim is now true behaviour once #1260 ships (SPA-14) |
| SPA-21 | *(new 08-03)* maxWidth upper bound (default 5000) undocumented | DOC-MISSING | doc | mechanical, merged PR #6 |
| SPA-22 | *(new 08-03)* origin-strategy "credentials must be supplied on POST" is wrong | DOC-WRONG | doc / code | RULED (a) (session 2): validator tidied + fail-fast, PR #1246 MERGED (then tidied upstream by 96868fc5); implementation work found SPA-24 |
| SPA-23 | *(new 08-10, session 1)* space defaultRoles/defaultTags non-functional; space.mdx documents unimplemented behaviour | DOC-WRONG / CODE-MISSING | code / doc / rfc | RULED (c) (session 2): interim cautions live on space.mdx/asset.mdx + samples; implement-or-drop decision issue #1253 (activation hazard captured); corroborated upstream by #1254/#1257 |
| SPA-24 | *(minted in session 2, from SPA-22 work)* origin-strategy credential wipe mis-ordered on strategy switch | CODE-WRONG | code | RESOLVED UPSTREAM (Donald Gray, protagonist 96868fc5, 2026-08-12) — verified; fixed both defects + a third (dangling DB credentials); no room ruling needed |
| SPA-25 | *(minted 08-14, found proving the maxUnauthorised reprocessing claim)* asset PATCH silently wipes roles/tags omitted from body; response masks the wipe | CODE-WRONG (SEVERE) | code | RULED (b) (session 2, 08-14): bug issue #1261 (detailed; wider RolesList-internal-use implications per PO); affects released v1.13.2, wire-verified |

### Session 3 · Processing — [file](./session-3-processing.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| PRO-01 | Batch model omits `assets` link although `/assets` works | CODE-WRONG | code / doc | RULED (a) session 3, 2026-08-17 (cascade confirmed): assets HydraLink + vocab op added — PR #1272; sample swap release-gated |
| PRO-02 | `completedImages` / `errorImages` links emitted but 404 | CODE-WRONG | code / doc / rfc | RESOLVED by XC-13: links removed (#1238 + PR #9) |
| PRO-03 | `errors` field present in API + example but undocumented | DOC-MISSING | doc | asset flavour merged PR #5; adjunct twin release-gated |
| PRO-04 | `estCompletion` in model, undocumented and never populated | DOC-MISSING / CODE-WRONG | code / doc / defer | RULED (b) session 3, 2026-08-17: phantom pruned — PR #1273; description parked in scratch batch.md |
| PRO-05 | Doc says GET priority queue "not supported" — but it is | DOC-WRONG | doc / code | (a) GET documented + sample (PR #9) |
| PRO-06 | `test` endpoint does more than update `superseded` | DOC-WRONG | doc | RULED (a) session 3, 2026-08-17: full reconciliation documented + success semantics; no issue/PR citations per PO; stale #491 blockquote removed |
| PRO-07 | CustomerQueue advertises `images` link, endpoint 404s | DOC-WRONG | doc / code | RULED (a)/XC-07 treatment session 3, 2026-08-17: dead link removed — PR #1274 (breaking); example fixed; broken sample deleted; spec parked in scratch |
| PRO-08 | Adjunct queue/batch endpoints — largely **built on develop** since 2026-07 (see card ⟳ update) | ⚠verify (was DOC-MISSING / DESIGN) | doc / sample / code | RULED (a) session 3, 2026-08-17: card largely overtaken (built on develop; XC-13 did link emission; #1166 closed); dead completedAdjuncts/errorAdjuncts removed from example; rest release-gated |
| PRO-09 | Pipelines page unported; no implementation exists | DESIGN / defer | rfc / defer | RULED (a) session 3, 2026-08-17: stays deferred, no ticket; scratch seed annotated (manifest-pipelines name collision, reserved slug, RFC-024 adjacency) |
| PRO-10 | `QueueSummaryClass` vocab wiring copy-paste bug | CODE-WRONG | code | mechanical, merged #1235 |
| PRO-11 | *(new 08-03)* Adjunct-queue POST `asset` field undocumented; both samples 400 | DOC-MISSING + sample | doc / sample | samples merged PR #7; doc half release-gated |
| PRO-12 | *(new 08-03)* "active" batch semantics wrong (asset + adjunct queues) | DOC-WRONG | doc | asset section merged PR #5; adjunct release-gated |
| PRO-13 | *(new 08-03)* GET /queue + /adjunctQueue can 404; tables say 200 only | DOC-MISSING | doc / code | /queue merged PR #5; adjunct release-gated |
| PRO-14 | *(new 08-06, session 0)* AdjunctBatch HydraClass references itself; no vocab class | CODE-WRONG | code | RULED (a+) session 3, 2026-08-17: AdjunctBatchClass + AdjunctClass (twin defect found at presentation) — PR #1276; last self-referencing HydraClass attrs gone |
| PRO-15 | *(new 08-17, session 3)* Priority queue response self-identifies as main queue (@id + links) | CODE-WRONG | code / doc | RULED (a) session 3, 2026-08-17 (same-day mint, out of PRO-07 live sweep): own @id, links deliberately shared — PR #1277 (breaking); doc twin release-gated |

### Session 4 · Discovery & delivery — [file](./session-4-discovery-delivery.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| DIS-01 | asset-query ordering now works — promote from scratch | STALE-SCRATCH | doc / sample | promoted (PR #9) |
| DIS-02 | `include=adjuncts` implemented — Aside & sample stale | STALE-SCRATCH | doc / sample | Aside fixed (PR #9) |
| DIS-03 | `manifests` filter supported but undocumented | DOC-MISSING | doc / sample | (b) leave undocumented — closed no-op |
| DIS-04 | tags / roles / id filters not implemented — keep or design? | DESIGN | code / rfc / defer | ruled (b) session 4 (2026-08-19): issue #1279 raised — RFC wanted, portal team audience; #753 prerequisite; Aside stays; sample docstrings corrected (silent ignore, never an error) |
| DIS-05 | multi-value string arrays unsupported (only `manifests`) | STALE-SCRATCH | rfc / defer | ruled (b′) session 4: folded into #1279 RFC scope (comment: OR/AND semantics, manifests precedent, 400-vs-silent-ignore); no live-doc change |
| DIS-06 | `orderBy` has no field whitelist — invalid name 500s | CODE-WRONG | doc / code | ruled (c) session 4: issue #1280 + fix PR **#1281** (400 whitelist, breaking); doc sentence tightened to wire-verified safe list; manifests-500 prediction overturned (200 on wire) |
| DIS-07 | named-query PDF & ZIP output implemented — promote | STALE-SCRATCH | doc / sample | ruled (b) session 4: pdf/zip/raw-resource all documented (Output types section); sample named_query_outputs.py wire-proven; thumbnail claim PO-corrected (closest to 1000px); purge 200-vs-204 twin release-gated (XC-01) |
| DIS-08 | objectname/coverpage/redactedmessage real; sequence/roles not params | STALE-SCRATCH | doc / sample | ruled (a) session 4: three real params documented with applicability + tokens; sequence/roles dropped as phantoms; sample objectname={s1}.zip wire-proven |
| DIS-09 | named-query `global` field undocumented | DOC-MISSING | doc | ruled (b) session 4: minimal `## global` section live; full wire-confirmed contract table in scratch gated on #566 (followable global links) |
| DIS-10 | `manifest` template key — placeholder value & broken `iiif` link | DOC-WRONG / DOC-MISSING | doc | ruled (d) session 4: row REMOVED for DIS-03 consistency; promotion-ready corrected row parked in scratch, gated on iiif.mdx |
| DIS-11 | `canvas` is obsolete alias for `assetOrder` — docs lead with it | DESIGN / STYLE | doc | ruled (a) session 4: docs lead with assetOrder (canvas = legacy alias per [Obsolete]); all examples + 3 samples swapped, wire-proven; addendum: asc/desc+multi promoted into table, raw-resource IGNORES assetOrder (DIS-07 sentence corrected) |
| DIS-12 | named-query syntax table `s3` row example typo | DOC-WRONG (STYLE) | doc | mechanical, merged PR #6 |
| DIS-13 | named-query model carries `[Unstable]`/`[Obsolete]` | CODE-WRONG (cleanup) | code | mechanical, merged #1235 |
| DIS-14 | EntryPoint docs show `queue` & `deliveryChannelPolicies`; model emits neither | DOC-WRONG / CODE-MISSING | doc / code / rfc | ruled (b′) session 4: deliveryChannelPolicies dropped (no route, 404); queue link added PR **#1282**; docs released-truthful now, twin release-gated |
| DIS-15 | EntryPoint emits legacy imageOptimisation/thumbnailPolicies | CODE-WRONG (cleanup) | code | RESOLVED by XC-07 (#1237) |
| DIS-16 | EntryPoint emits `portalRoles` — undocumented | DOC-MISSING | doc / code | ruled (a) session 4: PREMISE OVERTURNED — portalRoles always 404'd; dead link + orphaned vocab class removed PR **#1284** (breaking); docs correctly silent |
| DIS-17 | EntryPoint scratch note is stale/incorrect | STALE-SCRATCH | doc (scratch) | ruled (a) session 4: scratch rewritten to current state; PROV-01 closed (dropped), PROV-02 closed (presets already in delivery-channels.mdx) |
| DIS-18 | size-restrictions documents openMaxWidth + substitute (absent) | DOC-WRONG | doc / rfc | RESOLVED BY CASCADE (SPA-01, session 2): pages rewritten, prose preserved in scratch, ADR ticket #1249 — see card |
| DIS-19 | single-asset-manifest examples partly unverified | DESIGN | doc / sample | DEFERRED session 4: PO to verify outside the sprint; feasibility scout preserved (adjunct/file/no-channel verifiable now; AV needs fixtures + stage pipeline) |
| DIS-20 | broken `../iiif` links (page not yet ported) | DOC-MISSING (link) | doc | ruled (c) session 4: three live 404 links neutralised (incl. registering-assets, missed by card); re-link notes in scratch; iiif.mdx port scheduled by PO outside sprint |
| DIS-21 | collections.mdx host inconsistency in example JSON | STYLE | doc | mechanical, merged PR #6 |
| DIS-22 | *(new 08-03)* Batch endpoints support asset-query syntax — page omits them | DOC-MISSING | doc | ruled (a) session 4: both batch endpoints added to applicable list (wire-verified, released); cross-refs in batch.mdx; boundary comment on #960 |
| DIS-23 | *(new 08-03)* Versioned iiif-resource paths + Accept negotiation undocumented | DOC-MISSING | doc | ruled (b) session 4: v2/v3 segment + Accept negotiation documented on named-queries AND single-asset-manifest (adjacent gap folded in); all wire-confirmed |
| DIS-24 | *(new 08-03)* entrypoint.mdx uses production hostname in examples | STYLE | doc | mechanical, merged PR #6 |
| DIS-25 | *(new 08-03)* single-asset-manifest "always a Choice" wrong; no-transcode AV = no canvas | DOC-WRONG | doc / code | docs fixed + no-canvas documented (PR #9) |
| DIS-26 | *(new 08-03)* "thumbs channel serves only open content" — unsourced claim | DOC-WRONG? ⚠verify | doc | ruled (a) session 4: 'no thumbnails produced' FALSE (auth-location thumbs generated, never served); Aside tightened to wire-proven 404 behaviour; second sentence confirmed |
| DIS-27 | *(new 08-06, session 0)* NamedQuery global/template share JsonProperty Order 11 | STYLE | code | ruled (a) session 4: template → Order 12, PR **#1286** (byte-identical output); last known ACC-07-class duplicate |

### Session 5 · Adjuncts — [file](./session-5-adjuncts.md)

| ID | Title | Type | Track | Ruling (live) |
|:--|:--|:--|:--|:--|
| ADJ-01 | `content` sub-resource (POST/GET binary) not implemented | CODE-MISSING | code / rfc / defer | ✅ (a) leave parked; tracked by protagonist #1140; scratch is restore source |
| ADJ-02 | Live mdx still shows `content` in example GET responses | DOC-WRONG | doc | ✅ (a) `content` stripped from 3 examples + paragraph; text preserved in scratch |
| ADJ-03 | `roles` field not implemented | CODE-MISSING | doc / code / rfc / defer | ✅ (a) roles prose parked in scratch (#1141); live caution: adjuncts served openly |
| ADJ-04 | `creator` field not implemented | CODE-MISSING | doc / code / defer | ✅ (c) deferred with pipelines; prose parked in scratch; note on private-protagonist #13 (no new issue) |
| ADJ-05 | `source` field not implemented | CODE-MISSING | doc / code / defer | |
| ADJ-06 | null `iiifLink` / `otherAdjuncts` not implemented | CODE-MISSING | code / defer | |
| ADJ-07 | `label` required vs recommended (parked design Q) | DESIGN | code / doc | |
| ADJ-08 | `asset` back-link emitted but undocumented | DOC-MISSING | doc / code | |
| ADJ-09 | `mediaType` required, but example + sample omit it on AnnotationPage | DOC-WRONG + sample | doc / sample | sample merged PR #7; mdx example open |
| ADJ-10 | `@type` must be AnnotationPage when iiifLink=annotations — undoc'd | DOC-MISSING | doc / code | |
| ADJ-11 | Bulk-delete `POST /customers/{c}/deleteAdjuncts` undocumented | DOC-MISSING | doc / sample | note: annotation fixed #1234; doc + sample open |
| ADJ-12 | DELETE `?deleteFrom=` query parameter undocumented | DOC-MISSING | doc | |
| ADJ-13 | `size = -1` while unprocessed — code uses null | DOC-WRONG (low conf) | doc / code | |
| ADJ-14 | POST of single adjunct returns a HydraCollection | DOC-MISSING (clarify) | doc / sample / code | |
| ADJ-15 | Samples flagged "not implemented" though they now work | STALE-SCRATCH / STYLE | sample | addendum merged PR #7; caveat-narrowing open |
| ADJ-16 | Intro example + pipeline narrative aspirational | DOC-WRONG (composite) | doc | |
| ADJ-17 | *(new 08-03)* New `### batch` section carries asset-page copy-paste bugs | DOC-WRONG | doc | mechanical, merged PR #5 |
| ADJ-18 | *(new 08-03)* Adjunct POST 409 / PUT-update 200 undocumented | DOC-MISSING | doc | mechanical, merged PR #5 |

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
| AUTH-12 | `customer.authServices` link — verify and reconcile | DOC-WRONG | doc / code | RESOLVED by XC-07: links removed (#1237); revisit with auth API |

## Companion artefacts (separate punch-lists)

### Python sample fixes (factual, low-controversy — can be applied once decisions ratified)

> **2026-08-05:** items 1, 2, 4, 5 and 6 applied and merged in public-docs PR #7
> (mechanical track batch D3), which also fixed the PRO-11 `asset`-field bug in both
> adjunct queue-POST samples. Item 3 (`update_credentials.py` orphan) is borderline
> SPA-19 and remains untouched pending the room's call.
1. `p13_adjuncts/iiif_link_adjuncts.py` — AnnotationPage adjunct missing required `mediaType`.
2. `p12_origin_strategies/get_put_delete_origin_strategy.py` — `put_origin_strategy` docstring wrongly says credentials are not updated (full-object PUT does update; basic-http/sftp only).
3. `p12_origin_strategies/update_credentials.py` — orphan describing a non-existent `/credentials` sub-resource; delete or rewrite to full-object PUT.
4. `p15_asset_queries/asset_queries.py` — `get_images_ordered` docstring "ordering not supported" is stale (ordering works); pairs with the asset-queries doc promotion (DIS theme).
5. `p07_asset/get_put_patch_delete_asset.py:75` — `# Expected: DELETE 200 OK` → **204 No Content** (`ImageController.cs:201`).
6. `p11_delivery_channels/get_put_patch_delete_policy.py:66` — `# Expected: DELETE 202 Accepted` → **204 No Content** (`HandleDelete`→`NoContent()`).

> Items 5 & 6 also feed cross-cutting card(s) on DELETE status semantics (see session-0).
