# Queues - Scratch Notes

Notes on changes made while porting queues.mdx from the old documentation to the new site.

## Example JSON changes

- Changed example domain from `api.dlcs.io` to `api.dlcs.example` for consistency

## Changes made while porting sections

### `## batchesWaiting` and `## imagesWaiting` sections

- Old docs had only "??" as content for these sections
- Added descriptions based on inference from field names and context:
  - `batchesWaiting`: batches submitted but not yet active
  - `imagesWaiting`: assets submitted but not yet being processed (differs from `size` which includes assets currently being processed)

### `## active` section

- Ported as-is from old documentation
- Added code sample: `p08_queue/get_active_batches.py`

### `## recent` section

- Ported as-is from old documentation
- Added code sample: `p08_queue/get_recent_batches.py`

### `## priority` section

- Fixed typo: "went sent" → "when sent"
- Added Aside component for the iiif-av restriction note
- Added code sample: `p08_queue/post_to_priority_queue.py`
- **⟳ 2026-08-03 (PROV-04): the restriction's predicate shifted in the port and neither
  wording is exactly right.** OLD: *"The priority queue cannot be used for assets that
  specify the `iiif-av` delivery channel."* NEW Aside: *"The priority queue only
  supports image assets. Submitting any non-image asset ... is rejected."* Verified
  code (`CreateBatchOfImages.ValidatePriorityQueueRequest`, :158-171): non-image
  **family** is rejected **unless** the asset has an image delivery channel or an
  image media type — a blend of both wordings. The Aside should state the actual
  predicate when the queues page is next touched.

## Sections not yet ported from old documentation

The following sections from the old queues.mdx remain to be ported:

- `## Manifest Queues` - manifest-specific queues (marked as new feature)
- ~~`## The Global Queue` - platform-wide queue statistics~~ **⟳ 2026-08-03: this WAS
  ported** — and with three unrecorded corrections of old-doc errors, all verified
  against `DLCS.HydraModel\QueueSummary.cs`: `@type` vocab:Queue → vocab:QueueSummary
  (with the full 7-field shape incl. timebased/transcodeComplete/file);
  incoming/priority reworded to image-assets-only; success/failed "Always 0" →
  deprecated Deliverator back-compat (`[Obsolete]` in code). This stale entry was
  hiding those corrections.

### `## images` section (not yet implemented)

This endpoint is not yet implemented. ~~Code sample created at `p08_queue/get_queue_images.py`
but endpoint returns 404 when queue is empty.~~ ⟳ PRO-07 (ruled 2026-08-17, option (a)): the
endpoint 404s **always** — no `/queue/images` route has ever existed; "when queue is empty" was
a misdiagnosis. The dead `images` link was removed from the CustomerQueue model (protagonist
PR #1274, per the XC-07/XC-13 reachable-surface convention) and from the queues.mdx example;
the broken sample `get_queue_images.py` was deleted (SPA-06 precedent). This parked section is
now the only spec for the feature — if it is ever built, restore the section, re-add the model
link, and recreate the sample per the LinkCard below.

Content for when implemented:

```
## images

A link to a paged [Collection](collections) of assets, giving a merged view of assets on the queue, across batches. Typically you'd use this to look at the top or bottom of the queue (first or last page). This collection grows as you submit jobs to the queue, and shrinks as the platform processes them.

| domain | range | readonly | writeonly |
|:---|:---|:---|:---|
| vocab:CustomerQueue | 🔗 hydra:Collection (of vocab:Image) | True | False |

`/customers/{customer}/queue/images`

| Method | Label | Expects | Returns | Status |
|:---|:---|:---|:---|:---|
| GET | Retrieves all assets across batches for customer | - | a paged hydra:Collection of vocab:Image | 200 OK, 404 Not Found |

<LinkCard
  title="💻 Get queue images"
  href="https://github.com/dlcs/public-docs/blob/main/dlcs-docs-client/p08_queue/get_queue_images.py"
  description="Retrieve assets currently on the queue"
/>
```


### `## Manifest Queues 🆕` section (not yet implemented)

As well as a Customer queue, any Manifest you create has its own queue available; assets sent to that queue are processed in the same way as described above, but they are also associated with the Manifest.

See [IIIF Manifests and Collections](iiif).
## Replaced prose preserved (PRO-12, mechanical track, 2026-08-05)

Original `## active` and `## batchesWaiting` prose in queues.mdx (asset queue
section), replaced on the hygiene mechanical track:

> A link to a paged [Collection](../collections) of [Batches](../batch) that are currently in process - that contain at least one asset still being worked on. When you submit a batch it won't be active immediately (there may be other jobs ahead of it). It becomes active as the platform processes it (is present in this collection), and then drops out of this collection once finished. It drops out regardless of the success of the batch.

> Number of batches that are waiting to be processed. These are batches that have been submitted but are not yet [active](#active) - the platform has not yet started working on them.

**Why changed:** code (GetActiveBatches.cs:37; CustomerQueueRepository SQL) defines
active = submitted-and-not-finished (and not superseded) — a batch is active from
the moment of submission, including batches the platform has not started. The
adjunct-queue twin sections (:323 area) still carry the old wording and are
release-gated; fix them with the same wording when the adjunct queue ships.

**Disposition: probably-drop** (superseded by code reality). Restore only if batch
activation ever becomes start-of-processing rather than submission.

## XC-12 ruling — batch upsert status semantics (for the adjunct-queue docs when released)

Session 0 (2026-08-06) ruled: the status describes the AGGREGATE outcome of the
request, not itemised per-member results — 201 only when every member was newly
created (RFC 9110 permits 201 for "one or more new resources"), 200 when any member
updated existing state. A 201 therefore always means everything in the request is
new. When the adjunct-queue sections are promoted (PRO-08 release gate), state this
on the queue POST rows using the same wording as adjuncts.mdx "Registering multiple
adjuncts".

## Release-gated doc twin: priority queue @id (PRO-15, ruled 2026-08-17)

PRO-15 ruled (a): the priority queue response gets its own `@id`
(`/customers/{c}/queue/priority`) with collection links deliberately kept pointing
at the shared main-queue collections (protagonist PR #1277, develop-only). The live
queues.mdx#priority prose is @id-agnostic so needs no change now. When the carrying
release ships, optionally add to queues.mdx#priority after "A GET returns the
priority queue's own CustomerQueue resource, with its counts.":

> Its `batches`, `active` and `recent` links point at the *shared* batch
> collections — batches submitted to the priority queue appear there alongside
> everything else.

(Released v1.13.2 behaviour: the priority response's @id is the *main* queue's URL —
distinguishable from GET /queue only by its counts.)
