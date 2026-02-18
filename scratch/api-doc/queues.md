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

## Sections not yet ported from old documentation

The following sections from the old queues.mdx remain to be ported:

- `## Manifest Queues` - manifest-specific queues (marked as new feature)
- `## The Global Queue` - platform-wide queue statistics

### `## images` section (not yet implemented)

This endpoint is not yet implemented. Code sample created at `p08_queue/get_queue_images.py` but endpoint returns 404 when queue is empty.

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