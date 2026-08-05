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

~~Pages where the port was clean (all OLD prose either survives in NEW or is already
in a scratch note — no uncaptured loss): **overview, registering-assets,
collections, customer, space, queues (main body), batch (main body),
delivery-channels, origin-strategy, adjuncts, identifiers, single-asset-manifest,
size-restrictions, custom-headers.**~~

**⟳ REVISED 2026-08-03 — the "clean" list did not survive an independent re-audit.**
A second pass deep-diffed the four largest claimed-clean pages (customer, adjuncts,
delivery-channels, registering-assets): **all four carry uncaptured losses** — see
PROV-11..18 below. The original 10 entries all verified accurate (quotes exact,
genuinely uncaptured; 3 immaterial caveats on the "already in scratch?" column).
The remaining ten claimed-clean pages have NOT been re-audited with the deeper lens
and should be treated as *unverified*, not clean. The re-audit also surfaced a
category this file's framing missed: **silent normative changes** — statements
that changed between old and new (required/optional flips, limits, status codes)
with no scratch or register trail; these need *verification against protagonist*,
not a keep/park decision. See the "Silent normative changes" section at the end.
Fair summary for the room: ~~**~18 lost-nuance items, at most 10 of 19 pages
verifiably clean.**~~

**⟳ FINAL, 2026-08-03 (second refresh): all 19 pages now deep-audited.** The
remaining ten were diffed with the same lens (see PROV-19..24 and the silent-changes
additions below). Final verdict: **verifiably clean: overview, collections,
identifiers, custom-headers** (size-restrictions clean on losses but carries two
unsourced normative *additions*); **9 of 19 pages had uncaptured losses**; **24
lost-nuance items** in total, plus ~two dozen silent normative changes — the large
majority of which verified as deliberate *corrections* of old-doc errors that were
simply never recorded. Two silent changes turned out to be genuinely wrong in the
NEW docs and became cards: the single-asset-manifest "always a Choice" claim
(DIS-25) and origin-strategy's credentials "must be supplied on POST" (SPA-22).

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

## Lost-nuance entries added by the 2026-08-03 re-audit (8)

### PROV-11 · customer · "(You will already have this delivery channel)" — default channels pre-seeded
- **Already in scratch?** no
- **Lost prose:** old ~341: "(You will already have this delivery channel)." — dropped when the defaultDeliveryChannels example was swapped to `iiif-av`. The fact that new customers are pre-seeded with default delivery channels is stated nowhere in the new page.
- **Recommendation:** restore to the new `defaultDeliveryChannels` section (and see ACC-19 — the new example there is internally inconsistent: `iiif-img` channel with an `iiif-av/default-video` policy).

### PROV-12 · customer · space-level images endpoint shares the extended query syntax
- **Already in scratch?** no (scratch parks only the narrower allImages note)
- **Lost prose:** old ~155: "this and /customers/x/spaces/y/images should work the same way, using an extended asset query syntax that takes the metadata values, tags, roles, and id(s)."
- **Recommendation:** move to scratch/customer.md (design intent; ties to DIS-04).

### PROV-13 · customer · pointer to a "Managing portal users" page
- **Already in scratch?** no
- **Lost prose:** old ~418: "See [Managing portal users](portal-users) for details." — the only pointer to a portal-users topic. (The target never existed in the old repo either — dangling there too.)
- **Recommendation:** needs-decision — ties to ACC-10's "expand vs new page" question.

### PROV-14 · adjuncts · `iiifLink` expression semantics + cross-links
- **Already in scratch?** no
- **Lost prose:** old ~421: "This property is used when the adjunct is _expressed_ by the platform in the IIIF Presentation API, either in the [single asset manifest](asset#manifest) or in a [Named Query](named-queries)."
- **Recommendation:** restore to the new `iiifLink` section (explains what the field is *for*).

### PROV-15 · adjuncts · content-POST fragments dropped without capture
- **Already in scratch?** partially (the main content workflow is parked; these fragments are not)
- **Lost prose:** "removing the need to manage the origin" rationale (~89); "or by POSTing binary content to the adjunct's ../content URI" clause on `publicId` (~404); the "** assumes you will provide content later by binary POST" table footnote (~599); the "content | ignored ×4" table row (~593).
- **Recommendation:** fold into scratch/api-doc/adjuncts.md alongside the ADJ-01 material.

### PROV-16 · delivery-channels · default policy's Image API version deliberately unspecified
- **Already in scratch?** no
- **Lost prose:** old ~302: "_(future policy could dictate whether v2, v3 etc)_" — the only statement that the `default` iiif-img policy's unspecified version is future-extensible; its sibling notes were parked, this one wasn't.
- **Recommendation:** move to scratch/delivery-channels.md.

### PROV-17 · registering-assets · the `manifest` (singular) property and its URL pattern
- **Already in scratch?** partially (scratch has a bare TODO; scratch/asset.md's manifest note lacks the URL pattern)
- **Lost prose:** old ~74/100: `manifest` "links to a document that contains all the outputs the platform is providing for the asset", with worked pattern `https://dlcs.io/iiif-manifest/{customer}/{space}/{id}`. The new page's `manifests` is a *different* property.
- **Recommendation:** move to scratch/registering-assets.md; feeds SPA-04/SPA-15.

### PROV-18 · batch/registering/collections · queue-limit numeric conflict (100 vs 250)
- **Already in scratch?** no
- **Lost prose / conflict:** old batch said limit **100** (PROV-05); new registering-assets says **250** "(a platform-configured limit)" with the worked example rescaled; new batch says only "configurable"; old collections advice ("e.g., 100") lingers in the new page. Code: `ApiSettings.MaxBatchSize = 250` (verified 2026-08-03) — so 250 is the shipped default and PROV-05's "restore 100" recommendation is superseded.
- **Recommendation:** make batch.mdx, registering-assets.mdx and collections.mdx agree on "250 by default, platform-configured"; close PROV-05 accordingly.

---

## Lost-nuance entries from the completion pass (2026-08-03, remaining ten pages) (6)

### PROV-19 · space · `"maxUnauthorised": -1` dropped from the example JSON
- **Already in scratch?** only as the cryptic line "space has `maxUnauthorised` = 1" (which contradicts the old example's -1 and records nothing)
- **Lost prose:** old example included `"maxUnauthorised": -1`; no `## maxUnauthorised` section existed in old or new.
- **Recommendation:** ~~needs-decision~~ **probably-drop from docs** — PO intent (2026-08-03): the field is to be *replaced* by the planned space-level `defaultMaxWidth`/`defaultOpenFullMax` properties (ADR 0010 pattern), so the example omission stands; SPA-05 becomes a deprecate-and-replace sequencing card. scratch/space.md updated with the intent.

### PROV-20 · space · defaultRoles range rationale vs Deliverator docs
- **Already in scratch?** no (now added)
- **Lost prose:** "NB deliverator readthedocs has this a Hydra collection of vocab:Role, which is wrong - they are default values for the assets, therefore an array of string URIs."
- **Recommendation:** park — provenance for the `Array of xsd:string` range choice; a Deliverator cross-checker would otherwise find an unexplained conflict.

### PROV-21 · batch · "The following information will likely change" caveat on images
- **Already in scratch?** no (now logged)
- **Lost prose:** the volatility flag preceding the asset-in-one-batch paragraph. The semantics DID change (images/assets split), so the new settled prose is right.
- **Recommendation:** probably-drop; logged in scratch/batch.md as "caveat existed, resolved by the images/assets split".

### PROV-22 · origin-strategy · scratch silently normalised the original credentials-table status codes
- **Already in scratch?** the section is preserved, but with 200/204 substituted for the original's `201`/`201`
- **Lost prose:** old rows: `| PUT | Update stored credentials | xsd:string | owl:Nothing | 201 |` · `| DELETE | Remove credentials | - | owl:Nothing | 201 |` (201 on DELETE — odd, but that's what it said).
- **Recommendation:** park — one-line correction note added to scratch/origin-strategy.md; a preserved-original must not silently improve the original.

### PROV-23 · single-asset-manifest · adjuncts "with auth services if they have them"
- **Already in scratch?** no (now added)
- **Lost prose:** old line 30: "Any adjuncts are listed as seeAlso properties of the Canvas, _with auth services if they have them_."
- **Why it matters:** verified NOT implemented (`ManifestV3Builder.CreateExternalResource` emits no `Service` on adjunct entries) — dropping it from the live page was right, but the requirement must not be forgotten when adjunct access control lands (ADJ-03 territory).
- **Recommendation:** restore-candidate **for scratch** (done 2026-08-03), not for the live page.

### PROV-24 · single-asset-manifest · planned example-scenario coverage narrowed
- **Already in scratch?** no (now noted)
- **Lost:** old (empty) example headings promised video+two-adjuncts, image+file-channel-combination+three-adjuncts, and Word-doc+adjunct scenarios; the new set has no video+adjuncts, no channel-combination (which exercises the distinct rendering-alongside-painting path), and its file-only example has no adjunct.
- **Recommendation:** park — folded into DIS-19's example-debt scope as "scenario coverage narrowed".

## Silent normative changes — completion pass additions (2026-08-03)

- **space** (all verified as corrections, none recorded anywhere): PATCH status 202→200 (correct; and BOTH old and new omit the real 409s on PUT/PATCH — SPA-20); DELETE 202+body→204 (correct at runtime; the annotation still lies — SPA-09/XC-01); storage ops path corrected from the customer-level to the space-level route.
- **queues, Global Queue section** (all verified as corrections): `@type` vocab:Queue→vocab:QueueSummary with the full 7-field shape; incoming/priority reworded to image-assets-only; success/failed "Always 0"→deprecated-Deliverator. **The scratch file still said this section was "not yet ported" — fixed 2026-08-03**; that staleness is what hid these.
- **batch**: images GET semantics narrowed from "all assets regardless of state" to "assets for which this is the most recent batch" — verified correct (`GetBatchImages.cs:10`); domain cell vocab:Space→vocab:Batch (old was a copy-paste error); superseded wording "associated with"→"processed by" (consistent, low risk, unverified in detail).
- **origin-strategy**: credentials "**may** be supplied in a POST" → "**must** be supplied in a POST" — **the new claim is WRONG** (required for basic-http-authentication, de-facto required for sftp, actively rejected for s3-ambient; contradicts the page's own line 116) → card **SPA-22**.
- **single-asset-manifest**: "always a Choice resource" carried forward and elaborated — **WRONG** (bare Sound/Video body for a single transcode, `PaintingChoice` only for >1; and no-transcode AV assets get NO canvas, stated nowhere) → card **DIS-25**. Thumbnail id wording and adjunct-placement sentence both silently *corrected* (verified right).
- **custom-headers**: example `@context` changed to the real Hydra style (`.../contexts/CustomHeader.jsonld`) while other pages keep `future.json` — cross-page inconsistency, cosmetic, unnoted.
- **size-restrictions** (additions, not changes): "setting these fields with no roles is not an error" — verified consistent with the validator for `openFullMax`; "the `thumbs` delivery channel only serves content accessible without authentication" — **unverified** → card **DIS-26** (⚠verify).

---

## Silent normative changes (new category, 2026-08-03) — verify, don't just port

Statements that CHANGED between old and new with no scratch/register trail. Unlike
lost nuance, these need verification against protagonist (most now have it):

- **adjuncts:** `origin` optional→required (verified: exactly-one-of origin/externalId, correct); `iiifLink` recommended→required (verified correct); `mediaType` recommended→required (verified correct). All three flips are RIGHT but were silent — the pattern is the problem.
- **customer:** `allImages` readonly True→False (unverified); new unsourced claims — space-name 409 Conflict (verified correct, `CreateSpace.cs:47-52`), "any valid Unicode characters" (unverified).
- **delivery-channels:** DELETE 202→204 (verified correct; sample comment still stale — punch-list 6); `@mediaType`→`mediaType` and `defaultdeliverychannels`→`defaultDeliveryChannels` casing (unverified).
- **customer example:** new custom-header example adds `"space": 1` while keeping "you will already have this custom header" prose (unverified whether pre-seeded headers carry a space).
- **adjuncts:** new page still documents a working `content` GET that scratch says doesn't work (ADJ-02 — verified: not emitted).

---

## Cross-reference: accuracy concern noted in passing (out of scope but flagged)

The new `size-restrictions.mdx` documents the `openMaxWidth` / `substitute` image
service (scenarios 8–11) as implemented; MEMORY.md flags this as "documented but
absent from protagonist code". That is an accuracy concern, not a provenance loss,
but worth carrying into the sprint. *(2026-08-03: re-verified absent — repo-wide
grep hits only jquery. See SPA-01/DIS-18.)*
