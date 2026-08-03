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
- **Status:** ☐ undecided

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
- **Status:** ☐ undecided

### PRO-03 · `errors` field present in API + example but undocumented
- **Theme:** Processing
- **Surfaces:** batch.mdx (example line 32; no `## errors` section) · `DLCS.HydraModel\Batch.cs:53-56` · `API\Features\Queues\Converters\BatchConverter.cs:20`
- **Type:** DOC-MISSING
- **Docs say:** The example JSON shows `"errors": 0`, but there is no `## errors` property section (sections jump count → completed → finished → superseded).
- **Original-doc nuance:** "—"
- **Code does:** `Batch.Errors` is a populated `[RdfProperty]` ("Total number of error images in the batch", `Batch.cs:53-56`), set by `BatchConverter` (`BatchConverter.cs:20`) and recomputed in `TestBatch` (`TestBatch.cs:62`). It is a real, meaningful field.
- **Issues/RFCs:** to check
- **Decision needed:** Add an `## errors` section documenting the field.
- **Options:** (a) add `## errors` section (integer count of assets that errored; `completed` includes errored assets per the `completed` wording); (b) leave undocumented.
- **Possible outputs:** doc
- **Who's needed:** docs
- **Status:** ☐ undecided

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
- **Status:** ☐ undecided

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
- **⟳ Update 2026-08-03 — the docs' surface has largely been BUILT.** PR #1228 (merged to `develop`; **not yet on `main`/released**, v1.13.2 does not include it) adds:
  - GET `/adjunctQueue` — returns the new `CustomerAdjunctQueue` hydra model (`DLCS.HydraModel/CustomerAdjunctQueue.cs`) with `size` / `batchesWaiting` / `adjunctsWaiting` plus auto-emitted `batches` / `active` / `recent` links — **matching the queues.mdx example and field sections exactly**.
  - GET `/adjunctQueue/batches`, `/active`, `/recent` — paged `HydraCollection<AdjunctBatch>`, matching the documented URLs and semantics ("active" = incomplete; "recent" = finished, latest first).
  - GET `/adjunctQueue/batches/{batchId}/current` and `/batches/{batchId}/adjuncts` — paged adjunct collections (`?orderBy=` supports `Created` only), matching the URLs batch.mdx documents under `currentAdjuncts` / `adjuncts`.
  - Issues #1157, #1158, #1160 are now **closed**; #1166 (Adjunct Batch / Queue querying) remains open for the residue.

  **Still missing vs the docs:** (1) the `completedAdjuncts` (`.../completed`) and `errorAdjuncts` (`.../error`) sub-collections in the batch.mdx example — no routes, no model properties (the exact parallel of PRO-02 on asset batches); (2) the `AdjunctBatch` response emits **no link properties at all** — `CurrentAdjuncts`/`Adjuncts` are commented out in `AdjunctBatch.cs` with a TODO "will be added in future PR". Trap for that future PR: default `SetHydraLinkProperties` would generate `.../batches/{id}/currentAdjuncts`, which does **not** match the implemented `/current` route — the link needs `SetManually` + converter wiring (batch.mdx:180 already documents the `/current` form).

  **Sample impact (XC-10):** the adjunct samples already written for these pages (`p08_queue/get_and_post_adjunct_queue.py`, `get_adjunct_batches.py`, `get_adjunct_active_batches.py`, `get_adjunct_recent_batches.py`, `p09_batch/adjunct_batch_operations.py`) targeted endpoints that 404'd at card-writing time and should now run against a develop deployment — **except** `adjunct_batch_operations.py`, which reads `batch["currentAdjuncts"]` from the response and will KeyError until the link is emitted (interim fix: build the URL as `@id` + `/current`).
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
- **Status:** ☐ undecided
