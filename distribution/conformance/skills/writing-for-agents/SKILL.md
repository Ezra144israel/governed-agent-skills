---
metadata_schema: team-hub-skill/v1
summary: Architecture of documents an agent consumes, covering pointers, load budgets, hierarchy, and completion criteria.
skill_id: writing-for-agents
version: 1.0.0
lifecycle_status: active
family: design
capabilities: []
source_provenance:
  kind: adapted
  references:
  - https://github.com/mattpocock/skills
  note: skills/productivity/writing-for-agents/SKILL.md @ 1bb95954, MIT, scouted 2026-08-19; local-surface notes generalized for global eligibility.
authority_boundary: docs-only
eligibility: global
activation_triggers:
- trigger_id: agent-document-design
  task_kinds:
  - copy
  - design
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  description: a skill, doctrine file, or pointer-reached document is created or edited
activation_exclusions: []
full_load_required_when:
- agent-document-design
section_references: []
platforms:
- portable
surfaces:
- documentation
required_roles: []
required_lanes: []
related_doctrine: []
graph_edges: []
child_references: []
return_contributions: []
supersedes: []
---

# Writing for agents

Reference for writing any document an agent consumes: a skill, an `AGENTS.md`, a doctrine file, a doc reached by a pointer. The packaging differs; the writing does not. The same levers make each one predictable, since the agent takes the same *process* every run rather than producing the same output.

## Context pointers

A **context pointer** is a reference held in the agent's context that names some out-of-context material and encodes the condition for reaching it. A skill's description is one. A line in `AGENTS.md` naming a doc is the same object. The pointer's *wording*, not its target, decides when the agent reaches the material, and how reliably. A must-have target behind a weakly worded pointer is a variance bug: sharpen the wording first, and inline the material only if sharpening fails.

A pointer does two jobs: state what the material is, and list the **branches** that should trigger reaching it. Every word of an always-loaded pointer costs on every turn, so it earns harder pruning than the body.

- **Front-load the leading word.** The pointer is where it does its triggering work.
- **One trigger per branch.** Synonyms renaming a single branch are one branch written twice.
- **Cut identity the body already carries.**

## The two loads

Every document and pointer you add spends one of two budgets.

- **Context load** is the cost of always-loaded material on the window: an `AGENTS.md` line, a skill description, anything sitting in context every turn, spending tokens and attention whether or not it fires.
- **Cognitive load** is the cost on the human: which documents exist and when to reach for each. The human is the index. Not a cost to minimise; it is the price of human agency. Spend it where human judgement matters, remove it where it does not.

Material reached only through a pointer escapes context load at the price of the pointer's own line. Material with no pointer at all rides entirely on cognitive load.

## Information hierarchy

A document is built from **steps** (ordered actions) and **reference** (definitions, rules, facts consulted on demand). The two mix freely. The core decision is where each piece sits on a ladder ranked by how immediately the agent needs it:

1. **In-file step.** The primary tier: what the agent does, in order.
2. **In-file reference.** Consulted on demand. Often a legitimately flat peer set, which is a fine arrangement, not a smell.
3. **Disclosed reference.** Pushed into a separate file behind a pointer, loaded only when the pointer fires.

Push too little down and the top bloats. Push too much and you hide material the agent needs. That tension is the whole decision.

**Progressive disclosure** is the move down the ladder so the top stays legible. Not primarily a token optimisation: it is how the hierarchy is protected. Branching is the cleanest test: inline what every branch needs, push behind a pointer what only some branches reach.

**Co-location** is the within-file companion. Where the ladder decides how far down a piece sits, co-location decides what sits beside it. Keep a concept's definition, rules, and caveats under one heading rather than scattered. The test: the document should read like documentation written for the agent.

**Sprawl** is the failure mode: a document simply too long, even when every line is live and unique. Attention thins across the excess. The cure is the ladder.

## Steps and completion criteria

Every step ends on a **completion criterion**, the condition telling the agent the work is done. Two properties make it a lever.

- **Clarity**: can the agent tell done from not-done? A vague bound invites **premature completion**, ending the step before it is genuinely done, with attention slipping to *being done*. The visible steps still ahead supply the pull; the criterion's clarity is the resistance. Sharpen the bound first. Only if it is irreducibly fuzzy *and* you observe the rush, split the sequence so later steps are out of view. Hiding only works across a real context boundary; an inline call leaves the later steps in context and clears nothing.
- **Demand**: how much it requires. "Every modified model accounted for" forces thorough work where "produce a change list" does not. Demand drives the digging latent in the wording, and it is not step-bound: "every rule applied" binds a body of flat reference just as "every step done" binds a sequence.

The strongest criteria are both checkable and exhaustive.

## Leading words

A **leading word** is a compact concept already living in the model's pretraining that the agent thinks with while running the document (*frontier*, *fog of war*, *tracer bullet*). Repeated as a token, never as a sentence, it accumulates a distributed definition and anchors a whole region of behaviour in the fewest tokens, by recruiting priors the model already holds. Coining your own works if you define it clearly, but a made-up word recruits no priors: you pay in definition tokens what a pretrained word gives free. Reach for an existing word first.

It anchors twice. In the body, execution: the agent reaches for the same behaviour every time the word appears. In a pointer, invocation: when the same word lives in your prompts, your docs, and your codebase, the agent links that shared language to the material and reaches it more reliably.

Hunt for passages that collapse into a single token. "Fast, deterministic, low-overhead" becomes *tight*. "A loop you believe in" becomes *red*, turning a fuzzy gate into a binary observable state.

**Negation** is the failure mode beside this lever. Steering by prohibition drags the forbidden behaviour into context and makes it *more* available, not less. The negation is a weak modifier the strongly-activated concept overruns, so the ban half-reads as an instruction. Prompt the **positive**: state the target behaviour so the banned one is never spoken.

## Pruning

- Keep each meaning in a **single source of truth**, so changing the behaviour is a one-place edit. Duplication costs maintenance and tokens, and inflates a meaning's prominence past its real rank.
- The **environment** is a source of truth too (package scripts, config, directory layout, `--help` output), and a document restating it is a **cache**: a copy of a lookup, earning its load only when the lookup is expensive. Cache what the agent cannot find by looking: the unwritten convention, the reason behind a choice, the gotcha no config confesses.
- Check every line for **relevance**. A line loses relevance by never bearing on the task, or by going stale as the world it describes changes. Without pruning the default fate is **sediment**: stale layers that settle because adding feels safe and removing feels risky.
- Hunt **no-ops** sentence by sentence: an instruction the model already obeys by default pays load to say nothing. The test is model-relative, not reader-relative, and two people disagreeing about a no-op disagree about the default. Settle it by running the document. When a sentence fails, delete the whole sentence rather than trimming words.

---

## Boundary: this skill versus prose-quality skills

They cover different axes of the same document and both apply to a `SKILL.md`.

- A **prose-quality skill** (where installed) owns AI tells, filler, hedging, and formatting. It applies to every prose surface including chat replies.
- **This skill owns document architecture**: what goes in the file at all, where it sits on the hierarchy, what the pointer says, how the completion criterion binds.

A document can be architecturally correct and read like a machine wrote it, or beautifully written and structurally unusable. Run both.

## Note: negation in governance corpora

The negation rule is in genuine tension with governed environments whose doctrine
carries many hard prohibitions, several of which exist because a positive phrasing
was tried and failed.

That tension is **not resolved here**. Treat the rule as a real finding worth
testing, not as licence to rewrite locked governance into positive phrasings. Where
a prohibition is a hard authority guardrail, it stays. Where a prohibition is
steering rather than gating, pairing it with the positive target is a cheap
improvement worth trying.

## Scouted records and delivery rules

_Salvaged from the retired `scouted-rules` holding pen; sources cited in parentheses._

- Order delivery so the sequence proves itself. Failing test first, fix on top:
  the reviewer watches it go red, then green. Each commit lands on its own and
  the sequence reads as an argument.
  (`principle-sequence-verifiable-units`)
- Offer an encoding before deleting a constraint comment. A comment saying "do
  not remove" is a rule with no enforcement. Convert it to a type, a test, or a
  gate, then delete the comment. (`no-comments`)
- Config is an override layer with inline defaults. A missing line falls back
  rather than breaking. (`setup-pstack`)
- Fence transcript reads to the active workspace. Do not glob across all
  project directories; that crosses workspace boundaries and reads private
  chats from unrelated projects.
  (`automate-me`, `reflect`, `show-me-your-work`)
- Build a picture up one part at a time. For anything with three or more moving
  parts, draw a short series where each diagram adds a single part, rather than
  one crowded diagram at the end. A single all-at-once diagram is a reference,
  not teaching. (`teach`)

## Routing mechanics

Where the environment provides a generated skill router with per-skill activation
metadata, those mechanics govern invocation and this skill governs the documents
behind them. Where no router exists, the frontmatter name and description are the
only router; write them as the context pointer they are.
