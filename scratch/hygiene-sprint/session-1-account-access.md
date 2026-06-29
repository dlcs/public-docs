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

## Resolved (Category A) — already correct, no card needed

- **custom-headers PUT returns 200**, not 404-on-update. Confirmed: `CustomHeadersController.PutCustomHeader` is decorated `Status200OK` and returns `HandleUpsert` → 200 (`CustomHeadersController.cs:124-149`). Live mdx already says `200 OK, 400 Bad Request`.
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
- **Status:** ☐ undecided

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
- **Status:** ☐ undecided

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
- **Status:** ☐ undecided

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
- **Status:** ☐ undecided

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
- **Status:** ☐ undecided

### ACC-06 · Storage resources expose undocumented adjunct fields
- **Theme:** Account & access
- **Surfaces:** storage.mdx#CustomerStorage / #ImageStorage · CustomerStorage.cs:66-74 · ImageStorage.cs:44-47 · CustomerStorageConverter.cs:19-20 · ImageStorageConverter.cs:18
- **Type:** DOC-MISSING
- **Docs say:** `CustomerStorage` documents only `numberOfStoredImages`, `totalSizeOfStoredImages`, `totalSizeOfThumbnails`, `lastCalculated`, `storagePolicy`; `ImageStorage` documents only `thumbnailSize`, `size`, `lastChecked`, `checkingInProgress`.
- **Original-doc nuance:** Old Nextra storage.mdx also omits adjuncts (they post-date it) — so no prose to preserve.
- **Code does:** `CustomerStorage` emits `numberOfStoredAdjuncts` and `totalSizeOfStoredAdjuncts` (`CustomerStorage.cs:66-74`, populated `CustomerStorageConverter.cs:19-20`); `ImageStorage` emits `adjunctSize` (`ImageStorage.cs:44-47`, populated `ImageStorageConverter.cs:18`). All three appear on the wire but are undocumented.
- **Issues/RFCs:** see adjuncts.mdx / scratch for the broader "adjuncts" feature
- **Decision needed:** Document the three adjunct fields on the storage page, or is the adjuncts feature still too provisional to surface here?
- **Options:** (a) add field sections to storage.mdx; (b) leave undocumented until adjuncts page is finalised; (c) cross-link to adjuncts.mdx.
- **Possible outputs:** doc
- **Who's needed:** docs author (+ confirm adjuncts feature status)
- **Status:** ☐ undecided

### ACC-07 · ImageStorage has three properties sharing JsonProperty Order 55
- **Theme:** Account & access
- **Surfaces:** DLCS.HydraModel/ImageStorage.cs:44-57
- **Type:** STYLE
- **Docs say:** n/a (serialisation ordering only).
- **Original-doc nuance:** —
- **Code does:** `adjunctSize` (Order 55, l.46), `lastChecked` (Order 55, l.51) and `checkingInProgress` (Order 55, l.56) all declare the same `[JsonProperty(Order = 55)]`; only `thumbnailSize` (53) and `size` (54) are distinct. Property emission order among the three tied fields is undefined.
- **Issues/RFCs:** —
- **Decision needed:** Assign distinct `Order` values for deterministic output?
- **Options:** (a) renumber to 55/56/57; (b) leave (cosmetic).
- **Possible outputs:** code
- **Who's needed:** protagonist API maintainer
- **Status:** ☐ undecided

### ACC-08 · Customer-level storage @id shown as .../spaces/0/storage
- **Theme:** Account & access
- **Surfaces:** storage.mdx (customer-level example @id, l.22) · GetCustomerStorage.cs:30-32 · CustomerStorageConverter.cs:13 · CustomerStorage.cs:24-36
- **Type:** DOC-WRONG (to verify against live response)
- **Docs say:** Customer-level example `"@id": ".../customers/2/spaces/0/storage"` (storage.mdx:22), distinct from the space-level `.../spaces/5/storage` (l.36).
- **Original-doc nuance:** Old Nextra storage.mdx:14 shows the customer-level id as `.../customers/21/storage` (no `spaces/0`) — i.e. the original was right and the new page introduced `spaces/0`.
- **Code does:** `GetCustomerStorage` selects the row where `Space == null` (`GetCustomerStorage.cs:31`). The converter builds `new CustomerStorage(baseUrl, customer, customerStorage.Space)` with `Space == null` → ctor takes the no-space branch `Init(baseUrl, false, customerId)` (`CustomerStorage.cs:32-35`) → URI template `/customers/{0}/storage`. So the emitted `@id` should be `.../customers/2/storage`, **not** `.../spaces/0/storage`.
- **Issues/RFCs:** to check
- **Decision needed:** Confirm the customer-level `@id` is `/customers/{id}/storage` and correct the example (or, if a `Space=0` row really is what's served somewhere, reconcile with the `Space == null` query).
- **Options:** (a) fix the storage.mdx example to drop `spaces/0`; (b) verify against a live stage response first; (c) if code really returns `spaces/0`, file a code bug instead.
- **Possible outputs:** doc / sample
- **Who's needed:** docs author (quick live GET to confirm)
- **Status:** ☐ undecided

### ACC-09 · storagePolicy on space-level storage: docs vs model intent vs converter
- **Theme:** Account & access
- **Surfaces:** storage.mdx#storagePolicy (l.58-66, "present on both customer-level and space-level") · CustomerStorageConverter.cs:15 · CustomerStorage.cs:81-86 · DLCS.Model/Storage/CustomerStorage.cs:11
- **Type:** DESIGN (to verify)
- **Docs say:** "This property is present on both customer-level and space-level storage responses." (storage.mdx:60) and the space-level example includes `storagePolicy` (l.42).
- **Original-doc nuance:** Old Nextra storage.mdx:36 and the Hydra model comment both say the opposite: "*When the customer storage resource is for a Customer rather than a space, it will include this … property*" (`CustomerStorage.cs:81-83`).
- **Code does:** The converter **always** sets `StoragePolicy = $"{baseUrl}/storagePolicies/{customerStorage.StoragePolicy}"` (`CustomerStorageConverter.cs:15`), regardless of space level. The DB column `StoragePolicy` is a plain `string` (`DLCS.Model/Storage/CustomerStorage.cs:11`); if space rows store null/empty it would emit `.../storagePolicies/` with a trailing blank.
- **Issues/RFCs:** to check
- **Decision needed:** Should `storagePolicy` appear on space-level responses at all? Align three sources — the new docs (yes, both), the model comment/old docs (customer-only), and the converter (always emits) — and decide which is right.
- **Options:** (a) docs correct, update model comment + ensure space rows carry a policy; (b) suppress `storagePolicy` for space-level in the converter and revert the docs to customer-only; (c) verify live what space-level actually returns before deciding.
- **Possible outputs:** doc / code / sample
- **Who's needed:** protagonist API maintainer + docs author
- **Status:** ☐ undecided

### ACC-10 · Portal Users sub-resource is under-documented
- **Theme:** Account & access
- **Surfaces:** customer.mdx#portalUsers (ll.413-443 — only GET collection + POST) · PortalUsersController.cs:33-177 · DLCS.HydraModel/PortalUser.cs
- **Type:** DOC-MISSING
- **Docs say:** Only `GET /portalUsers` (200) and `POST /portalUsers` (201) are documented, with a POST body of `{email, password}`. No dedicated portalUsers page exists.
- **Original-doc nuance:** —
- **Code does:** `PortalUsersController` also implements `GET /portalUsers/{userId}` (l.65-79), `PATCH /portalUsers/{userId}` (l.128-154) and `DELETE /portalUsers/{userId}` (l.164-177). The `PortalUser` resource carries `email`, `password` (write-only, never returned — `PortalUser.cs:36-39`), `created`, `roles` (link) and `enabled`, none documented. Note PATCH does **not** toggle `enabled` ("Deliverator doesn't support toggling Enabled here so we won't for now", controller l.134) and create/patch errors return 400 (not 409 on duplicate email).
- **Issues/RFCs:** —
- **Decision needed:** How much of the portal-user lifecycle to surface — extend the customer.mdx section, or stand up a portalUsers.mdx page with full fields + GET-single/PATCH/DELETE?
- **Options:** (a) expand the section in customer.mdx; (b) new portalUsers.mdx page + Python sample; (c) document only the resource fields, defer PATCH/DELETE.
- **Possible outputs:** doc / sample
- **Who's needed:** docs author
- **Status:** ☐ undecided

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
- **Code does:** `DELETE /keys/{key}` returns 204 or 400 (`ApiKeysController.cs:95-99`). `PUT /customHeaders/{id}` can return 404 when the header doesn't exist (`UpdateCustomHeader.cs:37-41` → `WriteResult.NotFound`), though the controller's `[ProducesResponseType]` only declares 200/400 (`CustomHeadersController.cs:126-127`).
- **Issues/RFCs:** —
- **Decision needed:** Round out the documented status codes (add DELETE row + 204/400 to keys; add 404 to custom-header PUT) and, for PUT, decide whether the controller attribute should also advertise 404.
- **Options:** (a) docs-only: add the missing rows/codes; (b) docs + add `[ProducesResponseType(404)]` to PutCustomHeader; (c) leave.
- **Possible outputs:** doc / code
- **Who's needed:** docs author (+ optional API tweak)
- **Status:** ☐ undecided

### ACC-13 · Customer space-creation POST defaults undocumented
- **Theme:** Account & access
- **Surfaces:** customer.mdx#spaces (POST table l.132-137 — only `name`) · scratch/api-doc/customer.md:37-53
- **Type:** DOC-MISSING (to verify against Space converter)
- **Docs say:** The `POST /customers/{customer}/spaces` field table lists only `name` REQUIRED.
- **Original-doc nuance:** scratch/api-doc/customer.md:44-49 carries a richer field table — `defaultTags`, `defaultRoles`, `maxUnauthorised` as OPTIONAL — plus an open bug note (l.52): "If you POST … and DO supply an `id` that already exists, a new space is created with a new `id`. This feels wrong."
- **Code does:** Not re-verified in this pass — needs a check of the Space hydra model / create-space request to confirm which default fields are honoured on POST (belongs partly to the Space page).
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
- **Status:** ☐ undecided
