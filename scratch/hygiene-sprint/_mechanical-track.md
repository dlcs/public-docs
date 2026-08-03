# Mechanical track — candidate list (for the session-0 veto pass)

> **Status: CANDIDATES, nothing pre-approved.** Prepared 2026-08-03 from the 137-card
> register. Inclusion criteria: the card's facts are **verified against code** (2026-08-03
> passes), the fix is obvious, and no design question is attached. Session 0 spends ten
> minutes vetoing anything secretly contentious; whatever survives becomes the draft PRs
> described in README "Mechanical track". One commit per card ID; a named owner per surface
> merges.
>
> **Excluded on principle:** anything touching the published adjunct-queue sections of
> queues.mdx/batch.mdx (release-gated per the *main = released behaviour* decision) — their
> *sample* fixes are included, doc changes wait. Anything where code-vs-docs could go either
> way stays on the decision track.

## Batch D1 — public-docs: status-code & ops-table corrections (owner: PO)

| Card | Fix |
|:--|:--|
| SPA-20 | asset PUT row: remove 404, add 400; fix asset#id validation sentence (only `@id` is validated); space PUT row: add 400 + 409; space PATCH row: add 409 |
| ACC-12 (part) | keys ops table: add DELETE row (204/400); customer PATCH row: add 400; storage GET rows: add 404. *(custom-header PUT row EXCLUDED — waits on the ACC-15 ruling)* |
| PRO-03 | add `## errors` section to batch.mdx (asset flavour only; adjunct flavour is release-gated) |
| PRO-12 (part) | fix "active" semantics prose for the ASSET queue section (adjunct section release-gated) |
| PRO-13 (part) | add 404 to GET /queue method table (adjunct part release-gated) |
| ADJ-17 | adjuncts.mdx `### batch` section: "image"→"adjunct", `vocab:Image`→`vocab:Adjunct`, add 404 |
| ADJ-18 | adjuncts.mdx: note POST 409 on duplicate id; PUT-update returns 200 |
| SPA-22 | origin-strategy.mdx:166: "must be supplied" → "required for basic-http-authentication and sftp; not permitted otherwise" |

## Batch D2 — public-docs: cosmetics & consistency (owner: PO)

| Card | Fix |
|:--|:--|
| DIS-12 | named-queries syntax table `s3` example: `&manifest=s3` → `&s3=p2` |
| DIS-21 | collections.mdx page-2 example: `api.dlcs.digirati.io` → `api.dlcs.example` |
| DIS-24 | entrypoint.mdx examples: `api.dlc.services` → `api.dlcs.example` |
| ACC-19 (docs part) | customer.mdx LinkCard titles/descriptions; stray trailing spaces in sample; defaultDeliveryChannels example made internally consistent |
| SPA-21 | asset.mdx maxWidth: document upper bound "platform-configured, default 5000"; align size-restrictions "e.g., 10000px" |
| SPA-18 | add brief `## imageService` / `## thumbnailImageService` sections (thumbs-channel conditionality) |

## Batch D3 — samples & docstrings (owner: PO)

| Card / punch-list | Fix |
|:--|:--|
| Punch-list 1 / ADJ-09 (sample half) | `p13_adjuncts/iiif_link_adjuncts.py`: add `mediaType` to AnnotationPage adjunct |
| ADJ-15 addendum | same file: 5th adjunct (no `iiifLink`) — remove or comment out with pointer to ADJ-06 scratch |
| Punch-list 2 | `p12_origin_strategies/get_put_delete_origin_strategy.py`: fix credentials docstring |
| Punch-list 4 / XC-10 | `p15_asset_queries/asset_queries.py`: fix stale "ordering not supported" + "include ignored" docstrings |
| Punch-list 5 / SPA-16 | `p07_asset/...:75`: DELETE comment 200→204 |
| Punch-list 6 / SPA-16 | `p11_delivery_channels/...:66`: DELETE comment 202→204 |
| PRO-11 (sample half) | both adjunct queue-POST samples: `space`/`image` → required `asset` field; `adjunct_batch_operations.py`: build `/current` + `/adjuncts` URLs from `@id` until links are emitted |

## Batch C1 — protagonist: annotation one-liners, zero behaviour change (owner: named protagonist dev)

| Card | Fix |
|:--|:--|
| SPA-08 / XC-01 | `DeliveryChannelPoliciesController.cs:268`: 202 → 204 |
| SPA-09 / XC-01 | `SpaceController.cs:115`: 200+Space → 204 |
| XC-05 | `ImageController.cs` ×13: `ProblemDetails` → `Error` |
| XC-11 | `AdjunctsController.cs:92-94` PUT: annotate 200+201, type `Adjunct` |
| XC-01/05 family | `CustomerAdjunctsController.cs:42`: 404 annotation → 400 (matches code path) |

## Batch C2 — protagonist: cosmetic model/validator fixes (owner: named protagonist dev)

| Card | Fix |
|:--|:--|
| ACC-04 | `CustomHeader.cs:34`: `ReadOnly = true` → `false` (matches behaviour AND docs) |
| ACC-05 | validator message "named query" → "custom header"; rename `hydraNamedQuery` param |
| ACC-07 (+ extensions) | distinct `JsonProperty` Orders: ImageStorage 55/55/55, ApiKey key/secret 12/12, PortalUser created/roles 13/13 |
| ACC-19 (code part) | vocab typo strings: `ApiKey.cs:87`, `Customer.cs:123` |
| PRO-10 | `QueueSummary.cs`: fix `HydraClass` attribute + `BootstrapViaReflection` target |
| DIS-13 | `NamedQuery.cs`: drop stale `[Unstable]`; remove phantom PATCH from `DefineOperations` |

## Borderline — room assigns the track in the veto pass

| Card | Why borderline |
|:--|:--|
| PRO-05 | GET priority-queue works and docs deny it — but card asks devs to confirm GET is *intended* before documenting |
| DIS-01/02/03 | verified shipped (ordering / include=adjuncts / manifests filter) but they're promotions: new doc sections + Aside rewrites + sample additions — bigger than a correction |
| SPA-13 / SPA-19 | removing phantom Hydra operations (PATCH; credentials PUT) — code-only, safe, but "remove advertised surface" arguably needs a dev nod |
| SPA-12 | origin-strategy readonly/writeonly attribute fixes — depends on ruling "docs tables are the intended contract" (XC-09) |
| DIS-25 | single-asset-manifest Choice prose vs code — fix docs OR declare always-Choice the contract and change code; needs a dev call |
| ACC-15 | custom-header PUT 201: one-word handler fix (XC-03 makes it automatic) — but it IS a wire behaviour change |

**Not mechanical, despite being verified:** everything DESIGN/CODE-MISSING; the trailing-space
property names (XC-06 — breaking wire change); admin-field leakage (ACC-03); legacy link
removal (XC-07, DIS-14/15/16); all release-gated adjunct-queue doc changes; all scratch
promotions that add features to the published surface.
