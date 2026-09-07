# Sources — types, harvesting, and growing the list

A source arrives as a URL. Infer its type from the URL rather than asking the user to
declare it, then harvest according to that type.

| URL shape | Type | Behavior |
|---|---|---|
| `youtube.com/@handle` (± `/videos`) | `youtube_channel` | a set — read all, or triage under a budget (relevance.md) |
| `youtube.com/watch?v=…` | `youtube_item` | a single item — read it |
| `youtube.com/playlist?list=…` | `youtube_playlist` | same as channel |
| ends `.xml` / `/feed` / `/rss` | `feed` | standard feed parse |
| `github.com/owner/repo` | `repo` | classify by tree shape first — one artifact, or a collection of them |
| anything else | `unclassified` | fetch once, then **classify by observed shape** |

**The catch-all is not "article."** A Notion database, a Google Doc reading list, an
`awesome-*` index page, a conference schedule, a newsletter archive — none match a known
collection URL pattern, and all are collections. An earlier version routed them to `article`
and "fetch and read once," which skipped classification, the horizon receipt, and item-by-item
triage in a single step. A 200-item reading list read "once" produces a report shaped exactly
like a complete answer, which is this skill's defining failure.

So the type comes from the shape of what arrived, not the shape of the URL. After fetching an
`unclassified` source, ask: does this page enumerate multiple linked items of a consistent
kind — a list, a table, a feed, a database view, an index? If yes, it is a **collection**:
declare a horizon, judge its members per `references/relevance.md`, record a horizon receipt. If it is one continuous piece
of writing, it is an **article**: read it. If the shape is genuinely ambiguous — a long essay
that happens to link thirty repos — treat it as both: read it as an article *and* triage the
linked items as a collection under the same budget gate, since the cost of doing both is small and the cost of guessing
wrong in the skipping direction is a false absence.

**A repository is a URL shape, not a unit of work.** One repo is one artifact. Another
enumerates twenty: `skills/*/SKILL.md`, `plugins/*`, `rules/*`. The test is adoption, not
directory structure: if taking exactly one member and leaving the rest is coherent, they are
items and the repo is a collection; if a member only works as part of the whole, it is one
artifact. `src/commands/*` fails that test. `skills/*/SKILL.md` passes. Mixed kinds are
still one collection. On record: a skills repository scouted twice, reported empty both
times, from names and descriptions alone. A third pass found otherwise.

**`MATERIALIZATION: PINNED-GIT-TREE`** for a tree read at a resolved commit: immutable, so
drift-free by construction, the same standing as `SINGLE-SNAPSHOT`. `ITEM IDENTIFIER` is the
member's path at that pin. `ID CROSS-CHECK: N/A — a git tree has no title ordering.` A tree
API response marked truncated is `REACHED HORIZON: NO`.

If the fetch fails or returns something you cannot classify, record `PARTIAL` with the reason.
Never default an unclassifiable source to `article`, because that is the reading that does
least work and it will be wrong exactly when it matters.

A URL handed over for inspection is not authority to subscribe to it. If the user keeps a
list of sources, only an explicit "add this" instruction puts anything on it, and the user
writes the list — not the run.

## Relevance filtering before deep work

When a source is a set — a channel page, a roundup, a reading list — you cannot open
everything, and some of it will be only occasionally about technique.

Read every item unless a budget with a named owner exists, per `references/relevance.md`,
which governs when the filter may fire at all. Where it does fire, it runs on **title plus
description only**, before pulling any transcript.
Promote to deep read when an item plausibly carries mechanism: it names tools, repos,
architecture, workflow, testing, review, agents, or evaluation; or it is a walkthrough,
teardown, roundup, or postmortem; or the description carries a repo list or timestamped
chapters.

**`references/relevance.md` governs the skip decision and this section does not restate it.**
Three rules from there are load-bearing enough to name here, because getting them wrong
produces exactly the false absence this skill exists to prevent: a skip requires a
*description* that affirmatively establishes non-mechanistic content — a title alone never
suffices; a **direct item** the user handed over — a repository that is a single artifact included —
is never filtered at all, while a **direct
collection** they handed over is judged item-by-item per `references/relevance.md`; and an item with no usable
description is deep-read or recorded `PARTIAL`, never skipped, since the filter had no input
to judge on.

Log every skip with its title in this run's report. Absent an authorized deposit there is no cross-run memory in this
version, so a skip informs the operator now and nothing else — it does not accumulate into a
score, a tier, or a retirement suggestion.

## Enumerating a collection — the horizon receipt

A set has no natural edge. "Recent uploads" is unbounded, and a run that reads six of forty
produces something shaped exactly like a complete answer. `SKILL.md` requires a declared
horizon before enumeration; this is the receipt that proves the enumeration actually reached
it, which is a different claim from having declared it.

```
COLLECTION:        <the source>
HORIZON:           <last N items | since <date> | named range>
HORIZON SOURCE:    OPERATOR | DECLARED BY RUN — <if declared, why this bound>
ANCHOR:            <what fixes the top of the range: an as-of timestamp, or the ID of the
                    item that was newest when enumeration began>
MATERIALIZATION:   SINGLE-SNAPSHOT | STITCHED-REQUESTS | OPERATOR-SUPPLIED-LIST |
                    PINNED-GIT-TREE
PAGINATION:        <the cursor sequence or page/offset sequence actually used, or N/A>
ITEM IDENTIFIER:   <the stable per-item ID used, and how it was obtained>
ID CROSS-CHECK:    <that the identifier ordering agrees with the title ordering, or the
                    disagreement>
ENUMERATED:        <count of IN-HORIZON items listed — excludes any boundary witness>
UNIQUE ITEMS:      <count of distinct item IDs among those — this is the real coverage number>
DUPLICATES:        <count of repeated IDs across pages, and which>
DRIFT:             NONE | <items that appeared, vanished, or moved position mid-enumeration>
BOUNDARY WITNESS:  <the first out-of-horizon item observed, proving the bound was reached;
                    or NONE + why — not counted in ENUMERATED>
EXPECTED AT BOUND: <count the horizon implies, or UNKNOWN + why>
REACHED HORIZON:   YES | NO — <if NO, the last item reached and what stopped it>
BEYOND HORIZON:    explicitly unsearched
FILTER:            NOT FIRED — full read, N items | FIRED — limit, owner, usage
                    per references/relevance.md
FILTER INPUT:      TITLE+DESCRIPTION | TITLE+METADATA-ONLY (stage A only) |
                    DESCRIPTIONS FETCHED (N of M) — see references/relevance.md
STAGE_B_BUDGET:    <items the run was willing to fetch descriptions for, declared BEFORE
                    stage B ran — a budget set afterward is a result, not a budget>
STAGE_B_ROUTE:     <how a description was obtained, per item; or NONE AVAILABLE>
STAGE_B_ATTEMPTS:  <the stage-A-ordered item IDs actually attempted, and each outcome —
                    FETCHED | FAILED + error | NOT REACHED>
STAGE_B_STOP:      <budget exhausted | route failed | horizon complete>
DISPOSITION:       <deep-read N | skipped N | partial N — must sum to UNIQUE ITEMS>
```

**Why stage B needs its own accounting.** Two surfaces can both report "stage A then stage B"
and inspect completely different subsets — one fetching thirty descriptions cheaply, the other
managing four before a rate limit — and without the attempt list those two reports look
equivalent. Recording the ordered IDs attempted is what makes the difference inspectable
rather than narrated.

**Never shrink the horizon retroactively.** If stage B runs out of budget, that is
`ITEM: PARTIAL` on the unreached items, not a smaller collection. Re-declaring the bound
afterward converts an incomplete run into an apparently complete one, which is the same
false-completeness this receipt exists to prevent — arrived at through arithmetic instead of
through silence.

**`MATERIALIZATION` is what makes `DRIFT: NONE` mean anything.** Under `STITCHED-REQUESTS` —
offset or cursor pages assembled across separate calls — drift is possible and `NONE` is at
best an observation. Under `SINGLE-SNAPSHOT` — the whole list read once from a page that was
already fully loaded, so nothing was assembled across calls — drift is *structurally*
impossible and `NONE` is a proof. Under `OPERATOR-SUPPLIED-LIST` the set is fixed by
definition. Only the first and third license `DRIFT: NONE` as a positive claim; under
stitching, say what you checked. Without this field the two cases are indistinguishable in
the receipt, and the weaker one gets read as the stronger.

**`ITEM IDENTIFIER` exists because a list of titles is not an enumeration.** Titles are not
unique, not stable, and cannot be deduplicated reliably; two items in a weekly series often
differ only by a date. Capture a stable ID per item — the surface almost always has one, even
when its text layer does not expose it and it has to be read out of the page structure. Then
cross-check that the ID ordering and the title ordering agree. That cross-check is what turns
two independent readings of the page into evidence, and it is cheap.

**Why `UNIQUE ITEMS` is separate from `ENUMERATED`.** Offset pagination over a list that is
still receiving new items double-counts. Asking for the last 40: page one returns items 40
through 21; one new item arrives; page two, requested by offset, returns 21 through 2. Forty
rows came back, thirty-nine distinct items exist among them, and item 1 was never seen — yet
a receipt counting rows says forty and reads as complete. The count that means anything is
distinct IDs, and the anchor plus the cursor sequence is what lets a reader check it.

**Unresolved drift forces `REACHED HORIZON: NO`.** If items moved and you cannot account for
what that displaced, the enumeration did not demonstrably cover the range, whatever the counts
say. Prefer cursor or ID-based pagination over offsets wherever the surface offers it; offsets
over a live list are the case this whole field set exists for.

**The boundary witness is the positive evidence.** Reaching the end of a bounded range is
proved by seeing the first item *past* it — the June 30 item under a "since July 1" horizon.
That observation is evidence, not coverage, so it is recorded on its own line and deliberately
excluded from `ENUMERATED` and from `DISPOSITION`. Where no witness is obtainable — the
collection simply ends, or the surface stops paginating — say so; `BOUNDARY WITNESS: NONE`
with a reason is honest, and silently implying a clean edge is not.

`REACHED HORIZON: NO` does not invalidate a run. It converts the run's coverage claim into a
partial one, which is the honest shape — pagination caps, rate limits, and dead pages are all
normal. What is not acceptable is a report that lists what it read without saying what it
never got to.

## YouTube

Most of a video's useful content is not in the video. Four places to look, in order of value
per token:

1. **Description** — repo lists, star counts, links, timestamped chapters. Cheapest and
   densest, and the easiest to miss if you only watch.
2. **Chapters** — a free outline; useful for deciding whether the transcript is worth pulling.
3. **Transcript** — where the gems are. Pull for every item on a full read, or for
   survivors where a filter legitimately fired.
4. **Names with no link** — resolve rather than skip. An unlinked mention is often the most
   interesting, because the presenter raised it unprompted rather than being paid to feature it.

Load the page with whatever browser automation exists and read its text; a plain fetch is fine
for articles and repo pages. The outcome you need is description plus transcript as text, not
a particular tool call. If a transcript will not load, note it in the report and continue —
never let one source stall a run.

Expect the transcript to be the most brittle step. Element names change, a scripted click can
report success without opening anything, and a stale selector looks identical to an absent
transcript. **Confirm the panel is open by observing content, not by the click returning
success** — and if a scripted click fails, a real one on the visible control often works.
When retrieval fails, distinguish *no transcript exists* from *I could not open it*; only the
first is a fact about the source.

## When a supported route is blocked by policy

A source type can be supported here and still be unreachable: a feed URL the host disallows
by `robots.txt`, an API that rejects unauthenticated reads, a page behind a login. That is
**not** the same as a dead source, and recording it as `PARTIAL` loses the distinction.

Record `BLOCKED_BY_POLICY`, naming the policy and the exact surface, and then say which
fallback route you took instead and whether it succeeded. The reason to separate this is that
`PARTIAL` invites a retry and this does not — the same request will be refused every time, so
what the report needs to carry forward is the *route that worked*, which is durable
operational knowledge. A blocked primary route with a working fallback is a complete result,
not a degraded one.

Auto-generated transcripts have no punctuation and mangle proper nouns; a repo name heard
as three words is normal. When a transcript names something you cannot resolve, check the
description before giving up, and record it as unresolved rather than guessing at a spelling.

## Social sources — out of scope

Login-walled, public mirrors dead, generic fetch blocked. The only reliable route is browser
automation on an already-signed-in session. Operator decision, 2026-07-30: not in scope.
Recorded so a future session does not re-litigate it. If reopened, prefer a curated list over
an algorithmic timeline, and treat every post as a *lead* — trace to the underlying repo or
writeup before any recommendation.
