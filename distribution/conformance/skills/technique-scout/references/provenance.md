# Provenance — where the failure modes came from

`failure-modes.md` states twelve lessons as portable mechanics with the identifying details
removed, so they read the same on any surface and do not anchor a scout toward one project's
vocabulary.

This file records the incidents behind them. Read it only to check that a lesson is real
rather than plausible — a skill full of invented cautionary tales would be worse than one
with none, and this is how that claim stays checkable.

All incidents are from a single session, 2026-07-30, in which two independent agents on
different model families produced partly-wrong reconnaissance on the same three external
repositories. Both were wrong in different directions, which is what made the failure modes
visible.

---

**FM1 — reading the README instead of the code.** Three cases in one afternoon. A repo
advertised "LLM summaries" via an `ollama` extra; `ollama` appeared zero times in the
package. A repo's `rubric.md` prescribed blind judging of eval conditions while
`run_evals.py:290-298` wrote the condition label into every row in plaintext with no strip
or shuffle path. A "93x token reduction" headline rested on `token_benchmark.py:30`, which
summed every source file in the repo as its baseline; the repo's own committed
`*token_efficiency*.csv` rows showed graph tokens *larger* than naive, often by 20x.

**FM2 — "not wired" mistaken for "not conceived."** A crosswalk flagged a code-intelligence
graph as a gap after reading a compact project summary and an architecture JSON. The
internal design packet — `TEAM-HUB-INDEXPORT-PROJECT-INTELLIGENCE-CONVERGENCE-PACKET.md`,
36 KB, unread at the time — already specified tree-sitter extraction, four-state freshness
with fail-closed semantics on `stale_hard`, per-edge `sourceRefs` and confidence, nine query
kinds, a never-index list, and template allowlisting. It also already carried the verdict on
that external tool class: *CodeGraph = wrap, Graphify = inspire not adopt.*

**FM3 — absence from a capped search.** A governed read connector reported
`files_scanned: 23, truncated: true` on every query and returned zero matches for
`FEDERATED-KNOWLEDGE-GRAPH-DIRECTION-LOCK` and `index-port`, both of which exist. Four
subagents reproduced it independently. Effective coverage was ~100 of 1,753 files.

**FM4 — pipeline absence without tracing the chain.** A delegated reader saw `amplify.yml`
run `npm ci` → `npm run db:migrate` → `npm run build` and concluded no build gates executed.
It never opened `operator-web/package.json:16`, where `prebuild` chains
`check-file-sizes.cjs && run-test-battery.cjs && check-authorization-manifest.cjs` — 330
enumerated test files — ahead of `next build`, which itself type-checks because
`next.config.ts` sets no `ignoreBuildErrors`. The published claim "There is no CI. At all."
was retracted in full.

**FM5 — delegated reading as grounding.** FM4 is the instance: a subagent conclusion entered
a published artifact without re-verification at the named file.

**FM6 — unpinned external evidence.** A crosswalk pinned the internal repo to a commit and
named three external repositories with no refs. The reviewer resolved them independently and
correctly noted that its reads were not proof of what the assembling seat had classified.
They matched — `90d760aa…`, `07684c4a…`, `2ab95809…` — but only because they were checked.

**FM7 — scouted installers.** `code-review-graph`'s `cli.py:156-162` appends to `CLAUDE.md`,
and `cli.py:381` writes hooks into `.{platform}/settings.json`. Its MCP server also exposes
`apply_refactor_tool` (`main.py:723` → `tools/refactor_tools.py:167`), a source-mutating tool
co-located with a read-only intelligence surface.

**FM8 — name collision.** An `engineering` skill set from `mattpocock/skills` was assumed to
be the `engineering` plugin already installed. Different author (Anthropic, v1.2.0),
different skills; only `code-review` shared a name, with unrelated bodies.

**FM9 — compound classifications.** A crosswalk assigned "`TARGET_LOCKED` or
`DOCUMENTED_ACTIVE_GUIDANCE` throughout" to eight aggregated mechanisms in one row, and used
two tokens (`CONFIRMED ABSENT`, `USEFUL_VERIFICATION_PATTERN`) absent from its own declared
vocabulary. A reviewer could not tell which claim rested on which evidence.

**FM10 — quiet unattended failure.** Not from that session — identified during design review
of this skill by an independent pressure-tester, who observed that a run hitting three dead
sources and surfacing two findings is indistinguishable from a healthy run with two findings,
and that a cap binding every week silently becomes a ceiling nobody chose.

**FM11 — a gate after the work it gates.** From pilot 01, 2026-07-30 — the first run of this
skill against a live source. Draft v10's capability probe passed on network, host pages,
browser, and transcripts. The run then enumerated a 108-video channel under a declared
horizon, triaged ten repositories, and reached the crosswalk before finding that
`github.com/OWNER/REPO/commits/…` and `/tree/…` return `ROBOTS_DISALLOWED` and
`api.github.com` returns `403`. With no fetch-level route to a commit SHA, no external pin
resolved, so clause 2 of the `COMPLETE` predicate could not close and no row in the crosswalk
could reach `CONFIRMED_ABSENT`. Browser automation *could* resolve it — three pins were
recovered by reading the commits-page DOM — but nothing in the probe had checked for that.

**FM12 — a rejected mechanism reported as a missing one.** Also pilot 01. A crosswalk row for
"automatic multi-tier provider fallback" reached a `COMPLETE`, correctly-matched,
directly-read receipt: the mechanism was genuinely not implemented, verified across 114 files
and 264 hit lines plus live code, where `fallback_or_reroute_status`, `actual_responder_id`,
and `routing_target_id` returned zero hits. All seven admission conditions then in force were
satisfied, so `CONFIRMED_ABSENT` — and a keep recommendation — was formally available. The
same corpus also contained an explicit doctrine forbidding the mechanism: reroute is
*offered* and operator-approved, *"Fallback is never identity substitution"*, *"no fallback
lane replaces ChatGPT automatically"*, *"no tertiary silent reroute is allowed."* The absence
was a decision. Recommending it would have re-opened a settled question while looking
well-grounded, and the doctrine's reason — automatic substitution destroys attribution — was
the most transferable thing the crosswalk found.

---

## Pilot 01 — the first behavioral evidence

Everything in FM1-FM10 came from reconnaissance sessions or from reviewing this skill's own
text. FM11, FM12, and the entries below are the first findings produced by the skill *running*.

**What this pilot is and is not.** It ran draft v10 for harvest and triage; its findings were
folded through v11 and v12. It is therefore evidence that running the skill finds defects that
reviewing it does not — and it is **not** a conformance run for any later version. Its
receipts predate fields those versions added, so nothing here demonstrates that a current
receipt can be emitted exactly as specified. An independent reviewer raised this and was
right; a conformance pilot is a separate, still-outstanding piece of work.

Source identities for the run: the collection was `youtube.com/@full_stackYT`; the deep-read
item was `youtube.com/watch?v=N8hJ7buRTMY` (25:58, published 2026-07-28); the internal target
was pinned at `63ddb436cd3a8a30bfd9ac45b3bf3956b19b422c`, clean tree, 1753 tracked files under
`docs/`. External pins were self-resolved by browser DOM read of each repository's commits
page.

**Source figures repeated without verification.** A roundup video published two days before
the run ranked ten repositories by star count. Four of the ten headline figures were
falsified by read-only inspection of the repositories themselves: 8.8K claimed against 28
actual, 22K against 2.7K, 30K against 16.4K, and 26K "plus 6,000 this week" against 16K.
Stars accumulate, so a claim *below* the current count proves nothing either way — but a
claim *above* it cannot be explained by growth. The source ordered its ranking by those
figures, so the ranking itself does not survive correction.

This is the concrete case behind the completion predicate in `SKILL.md`: a run that had
stopped at the video would have reported ten candidates with star counts, four of them
false, in a document that looked complete. The candidate is a pointer; the artifact is the
evidence.

**A verdict recovered without a clone.** The same run re-established, from the repository's
own README on the host, that a code-intelligence MCP server exposes `apply_refactor_tool`
alongside 28 read-only tools — a finding originally made in a prior session by reading
`main.py:723` → `tools/refactor_tools.py:167` in a local checkout. Read-only inspection
reproduced a real kill criterion at source. That is evidence for the v10 reduction, recorded
alongside FM11, which is evidence against part of it.

---

## Why the unattended apparatus was withdrawn

`SKILL.md` and `MANIFEST.md` both say independent review established that the cross-run
apparatus — ledger, scheduling, source ranking — cannot be specified safely in prose. This
is the basis for that claim, recorded here so it is checkable rather than asserted.

Drafts v5 through v9 of this skill each went to an independent pressure-test seat — one that
did not assemble the draft it reviewed — and every round returned `FAIL` with blocking
findings. Across those rounds the apparatus attracted findings of a consistent kind: an
append-only ledger specified in prose has no crash-recovery or replay-identity semantics, so
a run interrupted mid-append is indistinguishable from one that never ran; item-level dedupe
across providers needs a stable identity function that prose can describe but not enforce;
and source ranking by yield needs persisted history the same ledger was supposed to hold.
Two helper scripts written to close those gaps were themselves withdrawn after one was found
to cache clones by basename — returning a different repository's contents under a requested
name — and to follow a repo-controlled symlink out of its clone.

The conclusion drawn was not that the apparatus is a bad idea. It is that it is code with
fixtures and crash tests, not prose, and it belongs to its own qualification track. What
shipped is the invoked-mode subset, which needs none of it.

Three limits on this record, stated because the alternative is a provenance file that
overstates its own rigor.

**The reviews are narrated here, not anchored.** The returns were delivered conversationally
and no immutable identity — digest, location, timestamp — was retained for any of them. An
auditor cannot resolve them from this file and should not treat the summary above as
verifiable. FM1-FM10 are anchored to a `file:line` you can check, and FM11, FM12, and the pilot
entries name the exact URLs, error codes, and pins involved; this section names nothing
resolvable, and the difference is deliberate rather than accidental. If this skill is ever
governed for real, the fix is to record each return's identity at the moment it arrives, which
costs nothing then and is unrecoverable afterward.

**The reviews were of a specification, not a running implementation.** This was the largest
gap in the record and it is now partly closed: pilot 01 (below) produced seven defects from
one live run, none of which five rounds of specification review had found. The reviews and
the pilot find different things, and neither substitutes for the other.

**The reviewers were independent of the assembling seat, not of each other.** Each round's
findings were folded in before the next round saw the artifact, so the sequence is serial
review, not independent replication.
