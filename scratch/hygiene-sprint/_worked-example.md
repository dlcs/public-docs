# A worked example: what actually happens in the room

> Written 2026-08-03 so everyone arrives Wednesday with the same picture. **Every
> "ruling" below is ILLUSTRATIVE** — invented to show the mechanics, not a decision
> anyone has made. Where a real PO leaning already exists it is labelled as such.

## The flow in one paragraph

We sit in a room (or call) with the register on a shared screen and Claude live in the
repo. We work a theme's triage table top to bottom. For each card Claude reads out the
discrepancy in under two minutes; we discuss until we can state a **ruling** in one
sentence; Claude records it on the card, drafts anything small enough to draft live
(doc edit, sample fix, GitHub issue text), and we move on. Big things become issues or
RFC stubs, not room time. At the end we re-read the rulings, Claude opens the session
PR, and named owners merge async. The register is the audit trail; git history mirrors
it one commit per card.

## Cast

| Role | Who | Does what in the room |
|:--|:--|:--|
| Product owner | Tom | chairs; owns doc rulings; merges public-docs PRs |
| protagonist dev(s) | TBC | says what the code actually intends; owns protagonist issues/PRs |
| iiif-presentation dev | Jack | owns anything touching the write path / PR #641 |
| Claude | (live) | reads cards, retrieves code/doc evidence on demand, records rulings, drafts changes and issue text, opens the session PR |

---

## Minute 0-10 · Session 0 only: the mechanical-track veto pass

Claude puts [`_mechanical-track.md`](./_mechanical-track.md) on screen — five batches,
~30 cards, one line each. The room's ONLY job: shout if anything is secretly
contentious.

*Illustrative exchange:*

> **Dev:** "Batch C1, the `CustomerAdjunctsController` 404→400 annotation — actually I
> think returning 400 for not-found is the bug, not the annotation. Pull it."
>
> **Claude:** *(moves the row to the borderline table, notes "dev suspects code is
> wrong way round — decision track, fold into XC-04 discussion")*
>
> **Tom:** "Everything else stands."

Result: the surviving batches are ratified. Claude turns them into draft PRs after the
session (or they were pre-drafted and now just leave draft state). Nobody discusses a
hostname typo in the room, ever.

## Minute 10-40 · Convention rulings (session 0's real work)

These are the ten XC cards. One worked example:

**Claude reads out XC-01 (≤2 min):** "Proposed rule: every DELETE returns 204, no
body. The framework already does this; five endpoints diverge — two are annotation
lies, verified: the policy DELETE annotated 202, Space DELETE annotated 200 plus a
body. Two return legacy 200-with-body: bulk deleteImages, which has an explicit
Deliverator back-compat comment, and the pdf purge. Question for the room: ratify the
rule, and decide whether the two legacy bodies migrate or get documented as
exceptions."

*Illustrative discussion and ruling:*

> **Dev:** "Annotations are just wrong, fix them — that's already Batch C1. The bulk
> deleteImages body… portal parses that message. Don't break it this quarter."
>
> **Tom:** "Then the rule is 204 with two named exceptions, and the exceptions are
> documented as such."
>
> **Claude records on the card:**
> - **Ruling:** DELETE→204 ratified. Named exceptions: bulk deleteImages, pdf purge
>   (legacy bodies, kept for portal back-compat; revisit when portal migrates).
> - **Track:** code (annotations — already Batch C1) + doc (document the two
>   exceptions where they appear).
> - **Owner:** dev X (code), Tom (docs).
> - **Artefacts:** none new needed — Batch C1 covers the code; doc rows join Batch D1.
> - **Status:** ☑ ruled 2026-08-06.

Why the XC cards come first: that one ruling just auto-resolved the DELETE aspects of
SPA-08, SPA-09, SPA-16 and the sample punch-list — they inherit the convention instead
of being argued one by one.

**Also in this block:** XC-02/XC-03 (POST 201 / PUT semantics) — where the recorded
move is *"hand the ruling to Jack's in-flight PR #641"* for iiif-presentation, and an
issue for any protagonist stragglers (e.g. `UpdateCustomHeader` returning Created on
update, ACC-15).

## Minute 40-80 · Decision-track cards, one at a time

The heart of every themed session. Full worked example with **DIS-14** (EntryPoint
docs show `queue` and `deliveryChannelPolicies`; the model emits neither):

**1. Claude reads out (≤2 min):**
"entrypoint.mdx documents a `queue` link and a `deliveryChannelPolicies` link, and
both appear in its JSON example. Verified: the model emits neither — it emits six
links including two legacy ones and `portalRoles`, none of which we document. Two
sub-questions. `queue`: the global `/queue` **endpoint exists**, only the link is
missing — adding the model property is a one-liner. `deliveryChannelPolicies`: no
endpoint, and the old docs themselves wrapped the section in a 'should this exist?'
callout. Tom's recorded leaning: drop it. Nuance status: the old prose is already
preserved in scratch with dispositions — `deliveryChannelPolicies` marked
probably-drop, the hardcoded-policies fact marked restore-candidate. Sample status:
`entrypoint.py` currently hand-builds the `/queue` URL with a TODO comment."

**2. Discussion** *(illustrative)*:

> **Dev:** "Agree on dropping deliveryChannelPolicies. And I'd add the queue link —
> the endpoint's public, it should be discoverable."
>
> **Tom:** "Then docs keep the `## queue` section, the example keeps `queue`, and we
> lose the other one everywhere."

**3. Claude records the ruling** (on the card, and mirrors the one-liner into the
register's Ruling column):

> - **Ruling:** add `queue` HydraLink to EntryPoint (code); remove
>   `deliveryChannelPolicies` from example + docs entirely (doc); DIS-16
>   (`portalRoles`) stays open — separate card.
> - **Track:** code + doc. **Owner:** dev X / Tom.
> - **Artefacts:**
>   - protagonist issue drafted **live** by Claude — title, one paragraph, card ID in
>     the body — the dev skims it, says "file it", Claude files it via `gh`.
>   - doc edit drafted **live** on the session branch (`hygiene/session-4`), one
>     commit: `DIS-14: remove deliveryChannelPolicies from entrypoint docs`.
>   - **Nuance:** nothing to do — scratch already holds the prose with the right
>     disposition. (If it didn't, capturing it would happen *before* the edit
>     commits.)
>   - **Sample parity:** `entrypoint.py`'s TODO comment updated in the same commit —
>     the sample keeps hand-building the URL until the protagonist change ships, and
>     says so. When the link lands, a follow-up sample change reads it properly —
>     that note goes on the card.
> - **Status:** ☑ ruled 2026-08-06, doc landed in session PR, code = protagonist #NNNN.

**4. Definition-of-done check** — Claude runs the checklist out loud: ruling ✓ track ✓
owner ✓ artefact ✓ nuance preserved ✓ sample parity ✓. Next card.

That's the rhythm: 3-6 minutes per decision card. Easy ones ride the conventions;
contentious ones get the discussion; anything that can't reach a one-sentence ruling
in ~5 minutes gets **parked** with a named blocker ("needs live test", "needs product
input", "wait for #641") rather than eating the room.

## When a card is DESIGN (can't be resolved by this room)

*Illustrative, with SPA-04 (asset `manifest`/`manifests`/`scopes`):*

The recorded PO intent is that `asset.manifest` will link to the single-asset manifest
and `manifests` becomes `scopes`. The room doesn't design that live. The ruling is
just: "intent confirmed; Claude drafts a protagonist issue (and RFC stub if the dev
wants one) capturing the target model + the breaking-rename consideration; docs stay
as-is until it ships." Two minutes, one artefact, move on. The whole session-6 AUTH
cluster works this way — the output is RFC skeletons and sequencing, not rulings on
prose.

## Minute 80-90 · Close

1. Claude re-reads every ruling made this session, one sentence each — last chance to
   object.
2. Parking lot read back (cards parked + their named blockers).
3. Claude opens the session PR (`hygiene/session-N` → `main`): the live-drafted doc
   and sample commits, one per card ID. Reviewers = the people who were in the room.
4. Register committed: Ruling column filled, card statuses flipped, any new cards that
   emerged get IDs and join the right theme file.

## After the room (async, before the next session)

- Owners merge: Tom the session PR + surviving mechanical batches D1-D3; the named dev
  reviews C1/C2 in protagonist; Jack anything routed to #641.
- Claude re-baselines the next session's theme against current `develop`/`main` (the
  repos move weekly — every card gets its facts re-checked before it's argued).
- Release-gated material (adjunct-queue docs) stays parked until protagonist cuts the
  release; the *main = released behaviour* rule decides what may merge.

## What Wednesday is NOT

- Not editing prose by committee — wording is drafted by Claude, approved by the owner
  in PR review.
- Not debugging live — anything needing a running system goes to the verify-first list
  with a named test.
- Not exhaustive — 137 cards will not all be touched Wednesday. Session 0's
  conventions + the mechanical track are designed to make most of them fall cheaply in
  later sessions.
