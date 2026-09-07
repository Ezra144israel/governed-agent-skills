# Calibrating the relevance filter

This decides which items get opened when a source is a **set** — a roundup, a channel page,
a reading list, a repository of independently adoptable members — **and the budget gate
below has already established that reading all of them is not affordable.** That gate is
the first section of this file and it is not optional: everything after it describes how to
filter *once filtering is legitimate*, never whether to filter. Where the gate does not
open, none of it applies and the run reads everything.

When it does apply, it runs on title plus description alone, before any transcript is pulled.

## First: is the filter needed at all?

**The default is to read every item.** Triage is the exception and needs a budget that
exists before enumeration, not a feeling afterwards. A budget is admissible only with all
three of:

```
FILTER:  NOT FIRED — full read, N items
         FIRED — limit <run-scoped resource bound>
                 owner <OPERATOR | RUN, declared before enumeration>
                 usage <consumed against that limit>
```

Without a limit, a named owner, and recorded usage, the run **reads everything** or records
`RUN: PARTIAL`, enumerates the unread set by identifier, and makes no completeness claim.

**This is a weak gate and it is worth knowing why.** It sets no threshold, so a run can
still declare a collection unaffordable. What it changes is that the count, the budget, and
the decision are on the record where a reader can disagree with them.

These are video economics: a description is a few hundred bytes against a transcript's tens
of thousands. They invert on a repository of markdown, where a description is one
frontmatter line written to make a router fire and the body costs less than a transcript.
Filtering there is failure mode 1 one level down.

## First: does the filter have any input?

**Most collection surfaces do not carry descriptions.** A YouTube channel page lists titles,
durations, view counts, and ages — the description lives on the watch page, which *is* the
deep read. The same is true of most index pages and feeds. So the filter's stated input
frequently does not exist at the point the filter is supposed to run, and the rule below
means it cannot legally fire: with no description, nothing may be skipped, and a twenty-item
collection becomes twenty deep reads. A budget tool that cannot reduce the budget is not
doing its job.

Resolve it by splitting triage in two, and declare which mode you used:

**Stage A — order, never skip.** On whatever the collection surface gives you (title,
duration, view count, series position, age), rank items by how likely they are to carry
mechanism. Roundups, teardowns, postmortems, and long-form items rank high; a two-minute clip
with an announcement title ranks low. Stage A produces an *order*, not a verdict. It skips
nothing, because it has not seen enough to skip anything.

**Stage B — the real filter.** Walk stage A's order and fetch each item's description, which
is far cheaper than its transcript. Apply the worked cases below to title *plus* description.
Now a skip is legal — the gate opened and the filter has its input. Both are required: a
description makes a skip *informed*, and only the budget gate makes it *permitted*.

Items the budget never reaches in stage B are `ITEM: PARTIAL` — enumerated, not triaged —
never `SKIPPED_RELEVANCE`. The distinction is the whole point: `ITEM: PARTIAL` says nobody
looked, `SKIPPED_RELEVANCE` says someone looked and decided. Recording an unreached item as
skipped claims a judgment that was never made.

**The precedence rule, stated once so it is not inferred differently in two places.** A
description is required *only* to justify a `SKIPPED_RELEVANCE`. It is not required to
deep-read: a full read supersedes the filter entirely, because reading the item answers the
question the description was only ever a cheap proxy for. So, in order:

1. Description available → apply the worked cases below; skip or deep-read.
2. No description, budget available → deep-read. This is a legal outcome, not a fallback.
3. No description, no budget → `ITEM: PARTIAL`.
4. No description route exists at all on this surface → stage A only, every item
   `ITEM: PARTIAL`, and **no `SKIPPED_RELEVANCE` may be issued in the entire run.**

Skipping on a title alone appears at no point in that list.

What it exempts is a **direct item**: one video, one article, or one repository that is a
single artifact. A repository whose members are independently adoptable is a direct
collection; `references/sources.md` carries the adoption test.
That one is already relevant; they decided.

Handing over a *collection* is not the same exemption, and conflating the two is the reading
error worth pre-empting here. When the user says "go through this channel," they have decided
the channel is relevant. They have not decided that all forty uploads are, and they cannot
have, since deciding that is the work they delegated. So the members of a handed-over collection are still judged individually — item by item,
under a declared horizon. The exemption attaches to
the unit the user actually named, and nothing below it.

It has the worst failure asymmetry in the skill, so it is worth getting right.

**The asymmetry:** a false positive costs one deep read. A false negative means the run
concludes there was nothing useful, which is the exact false-absence failure this skill
exists to prevent. So when genuinely uncertain, read it. The filter is a budget tool, not a
quality judgment, and it should be biased toward inclusion at the margin.

## The question

Not "is this good?" and not "is this about my stack?" — both are unanswerable from a title.
The question is:

> **Could this plausibly contain a mechanism — a way of structuring a gate, review, test,
> contract, boundary, or process — that someone might transfer?**

A mechanism is transferable structure. News, opinion, and announcement are not, however
well delivered.

## Worked cases

The categories below are the ones that actually decide runs. Judge new items by analogy.

**Clearly relevant — deep read**
- "How we cut our review time by gating on X" — names a gate and a result.
- "Top 10 GitHub repos this week" — a roundup; the description alone usually carries the
  candidate list, and the transcript carries why each was chosen.
- "Postmortem: the outage that taught us to stop trusting Y" — a named failure with a cause,
  which is the single densest gem type.
- "Building a code review agent — architecture walkthrough" — structure, stated.

**Clearly irrelevant — skip, and log it**

Only when the *description* affirmatively establishes non-mechanistic content. A title alone
is never sufficient, because titles are written for clicks and the uncertainty rule above
governs.
- "OpenAI announces GPT-X" — description confirms announcement coverage only.
- "AI stocks are crashing" — description confirms market commentary.
- "5 mindset shifts that changed my business" — skip only if the description shows it is
  motivational framing. If the description is thin, this could be an operating-practice talk
  wearing a self-help title; read it.
- "Weekly AI news roundup" — skip only if the description confirms it recaps announcements.
  Some roundups carry repo lists and reasoning in the description; those are exactly the
  highest-yield items in a roundup.

**Invoked items — never filtered. Invoked collections — read in full, or triaged under a
budget.**

When the user hands over a single item — "deep dive this," "look at this repo," a pasted
video URL — the relevance filter does not apply at all. They already decided it was relevant,
and overriding that with a title heuristic is the worst possible false negative. Read it.

When they hand over a *collection* — a channel, a playlist, a reading list — the filter
applies to its members. Their decision covers the collection, not each thing inside it; the
whole reason a collection needs triage is that nobody, including them, has judged the members
yet. Say which of the two you are treating the URL as before you start, because a channel URL
looks like a handed-over source and behaves like a set, and getting it wrong silently either
burns the budget or skips the good items.

**Missing, inaccessible, or sparse description — deep read, or record partial**

The filter runs on title plus description. With no usable description it has no input, so it
must not fire. Either deep-read the item or record it as `PARTIAL` coverage with the reason.
Never `SKIPPED_RELEVANCE` — that would log a decision the filter was not equipped to make.

**Relevant by mechanism, not by headline — deep read**

The most valuable and most-missed category. Judge the *shape* of what is described, not the
domain it is described in.
- "How I organize my Notion for client work" — could be a genuine information-architecture
  or state-visibility mechanism wearing a productivity title.
- "Why our sales team stopped using dashboards" — a metric-honesty argument, transferable to
  any measurement decision.
- A talk about hiring that turns out to be about evaluation criteria and rubric design.

If the *structure* being described could apply outside its stated domain, that is relevant.
This category is why the filter runs on plausibility rather than keyword matching.

**Relevant to one target only — deep read, note the target**

With several grounding targets, an item may bear on one and not others. Read it, and record
per-target outcomes; mark untouched targets `NOT_EVALUATED`, never silently omit them.

**Ambiguous — deep read**

"Our engineering culture" or "a day in the life of a staff engineer" could be either. The
asymmetry decides it: read.

**Adversarial descriptions — deep read, then judge harshly**

Descriptions optimized for engagement will oversell. "This changes everything about testing"
usually delivers nothing, but occasionally delivers something. Cheap to check, and the
verdict belongs to the crosswalk, not the filter. The filter's job is triage, not judgment.

**Terminology mismatch — deep read**

An item using unfamiliar vocabulary for a familiar mechanism is exactly what scouting is
for. Unfamiliar words are not evidence of irrelevance; they are often evidence of a
different tradition solving the same problem, which is where the transferable insight lives.

**Series and recurring formats — sample, do not assume**

A weekly format that yielded three times is not guaranteed to yield again, and one that has
never yielded may pivot. Judge each item on what it actually shows.

## Every skip is logged

Log skipped items with title and reason as `SKIPPED_RELEVANCE`, and count them in the horizon
receipt's `DISPOSITION` line. Two reasons, both real:

**The filter must be auditable.** The report lists every skip with its title so the operator
can see how aggressive the filter was on this run. An unlogged skip is a decision nobody can
check — and the report is the only place it exists unless a deposit was authorized
(`references/deposit.md`).

**Coverage arithmetic has to close.** Deep-read plus skipped plus partial must account for
every unique item enumerated. A skip that goes unlogged does not merely hide one judgment; it
breaks the sum, and a coverage claim whose parts do not add up is the same false-completeness
shape as an unbounded horizon — a report that looks like it covered the collection because
nothing in it says otherwise.

## When the filter is wrong

If a collection turns out to be consistently mis-filtered within a run — uninformative
titles, good content — say so in the report and read the rest. That is a judgment about this
collection, not a durable rule (`references/deposit.md`).

If the operator flags something skipped that should not have been, that is calibration data
worth telling them is worth capturing — but capturing it is their decision and their edit.
The run does not modify this file.
