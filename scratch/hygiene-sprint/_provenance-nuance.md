# Provenance: nuance lost in the Nextra → Starlight port

Prepared for the DLCS docs/API hygiene sprint, 2026-06-25.

Purpose: surface substantive prose (caveats, rationale, worked examples, footgun
warnings, conceptual explanations) that existed in the OLD Nextra docs
(`C:\git\dlcs\docs\pages\api-doc\`) but is ABSENT from the NEW Starlight docs
(`C:\git\dlcs\public-docs\src\src\content\docs\api-doc\`) AND not already captured
in the matching scratch note (`C:\git\dlcs\public-docs\scratch\api-doc\`). The aim
is that each loss is consciously kept or dropped, not silently lost.

## Pages compared (exist in both old and new — 19)

overview, registering-assets, collections, entrypoint, customer, space, asset,
queues, batch, delivery-channels, origin-strategy, adjuncts, asset-queries,
identifiers, named-queries, single-asset-manifest, size-restrictions, storage,
custom-headers.

Pages where the port was clean (all OLD prose either survives in NEW or is already
in a scratch note — no uncaptured loss): **overview, registering-assets,
collections, customer, space, queues (main body), batch (main body),
delivery-channels, origin-strategy, adjuncts, identifiers, single-asset-manifest,
size-restrictions, custom-headers.**

## Pages unported — old-only, prose awaiting migration (4)

- **iiif.mdx** — IIIF Manifests and Collections (implemented in iiif-presentation repo). Large page (~1938 lines), title marked 🆕; old header note says it "will need rewriting for public consumption". Scratch placeholder exists (`scratch/api-doc/iiif.md`).
- **pipelines.mdx** — ~205 lines, old page opens with a "to be completed" warning Callout. Scratch notes exist (`scratch/api-doc/pipelines.md`).
- **access-control.mdx** — ~70 lines, opens with a warning Callout. Covers IIIF Auth (iiif-auth-v2), which has no REST API yet. Scratch note exists (`scratch/api-doc/access-control.md`).
- **curl-examples.mdx** — stub only ("This page is to be completed"), a TODO to reproduce/test the old readthedocs walkthroughs (require content type, mediaType required, delivery channel examples). No new page, no scratch note. Essentially a backlog ticket, not lost prose.

Note: `roles.mdx` and `auth-service.mdx` are listed as "pages not yet ported" in
CLAUDE.md but have NO old-site source file in `C:\git\dlcs\docs\pages\api-doc\`, so
there is no old prose to migrate for them.

---

## Lost-nuance entries (10)

### PROV-01 · entrypoint · `deliveryChannelPolicies` EntryPoint property described in OLD, absent from NEW (but still in the JSON example)
- **Page:** `C:\git\dlcs\docs\pages\api-doc\entrypoint.mdx` → `C:\git\dlcs\public-docs\src\src\content\docs\api-doc\entrypoint.mdx`
- **Already in scratch?** no (scratch/api-doc/entrypoint.md only mentions the missing `queue` property and removing `imageOptimisationPolicies`/`thumbnailPolicies`)
- **Lost prose:** "A link to a paged [Collection](collections) of further collections of [delivery channel policies](delivery-channels). This is a rare example of a Collection of Collections, where the returned collections are like sub-folders, for organisational use. / These _Delivery Channel policies_ are common settings you can re-use for your own assets, as further explained in [Delivery Channels](delivery-channels)." (plus its domain/range table and GET HTTP-operation row)
- **Why it matters:** The new EntryPoint JSON example still lists `"deliveryChannelPolicies"` as a property, but the whole section documenting it was dropped — a navigable property shown with no explanation; an internal inconsistency.
- **Recommendation:** needs-decision (the OLD section header was `## DELETE deliveryChannelPolicies` wrapped in a Callout questioning whether the global set should exist; either restore a description or remove the property from the JSON example)

### PROV-02 · entrypoint · "hardcoded" non-dereferenceable policy names
- **Page:** `C:\git\dlcs\docs\pages\api-doc\entrypoint.mdx` → `...\entrypoint.mdx`
- **Already in scratch?** no
- **Lost prose:** "You get some default Delivery Channel **Policies** when your customer is created. For thumbs and AV. / You can also refer to \"hardcoded\" but not dereferenceable policies use-original, none and default. So what would be in here?"
- **Why it matters:** Records that `use-original`, `none` and `default` are valid policy references that exist as hardcoded values rather than dereferenceable resources — a real behavioural fact.
- **Recommendation:** move to scratch (open design question, but the hardcoded-policy fact is worth keeping)

### PROV-03 · asset · "Version 1" `max` / `maxBehaviour` design discussion
- **Page:** `C:\git\dlcs\docs\pages\api-doc\asset.mdx` → `C:\git\dlcs\public-docs\src\src\content\docs\api-doc\asset.mdx`
- **Already in scratch?** no (scratch/api-doc/asset.md covers `manifest`, `usedBy`, and the maxWidth/openFullMax/openMaxWidth "planned" status, but nothing about `max`/`maxBehaviour`)
- **Lost prose:** The trailing "(First draft) Version 1" block, e.g. "The effect of setting `max` depends on what you set `maxBehaviour` to: `maxWidth`: this is independent of roles... `substitute`: the effect is 'Anyone can see a request up to maxWidth but you need a role to see higher'... `thumbnail`: this only applies to images with roles... Note that for this choice it's not a width, it's a bounding box - like maxUnauthorised." plus the open design question "What about the scenario where you want to allow full thumbs up to 400 px, but still impose a maxWidth of 512 even for authed users?... Or have a fourth behaviour: `maxWidthWithOpenThumbs`..."
- **Why it matters:** Design rationale/history for the current `maxWidth`/`openFullMax`/`openMaxWidth` model — explains why the three-property design exists and records an unresolved combination case. Not recorded anywhere else.
- **Recommendation:** move to scratch (design history; superseded as live doc but worth preserving)

### PROV-04 · queues · priority-queue restriction wording narrowed (channel vs asset type)
- **Page:** `C:\git\dlcs\docs\pages\api-doc\queues.mdx` → `...\queues.mdx`
- **Already in scratch?** no
- **Lost prose:** OLD: "The priority queue cannot be used for assets that specify the `iiif-av` delivery channel." NEW replaces this with an Aside: "The priority queue only supports image assets. Submitting any non-image asset (such as audio, video, or files) is rejected."
- **Why it matters:** The two claims aren't equivalent — OLD keys the restriction on the `iiif-av` delivery channel, NEW keys it on asset type (non-image). If the precise trigger is the delivery channel rather than the media family, the new wording is a subtle footgun.
- **Recommendation:** needs-decision (verify against protagonist which is the true predicate; otherwise drop old as superseded)

### PROV-05 · batch · concrete "limit of 100" replaced with vague "configurable"
- **Page:** `C:\git\dlcs\docs\pages\api-doc\batch.mdx` → `...\batch.mdx`
- **Already in scratch?** no
- **Lost prose:** OLD `count`: "The platform imposes a limit of 100 on the size of collections that can be submitted to a queue, therefore a batch cannot have a count greater than this." NEW drops the number ("imposes a limit on the size...") and adds an Aside: "The maximum size is configurable, actual value will depend on configuration."
- **Why it matters:** The concrete default (100) is practically useful to an integrator sizing their POST collections; "configurable" gives them no starting number.
- **Recommendation:** needs-decision (restore a stated default, e.g. "100 by default, configurable", if 100 is still the shipped default)

### PROV-06 · asset-queries · roadmap rationale for growing query surface
- **Page:** `C:\git\dlcs\docs\pages\api-doc\asset-queries.mdx` → `...\asset-queries.mdx`
- **Already in scratch?** no (scratch covers ordering, multiple values, and tags/roles/id queries, but not this line)
- **Lost prose:** "We will need a full set of query features for portal use."
- **Why it matters:** A design/roadmap rationale explaining why the query surface is expected to grow — context for the "still under development" caution that the new caution drops.
- **Recommendation:** move to scratch (minor roadmap aside, not user-facing behaviour)

### PROV-07 · named-queries · the `sequence` template parameter
- **Page:** `C:\git\dlcs\docs\pages\api-doc\named-queries.mdx` → `...\named-queries.mdx`
- **Already in scratch?** no
- **Lost prose:** `| sequence | How to filter images in manifest | &sequence=n1 |` (used in old example templates such as `manifest=s1&sequence=n1&canvas=n2...`)
- **Why it matters:** A documented template keyword in the old syntax table is entirely absent from the new syntax table and from the scratch note. A reader can no longer learn that `sequence` exists or what it does.
- **Recommendation:** needs-decision (confirm against protagonist whether `sequence` is still supported; if yes restore the row, if not move to scratch as unimplemented)

### PROV-08 · named-queries · `manifest` redefined — image-grouping field vs stored-manifest selector
- **Page:** `C:\git\dlcs\docs\pages\api-doc\named-queries.mdx` → `...\named-queries.mdx`
- **Already in scratch?** partial — scratch only notes "Verify what the manifest id should look like in this query (currently 'xxxx')", not the original grouping semantics
- **Lost prose:** `| manifest | How to group images | &manifest=s1 |` and the worked statement: "This customer (acme-corp) has a named query called `\"manifest\"` that makes use of two parameters p1 and p2 … The query is internally defined to use an additional asset metadata field - `number1` - and to generate a manifest with each canvas having one asset." Old template was `\"manifest=s1&canvas=n1&space=p1&s1=p2\"` with `manifest=s1` as the grouping/selection key.
- **Why it matters:** In the old docs `manifest=<metadata field>` was the mechanism for grouping assets into manifests. The new docs silently redefine `manifest` to mean "select assets that are part of a stored IIIF Manifest" (`&manifest=xxxx`) and drop `manifest=s1` from the canonical example. Different features; the original grouping concept and the example's rationale are lost.
- **Recommendation:** needs-decision (verify real semantics against protagonist; reconcile the two meanings, move whichever is obsolete to scratch)

### PROV-09 · storage · "needs to be generalised to report per delivery channel" design caveat
- **Page:** `C:\git\dlcs\docs\pages\api-doc\storage.mdx` → `C:\git\dlcs\public-docs\src\src\content\docs\api-doc\storage.mdx`
- **Already in scratch?** no (there is no storage scratch file)
- **Lost prose:** "> This needs to be generalised to report on usage per delivery channel." (appears twice — once under CustomerStorage, once under ImageStorage)
- **Why it matters:** A known design limitation / future-work note (the storage model predates delivery channels and lumps everything into "images"/"thumbnails"). Dropped entirely, so the intent to generalise is no longer recorded.
- **Recommendation:** move to scratch (create `scratch/api-doc/storage.md`)

### PROV-10 · storage · explanation of what consumes storage capacity
- **Page:** `C:\git\dlcs\docs\pages\api-doc\storage.mdx` → `...\storage.mdx`
- **Already in scratch?** no
- **Lost prose:** "The platform requires storage capacity to service the images registered by customers. This setting governs how much capacity the platform can use for a Customer across all the customer's spaces. Capacity is affected by image optimisation policy (higher quality = more storage used) and the absolute size of the images (pixel dimensions)."
- **Why it matters:** The only place explaining why storage usage varies — that the image optimisation policy and source pixel dimensions drive it. New page reduces `storagePolicy` to "the maximum storage permitted" and loses this rationale, useful for a customer managing quota.
- **Recommendation:** keep (restore a trimmed version to the new doc's `storagePolicy` section)

---

## Cross-reference: accuracy concern noted in passing (out of scope but flagged)

The new `size-restrictions.mdx` documents the `openMaxWidth` / `substitute` image
service (scenarios 8–11) as implemented; MEMORY.md flags this as "documented but
absent from protagonist code". That is an accuracy concern, not a provenance loss,
but worth carrying into the sprint.
