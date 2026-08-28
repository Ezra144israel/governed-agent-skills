---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea, working a design tree in rounds. Use when the user wants to stress-test their thinking, before a convergence packet, or on any 'grill' trigger phrase.
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Source: `mattpocock/skills` `skills/productivity/grilling/SKILL.md` @ `1bb95954ef0d06ba4d64a9c267fb75f57c614a1f`, MIT, scouted 2026-08-19. Tweaked for this system: three boundary sections added at the end, the delegation qualification co-located with the instruction it qualifies, and no change to the mechanism.

Prior scout of this repo: `incubator/SCOUT-2026-08-15-mattpocock-skills-summary-derived.md`, pinned at `8b78b531ab965735c5dc74f6f7a219e1e37326df`. The source moved between scouts and neither record cited the other. That record is SUMMARY-DERIVED; its claims are not re-verified here.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask *now* without guessing at answers you have not heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each question is formatted like this:

```
Q1 - <question title>: <question body, may be several paragraphs, including options>

-> <your recommended answer>
```

Each round of answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

Finding **facts** is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, repository, tools), get it yourself or dispatch a subagent; do not ask the user for anything you could look up. **One exception, and it is not optional: if the fact is itself a grounding read, do it first-person.** Delegation after grounding is sound. Delegation of grounding moves the state change into the wrong agent, and the seat that did it never runs its Application Gate. Facts come back from a subagent. Posture does not. Do not block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait; ask the rest of the frontier now. The **decisions** are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on the design until the user confirms you have reached a shared understanding.

---

## Boundary: rounds and the consolidated-pass rule

`reasoning-doctrine` FRAME requires **one consolidated clarification pass, never a dribble**. Grilling does not weaken that; it operationalizes it.

- Each round **is** the consolidated pass. Never trickle questions one at a time within a round.
- A new round is legitimate only when the previous answers **unlocked** questions that were genuinely unanswerable before. If a question could have been asked in the last round, asking it now is a dribble, and the failure was in computing the frontier.
- If the frontier is empty after one round, there is one round. Grilling does not mandate iteration; it mandates completeness.

## Boundary: the confirm gate

The rule "do not act until the user confirms" is scoped to **the design being agreed**. It is not a general permission gate and it does not override the per-act authority model in `governed-operator`, where lock, build, commit, push, merge, deploy, walk, and cleanup are held separately and none inherits from another.

Authorization and reversibility are two separate rules with two separate owners, and this skill states neither as a gate of its own.

Authorization is per-act. `governed-operator` holds lock, build, commit, push, merge, deploy, walk, and cleanup separately, and none inherits from another. An act proceeds when that act is authorized.

Reversibility is not a second permission test on an already-authorized act. In `governed-operator` it decides whether an in-scope method choice is `EXECUTOR_OWNED`, whether an unpredicted obstacle may be adapted around rather than escalated, and whether an action needs a `METHOD_LOCKED` basis; that skill also states that reversible continuation is not an operator gate.

What waits here is committing to a **design** the user has not agreed.

## Boundary: subagents for facts

Dispatching a subagent to fetch an environment fact is a **bulk read** and is sound.

It is not a licence to delegate grounding. CIL field evidence from 2026-08-18 carries the qualification: delegation after grounding is sound; delegation *of* grounding moves the state change into the wrong agent. Facts come back from a subagent. Posture does not. If a fact the frontier needs is itself a grounding read, do it first-person.
