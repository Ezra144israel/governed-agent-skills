---
metadata_schema: team-hub-skill/v1
summary: Finds what a change could break beyond the diff and proves the one safety fact by running real code.
skill_id: blast-radius
version: 1.0.0
lifecycle_status: active
family: verification
capabilities: []
source_provenance:
  kind: adapted
  references:
  - https://github.com/cursor/plugins
  note: pstack/skills/blast-radius/SKILL.md @ 60c641e4, MIT (Lauren Tan), scouted 2026-08-19; localized grounding generalized for global eligibility.
authority_boundary: docs-only
eligibility: global
activation_triggers:
- trigger_id: change-risk-review
  task_kinds:
  - review
  - verification
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - build-review
  - repository
  description: a change's cross-module breakage risk is assessed before it ships
- trigger_id: small-diff-distrust
  task_kinds:
  - review
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - repository
  description: a small diff is reviewed without trust in its stated safety
activation_exclusions: []
full_load_required_when:
- change-risk-review
- small-diff-distrust
section_references: []
platforms:
- portable
surfaces:
- build-review
- repository
required_roles: []
required_lanes: []
related_doctrine: []
graph_edges: []
child_references: []
return_contributions: []
supersedes: []
---

# Blast radius

Find what a change breaks somewhere else, before it ships.

Listing the callers is not the job. You can grep those in a second. The job is the breakage grep won't show you.

## Don't trust your own writeup

A blast-radius writeup that sounds right is worthless. It reads as convincing whether
or not it is true, and that is the trap you are walking into. Don't hand back the
writeup. Find the one or two facts the whole thing depends on and prove them by
running code. Words are where you start, not what you ship.

## How sure are you

For each fact the change's safety depends on, get it as far down this list as is
cheap, and **say where it stopped**.

1. **You said so.** Worthless on its own.
2. **You pointed at the line.** A real `file:line`, or the library's own source.
3. **You showed the bad case can't happen.** You walked the failure step by step and it doesn't reach.
4. **You ran it.** A script or test that calls the real code and fails loud if you're wrong.
5. **You reproduced it in the running app.**

**Any safety fact you can't get to step 4, say so out loud. Don't write it up as
settled.** Step 4 is usually one small script that imports the same module the app
ships and calls the exact function you're worried about.

Where the project defines behavioral-evidence or done-standard gates, this ladder is
their general form: rung 4 is behavioral evidence, rung 5 is owner-demonstrated on
the real surface. The ladder's contribution is that it applies to **every** safety
fact, not only the ones a gate happens to cover, and that stopping at rung 2 becomes
visible instead of silent.

## Steps

1. **Read the change.** The diff, the symbols it adds, changes, and deletes, and what it now does differently, including the part the diff doesn't spell out.
2. **Find the one fact it is safe because of.** Most changes that look scary are safe because of a single fact, like "this call only drops already-dead cache entries and does nothing else". Find that fact. If it holds, most of the scary cases die at once. Spend your time here, not on a long list of maybes.
3. **Look where grep stops.** Read the source of the dependency you call, and check its pinned version and any local patch. Work out when things run: microtasks, unmount and teardown, server versus client. Follow what a symbol search misses: the JSON an API returns, a DB column, a wire format, a generated router, a feature flag, code three hops downstream.
4. **Be honest about each risk.** Give it a real chance of happening and a real cost if it does. Keep the risks you confirmed; list the ones you checked and cleared separately. Cite a real `file:line`. A search that finds nothing is still an answer. Never invent a caller or an API.
5. **Prove the one fact.** Write a script or test that runs the real code, run it, and paste what happened. If you can't prove it cheaply, mark it unproven. Don't round up.
6. **For a big or wide change, get a second seat.** Different reviewers catch different real bugs. Independence is a property of the seat: the reviewer must not have authored the artifact under review.

## Project grounding

Before step 3, check whether the project defines a high-risk file registry, an
authorization manifest, or equivalent stronger gates, and follow the stronger gate
when the file or behavior is covered. A change that passes local tests and review
but fails only in the deployed build (an unregistered server action is the classic
case) is exactly the breakage this skill exists to surface early.

## What to hand back

- **What it does.** What changed, including the part that isn't obvious.
- **The one fact it is safe because of.** State it, say which rung you got it to, and show the proof. If you couldn't prove it, write **unproven**.
- **Risks.** Only the real ones. Each names how it breaks, the `file:line`, how likely and how bad, and how to check.
- **Cleared.** What you checked and why it's fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including the script you wrote.

Cite real code, and strip anything private before it goes anywhere public.

**Reply:** the writeup above, with the one safety fact either proven or marked unproven.
