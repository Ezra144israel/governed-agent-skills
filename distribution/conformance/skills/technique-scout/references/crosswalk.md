# Tier 2 — the crosswalk protocol

Only shortlisted candidates reach here. The point of a crosswalk is not to describe the
external repo — Tier 1 already did that. It is to prove, mechanism by mechanism, what the
user's own project already has.

Most of this work is internal. If you find yourself spending the majority of the effort on
the external repo, you are writing a review, not a crosswalk.

## 1. Pin both halves

**External:** record a stable `EXTERNAL_SOURCE_ID @ pin` for every source. Resolve the pin
yourself through the host where the surface permits it — never a commit merely *reported* by
the source, quoted in a README badge, or relayed by a subagent. This version does not clone
(`references/security.md`), so the pin is a ref resolved to a commit SHA through whatever
read-only route works, recorded with `RESOLVED_REF` and `RESOLVED_AT`. For a non-repo source
— a talk, an article — the pin is a URL plus a content digest or retrieval timestamp,
whichever the surface supports.

`PIN SOURCE: OPERATOR` is the one admissible alternative, and it is not a loophole in the
rule above: what that rule forbids is trusting an *unverified* identity found inside the
source you are evaluating. An operator-supplied pin comes from outside the evaluation, is
recorded as such, and carries the operator's provenance rather than the source's. Both are
admissible; they fail differently, which is why the field exists.

**A mutable ref is pinned only as of a moment.** Three independent resolutions of one busy
repository's default branch, within about an hour, returned three different SHAs. `RESOLVED_AT`
is what makes a pin re-derivable — without it, "resolved `main` myself" is not a reproducible
claim, only a sincere one.

**A resolved SHA is not pinned evidence on its own.** Reading a file at that SHA is a
*separate* capability and it can fail while resolution succeeds. Where it does, mutable-branch
content is the only thing left and it cannot be shown to be the pinned bytes — record
`PINNED_READ: FAIL` and cap the receipt. `SKILL.md`'s capability probe tests both halves
before Tier 1 for exactly this reason.

`EXTERNAL_SOURCE_ID` is load-bearing, not bookkeeping. Mechanism IDs are only unique within
the source that produced them, so two sources can each call something `M-1`. Without the
source ID travelling alongside, a receipt grounding source A's `M-1` satisfies a string
equality against source B's `M-1` and authorizes a claim about a mechanism it never searched
for. This is not hypothetical — one real run crosswalked three sources that each numbered
their mechanisms from `M-1`.

Record `PIN SOURCE` alongside the pin. A pin you resolved yourself and a pin the operator
handed you are both admissible, and they fail differently: a self-resolved pin can be
re-derived by anyone with the same route, while an operator-supplied one is only as good as
its provenance. Naming the route also makes a blocked route visible to the next run —
`SELF-RESOLVED (browser, commits page DOM)` says something a bare SHA does not, particularly
when the obvious routes are refused. See `SKILL.md`'s capability probe: if no route resolves
a pin, that is a Tier 0 stop, not a Tier 2 surprise.

**Internal:** record the commit, branch, and working-tree cleanliness of the project you
are comparing against. If you censused a directory, record the file count from
`git ls-tree -r HEAD --name-only <dir> | wc -l` alongside your own count and confirm they
match — that is what turns a sample into tree-level coverage.

A crosswalk without both pins is not reproducible and should say so plainly rather than
implying otherwise.

## 2. Ground internally, in this order

1. **The design corpus** — convergence packets, doctrine, locked specs, architecture
   records. This is where a mechanism most often already exists in more depth than the
   external repo has it.
2. **Current-state records** — what is actually built, per whatever artifact the project
   treats as authoritative for build state.
3. **Live code** — the final arbiter for "is it wired." Code beats every doc claim about
   the present.
4. **Installed configuration** — for skills, plugins, and tooling, check what is already
   active. Compare content, not names.

Note the asymmetry: docs win for *intent*, code wins for *current state*. A mechanism can
be fully specified and completely unbuilt, and that is a different verdict from absent.

## 3. Enumerate mechanisms, not repos

Break each candidate into named mechanisms with stable IDs. "Adopt this repo" is never the
right unit — "adopt this repo's per-edge traversal table" might be. Give each mechanism a
one-sentence description precise enough that someone who has not read the repo can check
it against internal sources.

Keep the ID and the description in **separate fields**, everywhere either appears. A
`MECHANISM_ID` is a bare token — `M-1`, `traversal-table` — and nothing else. The moment a
row writes `M-1 — a per-edge traversal table` into the ID field, the exact-equality check in
§4 compares a token against a token-plus-prose and fails, or worse, is performed by eye and
silently succeeds. An admission test that cannot run mechanically will not run.

## 4. Classify — one declared token per mechanism

| Token | Meaning |
|---|---|
| `LIVE_PROVEN` | Built, and demonstrated working on the real surface |
| `DOCUMENTED_ACTIVE_GUIDANCE` | Binds behavior today via doctrine or an active skill |
| `DOCUMENTED_PRE_WIRING` | Specified in detail; implementation inert or partial |
| `TARGET_LOCKED` | Design authority locked, implementation not started |
| `TARGET_RECOMMENDED` | Preferred design, not yet locked |
| `OPEN` | Named as an unresolved decision |
| `DEFERRED` | Sequenced behind named prerequisites |
| `ALREADY_MET` | Internal equivalent exists; note if internal is *ahead* |
| `PARTIAL_INTERNAL_OVERLAP` | Adjacent internal mechanism, different axis — say which axis |
| `INTENTIONALLY_DIFFERENT` | Internal deliberately rejects this shape; give the reason |
| `NOT_EVALUATED` | Not compared against — give the reason; no receipt required |
| `UNGROUNDED` | Compared, but no usable internal grounding existed at all |
| `UNVERIFIED_LEAD` | The artifact itself was never inspected — only what a source said about it |
| `UNRESOLVED_MENTION` | Named without a link; a bounded search failed to identify it. Record the queries. |
| `PRESENCE_UNKNOWN` | The census ran but could not determine whether the mechanism is there |
| `INTERNAL_CONFLICT` | Internal surfaces disagree — usually docs against code. Name both. |
| `NOT_FOUND_IN_SEARCHED_SET` | Not found — **not** a gap claim; name the searched surface |
| `CONFIRMED_ABSENT` | Absent from a completely censused surface; name the surface and method |
| `OUTSIDE_SCOPE` | This target cannot contain this kind of mechanism; no receipt required |

**`UNVERIFIED_LEAD` binds in both directions.** An item never opened supports no verdict —
not an absence, and equally not a presence. `ALREADY_MET`, `PARTIAL_INTERNAL_OVERLAP`, and
`INTENTIONALLY_DIFFERENT` are claims about what an artifact *does*; a name, a description, a
directory listing, or a source's summary establishes none of them.

**It binds the run's verdict, not only its rows.** A run can create no rows and still report
`recommend passing on all`, so — **a negative verdict over a collection requires that every
member was opened.** A run that did not open every member reports only on those it opened,
and its verdict reads `RUN: PARTIAL` with the count opened against the count enumerated. It
may not say "pass on all." The absence side had a wall of conditions and the presence side
had none, so the cheapest route past it was to conclude the opposite thing.

Only `CONFIRMED_ABSENT` supports a keep recommendation, and a row may carry it only when all
nine of the following hold:

1. Its `GROUNDING_RECEIPT_ID` resolves to a real receipt.
2. That receipt reads `GROUNDING: COMPLETE`.
3. Its `EXTERNAL_SOURCE_ID` equals the receipt's exactly.
4. Its `MECHANISM_ID` equals the receipt's exactly.
5. Its `TARGET_ID` equals the receipt's exactly.
6. **That receipt reads `PRESENCE: ABSENT`** — not `REJECTED`, and not any other value.
7. **Its own `READ MODE` is `DIRECT`, or `DELEGATED` with `re-verified: YES`.**
8. **The census found no documented rejection of the mechanism.** If it did, `PRESENCE` is
   `REJECTED` and the row is `INTENTIONALLY_DIFFERENT`.
9. **Its `APPLICABILITY` is `YES`.** §4c gate 1 says `UNKNOWN` blocks any absence claim, but
   an earlier version left applicability as prose in that section and put it in no schema and
   no condition — so an `UNKNOWN`-applicability triple carrying a `COMPLETE`, `ABSENT`,
   directly-read receipt satisfied every *mechanically visible* condition and false-greened.
   A rule stated only in prose is not enforced by a test made of field comparisons.

All three ID equalities are required, and each closes a different hole. Without
`TARGET_ID`, a receipt for one project authorizes a claim about another. Without
`MECHANISM_ID`, a receipt that thoroughly grounded one mechanism authorizes an absence claim
for a different one it never searched for. Without `EXTERNAL_SOURCE_ID`, two sources that
both number their mechanisms from `M-1` collide, and the collision produces a false green
from documents that were each honest about something else.

**Condition 6 is the one that makes the rest mean anything.** Every other condition asks
whether the *search* was good. None of them asks what the search *found* — so a thorough,
complete, correctly-matched, directly-read receipt whose `SEARCHED` line records finding the
mechanism satisfies conditions 1 through 5 and 7 with room to spare. A row could then classify
it `CONFIRMED_ABSENT` and recommend keeping something the project already has. Grounding
quality and result are independent axes, and an absence claim needs both: a good search *and*
an empty result.

**Every `PRESENCE` value has exactly one row classification.** An earlier version admitted
`UNKNOWN` and `CONFLICTING` on the receipt while offering no token for either, so a mandatory
row had to invent an undeclared one or misclassify — which is failure mode 9 forced by the
schema rather than chosen.

| `PRESENCE` | Row classification | Keep authority |
|---|---|---|
| `PRESENT` | `ALREADY_MET`, `PARTIAL_INTERNAL_OVERLAP`, or the appropriate build-state token | none |
| `ABSENT` | `CONFIRMED_ABSENT` if all nine conditions hold, else `NOT_FOUND_IN_SEARCHED_SET` | only via `CONFIRMED_ABSENT` |
| `REJECTED` | `INTENTIONALLY_DIFFERENT` | none |
| `UNKNOWN` | `PRESENCE_UNKNOWN` | none |
| `CONFLICTING` | `INTERNAL_CONFLICT` | none |

`INTERNAL_CONFLICT` is worth having rather than collapsing into "not found": disagreement
between internal surfaces usually means docs and code have diverged, which is a finding about
the target that the operator wants regardless of the external mechanism that surfaced it.
Name both surfaces and what each says; do not resolve it by picking the more convenient side,
and do not let it authorize anything.

**Condition 8, and why `REJECTED` is not a flavour of `ABSENT`.** A mechanism can be missing
because nobody thought of it, or missing because someone thought about it and decided against
it. Those look identical to a grep and they are opposite findings. Recommending something the
project deliberately rejected is worse than reporting a false gap: a false gap wastes a read,
while a rejected-mechanism recommendation re-opens a settled decision while appearing
well-grounded, and the reasoning that settled it is exactly what the report failed to surface.

This is not hypothetical. One run reached a complete, correctly-matched, directly-read receipt
whose mechanism — automatic cross-provider fallback — was genuinely not implemented. Every
condition 1–7 held. The same corpus also contained an explicit doctrine forbidding it, on the
grounds that automatic substitution destroys attribution. `CONFIRMED_ABSENT` was formally
admissible and substantively wrong.

So when the census turns up a *reason* the mechanism is not there — a doctrine, a rejected
proposal, a decision record, a constraint that rules it out — record `PRESENCE: REJECTED`,
classify `INTENTIONALLY_DIFFERENT`, and give the reason. That reason is usually the most
transferable thing in the whole crosswalk, because it generalizes past the mechanism to the
principle that killed it. Looking for it costs one extra question during a search you were
already running: *not just "is it here," but "is there a record of deciding against it."*

Condition 7 is separate from the same test on the receipt, and both are needed, because the
two fields describe different reads. The receipt's mode covers how the *census* was done; the
row's covers how *this row's conclusion* was reached. A row can cite a receipt whose census
was direct and complete and still be written from a subagent's summary of it — that is
failure mode 5 wearing a valid receipt. A row carrying `DELEGATED (re-verified: NO)` is capped
at `NOT_FOUND_IN_SEARCHED_SET` regardless of how good its receipt is.

A row whose receipt is missing, `PARTIAL`, or bound to another source, target, or mechanism is
likewise capped at `NOT_FOUND_IN_SEARCHED_SET`, no matter how thorough the search felt.

`OUTSIDE_SCOPE`, `NOT_EVALUATED`, and `UNGROUNDED` are each reached by a different gate, and
§4c defines all three. They are not softer forms of "absent" and none of them supports a keep
recommendation.

### When internal is ahead

This happens more than you would expect, and it is a first-class result — not a null one.

Use `ALREADY_MET` and then say *how far* ahead and *why*, because the reason is the
transferable part. Real examples from one crosswalk: an external repo proposed a weighted
release gate with non-regression floors; internal used a non-compensatory rule where the
overall score equals the lowest category, which is strictly stronger because no weighting
can trade correctness for aggregate gain. Another proposed keeping two review axes
unmerged; internal already had a hard stop against collapsing them plus eight
independently scored gates.

Recording these does two things. It tells someone learning the field that their own
synthesis is outperforming the sources it came from, which is calibration they cannot get any
other way. And the *reason* internal won — non-compensatory beats weighted, separate axes
beat merged — is itself a mechanism worth stating, because it generalizes to the next
decision.

It does not prevent a future re-scout. Persistence is governed by `references/deposit.md`,
which owns that rule and its limits.

## 4b. One result per target — never a set

With several grounding targets, a mechanism gets an **independent verdict against each
one**. Collapsing them hides the most useful shape there is: already present in project A,
genuinely useful to project B, irrelevant to project C.

Every `(EXTERNAL_SOURCE_ID, MECHANISM_ID, TARGET_ID)` triple gets a row. Never silently
omitted — an absent row and a negative row look identical in a table, and only one of them is
a finding.

Relevance-routing (weighing a mechanism only against targets it plausibly touches) is a
future optimization, not a current rule. It may only be adopted on measured evidence of cost
and false-negative rate, never on target count alone. Routing wrongly is the same defect
class as everything in `failure-modes.md` — a narrowed surface producing a false absence.

## 4c. Three questions, asked in order — and only one of them is about grounding

Every triple passes through three gates. They are separate because they fail for separate
reasons, and an earlier version fused them: applicability was asked *inside* the grounding
predicate, so a target that could not possibly contain a mechanism produced a `PARTIAL`
receipt, which capped the row at `NOT_FOUND_IN_SEARCHED_SET` — while the same predicate said
the row should be `OUTSIDE_SCOPE`. Two rules, one row, no way to satisfy both.

**Gate 1 — APPLICABILITY.** *Could this target contain this kind of mechanism at all?*

| Answer | Row classification | Receipt |
|---|---|---|
| `NO` | `OUTSIDE_SCOPE` — say why the category does not apply | none; `GROUNDING_RECEIPT_ID: N/A` |
| `UNKNOWN` | continues to gate 2, but can never reach `CONFIRMED_ABSENT` | as gate 3 |
| `YES` | continues to gate 2 | as gate 3 |

A documentation set cannot contain a runtime mechanism. Calling it "absent" there is a
category error, not a finding, and it should cost nothing to record.

**Gate 2 — EVALUATION.** *Was this triple actually compared?*

| Answer | Row classification | Receipt |
|---|---|---|
| `NOT_EVALUATED` | `NOT_EVALUATED` — give the reason | none; `GROUNDING_RECEIPT_ID: N/A` |
| `EVALUATED` | continues to gate 3 | required |

Deciding not to evaluate is a legitimate, budget-driven choice. What is not legitimate is
leaving the row out, because a missing row reads as "nothing to say" when it means "nobody
looked."

**Gate 3 — GROUNDING.** *For evaluated triples only: how good was the census?*

| `GROUNDING` | Meaning | Strongest available verdict |
|---|---|---|
| `COMPLETE` | closed predicate below fully satisfied | any, including `CONFIRMED_ABSENT` — subject to §4 conditions 6 and 8 |
| `PARTIAL` | grounding existed but the census did not close | `NOT_FOUND_IN_SEARCHED_SET` |
| `UNGROUNDED` | no usable internal grounding existed to search | `UNGROUNDED` |

**This table caps absence claims only, and presence claims are capped by something else.**
A partial census supports a presence finding perfectly well — finding a thing does not
require having searched everywhere. What a `PARTIAL` census cannot do is prove a negative.
Read "strongest available verdict" as "strongest available *absence* claim."

Presence is not therefore free. `ALREADY_MET` discards an external mechanism on the grounds
that we have it, and it is capped by **read depth of the internal counterpart**, not census
breadth:

**A row may carry `ALREADY_MET` only if it states what the internal mechanism does and how
that covers the external one.** A `path:line` shows where a matching string sits, not that
the thing at that line does the same job.

**`PRESENCE` follows the read, not the match.** Locating a candidate line is not
`PRESENCE: PRESENT`; presence is a claim about behavior and needs the counterpart read.
Located but not read is `PRESENCE: UNKNOWN`, and the row is `PRESENCE_UNKNOWN`.

A false gap wastes one read. A false `ALREADY_MET` discards a mechanism we do not have,
behind a citation that looks like evidence, and it is what a skimming run produces by
default. On record: a run matched an external rule about counting items opened against an
internal rule about truncatable search surfaces. Different axes, same word. The row read
`ALREADY_MET` behind a real citation and was wrong.

`PARTIAL` and `UNGROUNDED` are not degrees of the same thing. `PARTIAL` means there was a
corpus and the search of it did not close. `UNGROUNDED` means there was no corpus — no design
record, no build-state artifact, no readable code, nothing to compare against. A row
classified `UNGROUNDED` reports the external mechanism and states plainly that no comparison
was performed. Neither supports a keep recommendation, and they are worth telling apart
because they call for different remedies: `PARTIAL` wants a better search, `UNGROUNDED` wants
the operator to point at something to search.

Extend the vocabulary if you must, but declare the addition — an undeclared token is
unauditable.

## 5. Grounding receipt — one per evaluated (source, mechanism, target) triple

A comparison is only as good as the census behind it, and the census is the step most likely
to be quietly incomplete. Every triple that clears gates 1 and 2 of §4c carries a receipt;
`OUTSIDE_SCOPE` and `NOT_EVALUATED` rows carry `GROUNDING_RECEIPT_ID: N/A` instead, since
there was no census to describe.

A receipt grounds **one mechanism from one source against one target**. That triple is the
unit, because two mechanisms need different searches: proving a traversal table is absent and
proving a gate is absent are not the same census, and a receipt honest about one says nothing
about the other. An earlier version issued receipts per target, which let a row cite a
complete receipt that had never looked for its mechanism.

```
RECEIPT_ID:            <unique within this run — rows cite this>
EXTERNAL_SOURCE_ID:    <source id> @ <pin — resolved commit, or URL + retrieval identity>
RESOLVED_REF:          <the ref that was resolved, e.g. main, release/v3 — not the SHA>
RESOLVED_AT:           <when the ref was resolved; a mutable ref is only pinned as of a time>
PIN SOURCE:            SELF-RESOLVED (<the route used>) | OPERATOR
PINNED_READ:           <a file read at this exact SHA, and the route — or FAIL + what that
                        caps this receipt at. Mutable-branch content is not pinned evidence.>
APPLICABILITY:         YES | NO | UNKNOWN — §4c gate 1; carried here and on the row
MECHANISM_ID:          <bare token — the one mechanism this receipt grounds; no description>
TARGET_ID:             <id> @ <fingerprint — commit, or content hash for a doc set>
READ MODE:             DIRECT | DELEGATED (re-verified: YES/NO)
AUTHORITY ORDER:       <which sources were treated as governing, in order>
SEARCHED:              <named surfaces, globs, and exact queries>
PRESENCE:              PRESENT | ABSENT | REJECTED | UNKNOWN | CONFLICTING — <what the
                        search found, with evidence: path:line for PRESENT and REJECTED,
                        the empty queries for ABSENT, the disagreeing surfaces for
                        CONFLICTING. REJECTED means the census found a record of deciding
                        against it — cite that record.>
DISCOVERY COMPLETE:    YES | NO — <the surfaces where THIS mechanism could live were
                        enumerated end to end, and where the mechanism is a pipeline or
                        chained behavior, the whole invocation chain was traced. If NO,
                        what was unreachable and why.>
DESIGN CORPUS READ:    YES | N/A + reason — <designed-but-unwired material, not just live code>
CURRENT-STATE READ:    YES | N/A + reason — <the project's own build-state record>
LIVE CODE READ:        YES | N/A + reason
INSTALLED CONFIG READ: YES | N/A + reason — <what is actually active: skills, plugins, tooling>
GROUNDING:             COMPLETE | PARTIAL | UNGROUNDED
```

`PRESENCE` and `GROUNDING` are independent and both are required, because they answer
different questions: `GROUNDING` is *how well did I look*, `PRESENCE` is *what did I see*. A
complete census that found the mechanism is a perfectly good receipt — it just grounds
`ALREADY_MET`, not an absence.

### The COMPLETE predicate — closed

`GROUNDING: COMPLETE` is permitted only when **every** clause below holds. This is a closed
list: if a clause cannot be satisfied, the receipt is `PARTIAL`. An earlier version checked
only the read lines, which let a receipt declare `DISCOVERY COMPLETE: NO` and still authorize
an absence claim.

1. `DISCOVERY COMPLETE: YES`, in the mechanism-specific sense the field defines. Enumeration
   of the target as a whole is not the claim — the claim is that the surfaces where *this
   mechanism* could live were read end to end. A capped, truncated, or partially-enumerated
   search cannot ground an absence, whatever it did or did not turn up. And where the
   mechanism is a pipeline, hook, or anything else invoked indirectly, the chain has to be
   traced through: config → invoked script → lifecycle hooks → transitive scripts →
   framework defaults. Failure mode 4 is what one un-traced link produces.
2. **Both pins are reproducible.** The target fingerprint resolves to a specific immutable
   state. A dirty working tree or an unpinned branch means the state cannot be re-derived —
   either supply a content identity covering tracked *and* untracked changes, or the receipt
   is `PARTIAL`.
3. **All four read lines are `YES`, or an explicit `N/A` with a reason.** A blank is not an
   `N/A`. `N/A` is legitimate on any of the four, but only where the target genuinely lacks
   that surface — a documentation-only target has no live code; a target with no build-state
   record has no current-state artifact; a library has no installed configuration. It is
   never a shortcut for "did not look," and the reason has to name the absent surface.
4. **The receipt's own `READ MODE` is `DIRECT`, or `DELEGATED` with `re-verified: YES`.**
   This is the *receipt's* read mode — how the census was performed. An earlier version
   checked only the row's field, so a delegated, unverified census could sit behind a row that
   looked admissible. The row's field is checked too, as condition 7 of `CONFIRMED_ABSENT` in
   §4; the two are separate gates on separate reads and neither substitutes for the other. A
   delegated read never re-verified at source is failure mode 5 and cannot ground a `COMPLETE`
   receipt.

Note what is *not* in this list: whether the search found anything. `GROUNDING` grades the
census only. What the census saw is `PRESENCE`, and §4 condition 6 is where it binds.

Current-state records and installed configuration are in the read set because omitting them
is how a mechanism gets called absent when it is merely unbuilt, or novel when it is already
installed under another name.

The verdict cap by grounding level is the gate-3 table in §4c and is not restated here.

`NOT_FOUND_IN_SEARCHED_SET` is necessary but not sufficient for an absence claim. A positive
completeness boundary is what turns "I did not find it" into "it is not there."

`DESIGN CORPUS READ` is its own line because skipping it is failure mode 2, and it is
invisible in a receipt that only records which files were grepped.

## 6. Per-row provenance

Each row carries how you know:

```
EXTERNAL_SOURCE_ID: <source id> @ <pin>
MECHANISM_ID: <bare token — no description in this field>
DESCRIPTION: <one sentence, precise enough to check against internal sources>
TARGET_ID: <which target this row is about> @ <fingerprint>
APPLICABILITY: YES | NO | UNKNOWN
GROUNDING_RECEIPT_ID: <the receipt that governs this row, or N/A + reason>
CLASSIFICATION: <one declared token>
INTERNAL EVIDENCE: <path:line, or the exact searches that came back empty>
READ MODE: DIRECT | DELEGATED (re-verified: YES/NO)
INTERNAL READ: <what was read of the internal counterpart, and one sentence on what it
               does — required for ALREADY_MET; N/A on absence rows>
DELTA: <what the external version adds, if anything>
MATERIALITY: <what not having it costs, or NONE — see §8. Never blank.>
```

`EXTERNAL_SOURCE_ID`, `MECHANISM_ID`, and `TARGET_ID` are spelled exactly as they are on the
receipt, because the admission test in §4 is a string equality against those three fields.
`DESCRIPTION` is separate for the same reason: a row that writes the sentence into the ID
field cannot be matched mechanically, and a check that cannot run mechanically will not run.

`GROUNDING_RECEIPT_ID: N/A` is correct and expected on `OUTSIDE_SCOPE` and `NOT_EVALUATED`
rows — those never had a census. Give the reason inline. On any other classification, `N/A`
is a defect.

The read-mode field is what makes contagion checkable. When one delegated conclusion turns
out wrong, this field tells you instantly which other rows share its method. It is also
condition 7 of `CONFIRMED_ABSENT` — see §4.

`MATERIALITY` is a **declared field addition**, not a classification token, and §8 fences what
it may and may not do. It is required on every row so that the question is asked every time
rather than only when the answer is interesting. `NONE` is a legitimate and common value.

## 7. Return template

```
VERDICT: <recommend keeping N mechanisms / recommend passing on all / mixed>

IDENTITY
  external: <EXTERNAL_SOURCE_ID @ pin, how the pin was resolved> (× each)
  internal: <TARGET_ID @ fingerprint | branch | tree clean? | censused counts> (× each)

CROSSWALK
  <one row per (EXTERNAL_SOURCE_ID, MECHANISM_ID, TARGET_ID) triple, per §6 —
   every triple appears, including OUTSIDE_SCOPE and NOT_EVALUATED>

GROUNDING RECEIPTS
  <one per evaluated triple, per §5 — the same unit as a crosswalk row, so every
   evaluated row resolves to exactly one receipt and no receipt is shared across
   sources, mechanisms, or targets. OUTSIDE_SCOPE and NOT_EVALUATED rows have none
   by construction and are not omissions.>

HORIZON RECEIPTS
  <one per collection enumerated, per references/sources.md — omit only if no
   collection was enumerated this run>

SURVIVING CANDIDATES
  <EXTERNAL_SOURCE_ID @ pin | MECHANISM_ID | TARGET_ID | why it survives against
   THAT target | what gate it must clear before adoption>

REJECTED SHAPES
  <EXTERNAL_SOURCE_ID @ pin | MECHANISM_ID | TARGET_ID | why it must not be copied>

RETENTION
  <mandatory, per SKILL.md Tier 3, which owns the rule. One bucket for every
   enumerated item that was OPENED, not one verdict for the source. Items never
   opened get no bucket. Never omitted. Buckets carry no keep authority.>
  WHOLE:   <item | the tweaks, named specifically | edit or decision>
  GEMS:    <item | each gem quoted verbatim, with where it came from>
  LINE:    <item | the line verbatim, with its source>
  NOTHING: <item | already met, or not worth carrying — say which, and on what
            evidence. Mark provisional where no census backs it. Unavailable on an
            unopened item and on a row classified PRESENCE_UNKNOWN,
            UNVERIFIED_LEAD, INTERNAL_CONFLICT, or NOT_EVALUATED.>
  PARTIAL: <item | enumerated, never opened, and why it was not reached>
  COUNT:   <N enumerated = W whole + G gems + L line + X nothing + P partial —
            the arithmetic has to close, per the numbers rule below>

GAP ANALYSIS
  <mandatory, per §8 — never omitted, including when it finds nothing>
  MATERIAL: <per gap: what it costs, the evidence, and that it carries no
             keep authority>
  NOT A GAP: <absences judged immaterial, and structural areas checked and
             found sound — a gap pass that produces only gaps is uncalibrated>

SEARCH BOUNDARY
  SEARCHED: <named surfaces, ranges, exact queries>
  DELIBERATELY NOT SEARCHED: <named adjacent surfaces, and why>
  COMPLETENESS CLAIM: limited to the SEARCHED set

UNVERIFIED LEADS
  <anything unproven — supports no recommendation>
```

The summary sections carry all three identity dimensions for the same reason the rows do: a
mechanism that survives against one target and is already met by another is *two different
results*, and a summary line naming only the mechanism collapses them into a recommendation
the crosswalk never made. One line per surviving triple, not per mechanism.

**Why `RETENTION` is in the template and not left to Tier 3 alone.** The buckets were defined
in `SKILL.md` and never reached this template, so nothing in the output contract asked for them
— and a rule the report format does not collect is a rule that gets collected when someone
remembers. One real run listed four gems in its report; the source held twenty, and the
operator had to ask twice before the other sixteen appeared. The rule was written, understood,
and skipped, because the template it had to survive did not have a slot for it.

That is the general shape: **a requirement that exists only in the method section is enforced by
attention, and attention is what runs out at report time.** Anything a run must always produce
belongs in the template, where its absence is visible as an empty heading rather than invisible
as an unasked question.

**The count has to close.** `COUNT` exists because the failure above is not a judgment error —
it is an undercount that reads as a complete answer. State the number of items enumerated and
the five counts, four buckets plus the partial count, and confirm they sum. An unopened
item is a real part of the collection and dropping it from the arithmetic is the undercount
this rule exists to catch. A retention section whose arithmetic does not
close is reporting on a subset while looking like it reported on everything, which is failure
mode 3 aimed at the run's own output. This rule is about the retention arithmetic specifically;
whether it should generalize to every number in a report is an open question and is not decided
here.

The buckets carry no authority — `SKILL.md` Tier 3 holds the fence, and it is not restated here.

## 8. Gap analysis — mandatory, and fenced

A crosswalk answers *do we have it*. That is not the question the operator is asking. The
question is **does not having it cost us something.**

Operator, 2026-08-20: *"lack of a feature does not constitute a gap per se, but the lack of a
needed functionality to materially improve outcomes does."*

An absence and a gap are different objects. A gap is an absence with a price. Most absences do
not have one — the target does not do that kind of work, or it does the same job another way, or
the mechanism solves a problem this target does not have. Reporting every absence as a gap is
how a scout inflates its own yield, and the scout's author is the party motivated to do it.

**Every run carries a gap section. It is never omitted, including when it finds nothing.** A
missing section reads as "no gaps" when it means "nobody asked," which is failure mode 3 wearing
one more disguise.

### The field

Every crosswalk row carries `MATERIALITY`, per §6. Two admissible shapes:

- **`NONE`** — the absence costs nothing that this run can name. Correct and common. Use it for
  anything you would defend with "it would be nice."
- **A named cost** — a specific outcome that is worse because the mechanism is not there, with
  the evidence for it. Not a category of benefit. Not a hypothetical. Name the outcome, and say
  how you know.

The test that separates them: *can you point at something that already went wrong, or is
structurally certain to, because this is missing?* If the answer is a benefit rather than a cost,
the value is `NONE`.

### Structural gaps carry no row

A gap pass reads the target while comparing it, and what it sees is often not about the external
source at all: an enforcement layer with a hole in it, a schema nothing validates, one rule
written into six documents. These are findings about the target's own architecture. The external
source was the occasion, not the cause, and most of them would stand if that source had never
been read.

Report them in the gap section. They get **no `MECHANISM_ID`, no row, and no classification
token**, because there is no external mechanism to classify — inventing one would put a finding
about the target inside a vocabulary built for weighing external work.

Say plainly what search backs each one, and cap the claim to it. A structural gap found while
looking for something else has, by construction, not had a `COMPLETE` census run against it.
State it as a diagnosis to be confirmed.

### Report the non-gaps

A gap pass that produces only gaps has not been calibrated, and cannot be trusted to have tried.
Record the absences judged immaterial and the structural areas checked and found sound. Where the
target is *ahead*, that belongs here too — §4's "When internal is ahead" says why that is a
first-class result.

### The fence

**`MATERIALITY` carries no authority.** It is declared here as a field addition per §4, and it is
quarantined:

- It never substitutes for a classification, never modifies one, and is never modified by one.
- It grants no keep authority. **Only `CONFIRMED_ABSENT`, under the nine conditions in §4,
  supports a keep recommendation.** Those nine conditions are unchanged by this section.
- Assign the classification on its own evidence first. Assign `MATERIALITY` after.

**What this section does not decide.** Whether materiality *should* become a further condition on
`CONFIRMED_ABSENT` — a tenth gate — is an open question, not settled here. So is who judges
materiality when the scout's author is the one motivated to find a gap, and whether the test
applies in reverse to retiring a held rule that is true but has never changed an outcome. Those
belong to convergence. This section adds the question to every run and requires the answer to be
recorded; it deliberately stops short of letting the answer authorize anything.

## 9. Authorization boundary

A crosswalk produces candidates. It authorizes nothing.

If the project has a governed adoption path — a convergence step, an independent review, a
publication gate — say explicitly that each surviving candidate must clear it. Watch your
own phrasing here: "usable as practice now" and "ready to apply" quietly grant authority a
diagnostic artifact does not have. This is easy to do by accident in a summary section
after having drawn the boundary correctly earlier in the same document.
