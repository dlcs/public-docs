# Hygiene sprint — external context: open issues & RFCs

_Generated 2026-06-25. `gh` CLI authenticated as `tomcrane` (scopes: repo, read:org, workflow) — all issue queries succeeded._

_⟳ Refreshed 2026-08-03: counts now **143** protagonist / **67** iiif-presentation / **8** iiif-auth-v2.
Closed since generation: #1157, #1158, #1160 (adjunct queue endpoints — implemented by PR #1228, develop-only);
#1218 (store size for all hosted adjuncts — PR #1220, on main); #1217, #1219 (bug-and-fix pairs, also on main).
New open issues: **#1233** "Stupidly large `size` requests overflow the cast from string path param"
(cross-cutting — error handling, sits alongside #1134/#823/#731), **#1229** "Reconcile `Queue` endpoint
values getting out of sync" (processing — linked from PRO-06). Open PR **#1230** proposes
`rfcs/024-pdf-generation-text-services.md` (see RFC list). Individual closures are struck through below._

_⟳ Refreshed 2026-08-12 (session-2 pre-flight): counts now **137** protagonist / **67** iiif-presentation /
**8** iiif-auth-v2. Triage closures since 08-03: #1050 (space DELETE swagger — closed citing session-0
DELETE-204 ruling), #744 (platform-wide maxWidth — shipped v1.13.1), #920 (bulk delete — superseded by
**#1064**), #899 (invalid hypermedia links — space `metadata` named as example; feeds SPA-06), #356 (stale,
Deliverator retired), plus adjunct items #1166/#1127/#1121 and #706. New open issues from hygiene session 1:
**#1240** (space-level storage policies, ACC-09) and **#1245** (customer→iiif-presentation link, ACC-16)._

_⟳ Refreshed 2026-08-17 (session-3 pre-flight): counts now **148** protagonist / **64** iiif-presentation /
**8** iiif-auth-v2. All six session-2 protagonist PRs (#1258/#1259/#1260/#1262/#1263/#1266) and public-docs
PR #14 merged 2026-08-17 morning; hydra-model-flags re-baselined @develop 6813b7a2 — only the expected Image
changes, no drift. New open issues from hygiene session 2: **#1248–#1253**, **#1261** (SEVERE: PATCH wipes
omitted roles/tags — watch), **#1264** (legacy-mode deprecation path). New from donaldgray 2026-08-14/17:
**#1265** (cleanup handler leaves thumbs across auth/open locations — fix is open PR **#1269**),
**#1270** (extend `/allImages` PATCH beyond `manifests` — explicitly plans to revert the #1259 Swagger
exclusion when implemented; annotate ACC-20 if it lands), **#1271** (💬 access levels for API keys — bears on
the auth cluster). Open PRs: **#1268** (map Hydra ReadOnly/WriteOnly onto OpenAPI — makes the vocab flags
operational in Swagger; its tests initially predated #1262 — clash fixed 2026-08-17, rebased with
`id`/`imageService` cases removed), #1269 (var rename applied same day), #1230._

_⟳ Refreshed 2026-08-19 (session-4 pre-flight): counts now **148** protagonist / **65** iiif-presentation /
**8** iiif-auth-v2. All five session-3 protagonist PRs (#1272/#1273/#1274/#1276/#1277) merged same day
2026-08-17; public-docs PR #15 merged 2026-08-19 morning; hydra-model-flags re-baselined @develop 92fa2661 —
only the expected session-3 changes (Batch −estCompletion +assets, CustomerQueue −images), no drift. Release
still **v1.13.2** (2026-07-17) — all release-gated twins remain parked. New issues: protagonist **#1275**
(PO: generate docs from HydraModel classes? — bears on XC-09/the dump tool), iiif-presentation **#649**
(reject painting request implying Choice without choiceOrder — single-asset-manifest/Choice adjacency,
DIS-25 family). Open protagonist PRs: only **#1278** (correlationId handling, donaldgray) and #1230 (RFC 024).
Watch list unchanged: #1261 (SEVERE PATCH wipe), #1270, #1271, #1229._

_⟳ Session-5 outputs (2026-08-26): counts unchanged **151** protagonist (no new issues — PO parked
adjunct gaps on existing tickets: **#1140** content (ADJ-01), **#1141** roles (ADJ-03), **#1142**
otherAdjuncts (ADJ-06), **#1128** cleanup handler = the reason `deleteFrom` is undocumented
(ADJ-11/12)). **dlcs/private-protagonist #13** ("Adjunct-producing pipeline" epic, 2023) now
carries two docs-note comments parking `creator` and `source` (ADJ-04/05). One new draft PR from
us: **#1292** (adjunct POST annotations; annotation-only). #1207 (adjunct delete uses origin-bucket
null check) noted as a live bug adjacent to the delete path now documented._

_⟳ Session-4 outputs (2026-08-19): counts now **150** protagonist (+2). New issues raised by us:
**#1279** (RFC wanted: tags/roles/id filtering, portal-team audience; scope comments add multi-value
semantics + the `space` filterOnSpace correction), **#1280** (unknown orderBy → 400 not handled-500).
Four new draft PRs from us: **#1281** (orderBy whitelist 400 — breaking), **#1282** (EntryPoint queue
link), **#1284** (dead portalRoles link + orphaned PortalRole vocab class removed — breaking),
**#1286** (NamedQuery template → Order 12). Comments: #960 (boundary — batch LIST endpoints only;
per-batch asset collections already order), #1279 (corrections/scope). #566 now load-bearing for the
DIS-09 global-NQ contract table (promotion gate)._

_⟳ Refreshed 2026-08-26 (session-5 pre-flight): counts now **151** protagonist / **65** iiif-presentation /
**8** iiif-auth-v2. All four session-4 protagonist PRs (#1281/#1282/#1284/#1286) merged 2026-08-19;
public-docs PR #16 merged 2026-08-26 morning. hydra-model-flags re-baselined @develop 1a77352a — only the
expected session-4 changes (EntryPoint −portalRoles +queue; PortalRole class removed), no drift; the
Adjunct / AdjunctBatch / CustomerAdjunctQueue tables are byte-identical to the 08-19 baseline. Release still
**v1.13.2** (2026-07-17) — all release-gated twins remain parked. develop has moved substantially in
non-adjunct areas: **.NET 10 + package upgrades**, **ImageSharp → netvips (libvips)**, correlationId
handling (#1278 merged), NQ ordering moved to the database, and **PR #1289** (merged) fixing **#1285**
(`/raw-resource/` NQ output ignored `assetOrder` — DIS-11's "DISCOVERY raw-resource ignores assetOrder"
observation is now a fixed bug on develop; the docs sentence describes released behaviour and stays until
release). No adjunct-surface code has changed since 2026-08-05 (AdjunctsController / validator / converter /
CustomerAdjunctsController / AdjunctQueues all older than the cards' 08-03 verification, bar our own #1234
annotation fix) — session-5 card premises are fresh. New issues: protagonist **#1283** (API endpoint to
delete a zip control-file — named-query zip projection adjacency, DIS-07), **#1287** (synchronous ingests
not cleaned up when cancelled — processing). Adjunct issue state for session 5: #1141 (access-controlled
adjuncts → ADJ-03), #1140 (binary content adjuncts → ADJ-01), #1142 (`otherAdjuncts` → ADJ-06), #1207
(delete/update null-check on origin bucket → ADJ-12 adjacency), #1128 (varnish cleanup for adjuncts)
all still open; #1127 / #1121 / #1166 confirmed closed. Open protagonist PRs: only #1290 (engine warnings
housekeeping) and #1230 (RFC 024). Watch list unchanged: #1261 (SEVERE PATCH wipe), #1270, #1271, #1229._

Theme tags: account-access · spaces-assets · processing · discovery-delivery · adjuncts · iiif-auth · cross-cutting · none

## Open issues by repo

### dlcs/protagonist (134 open at generation; 143 as of 2026-08-03)

Directly-related-to-known-discrepancy issues are flagged in the right column. Remainder listed compactly afterwards.

| # | title | theme | discrepancy note |
|:--|:--|:--|:--|
| 1233 | Stupidly large `size` requests overflow the cast from string path param | cross-cutting | new 2026-07 — error handling (XC-04 family) |
| 1229 | Reconcile `Queue` endpoint values getting out of sync | processing | new 2026-07 — linked from PRO-06 (`test` reconciliation) |
| 1207 | delete/update of adjuncts uses null check on origin bucket not storage bucket | adjuncts | adjuncts bug |
| 1183 | POST AssetQuerySyntax | discovery-delivery | **asset-queries** — POST query support (docs describe GET only) |
| 1166 | Adjunct Batch / Queue querying | adjuncts | **adjuncts** endpoints not yet documented |
| ~~1160~~ | ~~Get bulk adjuncts in batches endpoints~~ | adjuncts | **CLOSED 2026-07** — PR #1228 (develop) |
| ~~1158~~ | ~~GET /adjunctQueue/ endpoints~~ | adjuncts | **CLOSED 2026-07** — PR #1228 (develop) |
| ~~1157~~ | ~~Get customer AdjunctQueue~~ | adjuncts | **CLOSED 2026-07** — PR #1228 (develop) |
| 1142 | Handle "otherAdjuncts" iiifLink | adjuncts | **adjuncts** link/property naming |
| 1141 | Adjuncts can be access-controlled | adjuncts / iiif-auth | adjuncts |
| 1140 | Adjuncts consisting of binary content | adjuncts | adjuncts |
| 1134 | Update problem+json contents | cross-cutting | **error/status-code format** — affects documented error responses |
| 1132 | Update info.json behaviour for iiif auth v2 | iiif-auth | auth |
| 1128 | Extend varnish cleanup handler for adjuncts | adjuncts | adjuncts |
| 1127 | Exclude optimised s3-ambient sizes from AdjunctSize count | adjuncts | still open, but appears substantially delivered by PR #1220 (`Optimised` flag; confirm & close?) |
| 1121 | Extend recalculator job to tally adjunct size | adjuncts | adjuncts |
| 1100 | Allow deletion of zip NQ projections | discovery-delivery | **named-queries** projection lifecycle |
| 1064 | Improve batch deletion of content | processing | |
| 1063 | Revisit Batch testing for BatchAssets | processing | |
| 1050 | Swagger docs incorrect for DELETE space | spaces-assets | **docs discrepancy** — swagger vs behaviour for DELETE space |
| 1019 | Allow CustomerStoragePolicy to be updated for a customer | account-access | **storage** policy API gap |
| 1018 | Allow StoragePolicy to be deleted via API | account-access | **storage** policy API gap |
| 1017 | Allow StoragePolicy to be written via API | account-access | **storage** policy API gap |
| 1014 | Allow default Image + Presentation version per customer | account-access | |
| 1013 | Long "origin" values | spaces-assets | |
| 905 | Allow 'NoStorageCheck' in API | spaces-assets | API flag not documented |
| 899 | Invalid hypermedia links in responses | cross-cutting | **entrypoint/hypermedia links** discrepancy |
| 874 | Support required NQ parameters | discovery-delivery | **named-query params** |
| 823 | Tidy message returned when specifying invalid PolicyData | cross-cutting | error-message format |
| 794 | Remove specific services from Asset API response, link to Single Asset Manifest | spaces-assets | asset response shape |
| 744 | Platform-wide maxWidth | discovery-delivery | **openMaxWidth / maxWidth** related |
| 738 | Use more granular models for different operations | cross-cutting | |
| 731 | Unexpected property in error message if serialisation fails | cross-cutting | error-message format |
| 706 | Add default value to RestrictedAssetIdCharacterString setting | cross-cutting | **identifier policy** related |
| 668 | Add Rights Statement field to Asset | spaces-assets | |
| 623 | Drop IOP and ThumbnailPolicy columns from Asset | spaces-assets | delivery-channels migration |
| 601 | Add `scale` field to Asset | spaces-assets | |
| 566 | Customers can view Global NamedQueries | discovery-delivery | named-queries visibility |
| 538 | Manage Auth Services via API | iiif-auth | **auth REST API** (the missing subsystem) |
| 451 | Tighten up BatchPatch operation validation | processing | |
| 402 | Endpoint to reingest any failed assets in a batch | processing | |
| 401 | Allow failed assets to be queried per batch + space | processing | |
| 337 | Allow more Asset properties to be changed via PUT and PATCH | spaces-assets | asset readonly/writeonly tables |
| 316 | Strict max and lenient max | discovery-delivery | **openMaxWidth / maxWidth** related |
| 284 | Manage role-provider configuration | iiif-auth | **roles / auth REST API** |
| 74 | If we stick with Hydra, bring it up to date | cross-cutting | **Hydra property names / vocab** |
| 53 | Semantic versioning of DLCS APIs | cross-cutting | |
| 34 | Improve the developer experience for platform users | cross-cutting | docs |

Remaining protagonist issues (no direct doc-discrepancy link) by theme:
- **processing/engine**: 1147, 1133, 1068, 1065, 1025, 970, 968, 936(NQ errors), 927, 920, 910, 888, 861, 852, 840, 786, 768, 684, 678, 608, 355, 220-era, 318, 263, 252, 56(reingest)
- **discovery-delivery (orchestrator/image-server/thumbs/channels)**: 1145, 1117, 1059, 1003, 980, 789, 782, 744(above), 638, 503, 502, 498, 488, 486, 478, 457, 436, 412, 315, 285, 272, 258, 249, 207, 41, 31
- **cross-cutting/sustainability/tech-stack**: 1122, 1147, 769, 733, 706, 599, 529, 528, 470, 458, 446, 432, 348, 336, 335, 295, 296, 262, 154, 106, 57, 50, 28, 27
- **auth**: 1132, 1003, 413, 356, 282, 225, 164
- **portal**: 924, 897, 896, 291
- **usage scenarios (2020-21 legacy backlog)**: 47, 46, 45, 44, 43, 42, 40, 39, 38, 37, 36, 45 etc.

### dlcs/iiif-presentation (66 open at generation; 67 as of 2026-08-03)

| # | title | theme | discrepancy note |
|:--|:--|:--|:--|
| 620 | Return details of previous pipelines | processing | **pipelines** (scratch notes exist) |
| 619 | Custom Paths | discovery-delivery | path templates |
| 618 | Manifest requiring IIIF-CS ingestion | spaces-assets | |
| 617 | Manifests not requiring IIIF-CS ingestion | spaces-assets | |
| 616 | Search Within (epic) | discovery-delivery | |
| 612 | Rationalise the empty adjuncts array response | adjuncts | **adjuncts response shape** discrepancy |
| 597 | PathParts should flag errors | cross-cutting | |
| 579 | Manifest payloads missing `"Type":"Manifest"` return 500 | cross-cutting | **status-code** (500 vs 400) |
| 572 | paintedResource.asset string `"space"` returns 500 | cross-cutting | **status-code** (500 vs 400) |
| 571 | Slugs can contain forward slashes/FQDNs | discovery-delivery | identifier/slug validation |
| 566 | Support Presentation 4 | discovery-delivery | |
| 562 | Mix implicit and explicit ordering | discovery-delivery | **ordering** |
| 551 | Clean up path generation logic | discovery-delivery | |
| 550 | Revisit SeeAlso api-hierarchical links | cross-cutting | **entrypoint/hierarchical legacy links** |
| 540 | Tidy error messages? | cross-cutting | error-message format |
| 530 | Matched canvases act as hardpoint in canvas order | discovery-delivery | ordering |
| 504 | Multi-canvas constructs reject if canvasLabel mismatch | spaces-assets | |
| 500 | Support DELETE on hierarchical path | discovery-delivery | collections |
| 494 | support PATCH in IIIF collections | discovery-delivery | collections |
| 493 | Support paging of IIIF collections | discovery-delivery | **collections paging** |
| 492 | Update collection containment on moving children | discovery-delivery | collections |
| 491 | Update IIIF collections to allow children created | discovery-delivery | collections |
| 490 | Add properties to IIIF collections for containment | discovery-delivery | collections |
| 485 | Collections: containment vs membership | discovery-delivery | **collections** conceptual |
| 466 | @context should be first property in API response | cross-cutting | **Hydra/property ordering** discrepancy |
| 465 | Flesh out swagger docs | cross-cutting | docs |
| 464 | Consistent API PUT and POST behaviour | cross-cutting | **PUT/POST status-code** semantics |
| 237 | Include currentBatch identifiers in manifests response | processing | |
| 147 | Add `publicId` to the `items` property | spaces-assets | |

Other iiif-presentation issues: 567, 547, 538(healthchecks), 536, 519, 508, 478(NQ — n/a here), 447, 434, 423, 408, 404, 401(cache-control), 395, 388, 381, 371, 359, 358, 328, 315, 310, 302, 291, 289, 284, 278, 239, 235, 233, 226, 225, 220, 213, 208, 205, 169, 136, 135, 103, 64 — mostly tech-debt/processing/collections backlog.

### dlcs/iiif-auth-v2 (8 open) — all theme: iiif-auth

| # | title | discrepancy note |
|:--|:--|:--|
| 48 | Microsoft Entra role provider | role provider expansion |
| 46 | Create clickthrough on customer creation | auth onboarding |
| 43 | Set appropriate cached headers | |
| 42 | Fix gesture path default config | |
| 39 | Add sonarqube | |
| 7 | Expand RoleProvider logic | **roles** page subject |
| 10 | Update SessionUser for multi-customer/role tokens | |
| 9 | Remove expired SessionUsers | |

### dlcs/public-docs — 0 open issues
### dlcs/docs (old) — 0 open issues

## RFCs found

### dlcs/protagonist — `docs/rfcs/` (numbered RFC series) + `docs/adr/`
- `rfcs/001-thumbnails.md` — thumbnail generation/policy design.
- `rfcs/002-storage-and-orchestration.md` — storage + orchestration architecture.
- `rfcs/003-IIIF-3-support.md` — supporting IIIF Image/Presentation 3.
- `rfcs/004-Named-Queries.md` — **named queries design** (discovery-delivery).
- `rfcs/005-Access-Control.md` — **auth/access-control** original design (iiif-auth).
- `rfcs/006-Design-Principles.md` / `006-appendix-shape-of-traffic.md` — API design principles + traffic shape.
- `rfcs/007-cantaloupe-image-server.md` — image server choice.
- `rfcs/008-more-access-control-oidc-oauth.md` — **auth via OIDC/OAuth2** (iiif-auth).
- `rfcs/009-asset-family-improvements.md` — asset family model (image/av/file).
- `rfcs/010-special-server-implementation.md` — special/large-image server.
- `rfcs/011-pdfs-as-input.md` / `013-pdfs-as-input-storage.md` — PDFs as input + storage.
- `rfcs/012-auth-service.md` — **auth service design** (iiif-auth; relates to roles/auth-service docs pages).
- `rfcs/014-delivery-channels-database.md` — **delivery channels DB design** (delivery-channels page).
- `rfcs/015-iiif-av-delivery-channel-settings.md` — AV delivery channel settings.
- `rfcs/016-asset-metadata.md` — asset metadata model.
- `rfcs/017-asset-modified-cleanup.md` — cleanup on asset modify/delete.
- `rfcs/018-revisit-batches.md` — **batches rework** (queues/batch pages).
- `rfcs/019-presentation-dlcs.md` — querying across IIIF Presentation + DLCS.
- `rfcs/020-non-image-iiif.md` — non-image content resources.
- `rfcs/021-mediaconvert.md` — AWS MediaConvert transcoding.
- `rfcs/022-stub-assets.md` — stub asset concept.
- `rfcs/023-hosted-adjunct-id.md` — **adjunct identifier policy** (adjuncts + identifier policy).
- `rfcs/024-pdf-generation-text-services.md` — **proposed, not merged** (open PR #1230, 2026-07): Text-Services for PDF generation from named queries. Bears on **named-query PDF output** (DIS-07/DIS-08) and supersedes-or-extends `011`/`013` PDF thinking; also adjacent to the pipelines design space (PRO-09).
- ADRs: `adr/0000`–`0012` — project design, composite handler, image server, storage-use tracking, dependabot, optimised origin, engine-imageserver, image-server optimization, ET replacement, engine-appetiser-thumbs, **0010-replace-maxunauthorised** (relevant to maxWidth/auth), orchestrator-proxy, text-services-integration.

### dlcs/iiif-presentation — `docs/rfcs/` + `docs/ADR/` + `docs/notes/`
- `rfcs/0001-mermaid-diagrams.md` — tooling.
- `rfcs/0002-manifest-write-mvp.md` — manifest write MVP design.
- `rfcs/0003-identity-rewrites.md` — **identifier/identity rewrite policy**.
- `rfcs/0004-etag-changes.md` — ETag/concurrency handling.
- `rfcs/0005-mixed-manifests.md` — manifests mixing CS-ingested + external content.
- `rfcs/0006-adjuncts.md` — **adjuncts design** (adjuncts page).
- ADR `0001-database-update-failure.md`, `0002-canvas-id-parsing.md`; notes on batch-completion, canvas-paintings, manifest-generation, paintedresource-to-manifest, reingest-property, storage-keys.

### dlcs/iiif-auth-v2 — no RFC/ADR docs (only readme.md files). Auth design lives in protagonist RFCs 005/008/012.
### dlcs/docs (old) — no RFC docs (Nextra mdx content + node_modules only).

## Suggested links (issue/RFC → sprint theme / known item)

- **Adjuncts**: protagonist #1166 (still open) /~~#1160/#1158/#1157~~ (closed 2026-07, implemented by PR #1228 — see PRO-08) /#1142/#612(iiif-pres) + RFC `023-hosted-adjunct-id.md` + iiif-presentation RFC `0006-adjuncts.md` → adjuncts sprint card. #612 + #1142 directly touch documented response shape / `otherAdjuncts` link naming.
- **openMaxWidth / maxWidth** (known discrepancy: documented but absent): protagonist #744 "Platform-wide maxWidth" + #316 "Strict max and lenient max" + ADR `0010-replace-maxunauthorised.md` → decide whether to document or drop. No issue explicitly named "openMaxWidth"/"substitute service" — likely needs a new card.
- **Named-query params** (discovery): protagonist #874 "Support required NQ parameters" + #1100 (delete zip projections) + #566 + RFC `004-Named-Queries.md` → named-queries page accuracy.
- **Hydra property names / ordering** (cross-cutting discrepancy): protagonist #74 "bring Hydra up to date" + iiif-presentation #466 "@context first" + #562 ordering → Hydra/vocab decision card.
- **Status codes / error format**: protagonist #1134 (problem+json), #823, #731 + iiif-presentation #579/#572 (500-vs-400), #464 (PUT/POST consistency), #540 → error-response documentation card.
- **Entrypoint / hypermedia legacy links** (known discrepancy): protagonist #899 + iiif-presentation #550 (SeeAlso hierarchical links) → entrypoint page card.
- **Auth REST API** (the whole roles/auth-service/access-control doc cluster is blocked on this): protagonist #538 "Manage Auth Services via API" + #284 "Manage role-provider configuration" + iiif-auth-v2 #7/#48/#46 + RFCs `005`/`008`/`012` → design-the-auth-REST-API card (prerequisite for roles.mdx / auth-service.mdx / access-control.mdx).
- **Storage policy API** (storage.mdx): protagonist #1017/#1018/#1019 → storage management card.
- **Pipelines** (order-10 page, currently skipped): iiif-presentation #620 "Return details of previous pipelines" → pipelines card.
- **Collections** (discovery): iiif-presentation #485/#490–#494/#500/#493 cluster → collections containment/paging card.
- **Identifier policy** (identifiers.mdx): protagonist #706 (RestrictedAssetIdCharacterString) + iiif-presentation #571 (slug validation) + RFC `0003-identity-rewrites.md` + protagonist RFC `023` → identifier policy card.
- **Asset readonly/writeonly tables** (asset.mdx domain/range accuracy): protagonist #337 (more props via PUT/PATCH), #905 (NoStorageCheck), #601 (scale), #668 (rights) → asset property-table review card.
