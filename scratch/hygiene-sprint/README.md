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

- [ ] Pull the A–F divergence register from the 2026-06-24 audit into cards (memory:
      `audit-2026-06-24`, `resume-audit-fixes`).
- [ ] Convert each of the 17 `scratch/api-doc/*.md` notes into one or more cards.
- [ ] **Diff each new `.mdx` against its old Nextra source** (`C:\git\dlcs\docs\pages\api-doc`)
      to catch nuance dropped in the port — a dedicated prep task.
- [ ] Enumerate open issues in `dlcs/protagonist`, `dlcs/iiif-presentation`,
      `dlcs/iiif-auth-v2`; link each to the relevant card.
- [ ] Locate and index any RFCs (old docs repo? a dedicated RFC location?) and link them.
- [ ] Fold in the Python sample punch-list (6 items, see register) and the DELETE-status
      consistency finding.
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
