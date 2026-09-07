# Failure modes

Twelve ways a scouting verdict goes wrong. Every one of these shipped at least once. Ten
share a single root: **absence inferred from a partial surface.** If you internalize only
one thing, make it that one. The last two are different animals and are marked as such.

These are stated as portable mechanics. The specific incidents behind them — with source
identity and evidence — are in `provenance.md`, read only when someone wants to check that
a lesson is real rather than plausible.

---

## 1. Reading the README instead of the code

READMEs describe intent. Code describes behavior. They diverge constantly, and the
divergence is always in the flattering direction.

Real cases from one afternoon: a repo advertised "LLM summaries" via an `ollama` extra —
`ollama` appeared zero times in the package. A repo's docs prescribed blind judging of
eval conditions while the harness wrote the condition label into every row in plaintext,
with no strip or shuffle path. A headline "93x token reduction" rested on a baseline that
summed every source file in the repo; the repo's own committed benchmark CSVs showed the
opposite result by 20x.

Read the entry point through to output, at the resolved pin, through whatever read-only
acquisition route the surface provides — never a clone, which `security.md` removes outright.
Do **not** run its tests, build, or any of its code; `security.md` forbids executing scouted
source, and reading is sufficient to catch this. When code and README disagree, say so; that
disagreement is itself a finding about the project's honesty.

## 2. "Not wired" mistaken for "not conceived"

The most expensive error available. A compact project summary or an architecture snapshot
shows what a system *is*, not what it has *designed*. Detailed design corpora — convergence
packets, doctrine, locked specs — routinely contain a mechanism in far more depth than the
external repo has it, while the implementation is still inert.

A crosswalk once flagged a code-intelligence graph as a gap. The internal design corpus
already specified the extraction stack, a four-state freshness model with fail-closed
semantics, per-edge provenance, a closed query vocabulary, and an allowlist — and had
already rendered a verdict on that exact class of external tool: *inspire, don't adopt.*

Ground in the design corpus before calling anything novel. "Absent from the summary" means
nothing.

## 3. Absence claimed from a capped or partial search

A search tool that silently returns zero for a capped scan is worse than no search tool,
because absence reads as proof.

One search connector reported a truncated scan of 23 files and returned zero matches for
filenames that provably existed. Four independent agents hit it. Effective coverage was
about 6% of the corpus, and every "not found" produced under it was worthless.

Verify your search surface is complete before any absence claim. When it isn't, say
`NOT_FOUND_IN_SEARCHED_SET` and name exactly what you searched. That token is not a gap
claim and must never be argued as one.

## 4. Absence claimed about a pipeline without tracing the invocation chain

A reader looked at a CI config, saw install → migrate → build, and concluded no quality
gates ran. It never opened the package manifest, where a lifecycle hook chained three
checks and a 330-file test battery ahead of the build. The published finding — "there is
no CI, at all" — was false and loud.

A pipeline claim requires the whole chain: config → invoked script → lifecycle hooks →
transitive scripts → framework defaults. One surface is never enough. Frameworks in
particular do work by default that no config file mentions.

## 5. Delegated reading treated as grounding

Subagents are the right tool for sweeping a large corpus, and their reports are *leads*,
not evidence. A load-bearing claim from a subagent gets re-verified at the named file
before it enters an artifact. Failure mode 4 above is exactly what happens when it doesn't:
a delegated conclusion went straight into a published document.

## 6. External evidence left unpinned

A "source-backed" comparison where half of each comparison is a mutable branch is not
reproducible. Pin every external repo to a resolved commit, and resolve that commit
*yourself* through the host — another agent's read of the same repo at a different moment,
or a SHA quoted in a README, is not proof of what you classified.

## 7. Running a scouted repo's installer

Installers from scouted repos have been observed appending to agent memory files and
writing hooks into settings directories. Read them; never run them. This version does not
clone at all — inspection is read-only through the host — which removes the opportunity
rather than governing it.

There is no sandbox exception. An earlier version of this file offered one and it
contradicted `security.md`, which prohibits executing scouted source outright. Reading is
sufficient to establish everything triage needs. If a question genuinely cannot be answered
without running the code, that is a finding to report — not a licence to run it.

## 8. Assuming a name collision is the same artifact

A skill set found in the wild looked identical to a plugin already installed under the same
name. Different authors, different skills, one overlapping name, entirely different
content. Check what is already installed and compare bodies, not names — both to
avoid redundant adoption and to avoid dismissing something genuinely new.

## 9. Compound or undeclared classifications

"Mostly token-A or token-B throughout" is not auditable. Nor
is a token that appears nowhere in the declared vocabulary. One declared token per
independently checkable mechanism — otherwise a reviewer cannot tell which claim rests on
which evidence, and neither can you.

## 10. Unattended runs that fail quietly

Written for scheduled operation, which this version does not do — kept because it applies
whenever a run's own coverage is partial, and because it is the trap any future scheduled
version will fall into first.

A run that hits three dead sources and surfaces two findings produces a report that looks
exactly like a healthy run with two findings. A cap that binds every week becomes a
permanent ceiling nobody chose. A source whose fetch silently broke reads as a channel that
stopped publishing anything worthwhile.

The cure is that absence must always be *stated*, never implied by omission: report what
failed, what was deferred and which cap bound it, and which sources returned nothing. Keep
those sections in the report even when they are empty, because "none this run" is
information and a missing section is ambiguous.

Note this is failure mode 3 wearing different clothes — absence inferred from a partial
surface, except here the partial surface is the run itself.

## 11. A gate placed after the work it gates

The first failure mode found by *running* this skill rather than reviewing it.

A version dropped local cloning and moved repository inspection to read-only host access.
Its capability probe ran first and passed — network, host pages, browser, transcripts, all
present. The run harvested a collection, triaged ten candidates, and reached the crosswalk
before discovering that the host blocked every fetch-level route to a commit SHA. Without a
resolved external pin the grounding predicate could not close, so no verdict was reachable
and the entire crosswalk was unissuable. The capability the verdict depended on was never in
the probe.

The probe is not a formality that lists what the surface has. It is a fail-closed gate, and
a gate is only a gate if it runs before the thing it protects. **Every capability a verdict
depends on belongs in the probe, checked end to end** — not "can I reach the host" but "can
I obtain the specific artifact the predicate requires."

**Then it happened again, in the fix.** The next version added pin resolution to the probe
and declared the mode closed. Two independent reviewers, approaching from opposite ends,
found that the new gate still checked only a third of what a verdict needs. Resolving a
commit SHA proves nothing about *reading a file at* that SHA — one surface resolved pins
cleanly while every commit-addressed file read cache-missed, leaving only mutable-branch
content that cannot be shown to be the pinned bytes. And the whole gate was about the
*external* half; the internal target's immutable identity and census route, which the same
predicate also requires, were never probed at all.

So the rule has teeth only when stated as a conjunction over **every** precondition, and the
preconditions are per-host, not global: a route that works for one host family says nothing
about another. Enumerate what the verdict needs, probe each one by actually obtaining it
once, and let any failure stop the run before the expensive stage. A gate that passes on one
of three preconditions is not a partial gate; it is a gate that does not work, wearing the
appearance of one.

Generalize past pinning. Any check that fails a run belongs at the point where failing costs
least. A check that runs late does not prevent wasted work; it only documents it.

## 12. A rejected mechanism reported as a missing one

Also from running rather than reviewing.

A crosswalk established, on a complete and directly-read census, that a project did not
implement automatic cross-provider fallback. True. The same corpus also carried an explicit
doctrine forbidding it, because automatic substitution destroys attribution. The absence was
a decision, not an oversight, and every formal condition for an absence claim was satisfied.

*Not implemented* and *deliberately rejected* look identical to a search and are opposite
findings. Recommending the second is worse than a false gap — a false gap wastes a read, while
this re-opens a settled question while appearing well-grounded, and buries the reasoning that
settled it. The reasoning is usually the most valuable thing in the crosswalk, because it
generalizes past the mechanism to the principle.

Cost of avoiding it: one extra question during a search you are already running. Not just
*"is it here"* but *"is there a record of deciding against it."* Rejections live in doctrine,
decision records, rejected proposals, and constraints that rule a shape out — the same places
you are already reading for the design corpus.

---

## The pattern behind them

Ten of the twelve are the same shape: a conclusion drawn from a surface that did not cover
the question. The cure is not more caution in general — it is one specific habit. Before
stating that something is absent, missing, novel, or unique, name the surface you searched
and ask whether that surface could have contained the thing. If it could not, you have not
found an absence. You have found the edge of your search.

Eleven and twelve are the odd ones out and worth keeping separate for that reason. Neither is
a bad conclusion from a bad surface. Eleven is a correct process run in the wrong order.
Twelve is a correct conclusion given the wrong meaning. All three cost a run; all three need
different cures.
