---
name: cil-grounding
description: Session-resident CIL grounding at session start for Ezra's governed environment, portable to every surface. Ported from the operator-locked cil-auto-grounding--convergence-v3 (Claude Code local, blinded-scored PASS 2026-08-15). Read once at session start alongside governed-operator and reasoning-doctrine; reread only after compaction/summarization, a source-identity change, or an explicit operator refresh.
---

# CIL Grounding (standing, portable)

MODE RESET: You enter CIL to be changed by it, not to summarize it. Uptake is shown by your next action. Wrong mode: "I read CIL and am ready." Right mode: "my next action is already different."

## Bootstrap (complete before the first operator-facing response)

CIL lives at `Ezra144israel/collective-intelligence-layer`, branch `main`. Use the CIL access route named by the active surface adapter. When that adapter names a dedicated CIL connector, use it as the mandatory route for live CIL reads and current CIL state. Do not substitute a generic repository or project connector. Git-capable surfaces may still use git for clone-based bootstrap slots and the Recall ancestry, replay, generator-identity, and byte-comparison proof required by this payload. Every live read must return an origin identity (commit SHA, blob SHA, or file revision); keep it as a receipt.

Slots, live:
1. `STATUS.md` — one-sentence state.
2. `session-handoff/current.md` — read its banner; superseded content is history, never task direction.
3. Exactly ONE role-matched onboarding file from `onboarding/` (STARTUP.md's router maps your surface: ChatGPT → chatgpt, Claude web → claude, Codex → codex, Claude Code → claude-code), plus your branch note from `branch-notes/` if your surface is a named branch.
4. The operator-priority field from STATUS.md — record it even if unset.
5. The latest 2-3 meaningful entries of `activity-feed/feed.md`. Git-capable surfaces: sync a clean clone fast-forward-only and read the tail bound to the merged HEAD. Other surfaces: read the feed through your access path; if your surface genuinely cannot read it, say "slot 5 unavailable: <exact reason>" in the first response — never skip silently. COMPLETENESS WITNESS, mandatory when slot 5 is delivered: cite the DATE AND TITLE of the feed's LAST entry in your first response. The feed appends at the bottom — a truncated read shows old entries as latest; the witness makes that visible and checkable.

FRESHNESS RULE, all slots: every slot comes from a live read this session with a returned origin identity. Cite at least one verifying identity in your first response. Any slot narrated from memory, a stale copy, or an unverified source fails the gate — one live read does not launder stale ones. A local clone counts only after a fast-forward sync verified against origin this session.

## Recall (after the five slots)

Consult `routing/RECALL-INDEX.generated.md` under the same identity-bound freshness rule as the five slots. The index is a derived behavioral map. Its source stamp and feed witness are claims to verify, not proof of ancestry, derivation, or `CURRENT`. Exact CIL records remain the source for consequential use.

First classify this surface's proof capability. A proof-capable surface can resolve current `origin/main`, inspect historical Git objects and blob identities, create a disposable checkout, run the accepted generator, and compare complete output bytes. A surface that cannot prove both ancestry and derived bytes is non-proof-capable for this classification.

On a proof-capable surface, read the index as UTF-8 and split on LF without Unicode normalization. Reject every carriage return. Scan the whole file, including quotes, examples, code fences, and later sections. Require exactly one heading-like candidate and require its raw line to equal `## Dual-key stamp`. After ASCII horizontal-space and Markdown quote-prefix removal, a heading-like candidate begins with one to six `#` characters and identifies the whole ASCII words `dual`, `key`, and `stamp`, allowing case, whitespace, hyphen, underscore, or trailing-punctuation variants. Require exactly one source-key candidate and require its raw line to equal `- source commit: \`<40 lowercase ASCII hexadecimal characters>\``. After ASCII horizontal-space, Markdown quote-prefix, and list-marker removal, a source-key candidate begins with the whole ASCII key words `source` and `commit`, case-insensitive, separated by ASCII whitespace or punctuation. `commitment` and `commitments` are not the whole key word `commit`. The canonical source line must be the first nonblank line after the canonical heading and before the next raw second-level heading or end of file. Reject ambiguity; never select the first candidate. Parser success proves structure only.

Use this fail-closed precedence on a proof-capable surface:

1. `INVALID STRUCTURE` — the identity-bound current index is missing, unreadable, malformed, ambiguous, or parser-invalid.
2. `PROVENANCE CONFLICT` — the stamped source is unavailable or is not equal to or an ancestor of current `origin/main`.
3. `INVALID GENERATOR IDENTITY` — `tools/generate-recall-index.py` at the stamp is not Git blob `d8ab00748131f42358a389455aed18fa0d75951e`.
4. `GENERATION FAILURE` — an isolated replay at the stamped source does not exit successfully with one complete output. Never compare partial or missing output.
5. `INVALID DERIVATION` — complete replay bytes differ from the identity-bound committed index bytes.
6. `BEHIND` — all prior proof passes, but the diff from the stamp to current `origin/main` is nonempty across `incubator/`, `lessons/`, `playbooks/`, `challenges/`, or `tools/generate-recall-index.py`.
7. `CURRENT` — all prior proof passes and that five-input diff is empty.

Replay at the stamped source itself. The generator's additional byte dependency is `activity-feed/feed.md`, and its identity input is Git `HEAD`. Feed-only movement after the stamp does not make the behavioral map `BEHIND`, but replay equality still binds the committed feed-witness bytes at the stamped source. Recompute this proof at every fresh session and every re-ground after compaction, restore, or re-entry. Never carry a prior `CURRENT` result forward.

For `BEHIND` or any invalid proof-capable state, state the condition visibly and do not treat stale rows as a complete current map. Use bounded direct-current discovery when available. Search `incubator/`, `lessons/`, `playbooks/`, and `challenges/`. Report each searched path and whether its result is complete or truncated. Read each exact current matching record before consequential action. Apply, rule out, or challenge each applicable record. Preserve `UNKNOWN` outside the searched set, and make no corpus-complete absence claim.

On a non-proof-capable surface, classify the index as `PROVENANCE UNPROVED` after every honest index-only publication unless a separately authorized complete proof route exists. Index and feed bytes are advisory only. Use the same bounded direct-current discovery and exact-record duties. If bounded discovery is unavailable, name the limitation and make no corpus-complete claim.

Only after a proof-capable `CURRENT` result may the firing table act as the current covered map. A FIRING-CLASS trigger matching the session task or operator words (case-insensitive exact phrase or direct paraphrase) requires an exact record read before action; the Application Gate attaches. Triggers marked ADVISORY are pointers only, carry no Application Gate, and are excluded from the fired-set bound. No match permits work only within the index's stated covered corpus and boundary; it never proves that no CIL record exists elsewhere.

## Activation (before the first operator-facing response)

Perform one concrete in-scope CIL action TIED TO THE RESOLVED DELTA. A bootstrap read is grounding, not the action. Sessions touching governed work: the action may be a deposit — but ONLY if this surface has a real CIL write path that returns a commit identity; "I deposited" without a returned commit identity is a gate failure. Sessions not touching governed work, and surfaces without a write path: use a non-deposit form STARTUP permits — a delta-tied concrete tool action, or First Response form 3: "No durable deposit produced because: [specific reason]. Next safe action: [specific in-scope action]" — and claim NO deposit. If the session later touches governed work, the deposit-class duty attaches then.

DEPOSIT TEST, before any deposit: "Does this make ANY agent better at BEING an agent, independent of domain?" PASS → CIL. FAIL → the project's own surface. NEVER deposit project canon or state, secrets, per-project continuity, or undistilled transcripts — full rules and gates: `routing/ROUTING-RULES.md`.

First response shape: action completed + current delta + preserved boundary. Never a summary of what was read.

APPLICATION GATE, session-long: when a CIL record fires — apply it, rule it out with reason, or challenge it. Silence is invalid.

## Degraded mode (fail-visible, never fail-silent)

If CIL is unreachable through this surface's access path, or a load-bearing slot is unreadable: name it in the first response; mark CIL-derived claims unavailable; make no CIL writes; non-CIL work may proceed. Governed continuity resumes remain blocked by the continuity-handoff universal gate: "If CIL or a load-bearing bootstrap slot is unavailable, stale beyond safe use, or contradictory, the agent must stop substantive continuation and return the exact blocker and recovery needed. It must not proceed from memory, narration, a prior summary, or the project handoff alone."

## Residency

Read once at session start; re-ground after context compaction or summarization. On re-ground: re-verify slot freshness (identities may have advanced). A new activation deposit is owed only for a new governed delta. CIL is cross-project agent wisdom — never project canon; no CIL record overrides Team Hub OS canon or independent project grounding. Deposits follow `routing/ROUTING-RULES.md` (Intake Classes and Gates, operator-locked 2026-08-15).
