# DLCS docs/API hygiene sprint — plan

> **Status: DRAFT for discussion.** This is a starting structure, not a finished plan.
> Expect to redesign it. Prepared 2026-06-25.

## Why we're doing this

Porting the API docs from the old Nextra site to Starlight surfaced a large number of
discrepancies between **what the docs say**, **what the original (older) docs said**, and
**what the protagonist / iiif-presentation / iiif-auth-v2 code actually does**. Some are
plain doc errors. Many are not — they are genuine *decisions* about the product:

- the docs are wrong → fix the docs
- the **code** is wrong or inconsistent → change the API
- the docs should be re-shaped to match the code as-built
- the feature should be **stylistically consistent** with its siblings (same HTTP verbs →
  same status-code semantics, same identifier conventions, same error shape)
- the feature **shouldn't exist** (drop it, preserve the prose in case we reconsider)
- a **new feature / RFC** is required before anything can be documented

These cannot be decided by the product owner + AI alone. They need the colleagues who are
closest to the code and to the reality of running the platform. This sprint is the forum
for making those decisions **jointly**, with AI in the room to retrieve context, draft the
agreed change, and capture the decision.

## Guiding principles

1. **Every item is a decision, not a fix.** The outcome set is:
   `doc change` · `API code change` · `sample-code change` · `write/extend an RFC` ·
   `defer (park)` · `no-op (close)`. An item can produce several of these.
2. **Preserve nuance.** Before we delete or rewrite any prose, the original text is
   captured — in `scratch/api-doc/{page}.md` (existing convention) and, where it came from
   the old Nextra docs, cross-linked to the source. Losing a hard-won sentence is a defect.
3. **Consistency is an item in its own right.** Where several findings share a root cause
   (status-code semantics, identifier policy, Hydra model cleanliness, error model), we
   make one *convention ruling* and then sweep, rather than patching each site blindly.
4. **Code reality wins ties, but only after we've asked whether the code is right.** "The
   code does X" is the start of the conversation, not the end.
5. **Decisions are recorded.** Each item ends with a one-line ruling + owner + follow-up
   artrefact (issue link, PR, RFC, scratch entry). The register is the audit trail.
6. **Docs and samples move together.** The goal is comprehensive Python samples alongside
   every documented feature (as most pages have now). Therefore *any* user-facing feature
   change, addition, or removal carries a matching change to the Python sample in
   `dlcs-docs-client/` in the **same** unit of work — add a sample for a new feature, edit it
   for a changed one, delete/retire it for a removed one. A doc card that ships without
   touching its sample must explicitly state why none is needed (e.g. conceptual page, or the
   sample is unaffected). "Doc updated, sample left stale" is a defect, exactly like lost
   nuance (principle 2). See `XC-10`.

## Decision taxonomy (discrepancy types)

| Type | Meaning | Usual track |
|:---|:---|:---|
| `DOC-WRONG` | Docs misdescribe working code | Fix docs (often quick) |
| `CODE-WRONG` | Code is buggy or internally inconsistent vs intent | protagonist/iiif issue |
| `CODE-MISSING` | Doc/scratch describes a feature not in the code | Decide: build / drop / RFC |
| `DOC-MISSING` | Code has real behaviour or fields not documented | Document it |
| `STALE-SCRATCH` | A parked feature has since landed | Promote scratch → docs + sample |
| `STYLE` | Cross-cutting inconsistency across siblings | Convention ruling + sweep |
| `DESIGN` | Genuine gap needing design before docs | Write an RFC |

## Two tracks: mechanical vs decision (proposed 2026-08-03, ratify in session 0)

The 2026-08-03 verification pass showed roughly a third of the register (~45-50 of 134 cards)
is now **verified-factual with an obvious fix and no design question** — wrong status codes in
ops tables, hostname normalisation, stale docstrings, copy-paste bugs, the cosmetics sweeps
(ACC-19, ADJ-17, DIS-24, SPA-16…). Proposal, to be ratified in the first ten minutes of
session 0:

- **Mechanical track:** verified + uncontentious cards are batched into PRs, reviewed async
  by whoever owns the touched surface. No room time.
- **Decision track:** the sessions spend their 90 minutes only on genuine DESIGN / CODE-WRONG
  / CODE-MISSING calls (~60 cards).

Two routing rules that go with it:

- **Route conventions through work already in flight.** Jack is standardising PUT/POST
  semantics in iiif-presentation **PR #641** right now — the XC-02/XC-03 rulings are handed to
  that PR, not minted in parallel. Likewise RFC 024 (PR #1230) constrains DIS-07's PDF prose,
  and PR #228 gates the collections prose.
- **The samples are the regression suite.** The durable fix for weekly doc-rot is not
  repeating the hand audit — it is running `dlcs-docs-client` against a deployment on a
  schedule and treating failures as doc bugs (XC-10 grown into CI). Highest-leverage process
  decision available on Wednesday.

## Landing pipeline (how a ruling becomes merged docs)

1. **Before the sprint: merge public-docs PR #4** so sessions start from a clean `main`.
2. **One branch per session** (`hygiene/session-0`), **one commit per card ID**, PR at session
   end. The people in the room are the reviewers — review is a formality; the audit trail
   extends from the register into git history.
3. **Rulings that are code changes** become protagonist / iiif-presentation issues drafted
   live in the session, cross-referencing the card ID.
4. **Docs for unreleased API surface** (per the *main = released behaviour* decision below;
   today that's the adjunct-queue sections) go to a public-docs `develop` branch **or** held
   draft PRs labelled blocked-on-release — the room picks the mechanism Wednesday — merging
   when the feature ships. Paired working agreement for the devs: an API-surface PR carries a
   companion public-docs PR (PR #1228's six undocumented endpoints are the exhibit).
5. **Scratch flow unchanged:** promote-from-scratch moves prose into the mdx in the same
   commit; drop-the-feature rulings leave the prose in scratch with the ruling noted
   (principle 2).

## How a session runs (≈90 min, in a room, Claude live)

1. **Pick a theme** (see session plan below). Open the register filtered to that theme.
2. For each item, in order:
   - Claude reads out: the discrepancy, the doc text, the **original** doc text, the code
     reality, and any linked issue/RFC. (≤2 min.)
   - Discuss. Land on a ruling and a track.
   - Claude records the ruling in the card and, where the track is a quick `doc change` or
     `sample change` and there's consensus, drafts it **then and there** for review.
   - Anything bigger (`CODE-*`, `DESIGN`) becomes a GitHub issue / RFC stub Claude drafts.
3. End each session by re-reading the new rulings and confirming the parking lot.

**Definition of done for an item:** ruling recorded · track assigned · owner named ·
follow-up artefact created (PR / issue / RFC / scratch entry) · nuance preserved · **sample
parity** (matching Python sample added/changed/removed, or a recorded reason none is needed).

## Session plan (proposed order)

Cross-cutting goes **first** because its rulings cascade into every other theme.

| # | Session | Pages / subsystems | Repos in play |
|:--|:--|:--|:--|
| 0 | **Cross-cutting conventions** | status codes, Hydra model cleanliness, identifier policy, error model, domain/range table rules | protagonist |
| 1 | Account & access | customer, custom-headers, storage, (keys, portal users) | protagonist |
| 2 | Spaces & assets | space, asset, registering-assets, delivery-channels, origin-strategy | protagonist |
| 3 | Processing | queues, batch, pipelines | protagonist |
| 4 | Discovery & delivery | named-queries, asset-queries, single-asset-manifest, collections, identifiers, size-restrictions | protagonist |
| 5 | Adjuncts | adjuncts (partially implemented — many open questions) | protagonist |
| 6 | IIIF & Auth | iiif, roles, auth-service, access-control | iiif-presentation, iiif-auth-v2 |

## Inputs to assemble before / during the sprint (enrichment checklist)

- [x] **(done 2026-06-25, at register build)** Pull the A–F divergence register from the
      2026-06-24 audit into cards — the audit categories are cited throughout the theme
      files (e.g. session 4's "resume-audit-fixes Category C/D/E" references).
- [x] **(done 2026-06-25)** Convert each of the 17 `scratch/api-doc/*.md` notes into cards —
      the STALE-SCRATCH card type covers them; scratch files themselves refreshed with
      dispositions + verification annotations 2026-08-03.
- [x] **(done 2026-06-25; deepened 2026-08-03 — with a caveat)** Diff each new `.mdx` against
      its old Nextra source → `_provenance-nuance.md`. The 08-03 re-audit deep-diffed the four
      largest "clean" pages and found more (PROV-11..18); the remaining ten claimed-clean pages
      have NOT had the deeper pass and should be treated as unverified, not clean.
- [x] **(done 2026-06-25; refreshed 2026-08-03)** Enumerate open issues in the three repos →
      `_issues-rfcs.md` (counts, closures and new issues updated).
- [x] **(done 2026-06-25; refreshed 2026-08-03)** Locate and index RFCs → `_issues-rfcs.md`
      (29 RFCs + 15 ADRs; + RFC 024 proposed in protagonist PR #1230, RFC 0020 in
      iiif-presentation PR #228).
- [x] **(done 2026-06-25)** Fold in the Python sample punch-list (6 items, register.md) and
      the DELETE-status consistency finding (XC-01, SPA-16); sample coverage gaps tracked in
      XC-10 (re-checked 2026-08-03 — several since closed).
- [ ] **Deep-diff the remaining ten claimed-clean pages** (overview, collections, space,
      queues, batch, origin-strategy, identifiers, single-asset-manifest, size-restrictions,
      custom-headers) with the same lens that found PROV-11..18 in the four largest — can run
      per-session as each theme comes up rather than as one block.
- [ ] **Run the verify-first live tests** scripted in the ⚠verify card updates (ACC-08/09/11/13,
      SPA-10, PRO-13, the adjunct-queue samples) against a staging deployment — the one
      verification layer source-reading cannot provide.
- [x] **(done 2026-08-03) Re-baseline against protagonist `main`/`develop` + open PRs.**
      Outcome: adjunct-queue endpoints largely built on develop (PRO-08 refreshed); adjunct
      size/storage accounting reworked on main (ACC-06, ADJ-13 refreshed); issue counts and
      closures folded into `_issues-rfcs.md`; RFC 024 (PDF via Text-Services) proposed in PR
      #1230. **Repeat this re-baseline shortly before each session runs** — the repos move fast
      and cards cite file:line from a moment in time.

## Decisions made by the product owner (2026-06-25)

- **Location/visibility:** the register lives **here in `scratch/hygiene-sprint/`** (files,
  version-controlled, worked from a shared screen with Claude in the room). Not a GitHub
  Project for now — may export later once content is stable.
- **Granularity:** **maintain both views** — the one-line triage table *and* the detailed
  decision cards — and choose per-session which to drive from (table-only rapid sweep for
  easy themes; card-by-card for contentious ones).
- **Repo scope (auth):** iiif-auth-v2 (roles / auth-service / access-control) is **in scope
  but DESIGN-only** — captured as design/RFC cards, sequenced **last** (session 6), not
  blocking the doc-hygiene work on the existing API. The prerequisite is protagonist #538
  (+ #284, auth-v2 #7/#48, RFCs 005/008/012) — the auth REST API itself.
- **(2026-08-03) Editorial policy: `main` = released behaviour.** The published site
  documents what a customer hitting a current DLCS release actually gets — not `develop`.
  Docs for unreleased API surface are held back (docs `develop` branch or blocked-on-release
  PRs — mechanism to be settled Wednesday) and merge when the feature ships. Immediate
  consequence: the adjunct-queue sections of queues.mdx / batch.mdx currently describe
  develop-only endpoints (PR #1228, not in v1.13.2) and are therefore ahead of policy.
