# Hygiene Sprint — Session 3: Processing

**Scope.** This session covers the *Processing* theme: the Queue (`queues.mdx`), Batch
(`batch.mdx`) and Pipelines pages. Pipelines is **not yet ported** — it exists only as
salvage notes in `scratch/api-doc/pipelines.md`. Docs were cross-referenced against the
protagonist API implementation under
`C:\git\dlcs\protagonist\src\protagonist\API\Features\Queues\*` and
`...\Features\AdjunctQueues\*`, plus the hydra models `DLCS.HydraModel\Batch.cs`,
`QueueSummary.cs`, `CustomerQueue.cs`, `Queue.cs`. Where a doc statement could not be
matched to code it is recorded as a card below; trivial confirmations are in the Resolved
list.

A notable structural finding: the protagonist `Batch` hydra model and the
`CustomerQueueController` routes are **out of sync with each other** — the model emits link
properties (`completedImages`, `errorImages`) that have no controller route, and the
controller exposes a route (`/assets`) that has no model property. The docs sit between the
two, partly matching each.

---

**⟳ Pre-flight 2026-08-17 (session-3 run-up).** All repos pulled. Protagonist develop @
`6813b7a2`; latest release still **v1.13.2** (2026-07-17), so the main-docs = released-behaviour
constraint is unchanged and all six session-2 model/vocab PRs (#1258/#1259/#1260/#1262/#1263/#1266,
merged 2026-08-17) remain **develop-only** until the next release. Public-docs PR #14 merged;
session branch `hygiene/session-3` cut from main. `_hydra-model-flags.md` re-baselined @6813b7a2 —
only the expected Image-section changes, zero drift elsewhere (Batch/Queue/CustomerQueue/
QueueSummary/AdjunctBatch tables identical). Processing-area code history since the 2026-08-03 card
refresh contains only our own hygiene commits (XC-05/XC-11/XC-13/PRO-10) — no third-party premise
drift detected, though per [[confirm-latest-main-before-auditing]] each card is still re-verified
at presentation. Externals to keep in view this session: open PRs **#1268** (Hydra flags → OpenAPI;
tests need updating for #1262) and **#1269** (thumbs cleanup, fixes #1265); new issues **#1270**
(allImages PATCH extension — ACC-20 follow-up noted on that card) and **#1271** (API-key access
levels); **#1229** (queue values out of sync) is linked from PRO-06.

**Read-only live sweep, staging (released v1.13.2), 2026-08-17** — GETs only, no mutations
(customer 15; probed batch 591467 from /queue/batches):
- `/queue` 200 — QueueSummary with `incoming/priority/timebased/transcodeComplete/file` +
  deprecated `failed`/`success` still on the released wire.
- `/customers/15/queue` 200 — emits `batches`, `images`, `active`, `recent`, `priority` links.
  **`…/queue/images` → 404** — PRO-07's premise (advertised link, dead route) confirmed live on
  released, **and still advertised on develop** (`CustomerQueue.cs:46-47` — XC-13's sweep covered
  Batch + adjunct queue but not this link), so PRO-07 remains fully open.
- `/customers/15/queue/active` 200 (totalItems 0) · `/recent` 200 (30, paged) · `/batches` 200
  (30, paged) · `/priority` 200 returning a CustomerQueue-shaped body — PRO-05's ruling holds live.
- **`/customers/15/adjunctQueue` GET → 405** (not 404): released code has the route with other
  methods (POST ingest) but no GET — the #1228 GET surface is develop-only. Refines PRO-08/PRO-13
  in-room facts: the released failure mode for the documented GETs is **405**, and PRO-13's
  release-gated adjunct table should say so if it documents pre-#1228 behaviour at all.
- Batch 591467: body still emits `completedImages`/`errorImages` links, **both 404** — PRO-02's
  XC-13 fix (PR #1238) confirmed release-gated, released wire unchanged. **`/assets` 200** works
  while the model advertises no `assets` link (only `images`, also 200) — PRO-01's premise
  confirmed live; released Batch body shows no `estCompletion` (PRO-04: null-suppressed, never
  populated) and no `test` link. `…/test` GET → 405 — verified in code: the route is
  **POST**-only (`CustomerQueueController.cs:299-301`, `[HttpPost] batches/{batchId}/test`);
  cross-check the docs' method table at PRO-06.

---

## Resolved (Category A — verified, no card needed)

- **Batch max size = 250, configurable.** `ApiSettings.MaxBatchSize { get; set; } = 250`
  (`API\Settings\ApiSettings.cs:40`); enforced in `QueuePostValidator.cs:31-34`. Doc's
  "configurable, actual value will depend on configuration" Aside is correct.
- **Global queue `@type` = `vocab:QueueSummary`.** `DlcsResource.Type => vocab:{GetType().Name}`
  and the class is `QueueSummary` (`QueueSummary.cs`). Matches doc example.
- **Priority queue is image-only.** Enforced in
  `CreateBatchOfImages.ValidatePriorityQueueRequest` (`CreateBatchOfImages.cs:158-171`),
  rejecting non-image family unless it has an image delivery channel or image media type,
  with message "Priority queue only supports image assets". Matches the doc's caution Aside.
- **Global queue field set.** `QueueSummary.cs` defines exactly `incoming`, `priority`,
  `timebased`, `transcodeComplete`, `file`, plus `[Obsolete]` `failed` / `success`. Matches
  the queues.mdx example and the deprecated-field notes added in the previous audit.
- **Queue POST returns 201 + `vocab:Batch`.** `CustomerQueueController.CreateBatch` →
  `HandleUpsert(... WriteResult.Created)` (`CreateBatchOfImages.cs:155`). Matches doc.
- **`test` returns `{ "success": <bool> }`.** `TestBatch` action returns
  `Ok(new { success = response })` (`CustomerQueueController.cs:309`). Matches doc.

---

## Cards

### PRO-01 · Batch model omits the `assets` link although `/assets` works
- **Theme:** Processing
- **Surfaces:** batch.mdx#assets (example line 35, section L124-136) · `DLCS.HydraModel\Batch.cs:70-89` · `API\Features\Queues\CustomerQueueController.cs:257-279`
- **Type:** CODE-WRONG (model omission) + DOC partly-right
- **Docs say:** The batch resource has an `assets` link (`.../batches/{id}/assets`) returning "all the assets specified by the batch at creation time"; the example JSON includes it.
- **Original-doc nuance:** "Many batches can include the same asset in this property, whereas only one batch can include an asset in its `images` property."
- **Code does:** The route exists and works — `GetBatchAssets` at `CustomerQueueController.cs:257-279` (`[Route("batches/{batchId}/assets")]`). But the `Batch` hydra model (`Batch.cs:70-89`) has **no `Assets` property** — only `Images`, `CompletedImages`, `ErrorImages`, `Test`. `SetHydraLinkProperties` (`DlcsResource.cs:44-63`) only emits links for declared HydraLink properties, so a real batch response **never contains an `assets` link**, even though the endpoint is reachable.
- **Issues/RFCs:** to check
- **Decision needed:** Whether to add an `Assets` HydraLink property to the `Batch` model so the working endpoint is discoverable, or to drop the endpoint.
- **Options:** (a) add `Assets` property to `Batch.cs` so the link is emitted; (b) leave model as-is and remove `assets` from the doc example; (c) document `assets` as a known-undiscoverable endpoint.
- **Possible outputs:** code / doc
- **Who's needed:** API dev + docs
- **Status:** ☐ undecided — ⟳ session-0 cascade note (2026-08-06): XC-07/XC-13 ratified "the model advertises exactly the reachable surface", which makes option (a) (add the `Assets` HydraLink) the near-automatic outcome; the room did not rule it — session 3 confirms

### PRO-02 · `completedImages` / `errorImages` links are emitted but 404
- **Theme:** Processing
- **Surfaces:** batch.mdx (example lines 36-37) · `DLCS.HydraModel\Batch.cs:75-83,116-130` · `API\Features\Queues\CustomerQueueController.cs` (route list)
- **Type:** CODE-WRONG
- **Docs say:** Example batch JSON includes `completedImages` and `errorImages` links. (No dedicated `##` section documents them — see PRO-03 cluster.)
- **Original-doc nuance:** "—"
- **Code does:** The model declares `CompletedImages`/`ErrorImages` HydraLink properties (`Batch.cs:75-83`) and even defines GET operations for them (`BatchClass.DefineOperations`, `Batch.cs:116-130`), so `SetHydraLinkProperties` emits `.../completedImages` and `.../errorImages` on every batch. But `CustomerQueueController` defines **no routes** for these — only `batches/{batchId}`, `/images`, `/assets`, `/test`, and the collection routes. A grep for `completedImages|errorImages|/completed|/error` under `Features\Queues` returns nothing. Both links therefore 404.
- **Issues/RFCs:** to check
- **Decision needed:** Implement the two endpoints, or remove the links from model + doc example.
- **Options:** (a) add `completedImages`/`errorImages` routes (filter batch images by completion/error state — data already exists, cf. `TestBatch` counting `i.Error`); (b) remove the properties from `Batch.cs` and drop from doc example; (c) keep links, document as not-yet-implemented.
- **Possible outputs:** code / doc / RFC
- **Who's needed:** API dev + docs
- **Status:** ✅ RESOLVED by XC-13 cascade (session 0, 2026-08-06): option (b) — the `completedImages`/`errorImages` links (the #899 named examples) removed from Batch.cs and from the batch.mdx example (protagonist PR #1238 + public-docs PR #9); `batches/{id}/images` with asset-query filtering covers the need

### PRO-03 · `errors` field present in API + example but undocumented
- **Theme:** Processing
- **Surfaces:** batch.mdx (example line 32; no `## errors` section) · `DLCS.HydraModel\Batch.cs:53-56` · `API\Features\Queues\Converters\BatchConverter.cs:20`
- **Type:** DOC-MISSING
- **Docs say:** The example JSON shows `"errors": 0`, but there is no `## errors` property section (sections jump count → completed → finished → superseded).
- **Original-doc nuance:** "—"
- **Code does:** `Batch.Errors` is a populated `[RdfProperty]` ("Total number of error images in the batch", `Batch.cs:53-56`), set by `BatchConverter` (`BatchConverter.cs:19` as of 2026-08-03) and recomputed in `TestBatch` (`TestBatch.cs:62`). It is a real, meaningful field. *(⟳ 2026-08-03: the adjunct flavour has the identical gap — batch.mdx:179 shows `"errors": 0` on the AdjunctBatch example with no `### errors` section. Fix both in the same doc change.)*
- **Issues/RFCs:** to check
- **Decision needed:** Add an `## errors` section documenting the field.
- **Options:** (a) add `## errors` section (integer count of assets that errored; `completed` includes errored assets per the `completed` wording); (b) leave undocumented.
- **Possible outputs:** doc
- **Who's needed:** docs
- **Status:** ☑ mechanical (asset flavour) — `## errors` section merged in public-docs PR #5 (2026-08-05); the AdjunctBatch `### errors` twin is release-gated

### PRO-04 · `estCompletion` field exists in model, undocumented and never populated
- **Theme:** Processing
- **Surfaces:** batch.mdx (absent) · `DLCS.HydraModel\Batch.cs:65-68` · `API\Features\Queues\Converters\BatchConverter.cs:14-23`
- **Type:** DOC-MISSING + possible CODE-WRONG (dead field)
- **Docs say:** Nothing — `estCompletion` is not mentioned.
- **Original-doc nuance:** "—"
- **Code does:** `Batch.EstCompletion` ("Estimated Completion", `Batch.cs:65-68`) is a nullable `DateTime?`. `BatchConverter.ToHydra` never sets it, so it is always null (and, depending on serializer null-handling, likely omitted from responses). It appears to be aspirational / dead.
- **Issues/RFCs:** to check
- **Decision needed:** Decide whether `estCompletion` is a real feature to populate + document, or dead code to remove.
- **Options:** (a) implement an estimate and document; (b) remove the property from `Batch.cs`; (c) leave as-is (silent, always null).
- **Possible outputs:** code / doc / defer
- **Who's needed:** API dev + product
- **Status:** ☐ undecided

### PRO-05 · Doc says GET priority queue "is not supported" — but it is
- **Theme:** Processing
- **Surfaces:** queues.mdx#priority (line 148) · `API\Features\Queues\CustomerQueueController.cs:149-163`
- **Type:** DOC-WRONG
- **Docs say:** Under `## priority`: "Note that GET is not supported." The method table lists only POST.
- **Original-doc nuance:** "Batches sent to the priority queue will be visible in the batch collections available on the main queue..."
- **Code does:** `GetCustomerPriorityQueue` is `[HttpGet][Route("priority")]` returning 200 + a `CustomerQueue` for the priority queue (`CustomerQueueController.cs:149-163`, via `new GetCustomerQueue(customerId, "priority")`). GET `/customers/{id}/queue/priority` is fully supported. The `CustomerQueue.priority` link (`CustomerQueue.cs:58-61`) points here.
- **Issues/RFCs:** to check
- **Decision needed:** Correct the doc (add GET row) — or confirm whether GET-priority is intended to remain.
- **Options:** (a) update doc: add GET row returning `vocab:CustomerQueue`, remove the "GET is not supported" note; (b) if GET-priority is unwanted, remove the controller action.
- **Possible outputs:** doc / code
- **Who's needed:** docs + API dev (confirm intent)
- **Status:** ✅ RULED (session 0, 2026-08-06): option (a) — GET priority-queue is intended; add the GET row, remove the "not supported" note. Owner: PO. Outputs: public-docs hygiene/session-0 commit + sample parity (add GET to the priority-queue sample, closing the XC-10 gap)

### PRO-06 · `test` endpoint does more than update `superseded`
- **Theme:** Processing
- **Surfaces:** batch.mdx#test (L139-147) · batch.mdx#superseded (L93-104) · `API\Features\Queues\Requests\TestBatch.cs:27-76`
- **Type:** DOC-WRONG (incomplete)
- **Docs say:** "An HTTP POST to this resource will update the batch's `superseded` property." `## superseded` repeats: "you can force an update by POSTing to the test resource."
- **Original-doc nuance:** "Returns JSON object with single success property (boolean)." (correct)
- **Code does:** `TestBatchHandler.Handle` (`TestBatch.cs:27-76`) also: sets `Finished` and sends a batch-completed notification when the batch is complete-but-not-finished (L49-54); and **recalculates `Count`, `Errors`, and `Completed`** from the actual images when counts disagree (L57-64). `success:true` is returned whenever *any* of these changes are made — not only superseding. The controller XML doc agrees: "Tests batch to check if superseded or completed and updates underlying batch accordingly."
- **Issues/RFCs:** #1229 "Reconcile `Queue` endpoint values getting out of sync" (opened 2026-07, open) — the drift `test` papers over is now tracked as a code issue; worth linking when the room rules on this card
- **Decision needed:** Broaden the doc description of `test` to reflect that it reconciles finished-state and counts, not just `superseded`.
- **Options:** (a) reword `## test` to "forces reconciliation of the batch's `superseded`, `finished` and count fields"; (b) leave as a deliberate simplification.
- **Possible outputs:** doc
- **Who's needed:** docs
- **Status:** ☐ undecided

### PRO-07 · CustomerQueue example advertises `images` link, but the endpoint 404s
- **Theme:** Processing
- **Surfaces:** queues.mdx (example line 27) · scratch/api-doc/queues.md (L41-67, "not yet implemented") · `DLCS.HydraModel\CustomerQueue.cs:46-48` · `API\Features\Queues\CustomerQueueController.cs` (no `/queue/images` route)
- **Type:** DOC-WRONG (example) — code matches scratch note
- **Docs say:** The `vocab:CustomerQueue` example JSON (queues.mdx:27) includes `"images": ".../queue/images"`. The `## images` section was deliberately **not** ported (held in scratch as not-yet-implemented).
- **Original-doc nuance:** scratch: "This endpoint is not yet implemented... endpoint returns 404 when queue is empty."
- **Code does:** `CustomerQueue.Images` HydraLink is emitted by `SetHydraLinkProperties`, so the link appears in responses, but `CustomerQueueController` has **no `/queue/images` route** (only `batches/{batchId}/images`). GET `/customers/{id}/queue/images` 404s. So the published example shows a link with no documented section and no working endpoint.
- **Issues/RFCs:** to check
- **Decision needed:** Whether to keep `images` in the published example given the section is intentionally omitted and the endpoint is unimplemented.
- **Options:** (a) remove `images` from the example JSON until implemented; (b) implement the queue-level `/images` endpoint and port the section from scratch; (c) leave example as forward-looking.
- **Possible outputs:** doc / code
- **Who's needed:** docs + API dev
- **Status:** ☐ undecided

### PRO-08 · Adjunct queue/batch: docs describe many endpoints not in the implementation
- **Theme:** Processing
- **Surfaces:** queues.mdx#adjunct-queue (L230-360) · batch.mdx#adjunct-batch (L149-266) · `API\Features\AdjunctQueues\CustomerAdjunctQueueController.cs`
- **Type:** DOC-MISSING / DESIGN (doc overstates implemented surface)
- **Docs say:** A full `CustomerAdjunctQueue` resource (GET `/adjunctQueue` with `size`/`batchesWaiting`/`adjunctsWaiting`, plus `batches`/`active`/`recent` collections) and a full `AdjunctBatch` (`currentAdjuncts`, `adjuncts`, `completedAdjuncts`, `errorAdjuncts` sub-collections). Both pages carry a "still under development" caution Aside.
- **Original-doc nuance:** queues.mdx: "This supports most of the same functionality as asset queues but via the `/adjunctQueue/` resource."
- **Code does (as of 2026-06-25):** `CustomerAdjunctQueueController` implements only **two** operations: GET `/adjunctQueue/batches/{batchId}` and POST `/adjunctQueue` (create batch). There is **no** GET `/adjunctQueue` summary, no `active`/`recent`/`batches` collection routes, and **no** `current`/`adjuncts`/`completed`/`error` sub-collection routes. So the feature is partly built (more than the "under development" Aside implies for create/get-batch) but far less than the detailed endpoint tables claim.
- **⟳ Update 2026-08-03 — the docs' surface has largely been BUILT.** Two PRs, both merged to `develop` only (**not on `main`/released** — v1.13.2 includes neither), add: *(attribution corrected in second-pass verification, 2026-08-03)*
  - From **PR #1228** (`feature/adjunctQueueEndpoint`, 2026-07-28): GET `/adjunctQueue` — returns the new `CustomerAdjunctQueue` hydra model (`DLCS.HydraModel/CustomerAdjunctQueue.cs`) with `size` / `batchesWaiting` / `adjunctsWaiting` plus auto-emitted `batches` / `active` / `recent` links — **matching the queues.mdx example and field sections exactly** — and GET `/adjunctQueue/batches`, `/active`, `/recent` — paged `HydraCollection<AdjunctBatch>`, matching the documented URLs and semantics ("active" = incomplete; "recent" = finished, latest first).
  - From **PR #1226** (`feature/bulkAdjunctOperations`, 2026-07-27): GET `/adjunctQueue/batches/{batchId}/current` and `/batches/{batchId}/adjuncts` — paged adjunct collections, matching the URLs batch.mdx documents under `currentAdjuncts` / `adjuncts`. Ordering: the `?orderBy=` field value is **ignored** — ordering is always `Created` (adjunct lists) / `Submitted` (batch lists), with `orderByDescending` toggling direction only; `/recent` ignores ordering params entirely (fixed `Finished` desc) (`AdjunctQueryX.cs:15-18`).
  - Issues #1157, #1158, #1160 are now **closed**; #1166 (Adjunct Batch / Queue querying) remains open for the residue. POST `/adjunctQueue` can also return **404** (referenced asset doesn't exist, `CreateAdjunctBatch.cs:115-121`) and 400 (validator: every member needs an `asset` field, max 250, no duplicate (asset,id) pairs) — queues.mdx documents 201 only.

  **Still missing vs the docs:** (1) the `completedAdjuncts` (`.../completed`) and `errorAdjuncts` (`.../error`) sub-collections in the batch.mdx example — no routes, no model properties (the exact parallel of PRO-02 on asset batches); (2) the `AdjunctBatch` response emits **no link properties at all** — `CurrentAdjuncts`/`Adjuncts` are commented out in `AdjunctBatch.cs` with a TODO "will be added in future PR". Trap for that future PR: default `SetHydraLinkProperties` would generate `.../batches/{id}/currentAdjuncts`, which does **not** match the implemented `/current` route — the link needs `SetManually` + converter wiring (batch.mdx:180 already documents the `/current` form).

  **Sample impact (XC-10)** *(revised after second-pass verification)*: the three batch-list samples (`get_adjunct_batches.py`, `get_adjunct_active_batches.py`, `get_adjunct_recent_batches.py`) should now run clean against a develop deployment. Three others are broken: `adjunct_batch_operations.py` reads `batch["currentAdjuncts"]` and will KeyError until the link is emitted (interim fix: build the URL as `@id` + `/current`); and **both queue-POST samples** — `get_and_post_adjunct_queue.py`'s POST helper and `p13_adjuncts/get_adjunct_batch.py` (missing from the original list) — send per-member `space`/`image` fields where the validator requires an `asset` field (`"customer/space/assetId"` or full URI; `AdjunctBatchPostValidator.cs:26-28`) → 400 "All members must have an 'asset' field". The required `asset` field is documented nowhere (queues.mdx, batch.mdx, adjuncts.mdx) — see PRO-11.
- **Issues/RFCs:** #1157 ✅ / #1158 ✅ / #1160 ✅ (closed, implemented by PR #1228) · #1166 open
- **Decision needed (revised 2026-08-03):** Verify the new endpoints against a develop deployment; decide whether the docs wait for release to `main` (they currently describe unreleased behaviour); decide the fate of `completedAdjuncts`/`errorAdjuncts` (jointly with PRO-02) and confirm the batch link-emission plan; then run/fix the five samples and consider softening the "still under development" Asides.
- **Options:** (a) verify on develop, keep docs as-is (they're now nearly right), remove `completedAdjuncts`/`errorAdjuncts` from the example until built; (b) hold everything until the feature reaches `main`; (c) treat remaining gaps via #1166 and re-review after.
- **Possible outputs:** doc / sample / code (link emission)
- **Who's needed:** API dev + docs
- **Status:** ☐ undecided — card refreshed 2026-08-03 against develop

### PRO-09 · Pipelines page unported; no pipeline implementation exists
- **Theme:** Processing
- **Surfaces:** scratch/api-doc/pipelines.md (whole file) · queues.mdx progress table (order 10, "skipped for now") · protagonist API (no implementation)
- **Type:** DESIGN / defer
- **Docs say:** Nothing published. The scratch note is explicitly marked "DO NOT USE THIS PAGE" — salvage from the old adjuncts page. It describes a `creator: pipeline:*` mechanism where the platform generates adjuncts (OCR, annotationsFromOCR, AVTranscript, HTR, sentiment, NER, imageDescription, paletteInfo, etc.), versioned pipeline ids (`pipeline:OCR/v0.9.1`), and a `source` field linking adjuncts. The note itself flags "only one of these is supported so far!" (`pipeline:test`).
- **Original-doc nuance:** "It's also possible to supply adjuncts _and_ specify pipeline operations on them in the same POST." (scratch L40)
- **Code does:** No adjunct-creation pipeline implementation found. A grep for `pipeline|Pipeline` across `API` matches only MediatR behaviour pipelines (`Infrastructure\Requests\Pipelines\CacheInvalidationBehaviour.cs`) and unrelated delivery-channel-policy text — nothing implementing `creator: pipeline:*`. The adjunct subsystem that exists (PRO-08) only stores/serves adjuncts; it does not generate them.
- **Issues/RFCs:** to check
- **Decision needed:** Confirm pipelines remain deferred (design-only) and keep the page unpublished until the feature is built.
- **Options:** (a) keep deferred; retain scratch as the design seed; (b) promote to an explicit RFC for the pipeline/creator design; (c) discard the salvage note if the direction is abandoned.
- **Possible outputs:** RFC / defer
- **Who's needed:** product + API dev
- **Status:** ☐ undecided

### PRO-10 · `QueueSummaryClass` vocab wiring looks like a copy-paste bug
- **Theme:** Processing
- **Surfaces:** `DLCS.HydraModel\QueueSummary.cs:8,52-63` · cf. `DLCS.HydraModel\Queue.cs:7,58-62` · cf. `Batch.cs:8,92-97`
- **Type:** CODE-WRONG (vocab/doc generation; not consumer-facing JSON)
- **Docs say:** N/A — affects generated Hydra class metadata / `vocab` context, not the runtime `QueueSummary` payload.
- **Original-doc nuance:** "—"
- **Code does:** `QueueSummary` is annotated `[HydraClass(typeof(QueueClass), ...)]` (`QueueSummary.cs:8`) — i.e. it points at the *customer Queue's* class (`Queue.cs:58`), not its own. Separately, the `QueueSummaryClass` defined in the same file bootstraps over itself: `BootstrapViaReflection(typeof(QueueSummaryClass))` (`QueueSummary.cs:56`) instead of `typeof(QueueSummary)` — compare `BatchClass` → `typeof(Batch)` (`Batch.cs:95`) and `QueueClass` → `typeof(Queue)` (`Queue.cs:62`). Net effect: `QueueSummaryClass` is never referenced and reflects over the wrong type. The runtime JSON (counts) is unaffected, but generated vocab/documentation for `QueueSummary` is wrong.
- **Issues/RFCs:** to check
- **Decision needed:** Fix the `HydraClass` attribute and the `BootstrapViaReflection` argument for `QueueSummary`.
- **Options:** (a) change attribute to `[HydraClass(typeof(QueueSummaryClass), ...)]` and bootstrap `typeof(QueueSummary)`; (b) leave if `QueueSummary` vocab generation is unused; (c) remove dead `QueueSummaryClass`.
- **Possible outputs:** code
- **Who's needed:** API dev
- **Status:** ☑ mechanical — merged in protagonist PR #1235 (2026-08-06, donaldgray)

### PRO-11 · Adjunct-queue POST members need an `asset` field — undocumented, and both samples get it wrong *(added 2026-08-03 verification pass)*
- **Theme:** Processing
- **Surfaces:** queues.mdx adjunct POST row (:263) · batch.mdx · adjuncts.mdx · `AdjunctBatchPostValidator.cs:26-28` · `AdjunctConverter.TryParseAssetId` (:33-36) · `dlcs-docs-client/p08_queue/get_and_post_adjunct_queue.py` · `p13_adjuncts/get_adjunct_batch.py`
- **Type:** DOC-MISSING + sample bug (strongest new finding of the verification pass)
- **Code does:** Every member of a `POST /adjunctQueue` collection must carry an `asset` field — short form `"customer/space/assetId"` or full URI, customer must match the URL (mismatch → 400). Documented nowhere. Both queue-POST samples instead send `space`/`image` fields that don't exist on the hydra model → 400 "All members must have an 'asset' field". Validator also enforces: non-empty members, max = shared `MaxBatchSize` (250), no duplicate (asset,id) pairs, full per-adjunct validation.
- **Decision needed:** Document the `asset` field + validator constraints on the queues/batch pages (once release-gating is settled, see PRO-08); fix both samples.
- **Possible outputs:** doc / sample
- **Who's needed:** docs author
- **Status:** ☑ mechanical (sample half) — both queue-POST samples now send `asset`, and adjunct_batch_operations.py builds /current + /adjuncts from @id; merged in public-docs PR #7 (2026-08-05). Doc half release-gated (PRO-08)

### PRO-12 · "active" batch semantics wrong in docs (asset AND adjunct queues) *(added 2026-08-03 verification pass)*
- **Theme:** Processing
- **Surfaces:** queues.mdx:99 and :323 · `GetActiveBatches.cs:37` · `GetActiveAdjunctBatches.cs:30`
- **Type:** DOC-WRONG
- **Docs say:** A batch "won't be active immediately... becomes active as the platform processes it" — which also contradicts the page's own `batchesWaiting` description ("not yet active").
- **Code does:** active = `Finished == null` (plus `!Superseded` for asset batches) — a batch is active from the moment of submission, **including batches not yet started**.
- **Decision needed:** Correct the prose on both queue sections (active = submitted-and-not-finished) and reconcile with `batchesWaiting`.
- **Possible outputs:** doc
- **Who's needed:** docs author
- **Status:** ☑ mechanical (asset section) — active + batchesWaiting prose merged in public-docs PR #5 (2026-08-05), originals preserved in scratch/api-doc/queues.md; adjunct section release-gated

### PRO-13 · GET `/queue` and `/adjunctQueue` can 404 — method tables say 200 only *(added 2026-08-03 verification pass)*
- **Theme:** Processing
- **Surfaces:** queues.mdx method tables · `CustomerQueueRepository.cs:50-58` · `CustomerAdjunctQueueController.cs:35`
- **Type:** DOC-MISSING
- **Code does:** The adjunct queue row is created lazily — a customer who has never POSTed an adjunct batch gets 404 from GET `/adjunctQueue` (joins `Queues` on `Name='adjunct'`). Worth verifying whether the plain `/queue` has an equivalent empty-state.
- **Decision needed:** Add 404 to the method tables (part of the ops-table sweep with ACC-12/SPA-20); or code could auto-vivify an empty queue summary.
- **Possible outputs:** doc / code
- **Who's needed:** docs author + API dev
- **Status:** ☑ mechanical (/queue table) — 404 added, merged in public-docs PR #5 (2026-08-05); adjunct table release-gated; auto-vivify option not pursued

### PRO-14 · AdjunctBatch's HydraClass attribute references itself *(minted in session 0, 2026-08-06)*
- **Theme:** Processing
- **Surfaces:** `DLCS.HydraModel/AdjunctBatch.cs:7` (`[HydraClass(typeof(AdjunctBatch), ...)]`) · cf. the PRO-10 fix (`QueueSummary.cs`, merged in protagonist PR #1235) · cf. `Batch.cs` (`[HydraClass(typeof(BatchClass))]` + `BatchClass : Class`)
- **Type:** CODE-WRONG (vocab/doc generation; not consumer-facing JSON)
- **Docs say:** n/a — affects generated Hydra class metadata only.
- **Code does:** `AdjunctBatch` is annotated `[HydraClass(typeof(AdjunctBatch))]` — pointing at *itself* rather than a `Class`-derived vocab type. There is no `AdjunctBatchClass` at all, so no vocab operations are defined for the resource. Same defect family as PRO-10 (QueueSummary pointed at the wrong class and bootstrapped over itself). Observed while implementing XC-13 (PR #1238), where the two reinstated links got property definitions but the class itself still has no vocab class.
- **Issues/RFCs:** —
- **Decision needed:** Create an `AdjunctBatchClass : Class` (bootstrapping `typeof(AdjunctBatch)`, defining GET) and point the attribute at it, mirroring `Batch`/`BatchClass`.
- **Options:** (a) add the vocab class + fix the attribute; (b) leave (vocab generation for AdjunctBatch stays wrong/absent).
- **Possible outputs:** code (mechanical-track candidate — verified, obvious fix, no design question)
- **Who's needed:** protagonist dev
- **Status:** ☐ undecided
