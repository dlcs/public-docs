# Storage — scratch notes

File created 2026-08-03 by the provenance re-audit (there was no storage scratch file;
two lost-nuance items had nowhere to live).

## "Generalise to per-delivery-channel reporting" design caveat (PROV-09) — **park (design intent)**

Old-doc note, appearing twice (under CustomerStorage and under ImageStorage), dropped
in the port. The storage model predates delivery channels and lumps usage into
"images"/"thumbnails":

> "This needs to be generalised to report on usage per delivery channel."

(2026-08-03 context: the model has since ALSO grown adjunct tallies —
`numberOfStoredAdjuncts`, `totalSizeOfStoredAdjuncts`, `adjunctSize`, undocumented,
see ACC-06 — so the generalisation pressure is real and growing.)

## What consumes storage capacity (PROV-10) — **restore-candidate**

The only prose explaining *why* storage usage varies; the new page reduces
`storagePolicy` to "the maximum storage permitted". Restore a trimmed version to the
`storagePolicy` section:

> "The platform requires storage capacity to service the images registered by
> customers. This setting governs how much capacity the platform can use for a
> Customer across all the customer's spaces. Capacity is affected by image
> optimisation policy (higher quality = more storage used) and the absolute size of
> the images (pixel dimensions)."

## Related open items (pointers, not prose)

- ACC-06: adjunct fields on both storage resources are emitted but undocumented
  (with the optimised carve-out semantics from PR #1220).
- ACC-08/ACC-17: the customer-level example `@id` is wrong (`/spaces/0/storage` now
  denotes real stub-asset space storage since the May 2026 migration).
- ACC-16 (family): storage GETs can 404; ops tables say 200 only.
- Storage-policy management API gaps: protagonist #1017/#1018/#1019.
