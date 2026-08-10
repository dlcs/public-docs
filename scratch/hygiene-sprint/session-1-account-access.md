# Hygiene sprint — Session 1: Account & access

**Scope.** This file collects decision cards for the **Account & access** theme: the
`customer.mdx`, `custom-headers.mdx` and `storage.mdx` documentation pages plus the customer
sub-resources (API keys, portal users). Each card cross-references the live Starlight docs
(`src/src/content/docs/api-doc/*.mdx`), the parked scratch notes (`scratch/api-doc/*.md`), the
richer original Nextra prose (`C:\git\dlcs\docs\pages\api-doc`), and the protagonist API
implementation (`API/Features/{Customer,CustomHeaders,Storage}` and `DLCS.HydraModel`). Findings
are framed as questions for the room — in several cases the code, not the docs, may be what needs
to change. Nothing here has been verified against a live/running API; status-code and field claims
are read from source. Cards namespaced ACC-NN.

**⟳ Verified 2026-08-03** against protagonist develop@8341d780: all 14 cards re-checked against
handlers (not annotations) and hold; the ⚠verify cards are now traced to ground (see inline
updates on ACC-08/09/11/13). One Resolved-list entry proved WRONG for exactly the
annotation-trusting reason this file warns about — see the corrected first bullet below and
ACC-15. New cards ACC-15..19 added from the second pass.

**⟳ Session-1 pre-flight, 2026-08-10:** re-baselined (protagonist release still v1.13.2;
develop@59551f4d = #1236/#1237/#1238 all merged, unreleased; only open PR is #1230/RFC 024;
`_hydra-model-flags.md` regenerated). Read-only live sweep run against **staging**
(`api.dlcs-stage.digirati.io`, customer 15) — note staging serves **pre-session-0 released
code**: trailing-space keys and the three auth links are still on the wire there, so the
session-0 fixes are merged-but-not-deployed. Live results recorded inline on ACC-06/08/09/16.
The two mutating ⚠verify checks (ACC-11 key-POST as non-admin, ACC-13 space-POST defaults)
were deliberately not run pre-session — runnable in-room on request.

## Resolved (Category A) — already correct, no card needed

- ~~**custom-headers PUT returns 200**, not 404-on-update.~~ **⟳ CORRECTED 2026-08-03 — this entry was wrong, and instructively so.** It trusted the `Status200OK` annotation — the exact trap this register's own preamble warns about. `UpdateCustomHeaderHandler` returns `WriteResult.Created` on a successful *update* (`UpdateCustomHeader.cs:50`, unchanged since 2023), which `ModifyResultToHttpResult` maps to **201 Created + Location** (`ControllerBaseX.cs:146-147`). So custom-header PUT success is 201, and custom-headers.mdx:31 ("200 OK, 400 Bad Request") is wrong twice over: wrong success code AND missing the 404 (see ACC-12). Needs a ruling: change the handler to `WriteResult.Updated` (→200, one-word fix, XC-03 family) or document 201. Promoted to card ACC-15 below.
- **Customer PATCH is `displayName`-only.** Confirmed: `CustomerPatchValidator` rejects `id`, `name`, `administrator`, `created`, `keys`, `acceptedAgreement` and requires `displayName` (`CustomerPatchValidator.cs:13-20`); `PatchCustomer` reads only `DisplayName` (`CustomerController.cs:149`). Live mdx already states this.
- **ApiKey `@type` is `vocab:Key`.** Confirmed `ApiKey.cs:58`. mdx key examples use `vocab:Key` — match.
- **CustomHeader PUT does not create.** `UpdateCustomHeaderHandler` returns `WriteResult.NotFound` when the header is absent (`UpdateCustomHeader.cs:37-41`), so the mdx claim that a header "can only be created via POST … not by PUT to a chosen URL" is accurate (but see ACC-12 re: the missing 404 in the PUT operations table).
- **CustomerStorage `numberOfStoredImages` counts all assets, not just images.** mdx note matches old Nextra prose.

---

## Cards

### ACC-01 · Customer JSON emits property names with trailing spaces
- **Theme:** Account & access
- **Surfaces:** customer.mdx#created (and the omitted administrator/acceptedAgreement) · DLCS.HydraModel/Customer.cs:135,140,145 · CustomerConverter.cs:17-19
- **Type:** CODE-WRONG
- **Docs say:** Property is `"created"` (customer.mdx:19) — no trailing space; `administrator`/`acceptedAgreement` not shown at all.
- **Original-doc nuance:** scratch/api-doc/customer.md:5 — "for admin, they should come back *without* trailing spaces!!!"
- **Code does:** `Customer.cs` hard-codes `[JsonProperty(PropertyName = "administrator ")]` (line 135), `"created "` (line 140) and `"acceptedAgreement "` (line 145) — each with a trailing space. The converter always populates `Created`/`Administrator`/`AcceptedAgreement` (`CustomerConverter.cs:17-19`), so the wire JSON keys are literally `"created "`, `"administrator "`, `"acceptedAgreement "`.
- **Issues/RFCs:** to check
- **Decision needed:** Confirm these trailing spaces are unintended and should be removed from the Hydra model JSON property names (a JSON-key change is technically a breaking change for any consumer keying on the buggy name).
- **Options:** (a) fix the three `PropertyName` strings in `Customer.cs`; (b) leave and document the quirk (undesirable); (c) fix + add a regression/serialisation test.
- **Possible outputs:** code / RFC
- **Who's needed:** protagonist API maintainer
- **Status:** ✅ RESOLVED by XC-06 cascade (session 0, 2026-08-06): option (c) exactly — the three PropertyName strings trimmed AND a reflection guard test added (DLCS.Hydra.Tests), protagonist PR #1236 (breaking, signposted for release notes; Donald to confirm the portal reads clean keys). Docs already showed the clean names

### ACC-02 · Customer resource emits authServices / roleProviders / roles links
- **Theme:** Account & access
- **Surfaces:** customer.mdx (links list ll.20-31, intentionally omits them) · scratch/api-doc/customer.md:8-21 · DLCS.HydraModel/Customer.cs:80-97
- **Type:** CODE-WRONG
- **Docs say:** The Customer link block deliberately does **not** list `authServices`, `roleProviders` or `roles`.
- **Original-doc nuance:** scratch/api-doc/customer.md:8 — "Need to remove `authServices` and `roleProviders` and `roles` from customer object … replace with https://github.com/dlcs/protagonist/issues/538 (pending seeing how this actually works in DB)". The old Nextra customer page documented all three as live link collections (now parked in scratch ll.219-279).
- **Code does:** `Customer.cs` still declares `AuthServices` (l.83), `RoleProviders` (l.89) and `Roles` (l.96) as `HydraLink`s. The `Customer(baseUrl, id, name, displayName)` ctor calls `Init(..., setLinks: true, ...)` (`Customer.cs:34`), so reflection auto-populates **every** HydraLink — these three URLs appear in every GET /customers/{id} response.
- **Issues/RFCs:** protagonist #538 (per scratch)
- **Decision needed:** Should these three legacy auth links be removed from the Customer model now, kept until the IIIF-Auth management API (#538) is designed, or documented as-is in the interim?
- **Options:** (a) remove the three properties from `Customer.cs`; (b) keep but suppress from serialisation until #538 lands; (c) document them now as provisional.
- **Possible outputs:** code / RFC / doc
- **Who's needed:** protagonist API maintainer + auth (iiif-auth-v2) owner
- **Status:** ✅ RESOLVED by XC-07 cascade (session 0, 2026-08-06): option (a) — all three properties removed from Customer.cs in protagonist PR #1237 (none had a route; the exact #899 bug class). They return when the #538 auth management API exists. Docs were already correct in omitting them

### ACC-03 · administrator / acceptedAgreement always emitted, undocumented, and leak to non-admins
- **Theme:** Account & access
- **Surfaces:** customer.mdx (no section for either field) · scratch/api-doc/customer.md:3-5 · CustomerConverter.cs:18-19 · Customer.cs:133-146
- **Type:** CODE-WRONG / DOC-MISSING
- **Docs say:** Neither `administrator` nor `acceptedAgreement` is documented or shown in the sample JSON.
- **Original-doc nuance:** scratch/api-doc/customer.md:3 — "Actual JSON response for non admin should not have `administrator`, `acceptedAgreement` fields."
- **Code does:** `CustomerConverter.ToHydra` unconditionally sets `Administrator = dbCustomer.Administrator` and `AcceptedAgreement = dbCustomer.AcceptedAgreement` (`CustomerConverter.cs:18-19`); both serialise for every caller regardless of privilege.
- **Issues/RFCs:** to check
- **Decision needed:** Should these internal fields be suppressed for non-admin callers (code), or accepted as part of the resource and documented (doc)? Ties to ACC-01 (the trailing-space bug is on the same two fields).
- **Options:** (a) omit both unless `User.IsAdmin()`; (b) keep and document them (after fixing ACC-01); (c) remove `acceptedAgreement` entirely as obsolete EULA state.
- **Possible outputs:** code / doc / RFC
- **Who's needed:** protagonist API maintainer
- **Status:** ✅ RULED (session 1, 2026-08-10): hybrid of (a)+(c) — `acceptedAgreement` removed
  from the wire entirely (obsolete EULA state); `administrator` emitted **only when true**
  (value-conditional, not caller-conditional — `administrator: false` is never serialised, so
  ordinary customers don't see the field). Breaking on the same two keys #1236 just renamed —
  land in the same release so consumers absorb one wire change. Docs: both fields stay
  undocumented for now; documenting `administrator`-when-true is release-gated (main = released
  behaviour). Sample parity: no sample reads either field — no sample change needed. Check with
  Donald that the portal doesn't rely on `administrator: false` / `acceptedAgreement`. Output: protagonist draft **PR #1241**

### ACC-04 · CustomHeader `role` carries stray Hydra readonly attribute
- **Theme:** Account & access
- **Surfaces:** custom-headers.mdx#role (domain table: readonly False) · DLCS.HydraModel/CustomHeader.cs:32-36
- **Type:** STYLE
- **Docs say:** `role` is `readonly False, writeonly False` (custom-headers.mdx:77-79); old Nextra agrees (custom-headers.mdx:54-56).
- **Original-doc nuance:** —
- **Code does:** `CustomHeader.Role` is declared `[HydraLink(..., ReadOnly = true, ...)]` (`CustomHeader.cs:34`), yet `role` is freely settable on POST and PUT (`CustomHeaderConverter.ToDlcsModel` copies it; `UpdateCustomHeader.cs:43` writes it). So the `ReadOnly = true` is inaccurate vs behaviour and vs docs.
- **Issues/RFCs:** to check
- **Decision needed:** Should the model attribute be corrected to `ReadOnly = false` to match the writable behaviour and the documented table?
- **Options:** (a) set `ReadOnly = false` on `CustomHeader.Role`; (b) leave (only affects generated vocab/Hydra docs); (c) change docs to match code (not advised — role is genuinely writable).
- **Possible outputs:** code
- **Who's needed:** protagonist API maintainer
- **Status:** ☑ mechanical — merged in protagonist PR #1235 (2026-08-06, donaldgray)

### ACC-05 · CustomHeader validator error message mentions "named query"
- **Theme:** Account & access
- **Surfaces:** HydraCustomHeaderValidator.cs:10-12 · (also CustomHeaderConverter.cs:25 param name `hydraNamedQuery`)
- **Type:** STYLE
- **Docs say:** n/a (internal error text).
- **Original-doc nuance:** —
- **Code does:** The "@id must not be supplied" rule emits `"DLCS must allocate named query id, but id {ch.Id} was supplied"` on a **custom header** request (`HydraCustomHeaderValidator.cs:12`). The converter's parameter is likewise mis-named `hydraNamedQuery` (`CustomHeaderConverter.cs:25-29`). Copy-paste from the NamedQuery feature.
- **Issues/RFCs:** —
- **Decision needed:** Trivial copy-paste cleanup — worth doing while in this area?
- **Options:** (a) fix message + param name; (b) skip as cosmetic.
- **Possible outputs:** code
- **Who's needed:** protagonist API maintainer
- **Status:** ☑ mechanical — merged in protagonist PR #1235 (2026-08-06, donaldgray)

### ACC-06 · Storage resources expose undocumented adjunct fields
- **Theme:** Account & access
- **Surfaces:** storage.mdx#CustomerStorage / #ImageStorage · CustomerStorage.cs:66-74 · ImageStorage.cs:44-47 · CustomerStorageConverter.cs:19-20 · ImageStorageConverter.cs:18
- **Type:** DOC-MISSING
- **Docs say:** `CustomerStorage` documents only `numberOfStoredImages`, `totalSizeOfStoredImages`, `totalSizeOfThumbnails`, `lastCalculated`, `storagePolicy`; `ImageStorage` documents only `thumbnailSize`, `size`, `lastChecked`, `checkingInProgress`.
- **Original-doc nuance:** Old Nextra storage.mdx also omits adjuncts (they post-date it) — so no prose to preserve.
- **Code does:** `CustomerStorage` emits `numberOfStoredAdjuncts` and `totalSizeOfStoredAdjuncts` (`CustomerStorage.cs:66-74`, populated `CustomerStorageConverter.cs:19-20`); `ImageStorage` emits `adjunctSize` (`ImageStorage.cs:44-47`, populated `ImageStorageConverter.cs:18`). All three appear on the wire but are undocumented.
- **⟳ Update 2026-08-03:** the *semantics* of these fields were refined by PR #1220 (on `main`): **optimised** adjuncts (e.g. s3-ambient, bytes stay at the origin) count toward `numberOfStoredAdjuncts` but contribute **0** to `totalSizeOfStoredAdjuncts` / `adjunctSize`; and `adjunctSize` is now a running tally preserved across asset reingest (previously wiped — that was bug #1218, closed). If the room decides to document these fields, the optimised carve-out belongs in the prose. Still open: #1127 (exclude optimised sizes — appears substantially delivered by #1220, confirm and close?) and #1121 (recalculator job doesn't yet tally adjunct size, so `lastCalculated` recalcs won't include it).
- **Issues/RFCs:** see adjuncts.mdx / scratch for the broader "adjuncts" feature · #1218 closed · #1127, #1121 open
- **⟳ LIVE-VERIFIED 2026-08-10 (staging, customer 15):** both customer- and space-level storage
  responses emit `numberOfStoredAdjuncts` / `totalSizeOfStoredAdjuncts` (value 0) on the wire —
  the fields are user-visible in the current release, not develop-only.
- **Decision needed:** Document the three adjunct fields on the storage page, or is the adjuncts feature still too provisional to surface here?
- **Options:** (a) add field sections to storage.mdx; (b) leave undocumented until adjuncts page is finalised; (c) cross-link to adjuncts.mdx.
- **Possible outputs:** doc
- **Who's needed:** docs author (+ confirm adjuncts feature status)
- **Status:** ✅ RULED (session 1, 2026-08-10): option (c) — three brief field sections added to
  storage.mdx (examples updated to show the fields, which are in the current release), each
  cross-linking to adjuncts.mdx for semantics; one-sentence carve-out for origin-resident
  ("optimised") adjuncts kept so a 3-count/0-bytes response doesn't read as a bug. Text
  reviewed in-room before applying. Deliberately NOT documented: the #1121 recalculator gap
  (live bug, not contract). Sample parity: no-op — p18_storage/storage.py pretty-prints whole
  resources, new fields appear without a code change. #1127 confirm-and-close handed to
  session 5. Output: public-docs hygiene/session-1 commit

### ACC-07 · ImageStorage has three properties sharing JsonProperty Order 55
- **Theme:** Account & access
- **Surfaces:** DLCS.HydraModel/ImageStorage.cs:44-57 · *(added 2026-08-03)* ApiKey.cs:33,55 · PortalUser.cs:43,51
- **Type:** STYLE
- **Docs say:** n/a (serialisation ordering only).
- **Original-doc nuance:** —
- **Code does:** `adjunctSize` (Order 55, l.46), `lastChecked` (Order 55, l.51) and `checkingInProgress` (Order 55, l.56) all declare the same `[JsonProperty(Order = 55)]`; only `thumbnailSize` (53) and `size` (54) are distinct. Property emission order among the three tied fields is undefined. *(⟳ 2026-08-03: same defect elsewhere in this theme — `ApiKey.cs`: `key` and `secret` both Order 12; `PortalUser.cs`: `created` and `roles` both Order 13. Fix as one sweep.)*
- **Issues/RFCs:** —
- **Decision needed:** Assign distinct `Order` values for deterministic output?
- **Options:** (a) renumber to 55/56/57; (b) leave (cosmetic).
- **Possible outputs:** code
- **Who's needed:** protagonist API maintainer
- **Status:** ☑ mechanical — merged in protagonist PR #1235 (2026-08-06, donaldgray), including the ApiKey and PortalUser extensions

### ACC-08 · Customer-level storage @id shown as .../spaces/0/storage
- **Theme:** Account & access
- **Surfaces:** storage.mdx (customer-level example @id, l.22) · GetCustomerStorage.cs:30-32 · CustomerStorageConverter.cs:13 · CustomerStorage.cs:24-36
- **Type:** DOC-WRONG (to verify against live response)
- **Docs say:** Customer-level example `"@id": ".../customers/2/spaces/0/storage"` (storage.mdx:22), distinct from the space-level `.../spaces/5/storage` (l.36).
- **Original-doc nuance:** Old Nextra storage.mdx:14 shows the customer-level id as `.../customers/21/storage` (no `spaces/0`) — i.e. the original was right and the new page introduced `spaces/0`.
- **Code does:** `GetCustomerStorage` selects the row where `Space == null` (`GetCustomerStorage.cs:31`). The converter builds `new CustomerStorage(baseUrl, customer, customerStorage.Space)` with `Space == null` → ctor takes the no-space branch `Init(baseUrl, false, customerId)` (`CustomerStorage.cs:32-35`) → URI template `/customers/{0}/storage`. So the emitted `@id` should be `.../customers/2/storage`, **not** `.../spaces/0/storage`. *(⟳ 2026-08-03: doc line is storage.mdx:21, not 22. And the example is now doubly wrong: migration `20260518133605_StopSpaceZeroCustomerStorage` converted all Space=0 aggregate rows to NULL and reserves Space=0 as a real per-space row for stub assets — so `/spaces/0/storage` today denotes a different, real resource (see ACC-17). Live test: GET `/customers/{id}/storage` → assert `@id` ends `/customers/{id}/storage`.)*
- **Issues/RFCs:** to check
- **Decision needed:** Confirm the customer-level `@id` is `/customers/{id}/storage` and correct the example (or, if a `Space=0` row really is what's served somewhere, reconcile with the `Space == null` query).
- **Options:** (a) fix the storage.mdx example to drop `spaces/0`; (b) verify against a live stage response first; (c) if code really returns `spaces/0`, file a code bug instead.
- **Possible outputs:** doc / sample
- **Who's needed:** docs author (quick live GET to confirm)
- **⟳ LIVE-VERIFIED 2026-08-10 (staging, customer 15):** `GET /customers/15/storage` → 200 with
  `"@id": ".../customers/15/storage"` — **no** `spaces/0` segment. The storage.mdx:21 example is
  confirmed wrong on the wire; option (a) is fact-backed.
- **Status:** ✅ RULED (session 1, 2026-08-10): option (a) — example `@id` corrected to
  `.../customers/2/storage` (restores what the old Nextra page had; live-verified). Space-0
  documentation question stays with ACC-17. Sample parity: no-op — the sample GETs by path and
  doesn't assert `@id`. Output: public-docs hygiene/session-1 commit

### ACC-09 · storagePolicy on space-level storage: docs vs model intent vs converter
- **Theme:** Account & access
- **Surfaces:** storage.mdx#storagePolicy (l.58-66, "present on both customer-level and space-level") · CustomerStorageConverter.cs:15 · CustomerStorage.cs:81-86 · DLCS.Model/Storage/CustomerStorage.cs:11
- **Type:** DESIGN (to verify)
- **Docs say:** "This property is present on both customer-level and space-level storage responses." (storage.mdx:60) and the space-level example includes `storagePolicy` (l.42).
- **Original-doc nuance:** Old Nextra storage.mdx:36 and the Hydra model comment both say the opposite: "*When the customer storage resource is for a Customer rather than a space, it will include this … property*" (`CustomerStorage.cs:81-83`).
- **Code does:** The converter **always** sets `StoragePolicy = $"{baseUrl}/storagePolicies/{customerStorage.StoragePolicy}"` (`CustomerStorageConverter.cs:15`), regardless of space level. The DB column `StoragePolicy` is a plain `string` (`DLCS.Model/Storage/CustomerStorage.cs:11`); if space rows store null/empty it would emit `.../storagePolicies/` with a trailing blank. *(⟳ 2026-08-03 — the 3-way contradiction is now largely answerable: `CustomerStorageRepository.TryCreateCustomerStorage` (`CustomerStorageRepository.cs:86-108`) always writes `StoragePolicy` (default `'default'`) on BOTH customer- and space-level rows, and the 2026-05 migration backfilled space-0 rows inheriting the aggregate's policy. So space-level responses genuinely carry a policy → the new docs match runtime; the model comment and old Nextra prose are what's outdated → leans option (a). Residual risk: legacy space rows with null policy → the empty-tail URL bug. Live test: GET the docs space's storage → assert `storagePolicy` is a resolvable URL.)*
- **Issues/RFCs:** to check
- **Decision needed:** Should `storagePolicy` appear on space-level responses at all? Align three sources — the new docs (yes, both), the model comment/old docs (customer-only), and the converter (always emits) — and decide which is right.
- **Options:** (a) docs correct, update model comment + ensure space rows carry a policy; (b) suppress `storagePolicy` for space-level in the converter and revert the docs to customer-only; (c) verify live what space-level actually returns before deciding.
- **Possible outputs:** doc / code / sample
- **Who's needed:** protagonist API maintainer + docs author
- **⟳ LIVE-VERIFIED 2026-08-10 (staging, customer 15):** space-level
  `GET /customers/15/spaces/98765/storage` → 200 **with** `storagePolicy` =
  `.../storagePolicies/default`, and that URL resolves (200, `vocab:StoragePolicy`). New docs
  match runtime; the model comment + old Nextra prose are what's outdated → supports option (a).
  Residual: a legacy null-policy space row would still emit the empty-tail URL (not observable
  from one GET).
- **Status:** ✅ RULED (session 1, 2026-08-10): option (b) — the room judged the space-level
  `storagePolicy` meaningless (echoes the customer's policy; not editable per space; not
  enforced per space), so the converter now emits it on customer-level responses only
  (protagonist draft **PR #1242**, with integration tests pinning both directions; breaking wire
  change). Model comment stands as the correct description (spacing tidied). Designing real
  per-space policy management minted as protagonist **#1240** (none existed; #1017/#1018/#1019
  are adjacent but customer/resource-level). Docs half is **release-gated** — twin recorded in
  scratch/api-doc/storage.md, apply when the release ships. Sample parity: no-op (sample reads
  policy from customer level only)

### ACC-10 · Portal Users sub-resource is under-documented
- **Theme:** Account & access
- **Surfaces:** customer.mdx#portalUsers (ll.413-443 — only GET collection + POST) · PortalUsersController.cs:33-177 · DLCS.HydraModel/PortalUser.cs
- **Type:** DOC-MISSING
- **Docs say:** Only `GET /portalUsers` (200) and `POST /portalUsers` (201) are documented, with a POST body of `{email, password}`. No dedicated portalUsers page exists.
- **Original-doc nuance:** —
- **Code does:** `PortalUsersController` also implements `GET /portalUsers/{userId}` (l.65-79), `PATCH /portalUsers/{userId}` (l.128-154) and `DELETE /portalUsers/{userId}` (l.164-177). The `PortalUser` resource carries `email`, `password` (write-only, never returned — `PortalUser.cs:36-39`), `created`, `roles` (link) and `enabled`, none documented. Note PATCH does **not** toggle `enabled` ("Deliverator doesn't support toggling Enabled here so we won't for now", controller l.134) and create/patch errors return 400 (not 409 on duplicate email). *(⟳ 2026-08-03: the 409 machinery half-exists — `CreatePortalUser.cs:60-65` sets `Conflict = true` on duplicate email but the controller ignores the flag and returns 400 (`PortalUsersController.cs:106-109`). Also: the duplicate-email check is **global across all customers**, not per customer (`CreatePortalUser.cs:60-61`). A sample `p05_customer/portal_users.py` now exists covering list/POST/DELETE; GET-single and PATCH remain unsampled.)*
- **Issues/RFCs:** —
- **Decision needed:** How much of the portal-user lifecycle to surface — extend the customer.mdx section, or stand up a portalUsers.mdx page with full fields + GET-single/PATCH/DELETE?
- **Options:** (a) expand the section in customer.mdx; (b) new portalUsers.mdx page + Python sample; (c) document only the resource fields, defer PATCH/DELETE.
- **Possible outputs:** doc / sample
- **Who's needed:** docs author
- **Status:** ✅ RULED (session 1, 2026-08-10): option (b) **plus deprecation notice** — the
  feature will be deprecated (the current customer portal manages its users externally).
  Delivered:
  - **Docs:** new `portal-users.mdx` (sidebar order 5.5) with caution Aside, full lifecycle
    (GET/POST collection; GET/PATCH/DELETE single), field sections from the model; customer.mdx
    portalUsers section trimmed to a pointer + caution. Page omits the `roles` link
    (ACC-02-style: phantom, see cascade below).
  - **Sample:** portal_users.py extended to full lifecycle (POST → GET-single → PATCH →
    DELETE); **run verified against staging** (201/200/200/204). Stays in p05_customer/
    (sub-resource of the customer page; recorded deviation from the dir-per-page convention).
  - **Code (protagonist draft **PR #1243**):** duplicate-email 409/Conflict machinery ruled
    IGNORE (deprecated), but messages split per PO: same-customer duplicate → "Portal user
    already exists." / cross-customer → opaque (matches generic failure text), on both create
    and patch (commit 805f6dd7). **Security fix found en route:** PatchPortalUser had no
    customer-ownership check (DELETE did) — an authenticated customer could change another
    customer's portal-user email/password by GUID; fixed + integration-tested in the same
    commit. Flag to Donald: candidate for prompt release/backport, and consider whether it
    warrants a private-protagonist record. XC-07 cascade: phantom `roles` link (no route,
    always 404) + phantom PUT operation removed from the model (3c7c0276); created/enabled
    readonly flags corrected to actual contract (71eb78bf).
  - GET-single 404 / PATCH-no-enabled / DELETE 204-400 documented as released behaviour
    (verified: endpoints all in v1.13.2)

### ACC-11 · API-key creation: docs require "administrator privileges" but code does not
- **Theme:** Account & access
- **Surfaces:** customer.mdx#keys (l.477 prose) · DLCS.HydraModel/Customer.cs:121-124 (model description) · ApiKeysController.cs:78-87 · CreateApiKey.cs:35-55
- **Type:** DOC-WRONG (to verify)
- **Docs say:** "make an empty POST to this collection **with administrator privileges** and the returned Key object will include the generated secret" (customer.mdx:477); the Hydra model description repeats this (`Customer.cs:122`).
- **Original-doc nuance:** —
- **Code does:** `ApiKeysController.CreateApiKey` has no `User.IsAdmin()` check (contrast `CustomerController.CreateCustomer` l.84) and no `[Authorize(Roles=…)]`; the handler just looks up the customer and mints a key (`CreateApiKey.cs:35-51`). So any caller authenticated **as that customer** can create a key for it — "administrator privileges" appears inaccurate (it may be conflating admin-customer with normal auth).
- **Issues/RFCs:** to check
- **Decision needed:** Is an admin/elevated check intended for key creation (then code is missing it), or is normal customer auth sufficient (then docs + model description should drop "administrator privileges")?
- **Options:** (a) reword docs/model to "authenticated as this customer"; (b) add the missing privilege check in the controller; (c) verify intended auth policy first.
- **Possible outputs:** doc / code / RFC
- **Who's needed:** protagonist API maintainer + security owner
- **Status:** ☐ undecided

### ACC-12 · Operations tables miss real status codes (keys DELETE; custom-header PUT 404)
- **Theme:** Account & access
- **Surfaces:** customer.mdx#keys (ops table ll.487-490 lists only GET/POST) · custom-headers.mdx (PUT row l.31) · ApiKeysController.cs:95-108 · CustomHeadersController.cs:124-127 · UpdateCustomHeader.cs:37-41
- **Type:** DOC-MISSING
- **Docs say:** The keys operations table lists only GET and POST; DELETE is only mentioned in prose (customer.mdx:523-527) with no status code. The custom-header PUT row advertises `200 OK, 400 Bad Request` only.
- **Original-doc nuance:** Old Nextra custom-headers.mdx:22 listed PUT as "200 OK, 404 Not Found".
- **Code does:** `DELETE /keys/{key}` returns 204 or 400 (`ApiKeysController.cs:95-99`). `PUT /customHeaders/{id}` can return 404 when the header doesn't exist (`UpdateCustomHeader.cs:37-41` → `WriteResult.NotFound`), though the controller's `[ProducesResponseType]` only declares 200/400 (`CustomHeadersController.cs:126-127`). *(⟳ 2026-08-03: the custom-header PUT row needs **three** changes, not two — a successful update actually returns **201**, not 200 (see ACC-15): so the row is wrong on success code, missing 404, keeps 400. Also: customer.mdx PATCH row (l.46) omits its 400 (validator failures); storage GETs can 404 when no row exists (`GetCustomerStorage.cs:34-36`, `GetSpaceStorage.cs:37-39`) while storage.mdx:49-51 and customer.mdx:459-461 list 200 only — fold into the same ops-table sweep, alongside SPA-20's asset/space rows.)*
- **Issues/RFCs:** —
- **Decision needed:** Round out the documented status codes (add DELETE row + 204/400 to keys; fix custom-header PUT row per ACC-15; add customer PATCH 400 + storage 404s) and, for PUT, decide whether the controller attribute should also advertise 404.
- **Options:** (a) docs-only: add the missing rows/codes; (b) docs + add `[ProducesResponseType(404)]` to PutCustomHeader; (c) leave.
- **Possible outputs:** doc / code
- **Who's needed:** docs author (+ optional API tweak)
- **Status:** ☑ mechanical (part) — keys DELETE row, customer PATCH 400 and storage GET 404s merged in public-docs PR #5 (2026-08-05); custom-header PUT row still waits on the ACC-15 ruling, and the optional PutCustomHeader 404 annotation remains open

### ACC-13 · Customer space-creation POST defaults undocumented
- **Theme:** Account & access
- **Surfaces:** customer.mdx#spaces (POST table l.132-137 — only `name`) · scratch/api-doc/customer.md:37-53
- **Type:** DOC-MISSING (to verify against Space converter)
- **Docs say:** The `POST /customers/{customer}/spaces` field table lists only `name` REQUIRED.
- **Original-doc nuance:** scratch/api-doc/customer.md:44-49 carries a richer field table — `defaultTags`, `defaultRoles`, `maxUnauthorised` as OPTIONAL — plus an open bug note (l.52): "If you POST … and DO supply an `id` that already exists, a new space is created with a new `id`. This feels wrong."
- **Code does (⟳ verified 2026-08-03):** `SpaceController.CreateSpace` (`SpaceController.cs:97-102`) copies `defaultRoles`, `defaultTags` and `maxUnauthorised` from the posted Space into the `CreateSpace` command (`CreateSpace.cs:54-57`) — **all three optional fields are honoured on POST**, so the scratch field table is accurate and should be restored. A supplied `id`/`@id` is silently ignored (never read — DLCS mints identity), consistent with the scratch bug note; duplicate `name` → 409 (`CreateSpace.cs:47-52`). Live test: POST with defaults then GET the space back; POST with an explicit existing `id` → expect 201 with a different minted id.
- **Issues/RFCs:** to check
- **Decision needed:** Should the customer.mdx spaces-POST table list the optional default fields (and is the "duplicate id mints a new space" behaviour a bug to file), or leave full space detail to space.mdx?
- **Options:** (a) add optional fields to the customer.mdx POST table; (b) keep minimal here and document defaults only on space.mdx; (c) investigate + file the duplicate-id behaviour separately.
- **Possible outputs:** doc / code / RFC
- **Who's needed:** docs author + protagonist API maintainer
- **Status:** ☐ undecided

### ACC-14 · API-key POST status: 200 (controller) vs 201 (Hydra metadata)
- **Theme:** Account & access
- **Surfaces:** customer.mdx#keys (POST row "200 OK", l.490) · ApiKeysController.cs:76,83 · DLCS.HydraModel/ApiKey.cs:91-97
- **Type:** STYLE / CODE
- **Docs say:** `POST /keys` returns `200 OK` (customer.mdx:490) — matches the controller.
- **Original-doc nuance:** —
- **Code does:** Controller returns `Ok(...)` = 200 and declares `Status200OK` (`ApiKeysController.cs:76,83`). But the Hydra class operation metadata for key creation declares `StatusCode = 201, "Job has been accepted - key created and returned"` (`ApiKey.cs:91-97`). The generated vocab/Hydra docs would therefore claim 201 while the live API returns 200.
- **Issues/RFCs:** —
- **Decision needed:** Which is canonical — 200 (current behaviour, and a key isn't really async/accepted) or 201 Created? Align the controller and the Hydra metadata.
- **Options:** (a) change Hydra metadata to 200 to match behaviour; (b) change controller to return 201 Created and update docs; (c) leave (docs already match runtime, only generated vocab diverges).
- **Possible outputs:** code / doc
- **Who's needed:** protagonist API maintainer
- **Status:** ✅ RULED by XC-02 cascade (session 0, 2026-08-06): option (a) — key creation is a sanctioned action-POST exception returning 200; the Hydra operation metadata changes 201→200 to match (protagonist hygiene/session-0)

### ACC-15 · Custom-header PUT returns 201 Created on a successful *update* *(added 2026-08-03 verification pass; promoted from the corrected Resolved entry)*
- **Theme:** Account & access
- **Surfaces:** custom-headers.mdx:31 (PUT row "200 OK, 400 Bad Request") · `UpdateCustomHeader.cs:50` · `ControllerBaseX.cs:146-147` · `CustomHeadersController.cs:126-127`
- **Type:** CODE-WRONG (XC-03 family) + DOC-WRONG
- **Code does:** `UpdateCustomHeaderHandler` returns `WriteResult.Created` after mutating an *existing* row (unchanged since 2023), mapping to **201 Created + Location** on every successful update. The annotation says 200; the docs say 200; the wire says 201.
- **Decision needed:** One-word handler fix to `WriteResult.Updated` (→200; the XC-03 ruling makes this automatic) or document 201. Either way the docs row also needs 404 (ACC-12).
- **Possible outputs:** code / doc
- **Who's needed:** protagonist API maintainer
- **Status:** ✅ RULED (session 0, 2026-08-06): one-word handler fix to `WriteResult.Updated` — PUT-update returns 200. Owner: Donald. Outputs: protagonist hygiene/session-0 commit; custom-headers.mdx PUT row (the ACC-12 leftover) becomes 200/400/404 in the same unit of work

### ACC-16 · customer.mdx sample JSON advertises an `iiif` link protagonist does not emit *(added 2026-08-03 verification pass)*
- **Theme:** Account & access
- **Surfaces:** customer.mdx:21 (example `"iiif": ...`) · `DLCS.HydraModel/Customer.cs` (no such property) · scratch/api-doc/customer.md:59-74 (parked `## iiif` section)
- **Type:** DOC-WRONG
- **Code does:** No `iiif` property exists on the Customer Hydra model; nothing found injecting it. The example shows a link that a real GET will not contain, whose section is parked in scratch, and whose target page (`iiif.mdx`) is unported. Same pattern as the entrypoint's phantom links (DIS-14).
- **Decision needed:** Remove from the example until the iiif-presentation integration actually surfaces the link (verify against live first), or implement the link.
- **⟳ LIVE-VERIFIED 2026-08-10 (staging, customer 15):** `GET /customers/15` → 200; response has
  **no** `iiif` key. Docs example confirmed wrong on the wire.
- **Possible outputs:** doc / code
- **Who's needed:** docs author + iiif-presentation owner
- **Status:** ☐ undecided

### ACC-17 · Space 0 / stub-asset storage semantics undocumented *(added 2026-08-03 verification pass)*
- **Theme:** Account & access
- **Surfaces:** storage.mdx (customer-vs-space framing only) · migration `20260518133605_StopSpaceZeroCustomerStorage` · `CustomerStorageRepository.cs`
- **Type:** DOC-MISSING
- **Code does:** Since May 2026, Space=0 is a real per-customer space whose storage row holds stub-asset storage; the customer-level aggregate lives on the Space=NULL row. The storage page doesn't mention space 0 at all; interacts with ACC-08's wrong example (which uses `/spaces/0/storage` *as* the customer aggregate).
- **Decision needed:** Whether/how to document space-0 storage (it's user-visible via `/spaces/0/storage`), coordinated with the ACC-08 fix.
- **Possible outputs:** doc
- **Who's needed:** docs author + API maintainer (stub-asset feature status)
- **Status:** ☐ undecided

### ACC-18 · Bulk `POST /customers/{id}/deleteImages` completely undocumented *(added 2026-08-03 verification pass)*
- **Theme:** Account & access
- **Surfaces:** `CustomerImagesController.cs:173-178` · customer.mdx (no mention) · no scratch note
- **Type:** DOC-MISSING
- **Code does:** Implemented bulk asset delete (the XC-01 outlier returning 200 `{message}`). Its sibling `deleteAdjuncts` has a card (ADJ-11); this one had none anywhere.
- **Decision needed:** Document alongside the queues/customer bulk operations (with whatever status shape XC-01 rules), + sample (XC-10 gap).
- **Possible outputs:** doc / sample
- **Who's needed:** docs author
- **Status:** ☐ undecided — ⟳ session-0 cascade note (2026-08-06): XC-01 migrated this endpoint from 200+message to 204 No Content (protagonist PR #1236, breaking). When documented, the row is 204/400 — and per main = released behaviour, document it only once the release carrying #1236 ships

### ACC-19 · Doc/vocab cosmetics sweep for this theme *(added 2026-08-03 verification pass — batch of small fixes, one PR)*
- **Theme:** Account & access
- **Type:** STYLE (quick wins, no decisions)
- **Items:** customer.mdx LinkCard copy-paste errors — the "GET and POST customer/spaces" card (l.139-143) carries the PATCH description, and there are two cards titled "💻 GET Customer" (l.36, l.51; the second is the PATCH sample) · customer.mdx sample lines 17/19 end with a stray trailing space (ironic echo of ACC-01) · Hydra vocab typos: `ApiKey.cs:87` ("Requires eleveated ", ends mid-sentence), `Customer.cs:123` ("the generates secret") · the new-customer `defaultDeliveryChannels` example in customer.mdx is internally inconsistent (`iiif-img` channel with `iiif-av/default-video` policy — pasted from a scratch working note) with prose "you will already have this delivery channel" dropped (see _provenance items).
- **Decision needed:** None — assign an owner, fix in one docs PR (+ one protagonist PR for the two vocab strings).
- **Possible outputs:** doc + code (trivial)
- **Status:** ☑ mechanical — docs half merged in public-docs PR #6 (2026-08-05); vocab typo strings merged in protagonist PR #1235 (2026-08-06, donaldgray). CLOSED
