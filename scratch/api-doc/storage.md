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

## RELEASE-GATED doc change: storagePolicy becomes customer-level only (ACC-09, session 1, 2026-08-10)

Ruled in hygiene session 1: the space-level `storagePolicy` link is meaningless (echoes the
customer's policy; not editable or enforced per space), so protagonist stops emitting it on
space-level responses (hygiene/session-1 branch; commit "ACC-09: stop emitting storagePolicy
on space-level storage responses"). Designing real per-space policies is protagonist #1240.

**Apply to storage.mdx when the release carrying that change ships** (per main = released
behaviour; today's release still emits it on both):

1. In the space-level example JSON, delete the line
   `"storagePolicy": "https://api.dlcs.example/storagePolicies/default"`.
2. In the `### storagePolicy` section, replace the sentence
   > "This property is present on both customer-level and space-level storage responses."
   with:
   > "This property is present only on customer-level storage responses — storage policies
   > apply to the whole Customer, not to individual spaces."

(Original sentence preserved above per principle 2. Sample parity: no-op — storage.py follows
`storagePolicy` from the customer-level resource only.)

## Related open items (pointers, not prose)

- ACC-06: adjunct fields on both storage resources are emitted but undocumented
  (with the optimised carve-out semantics from PR #1220).
- ACC-08/ACC-17: the customer-level example `@id` is wrong (`/spaces/0/storage` now
  denotes real stub-asset space storage since the May 2026 migration).
- ACC-16 (family): storage GETs can 404; ops tables say 200 only.
- Storage-policy management API gaps: protagonist #1017/#1018/#1019.
