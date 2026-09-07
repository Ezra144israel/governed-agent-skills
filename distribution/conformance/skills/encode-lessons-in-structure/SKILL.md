---
metadata_schema: team-hub-skill/v1
summary: Encodes recurring corrections as tests, gates, or generated artifacts instead of repeated prose instructions.
skill_id: encode-lessons-in-structure
version: 1.0.0
lifecycle_status: active
family: code-quality
capabilities: []
source_provenance:
  kind: adapted
  references:
  - https://github.com/cursor/plugins
  note: pstack/skills/principle-encode-lessons-in-structure/SKILL.md @ 60c641e4, MIT (Lauren Tan), scouted 2026-08-19; rung examples generalized for global eligibility.
authority_boundary: docs-only
eligibility: global
activation_triggers:
- trigger_id: recurring-correction
  task_kinds:
  - implementation
  - refactor
  - review
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  - repository
  description: the same instruction or correction recurs and should become structure
activation_exclusions: []
full_load_required_when:
- recurring-correction
section_references: []
platforms:
- portable
surfaces:
- documentation
- repository
required_roles: []
required_lanes: []
related_doctrine: []
graph_edges: []
child_references: []
return_contributions: []
supersedes: []
---

# Encode lessons in structure

Encode recurring fixes in mechanisms instead of textual instructions. Every error,
operator correction, and unexpected outcome is a learning signal. Capture it, route
it, and close the loop.

**Why:** textual instructions are easy to miss. They require the reader to notice,
remember, and comply. Structural mechanisms enforce the rule without cooperation.

**The evidence this exists for.** On 2026-08-19 one seat wrote the same
malformed-field defect into a shared activity feed twice in a row — and the second
write was the correction entry for the first, reproducing the defect while
describing it. Two further facts make this structural rather than careless: the
write path returned byte-verified success on both malformed writes, because it
compares bytes and never schema; and the seat had read the correct prevention in
its own grounding pass minutes earlier. A documented defect does not become a
prevented defect. The warning lived in prose while the error lived in the call
shape.

## Pattern

When you catch yourself writing the same instruction a second time:

1. Ask: can this be a test, a build gate, a generated artifact, a schema field, or a script?
2. If yes, encode it. **Delete the instruction.**
3. If no, because it genuinely requires judgment, make the instruction more prominent and add an example of the failure mode.

## Pick the strongest rung

When more than one mechanism would work, choose the strongest the situation allows.
Agents copy whatever the surrounding code already does, so a weaker guard becomes the
next template.

Strongest first:

1. **A state that cannot be represented.** A type or schema where the wrong value does not compile.
2. **A test in the battery.** It fails before merge, on every run, for everyone.
3. **A build gate.** A check that fails the deployed build — an authorization-manifest or file-size ceiling check is this rung where the project defines one. It catches what the battery and review seats miss.
4. **A generated artifact with a fail-closed rule.** Generated from source, carrying a digest of the corpus it came from, refusing to answer when stale: "if stale or disagreeing, return BLOCKED". A generated skill router is the archetype; confirm one exists on your surface before citing it.
5. **A runtime check.** Fails at the point of use rather than at build.
6. **A canonical helper.** Correct by default, but only for callers who use it.
7. **Prose in a skill or doctrine file.** Weakest. This is where you started.

## Corollary

Don't paper over symptoms. If the fix is structural, **only** use the structural fix.
The instruction is the symptom.

## Feedback loop

- **Capture every correction.** When the operator intervenes or a gate fails, decide if it's a one-off or a pattern.
- **Route to the right layer.** One-off goes in the working record. Recurring fix goes to a skill, a test, or a gate. Systemic issue goes to doctrine, through convergence.
- **Close the loop.** Don't just record. Apply now or create a concrete named next action.

## Authority boundary

Encoding a rule is a change to shared state and inherits that change's gates. Adding
a test or a script is ordinary work. Adding a build gate, changing a generated
router's source, or amending doctrine is not: it needs its own authorization, and
promoted shared-knowledge records need operator approval rather than an agent
deposit.

## Anti-patterns

- Acknowledging without recording. "I'll keep that in mind" does not persist.
- Recording without routing. A note about a gate that should exist is wasted unless the gate gets built.
- Fixing without generalizing. Fixing one instance while the recurring pattern stays intact.
- **Writing the same rule into a third document instead of building the rung.** Three prose copies is not defense in depth. It is three places to drift.
