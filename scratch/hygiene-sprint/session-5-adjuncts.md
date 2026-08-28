# Hygiene sprint · Session 5 · Adjuncts

## Scope

Theme: **Adjuncts** — asset side-files (ALTO/METS XML, IIIF annotations, renderings, captions, any
linked data). Surfaces reviewed in full:

- Docs: `src/src/content/docs/api-doc/adjuncts.mdx` (the live page)
- Scratch: `scratch/api-doc/adjuncts.md` (parked, unimplemented prose)
- Samples: `dlcs-docs-client/p13_adjuncts/` (6 files)
- Old Nextra source: `C:\git\dlcs\docs\pages\api-doc\adjuncts.mdx`
- API code (protagonist), all of `API/Features/Adjuncts/*` plus:
  - `API/Features/Customer/CustomerAdjunctsController.cs`
  - `API/Converters/AdjunctConverter.cs`
  - `DLCS.HydraModel/Adjunct.cs`
  - `DLCS.Model/Assets/Adjunct.cs`, `AdjunctX.cs`, `AdjunctBatch*.cs`

A previous quick check wrongly concluded "no adjunct controller exists". That is **false**:
`AdjunctsController.cs` and `HydraAdjunctValidator.cs` both exist and adjuncts are **partially
implemented** (full external/origin CRUD; no content endpoint, no roles/creator/source).

---

## Implemented today (verified)

**Routes — `AdjunctsController.cs`** (route base `/customers/{customerId}/spaces/{spaceId}/images/{imageId}/adjuncts`):

| Verb | Route | Returns | Cite |
|:---|:---|:---|:---|
| GET | `/adjuncts` | 200 `HydraCollection<Adjunct>`, 404 | AdjunctsController.cs:32-45 |
| GET | `/adjuncts/{adjunctId}` | 200 `Adjunct`, 404 | :51-64 |
| POST | `/adjuncts` | 200/201 `Adjunct` **or** `HydraCollection<Adjunct>`; body via `FlexCollection<Adjunct>` (single object, array, or Hydra collection); empty body → 400; **⟳ 2026-08-03: POST of an already-existing adjunct id → 409 Conflict** (`CreateOrUpdateAdjunct.cs:85-87`, CreateOnly path) | :70-86 |
| PUT | `/adjuncts/{adjunctId}` | 200 (and 201 on create via HandleUpsert); body-`id` must match URL else 400; **⟳ 2026-08-03: PUT-update returns 200/Updated** (`CreateOrUpdateAdjunct.cs:121-122`) — adjuncts.mdx:133/202 mention only 201 | :92-108 |
| DELETE | `/adjuncts/{adjunctId}` | **204**, 404; accepts `?deleteFrom=` query (ImageCacheType, comma list) | :114-123 |

**Bulk delete — `CustomerAdjunctsController.cs`**: `POST /customers/{customerId}/deleteAdjuncts`
(Hydra collection of `{ id, adjunct: [...] }`), returns 204 / 400 / 404. CustomerAdjunctsController.cs:39-69.

**Validation rules actually enforced — `HydraAdjunctValidator.cs`:**
- `iiifLink` **required** (:14-15) and must be one of `seeAlso`/`annotations`/`rendering`/`inlineAnnotation` (:16-18, enum `IIIFLinkType`).
- `mediaType` **required** (:20-21).
- **Exactly one** of `origin` / `externalId` — required, not both (:23-25). Both well-formed-URI checked (:27-35).
- `id` (ModelId) NotEmpty (:37-39), ≤ 200 chars (`Adjunct.MaxIdLength`, :41-43), no restricted chars (:45-47).
- `@type` required (:49-51); when `iiifLink == annotations`, `@type` must be `"AnnotationPage"` (:58-61).
- each `language` value ≤ 10 chars (:54-56).
- **NOT enforced:** `label` (confirms scratch note).

**Persistence / conversion:**
- Hosted (has `origin`) vs external (has `externalId`) decided by `IsHosted()` = origin non-empty (AdjunctX.cs:9).
- Create hosted: `Size = null`, `SetFieldsForIngestion()` sets `Ingesting=true, Error=""`, increments stored-adjunct count (AdjunctUpsertService.cs:81-88; AdjunctConverter.cs:82-86; DeliverableX.cs:10-14).
- External: `Finished` set immediately, no Engine involvement (AdjunctUpsertService.cs:91-95).
- `ToHydra` emits: `@type, id, asset, mediaType, iiifLink, profile, label, language, externalId, publicId, origin, size, created, finished, error, motivation, provides, ingesting, batch` (AdjunctConverter.cs:102-125).
- `publicId` = `externalId` for external, else managed `{ResourceRoot}adjuncts/{customer}/{space}/{asset}/{id}` (customer-before-space order — matches current mdx) (:114).
- `batch` link emitted only when `Batch` has a value (:122-124).

**Hydra model fields present** (`DLCS.HydraModel/Adjunct.cs`): Type, ModelId(`id`), Asset, MediaType,
IIIFLink, Profile, Label, Language, ExternalId, PublicId, Size, Created, Finished, Origin, Motivation,
Provides, Ingesting, Error, Batch.
**Absent from model entirely:** `roles`, `creator`, `source`, `content`.

---

## ⟳ Development update (2026-08-03) — protagonist has moved since these cards were written

Checked against protagonist `main` (v1.13.2) and `develop`. Cards below carry inline updates
where affected; the headline changes:

- **Adjunct queue endpoints built** (PR #1228, on `develop` only, unreleased): GET
  `/adjunctQueue` (new `CustomerAdjunctQueue` hydra model), `/batches`, `/active`, `/recent`,
  and per-batch `/current` + `/adjuncts` collections. Issues #1157/#1158/#1160 closed; #1166
  open for the residue. Full detail, residual gaps and sample impact are in **PRO-08**
  (session 3), which now owns that story.
- **`Optimised` flag added to the `Adjunct` entity** (PR #1220, on `main`, DB migration
  2026-07-09). **Not** exposed on the Hydra model — no new wire field on adjunct responses —
  but it changes storage accounting: optimised (e.g. s3-ambient) adjuncts count toward
  `numberOfStoredAdjuncts` but contribute **0** to `totalSizeOfStoredAdjuncts` / `adjunctSize`
  (see ACC-06 update, session 1). Issue #1218 (store size for all hosted adjuncts) closed;
  #1127 / #1121 remain open.
- **Size is now recorded for every hosted adjunct, including optimised/s3-ambient ones**
  (`Engine/Ingest/File/FileChannelWorker.RecordAdjunctSizeChange`), and
  `ImageStorage.AdjunctSize` is a running tally that asset reingest no longer overwrites
  (`ImageStorageX.UpsertImageStorageRecord`; deltas applied via `AdjustAdjunctSize`, signed,
  clamped ≥ 0). Affects **ADJ-13** — see its inline update.
- Single and bulk delete (`DeleteAdjunct`, `DeleteMultipleAdjunctsById`) now apply
  optimised-aware storage decrements; the endpoint surface for **ADJ-11**/**ADJ-12** is
  otherwise unchanged. Open bug #1207 (delete/update null-checks the origin bucket instead of
  the storage bucket) is still open — relevant when delete semantics are discussed.
- Several `AdjunctUpsertService` / Engine line references in the cards below have shifted —
  re-cite against current `develop` before quoting file:line in the room.

---

**⟳ SESSION 5 PRE-FLIGHT 2026-08-26.** Repos synced; branch `hygiene/session-5` cut from main (public-docs
main @ 84c033e = PR #16 merge). All four session-4 protagonist PRs (#1281/#1282/#1284/#1286) merged into develop
2026-08-19; public-docs PR #16 merged 2026-08-26. Release still **v1.13.2** — every release-gated twin stays parked
(incl. the adjunct-queue/adjunct doc twins from sessions 1–3), and docs main describes released behaviour only.
hydra-model-flags re-baselined @develop **1a77352a**: only the expected session-4 deltas (EntryPoint −`portalRoles`
+`queue`; `PortalRole` class removed); the **Adjunct / AdjunctBatch / CustomerAdjunctQueue tables are byte-identical**
to the 08-19 baseline. (Dump tool retargeted net8.0→net10.0 — protagonist develop now builds on .NET 10.) Adjunct-surface
code freshness: `API/Features/Adjuncts/*`, `CustomerAdjunctsController.cs`, `AdjunctQueues/*` last touched 2026-08-05
(our #1234 annotation fix), `AdjunctConverter.cs` 2026-04-01, `DLCS.Model/Assets/Adjunct*.cs` 2026-07-09 (#1220),
`Engine/Ingest/File` 2026-07-10, `DLCS.HydraModel/Adjunct.cs` 2026-08-17 (#1276 twin fix) — **all card premises and
`file:line` cites below remain valid** (mdx line drift ≤4 lines: e.g. roles example :157 not :161, `size` prose :365
not :363). Issue counts 151/65/8; adjunct-issue map: #1141 → ADJ-03, #1140 → ADJ-01, #1142 → ADJ-06, #1207 → ADJ-12
adjacency, #1128 open; #1127/#1121/#1166 closed. develop's big non-adjunct moves (.NET 10, netvips, #1289 raw-resource
assetOrder fix for #1285) are noted in `_issues-rfcs.md`. Local merged hygiene branches pruned in both repos; the
remote `hygiene/dis-*` (protagonist) and `hygiene/session-0/2/3/4` (public-docs) branches still need deleting by hand.
**Read-only released-wire sweep (stage, v1.13.2, docs space 98765 — 15 assets):**
- Exactly one asset carries an adjunct (`put-example-1-rusty-boat` → `external-alto.xml`, external/`seeAlso`).
  GET collection member keys: `@context @id @type asset created externalId finished id iiifLink label language
  mediaType profile publicId size` — **`asset` is emitted** (ADJ-08 premise ✓); **no `content`, `roles`, `creator`,
  `source`** (ADJ-02/03/04/05/16 premises ✓); **null fields are omitted on the wire** (`origin`, `batch`, `ingesting`,
  `error`, `motivation`, `provides` absent for this external adjunct) — relevant to ADJ-13's "size: null" wording
  (an in-flight hosted adjunct would show *no* `size` key, not `null`).
- No hosted (origin-based) adjunct exists in the docs space, so the ADJ-13 in-flight `size` value and the ADJ-14
  POST-envelope shape remain **in-room mutating checks** (origin_adjunct.py / multiple_adjuncts.py runs).
- `GET /customers/15/adjunctQueue` → **405** on the released API (not 404): the adjunct-queue surface (PR #1228) is
  develop-only, as the dev-update section says.
**Open cards to rule (14):** ADJ-01 02 03 04 05 06 07 08 10 11 12 13 14 16; partial ADJ-09 (mdx example half) and
ADJ-15 (caveat narrowing after a live run); ADJ-17/18 mechanical, done. Session 5 not yet started — awaiting PO to
open the first card.

---

## Resolved (Category A) — already correct in current mdx

- `publicId` path order is `customer/space` (e.g. `/adjuncts/2/5/...`) — matches `ToHydra` (:114). Old Nextra had it reversed (`5/2`).
- `mediaType` marked **required** in the field-usage table — matches validator (:20). Old Nextra said "recommended".
- `iiifLink` documented as **required** — matches validator (:14). Old Nextra said "recommended" and allowed null.
- `label` table cells softened from "required" to "recommended" — matches validator (label not enforced). See ADJ-07 for the parked design question.
- `content` separate-supply workflow and the `content` field section moved out to `scratch/api-doc/adjuncts.md` — content endpoint genuinely absent. See ADJ-01/ADJ-02.

---

## Cards

### ADJ-01 · `content` sub-resource (POST/GET binary) not implemented
- **Theme:** Adjuncts
- **Surfaces:** scratch/api-doc/adjuncts.md §"Creating an adjunct by supplying content separately", §"content field" · API/Features/Adjuncts/* (no `content` route); grep for `content` in Features/Adjuncts → 0 hits
- **Type:** CODE-MISSING (scratch correctly parks it)
- **Docs say:** A third creation mechanism: create the resource, then `POST .../adjuncts/{id}/content` with a binary body; `GET .../content` returns the same bytes as `publicId` but auth'd by API key not roles.
- **Original-doc nuance:** Old Nextra §"content" (adjuncts.mdx:410-416): *"A link to the adjunct content ... The other use of `content` is to _supply_ the bytes of an adjunct, via HTTP POST. If created without an `origin` ... the adjunct will have no content and size 0, _until_ the bytes ... are POSTed to this URL."* (full block preserved in scratch lines 63-86)
- **Code does:** No `content` action on `AdjunctsController`; `ToHydra` never emits a `content` property (AdjunctConverter.cs:102-125); validator requires exactly one of origin/externalId so a "neither" adjunct is rejected (HydraAdjunctValidator.cs:23-25).
- **Issues/RFCs:** ⟳ 2026-08-26: protagonist **#1140** (open) is this feature; RFC 023 silent on API-supplied bytes
- **Decision needed:** Whether to keep the content endpoint parked or schedule it; the validator's exactly-one-of rule must change to permit a content-only adjunct.
- **Options:** (a) leave parked, scratch is sufficient (b) implement content POST/GET + relax validator + restore docs (c) RFC the upload design first
- **Possible outputs:** code / RFC / defer
- **Who's needed:** API owner
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — leave parked. The content endpoint stays out of the live docs; `scratch/api-doc/adjuncts.md` (content-supply section, `content` field, PROV-15 fragments) is the restore source, now pointing at protagonist **#1140** ("Adjuncts consisting of binary content", open since 2026-03-18) as the tracking ticket — no new issue or RFC minted. Design notes for whoever picks #1140 up: validator's exactly-one-of origin/externalId must become at-most-one; RFC 023 notes no content-vs-@type validation exists. Cascade: ADJ-02 → strip `content` from live examples; ADJ-16 headline example loses `content`; `content_adjunct.py` handled under ADJ-15.

### ADJ-02 · Live mdx still shows `content` in example GET responses
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §intro collection example (lines 56, 76), §"Creating an adjunct from an origin" GET response (line 228), and prose at line 233 · AdjunctConverter.cs:102-125
- **Type:** DOC-WRONG
- **Docs say:** The example GET/collection JSON includes a `"content": ".../content"` property on each hosted adjunct, and prose explains the `content` URL.
- **Original-doc nuance:** "—" (inherited from old Nextra which fully documented content)
- **Code does:** `ToHydra` does not emit `content`; the endpoint does not exist (see ADJ-01). So a real GET will not contain `content`.
- **Issues/RFCs:** to check
- **Decision needed:** Bring the published examples in line with what the API returns while ADJ-01 is parked.
- **Options:** (a) remove `content` from the three example payloads + the explanatory sentence (b) leave as aspirational with an Aside that content is not yet returned (c) wait for ADJ-01
- **Possible outputs:** doc
- **Who's needed:** docs author
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — `content` removed from all three example payloads (intro collection ×2, origin-create GET) and the explanatory paragraph deleted from adjuncts.mdx; paragraph text already preserved verbatim in `scratch/api-doc/adjuncts.md` §"content field". Live page now contains no `content` property. Note: the removed paragraph also carried `roles`-dependent prose — that leaves with it (see ADJ-03).

### ADJ-03 · `roles` field not implemented
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §intro example (roles:[] lines 47,65), §"Creating an adjunct that links to an external URL" (line 161), §"Registering multiple adjuncts" + auth Aside (lines 268-272), §"roles" (337-341), field table row `roles` (548) · DLCS.HydraModel/Adjunct.cs (no Roles property); DLCS.Model/Assets/Adjunct.cs (no Roles)
- **Type:** CODE-MISSING
- **Docs say:** `roles` works like `asset.roles`; if set the platform enforces IIIF Auth 2.0; *"Unless you explicitly provide `roles` as an empty array, adjuncts will be assigned the roles of their parent asset."*; for auth, adjuncts behave like assets on the File delivery channel.
- **Original-doc nuance:** Old Nextra §roles (adjuncts.mdx:381-385) identical; auth IMPORTANT callout (321-322).
- **Code does:** No `roles`/`Roles` anywhere in the adjunct model, validator, converter or examples in code. Field is silently dropped on input and never emitted.
- **Issues/RFCs:** ⟳ 2026-08-26: protagonist **#1141** (open, one-liner "Support roles etc, same as Assets"); Orchestrator explicitly not auth-covered
- **Decision needed:** Whether to implement adjunct roles + parent-inheritance now, or move all roles prose to scratch until then.
- **Options:** (a) move roles prose/examples to scratch, mark unimplemented (b) implement roles end-to-end (c) RFC adjunct auth design
- **Possible outputs:** doc / code / RFC / defer
- **Who's needed:** API owner + docs author
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — all seven `roles` surfaces removed from adjuncts.mdx (4 example lines, :159 paragraph, :265 paragraph + File-channel Aside, `### roles` section, `publicId` clause, field-usage row) and preserved verbatim in `scratch/api-doc/adjuncts.md` §roles with a protagonist **#1141** pointer. Replaced by a live **caution**: adjuncts are not access-controlled — hosted adjuncts served openly regardless of parent-asset roles, no IIIF Auth services emitted, `roles` on input ignored/not stored (`OrchestrationAdjunct.cs:42-44`, `AdjunctRequestHandler.cs:59`). Parent-role inheritance flagged in scratch as design intent to re-decide at implementation. Samples send no `roles` → no sample change (XC-10 satisfied). Cascade: ADJ-16 example already stripped of roles; session-6 AUTH cluster to note #1141.

### ADJ-04 · `creator` field not implemented
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §intro example (`creator` line 66) + narrative (84), §mediaType/§profile cross-refs (298,315), §"creator" (343-349), field table row `creator` (549) · DLCS.HydraModel/Adjunct.cs (no Creator)
- **Type:** CODE-MISSING
- **Docs say:** `creator` is a URI naming the process that made (or should make) the adjunct; for self-supplied adjuncts it is stored for reference; for platform pipelines it names a known pipeline and enqueues processing.
- **Original-doc nuance:** Old Nextra §creator (adjuncts.mdx:387-393) identical.
- **Code does:** No `creator`/`Creator` property in model, validator, or converter. The whole pipeline-creation path is unimplemented (page Aside already defers pipelines to a not-yet-ported page).
- **Issues/RFCs:** ⟳ 2026-08-26: dlcs/private-protagonist **#13** (pipeline epic) is the home; nothing in the public repos
- **Decision needed:** Whether `creator` (storage-only, the self-supplied use) should exist independently of the unbuilt pipeline feature.
- **Options:** (a) move creator prose to scratch (b) add a store-only `creator` field now (c) defer with pipelines
- **Possible outputs:** doc / code / defer
- **Who's needed:** API owner
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(c)** — defer with pipelines; **PO instruction: no new issue — text added as a comment to dlcs/private-protagonist #13 ("Adjunct-producing pipeline" epic, open since 2023-06)**. `### creator` section, the `### profile` creator sentence and the field-usage row removed from adjuncts.mdx and preserved verbatim in `scratch/api-doc/adjuncts.md` §creator; the intro example's `creator` line + :80 narrative left for ADJ-16's rewrite. The store-only-vs-pipeline design question is recorded in the #13 comment. Samples never sent `creator` → no sample change.

### ADJ-05 · `source` field not implemented
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §intro example (`source` line 67) + narrative (84), §"source" (351-355) · DLCS.HydraModel/Adjunct.cs (no Source)
- **Type:** CODE-MISSING
- **Docs say:** `source` points at the asset or another adjunct used to derive this one; platform-created adjuncts always get it set; self-supplied adjuncts may set it for reference.
- **Original-doc nuance:** Old Nextra §source (adjuncts.mdx:396-400) identical.
- **Code does:** No `source`/`Source` in model, validator or converter.
- **Issues/RFCs:** ⟳ 2026-08-26: dlcs/private-protagonist **#13** (with creator)
- **Decision needed:** Same as creator — store-only field vs defer with pipelines.
- **Options:** (a) move source prose to scratch (b) add store-only `source` now (c) defer with pipelines
- **Possible outputs:** doc / code / defer
- **Who's needed:** API owner
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(c)** — same treatment as ADJ-04: deferred with pipelines, docs note appended as a second comment on dlcs/private-protagonist #13 (no new issue). `### source` section + field-usage row removed from adjuncts.mdx and preserved in `scratch/api-doc/adjuncts.md` §source; intro example :64 + narrative :80 left for ADJ-16. Samples never sent `source`.

### ADJ-06 · null `iiifLink` / `otherAdjuncts` not implemented
- **Theme:** Adjuncts
- **Surfaces:** scratch/api-doc/adjuncts.md §"No iiifLink / otherAdjuncts" (lines 89-120) · HydraAdjunctValidator.cs:14-18 · also single-asset-manifest.mdx (Canvas `otherAdjuncts`)
- **Type:** CODE-MISSING (scratch correctly parks it)
- **Docs say (parked):** `iiifLink` may be null/absent; such adjuncts appear under a non-standard `otherAdjuncts` Canvas property (defined in the single-asset-manifest @context); consumers should strip it.
- **Original-doc nuance:** Old Nextra §iiifLink (adjuncts.mdx:419-421, 541-554) documents null `iiifLink`, the 5th example adjunct, and the `otherAdjuncts` canvas output — all preserved in scratch.
- **Code does:** Validator makes `iiifLink` NotEmpty and constrains it to the four enum values (:14-18); a null/absent value is a 400. No `otherAdjuncts` support.
- **Issues/RFCs:** ⟳ 2026-08-26: protagonist **#1142** (open) ← digirati-co-uk/iiif-net #62
- **Decision needed:** Keep parked, or implement optional `iiifLink` + `otherAdjuncts`.
- **Options:** (a) leave parked (b) make `iiifLink` optional + emit `otherAdjuncts` (c) RFC
- **Possible outputs:** code / defer
- **Who's needed:** API owner
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — leave parked. Scratch section now points at protagonist **#1142** (+ upstream digirati-co-uk/iiif-net #62); sample comment in `iiif_link_adjuncts.py` cites the ticket instead of the card id (PO rule: no hygiene-card refs a later reader can't resolve). Live page and single-asset-manifest.mdx already clean. No new issue.

### ADJ-07 · `label` required vs recommended (parked design question)
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §"label" (317-319), field table `label` row (544) · scratch/api-doc/adjuncts.md §"label requirement" (124-130) · HydraAdjunctValidator.cs (no Label rule)
- **Type:** DESIGN (with CODE-WRONG or DOC option)
- **Docs say (now):** "recommended"; default label assigned for platform-generated adjuncts.
- **Original-doc nuance (removed):** *"It is recommended to always supply this, and is required when supplying the adjunct yourself."* (old Nextra adjuncts.mdx:363)
- **Code does:** Validator enforces no `label` rule; AdjunctConverter maps `Label` straight through, nullable (AdjunctConverter.cs:75). So label is genuinely optional today — docs already match.
- **Issues/RFCs:** to check
- **Decision needed:** Should the API require `label` when the caller supplies the adjunct? If yes → add `RuleFor(a => a.Label).NotEmpty()` and restore "required" in prose+table.
- **Options:** (a) keep optional/"recommended" (status quo) (b) enforce required for the 4 self-supply scenarios + restore docs (c) require only for non-pipeline creates
- **Possible outputs:** code / doc
- **Who's needed:** API owner + docs author
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — `label` stays optional/"recommended"; no validator change. Doc tweak: `### label` now says why it is recommended (manifest seeAlso/rendering/annotations entries carry no `label` without it — `ManifestV3Builder.cs:513,564`). Scratch open question closed. Samples all send label → sample-neutral.

### ADJ-08 · `asset` back-link emitted but undocumented
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §"Adjunct fields" (no `asset` entry; not in any example payload) · DLCS.HydraModel/Adjunct.cs:34-37 · AdjunctConverter.cs:111
- **Type:** DOC-MISSING
- **Docs say:** Nothing — `asset` is absent from the field list and every example response.
- **Original-doc nuance:** "—"
- **Code does:** Hydra model has an `asset` property; `ToHydra` always populates it with the asset `@id` (`{base}/customers/{c}/spaces/{s}/images/{asset}`). So every GET returns an `asset` field the docs never mention. *(⟳ 2026-08-03: adjuncts.mdx has since gained a `### batch` section (:365-389), so `asset` is now the **only** emitted-but-undocumented adjunct field — and that new batch section has its own copy-paste bugs, see ADJ-17.)*
- **Issues/RFCs:** to check
- **Decision needed:** Document `asset` (and add to example payloads).
- **Options:** (a) add an `### asset` field section + include in examples (b) leave undocumented (c) treat as internal and suppress in output
- **Possible outputs:** doc / code
- **Who's needed:** docs author
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — `### asset` section added after `### id` (Order 11 parity) with XC-09 table `vocab:Adjunct | xsd:string | False | False` (matches dump); `asset` inserted into all four response examples; field-usage row added (ignored on per-asset endpoints, required per member via queue). Presentation finding: `asset` is not only a back-link — it is the **required per-member input on `/adjunctQueue` POSTs** (`AdjunctBatchPostValidator.cs:27-36`, `AdjunctConverter.ToDlcsModel(hydra, customerId)` :24-38: short form or URI, same-customer, unique asset/id pairs) and the queues page had never documented it (PRO-11 fixed the sample only) → sentence + cross-link added under the adjunct-queue POST row in queues.mdx. Sample-neutral (p08 queue sample already sends `asset`; p13 per-asset samples correctly don't).

### ADJ-09 · `mediaType` required, but iiifLink example + sample omit it on the AnnotationPage adjunct
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §iiifLink example, the `annotations-from-origin.json` block (lines 411-418, no `mediaType`) · dlcs-docs-client/p13_adjuncts/iiif_link_adjuncts.py:39-46 (same omission) · HydraAdjunctValidator.cs:20-21
- **Type:** DOC-WRONG (+ sample bug)
- **Docs say:** The field table marks `mediaType` required, but the doc's own multi-adjunct example and the matching sample leave `mediaType` off the `AnnotationPage` adjunct.
- **Original-doc nuance:** Old Nextra example (adjuncts.mdx:437-444) has the same omission — inherited.
- **Code does:** `mediaType` NotEmpty for every adjunct (:20-21), so that adjunct would 400. (`application/json` would be the natural value.)
- **Issues/RFCs:** to check
- **Decision needed:** Add `mediaType` to the example and the sample so they pass validation.
- **Options:** (a) add `"mediaType": "application/json"` in both mdx example and sample (b) doc only (c) sample only
- **Possible outputs:** doc / sample
- **Who's needed:** docs author
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — `"mediaType": "application/json"` added to the AnnotationPage member of the mdx iiifLink example; sample half was merged earlier in public-docs PR #7 (2026-08-05). Card closed.

### ADJ-10 · `@type` must be `AnnotationPage` when `iiifLink=annotations` — undocumented rule
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §"iiifLink" / §"@type" (no mention) · HydraAdjunctValidator.cs:58-61
- **Type:** DOC-MISSING
- **Docs say:** `@type` should use IIIF types but is otherwise free; no stated constraint tying it to `iiifLink`.
- **Original-doc nuance:** "—"
- **Code does:** When `iiifLink == "annotations"`, validator requires `@type == "AnnotationPage"`, else 400.
- **Issues/RFCs:** to check
- **Decision needed:** Document this constraint (and consider whether `inlineAnnotation` should have a parallel rule — it currently does not).
- **Options:** (a) note the rule under `iiifLink`/`@type` (b) leave undocumented (c) also add an `inlineAnnotation` type rule in code for symmetry
- **Possible outputs:** doc / code
- **Who's needed:** docs author + API owner
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — rule documented under `### @type` (with the why: adjunct is placed directly in Canvas `annotations`, `ManifestV3Builder.cs:508-514`), cross-noted under `### iiifLink`, and the intro's "they can be anything" qualified. **Option (c) considered and rejected on evidence:** `seeAlso`/`rendering`/`inlineAnnotation` all pass `@type` through `CreateExternalResource(adjunct)` (`:556-558`) — an inline-annotation adjunct is an Annotation *body* and may legitimately be any IIIF type, so a symmetric rule would be wrong. No code change.

### ADJ-11 · Bulk-delete endpoint `POST /customers/{c}/deleteAdjuncts` undocumented
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx (no mention) · CustomerAdjunctsController.cs:39-69
- **Type:** DOC-MISSING
- **Docs say:** Nothing. Page only covers per-adjunct DELETE.
- **Original-doc nuance:** "—"
- **Code does:** Implemented bulk delete: body is a Hydra collection of `{ id: "c/s/asset", adjunct: ["ocr.txt","mets.xml"] }`, validated by `AdjunctIdListValidator`, supports `?deleteFrom=`, returns 204 (400 if none found).
- **Issues/RFCs:** to check
- **Decision needed:** Whether to document bulk adjunct delete (parallels the bulk asset-delete pattern on the customer/queue pages).
- **Options:** (a) add a "Deleting multiple adjuncts" section + sample (b) leave undocumented for now (c) document under queues/customer page instead
- **Possible outputs:** doc / sample
- **Who's needed:** docs author
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — `## Deleting multiple adjuncts` section added to adjuncts.mdx (ACC-18 template shape; body form, 500 cap, none-found → 400, method table 204/400) + new sample `p13_adjuncts/delete_adjuncts.py`, **run live on released stage: POST 201 → GET 200/200 → deleteAdjuncts 204 → GET 404/404**. **Not release-gated** (unlike ACC-18): the route and its 204 are on v1.13.2; only the annotation changed on develop (#1234). **PO instruction: `deleteFrom` NOT documented — parsed but not implemented for adjuncts** (corroborated by open #1128 "Extend varnish cleanup handler for adjuncts"); cascades to ADJ-12. Forward pointer + the same deleteFrom instruction written into the parked ACC-18 twin (scratch/api-doc/customer.md).

### ADJ-12 · DELETE `?deleteFrom=` query parameter undocumented
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx (no DELETE section at all) · AdjunctsController.cs:117-122; CustomerAdjunctsController.cs:45,57
- **Type:** DOC-MISSING
- **Docs say:** The page never documents the single DELETE verb or its `deleteFrom` option.
- **Original-doc nuance:** "—"
- **Code does:** Both DELETE endpoints accept `?deleteFrom=` parsed by `ImageCacheTypeConverter` (comma-separated cache layers), passed into the delete notification.
- **Issues/RFCs:** to check (cross-ref asset delete `deleteFrom` docs if any)
- **Decision needed:** Document the DELETE verb + `deleteFrom` for adjuncts (consistent with asset delete).
- **Options:** (a) add a DELETE subsection covering 204 + `deleteFrom` (b) link to a shared `deleteFrom` explanation (c) defer
- **Possible outputs:** doc
- **Who's needed:** docs author
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a′)** — new `## HTTP operations` section on adjuncts.mdx (collection: GET 200/404, POST 201/200/400/409 returning a collection; item: GET 200/404, PUT 201/200/400, DELETE 204/404) consolidating ADJ-18's scattered codes, with the 409/PUT-replace and delete-removes-stored-content notes; asset.mdx:464-470 adjuncts table aligned (stale pipelines-era POST label "instructing the platform to create… via OCR" replaced; statuses completed). **`deleteFrom` deliberately NOT documented** (PO, ADJ-11): code-confirmed parsed-but-ignored — `AdjunctDeletedHandler.cs` never reads `DeleteFrom`; parked note in scratch/api-doc/adjuncts.md pointing at #1128. Sample-neutral (every p13 sample already DELETEs; 204 wire-proven today).

### ADJ-13 · `size = -1` while unprocessed — code uses null instead
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §"size" (line 363) · AdjunctUpsertService.cs:84; DeliverableX.cs:10-14; AdjunctConverter.cs:117
- **Type:** DOC-WRONG (low confidence — Engine path not fully traced)
- **Docs say:** *"This will be 0 if no content has been supplied yet, and it will be -1 if the origin has not been fetched or the asset has yet to be processed."*
- **Original-doc nuance:** Same in old Nextra (adjuncts.mdx:406-408).
- **Code does:** On hosted create, `Size` is set to `null` (not -1); `SetFieldsForIngestion` only touches Error/Ingesting. `ToHydra` emits `Size` as-is, so an in-flight adjunct returns `size: null` (omitted), not `-1` or `0`. The `-1` sentinel is not produced anywhere in the adjunct create path examined.
- **⟳ Update 2026-08-03:** the Engine question is now answerable from PR #1220 (on `main`): `FileChannelWorker.RecordAdjunctSizeChange` (`:142-163`) records `Size` for hosted adjuncts once ingested — including optimised-origin ones ("recording size only") — and reingest no longer loses it. One exception *(second pass)*: when an **optimised** adjunct's size cannot be determined, `RecordAdjunctSizeChange` leaves `Size` unchanged (possibly null) and logs a warning (`FileChannelWorker.cs:155-160`) — so "recorded for every hosted adjunct" is almost-always. The `-1` sentinel is still produced **nowhere**; in-flight remains `size: null`. Confidence in "docs wrong, code uses null" is now high, not low. Current cites: hosted create `Size = null` → `AdjunctUpsertService.cs:89`; external→hosted reset → `:64`.
- **Issues/RFCs:** #1218 closed (store size for all hosted adjuncts); #1121 open (recalculator tally)
- **Decision needed:** Confirm the real in-flight `size` value and correct the prose.
- **Options:** (a) verify against Engine + a live ingest, then fix prose (b) change docs to "absent/null until measured" (c) make code emit the documented sentinel
- **Possible outputs:** doc / code
- **Who's needed:** API owner
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — **wire-proven in-room** (stage v1.13.2, hosted origin adjunct `size-probe.xml`): POST 201 response `ingesting: true`, `finished: null`, **no `size` key** (nulls omitted on the wire); GET after ingest `size: 36032`; DELETE 204. `-1`/`0` sentinels never occur. `### size` prose rewritten (absent until stored; then actual byte count; rare optimised-origin case may stay absent; externalId may supply). Original sentinel sentence preserved in scratch/api-doc/adjuncts.md §size with the note that the "0 pre-upload" case belongs to ADJ-01/#1140. Confidence upgraded low → proven. Sample note: `origin_adjunct.py` docstrings still say "content will be populated" → ADJ-15 sweep.

### ADJ-14 · POST of a single adjunct returns a HydraCollection, not a single object
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §"Creating an adjunct..." (shows a GET single-object representation as the result; no POST response body) · AdjunctsController.cs:152-162
- **Type:** DOC-MISSING (clarification)
- **Docs say:** After POST "the created adjunct ... looks like this" followed by a single-object GET — implying POST returns a single object.
- **Original-doc nuance:** "—"
- **Code does:** `PostAdjunct` always routes through `CreateOrUpdateAdjunct(isPost: true)`, and `BuildHydraResponse` returns a `HydraCollection<Adjunct>` even for one item; only PUT returns a single object (`adjuncts.Single().ToHydra(...)`).
- **Issues/RFCs:** to check
- **Decision needed:** Clarify in docs/samples that POST always wraps results in a Hydra collection.
- **Options:** (a) add a note + show the collection envelope for POST (b) leave implicit (c) change API to unwrap single POSTs (riskier)
- **Possible outputs:** doc / sample / code
- **Who's needed:** docs author + API owner
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a+)** — docs: both creation walkthroughs now state POST always returns a collection (PUT returns the bare adjunct), with the envelope shown once; operations table Returns column already said so. Samples: `external_adjunct.py` and `origin_adjunct.py` unwrap `r.json()["member"][0]` with a comment; `external_adjunct.py` also gained a leading clean-up DELETE (a leftover adjunct from a previous partial run made the POST 409 — sample now idempotent), run live green (201/200/204/201/200/204). Protagonist: draft PR **#1292** (branch `hygiene/adj-14`, base develop) removes the two single-`Adjunct` `ProducesResponseType` lines on POST and fixes the doc comment — annotation-only, non-breaking, builds clean; wire-proven premise (single POST → `totalItems: 1` collection) recorded in the PR body. Option (c) rejected as breaking.

### ADJ-15 · Samples flagged "not yet implemented" though external/origin/multiple now work
- **Theme:** Adjuncts
- **Surfaces:** dlcs-docs-client/p13_adjuncts/iiif_link_adjuncts.py:102 ("Adjunct support is not yet fully implemented") and similar caveats across the p13 samples · AdjunctsController.cs (CRUD implemented)
- **Type:** STALE-SCRATCH / STYLE
- **Docs say:** Sample header comments warn the whole feature is unimplemented.
- **Original-doc nuance:** "—"
- **Code does:** external-adjunct, origin-adjunct, multiple-adjunct and per-adjunct delete are fully implemented and should run today (subject to ADJ-09 fix); only content-supply (ADJ-01) and null-iiifLink (ADJ-06) genuinely don't work. *(⟳ 2026-08-03: "subject to ADJ-09 fix" is incomplete — `iiif_link_adjuncts.py` fails twice over: adjunct #2 lacks `mediaType` (ADJ-09) AND adjunct #5 (lines 66-73) has no `iiifLink` at all → 400 on ADJ-06 grounds. The 5th adjunct needs removing or parking with the ADJ-06 material before the sample can run.)*
- **Issues/RFCs:** to check
- **Decision needed:** Once the page caveats settle, run the runnable samples and narrow the "not implemented" warnings to content/null-iiifLink only.
- **Options:** (a) update caveats + actually run external/origin/multiple samples (b) leave warnings until full feature lands (c) remove `content_adjunct.py` to scratch alongside ADJ-01
- **Possible outputs:** sample
- **Who's needed:** docs author
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — the four boilerplate "not yet fully implemented" NOTEs removed (external/origin/multiple/iiif_link); `origin_adjunct.py` docstrings no longer promise a `content` property; **all three re-run live green** (origin 201/200×3/204; multiple 201/200×2/204×2; iiif_link 201/200×2/204×4) plus external earlier under ADJ-14. `content_adjunct.py` (unrunnable, never LinkCard-linked) moved to `scratch/api-doc/adjuncts-content_adjunct.py.txt` with a parked-sample header citing #1140 — ADJ-01 restore source; scratch pointer updated. Fifth-adjunct addendum (#1142) merged earlier in PR #7.

### ADJ-16 · Intro collection example + pipeline narrative are aspirational
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx §intro collection example (lines 31-79) and the paragraph "This second adjunct was made by the platform itself..." (line 84) · model lacks creator/source/roles/content
- **Type:** DOC-WRONG (composite of ADJ-02/03/04/05)
- **Docs say:** The opening worked example shows a platform-created second adjunct carrying `creator`, `source`, `roles` and `content` — none of which the API stores or returns today.
- **Original-doc nuance:** Inherited verbatim from old Nextra (adjuncts.mdx:26-79).
- **Code does:** Of those four, only nothing is emitted; `ToHydra` would return this adjunct without creator/source/roles/content. The pipeline-created scenario depends on the unported pipelines feature.
- **Issues/RFCs:** to check
- **Decision needed:** Whether the headline example should reflect today's API (drop the unimplemented fields / second adjunct) or stay aspirational with a clear caveat.
- **Options:** (a) trim example to implemented fields and add an Aside about pipeline-generated adjuncts (b) keep aspirational, caveat each field (c) resolve via ADJ-02/03/04/05 individually then revisit
- **Possible outputs:** doc
- **Who's needed:** docs author
- **Status:** ✅ RULED (session 5, 2026-08-26): option **(a)** — second example member rewritten as a caller-supplied AnnotationPage via `origin` (the `iiif_link_adjuncts.py` shape, live-proven today); `creator`/`source` lines gone (page now has zero occurrences); :80 narrative rewritten for two supplied adjuncts; Aside rewritten (pipelines = planned, **no link**); dead `../pipelines` link in the field-usage intro removed (DIS-20 treatment). Removed text preserved in scratch/api-doc/adjuncts.md §intro example. Page now contains no pipelines links and every example byte is producible on v1.13.2.

### ADJ-17 · New `### batch` section in adjuncts.mdx carries asset-page copy-paste bugs *(added 2026-08-03 verification pass)*
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx:365-389 (`### batch`)
- **Type:** DOC-WRONG (quick fix)
- **Docs say:** Line 366: "The batch this **image** was ingested in"; domain table line 375: domain `vocab:Image`; method table (:383) lists 200 only.
- **Code does:** The field is on the Adjunct (`vocab:Adjunct` domain); the batch GET returns 200 **and 404** (`CustomerAdjunctQueueController` batch route, mirroring batch.mdx:46's asset table).
- **Decision needed:** None of substance — fix "image"→"adjunct", `vocab:Image`→`vocab:Adjunct`, add 404.
- **Possible outputs:** doc
- **Who's needed:** docs author
- **Status:** ☑ mechanical — merged in public-docs PR #5 (2026-08-05)

### ADJ-18 · Adjunct POST/PUT status codes undocumented: 409 on duplicate create, 200 on PUT-update *(added 2026-08-03 verification pass)*
- **Theme:** Adjuncts
- **Surfaces:** adjuncts.mdx:133, :202 (mention 201 only) · `CreateOrUpdateAdjunct.cs:85-87` (CreateOnly → 409 Conflict), `:121-122` (PUT update → 200/Updated)
- **Type:** DOC-MISSING
- **Code does:** POSTing an adjunct whose id already exists on that asset → **409 Conflict**; PUT of an existing adjunct → **200**, not 201. Docs mention only 201 for both flows.
- **Decision needed:** Add the missing codes to the adjuncts page's creation/update flows (part of the ops-table sweep with ACC-12/SPA-20/PRO-13). Cross-ref XC-12 for the multi-member POST case.
- **Possible outputs:** doc
- **Who's needed:** docs author
- **Status:** ☑ mechanical — merged in public-docs PR #5 (2026-08-05); XC-12 (mixed-batch status semantics) still open


---

## ✅ SESSION 5 COMPLETE 2026-08-26

All 18 ADJ cards carry final statuses: ADJ-17/18 mechanical (PR #5), ADJ-09/15 partials finished
today, 14 ruled in-room today. Rulings: ADJ-01 (a), ADJ-02 (a), ADJ-03 (a + live caution),
ADJ-04 (c → #13 comment, no new issue), ADJ-05 (c → #13 comment), ADJ-06 (a), ADJ-07 (a),
ADJ-08 (a + queues cross-link), ADJ-09 (a), ADJ-10 (a; (c) rejected), ADJ-11 (a; deleteFrom
excluded by PO), ADJ-12 (a′), ADJ-13 (a, wire-proven), ADJ-14 (a+ → PR #1292), ADJ-15 (a),
ADJ-16 (a).

**Artefact roster:**
- Protagonist issues raised: **none** (PO: use existing #1140 content, #1141 roles, #1142
  otherAdjuncts, #1128 cleanup/deleteFrom; creator/source on dlcs/private-protagonist **#13**
  "Adjunct-producing pipeline" epic — two docs-note comments posted there).
- Protagonist draft PR: **#1292** (branch `hygiene/adj-14`, base develop) — POST adjunct
  single-`Adjunct` ProducesResponseType lines removed + doc comment; annotation-only, builds clean.
- Live-doc changes (branch `hygiene/session-5`): adjuncts.mdx — `content`/`roles`/`creator`/
  `source` removed; access-control caution; `### asset` section + examples + field-usage row;
  `## HTTP operations` (collection + item tables, 409/PUT notes); `## Deleting multiple adjuncts`
  + LinkCard; `@type`/`iiifLink`/intro AnnotationPage rule; `label` why-recommended; `size`
  prose; POST-collection envelope; intro example rewritten (both members origin-supplied),
  pipelines Aside = planned, dead `../pipelines` links removed. queues.mdx — adjunct-queue POST
  member `asset` requirement + cross-link. asset.mdx — adjuncts table aligned (de-pipelined,
  statuses completed). Site build green.
- Samples: new `p13_adjuncts/delete_adjuncts.py` (live 204); external/origin unwrap POST
  collection; external made idempotent; stale NOTEs removed; origin docstrings no longer mention
  `content`; `content_adjunct.py` → `scratch/api-doc/adjuncts-content_adjunct.py.txt`. All five
  runnable p13 samples run green on stage v1.13.2 today (get_adjunct_batch is develop-only
  surface — not run; PRO-08).
- Scratch (`scratch/api-doc/adjuncts.md`): sections for roles, creator, source, size sentinels,
  intro example, deleteFrom; ADJ-01/06 sections pointed at #1140/#1142; label question closed.
  `customer.md` ACC-18 twin: ADJ-11 live pointer + PO deleteFrom instruction.
- Wire evidence gathered today (stage v1.13.2): adjunct member keys (no content/roles/creator/
  source; `asset` present; nulls omitted); adjunctQueue → 405 on released; in-flight hosted
  adjunct has no `size` key, `ingesting: true`; single POST → collection `totalItems: 1`;
  deleteAdjuncts → 204; duplicate POST → 409.

**Carry-forwards:**
- #1292 is annotation-only — no hydra-model-dump re-run needed when it merges.
- Release-gated adjunct twins from sessions 1–3 (ACC-06 storage fields, ACC-18 deleteImages
  pairing, XC-12 queue wording, PRO-08/PRO-14 adjunct-queue surface, adjunct Asides softening)
  remain parked until the release carrying #1228/#1236 ships — none un-gated by session 5.
- When #1140 / #1141 / #1142 / #1128 / private-protagonist #13 ship: restore from the scratch
  sections named on each card (ADJ-01/03/06/12, 04/05/16).
- Watch: #1261 (SEVERE PATCH wipe), #1207 (adjunct delete null-check bug — exercise when the
  cleanup handler is touched), #1292 (ours).

**Next: session 6 (IIIF + auth, DESIGN-only; gated on protagonist #538 / auth-API RFC) — re-baseline first.**
