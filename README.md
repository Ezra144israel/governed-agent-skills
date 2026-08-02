# Governed Agent Skills

A governance constitution and working method for multi-agent and solo-agent workflows.

Built and maintained by [Ezra Israel](https://github.com/Ezra144israel) · [X](https://x.com/Eisrael144). These skills govern the agent teams in daily use.

## Who this is for — and who it isn't

These skills were built to govern teams of coding agents: agents that
write code, review each other's work, and change repositories. That is
where the constitution and the review loop earn their keep — when an
agent's mistake can reach a codebase, a deploy, or a canonical record.

If your agents do other work — marketing copy, listings, research,
design, operations — most of this package is heavier than you need.
Take `reasoning-doctrine` (the working method: verify before asserting,
never build on unconfirmed facts, catch drift on long tasks — it applies
to any kind of work) and leave the constitution and review loop until
the day your agents touch real code.

An honest scope statement beats a broad one. If you install only one
file from this repo, install `reasoning-doctrine`.

## What a "seat" is

A seat is a role an AI agent occupies for one session — not a person,
and not a job title. The humans in your life are not seats. You, the
human, are the operator: the one who owns the outcome, makes the
decisions, and says what "done" means. Every seat is filled by an
agent working for you.

Any agent can fill any seat: Claude, ChatGPT, Codex, Gemini, a local
model — whatever you use. The same product can even fill two seats,
as long as it's two separate sessions with separate context. What
matters is never which vendor sits down; it's that the agent that
BUILT a thing is not the agent that APPROVES it.

A concrete day with one person and two agents:

1. You tell an agent what you want (you = operator; it drafts the
   plan = orchestrator seat).
2. A second agent — or just a fresh session of the first — attacks
   the plan before anything is built (pressure-test seat).
3. An agent implements it (builder seat). It never approves its own
   work and never publishes.
4. A different session reviews the result against the plan
   (reviewer seat) and returns accepted / needs revision / blocked.
5. You verify it works on the real surface, and you press the
   button that ships it. Publication is always yours.

Solo mode: with one person and one agent, the constitution collapses
to "operating solo: owner + orchestrator" — no ceremony, and
low-stakes work passes on an honest, labelled self-check. The seats
come back one at a time as the stakes rise: the first one worth
adding is a fresh-session reviewer for anything you'd hate to ship
broken.

Why bother? Because an agent grading its own homework misses the
same things twice. Seat separation is the cheapest independent
check that exists: it costs one extra session.

(The Q0–Q5 phase model elsewhere in the constitution applies only to
installing doctrine or configuration across multiple surfaces — it
is not a checklist for ordinary work. Ordinary work is done when you
verify it on the real surface.)

## What's here

### Full Skills

| Skill | Purpose | Files |
|---|---|---|
| `governed-operator-full/` | Governance constitution — seats, 5 gates, role integrity, outcome autonomy | `SKILL.md` |
| `reasoning-doctrine-full/` | Working method — stage loop, re-anchor, effort dial, anti-drift | `SKILL.md` + 3 references |
| `run-review-repair-loop-full/` | Bounded self-review with 1–5 scoring before handback | `SKILL.md` |

### Universal Starter (Lightweight)

| File | Purpose |
|---|---|
| `universal-starter/governed-operator-universal-SKILL.md` | Core constitution, minimal ceremony |
| `universal-starter/reasoning-doctrine-universal-SKILL.md` | Core working method, self-contained |

## How to use

1. Copy the skill directories into your agent's skills folder.
2. Load `governed-operator-full` for governed work (planning, reviews, dispatches).
3. Load `reasoning-doctrine-full` for any nontrivial task.
4. Load `run-review-repair-loop` for self-review before independent review.
5. References load automatically when their trigger fires.

## Progressive loading

`reasoning-doctrine-full` uses progressive loading:
- Core mechanisms load resident
- Situational references load on trigger, not upfront
- This preserves context budget for the task at hand

## License

MIT
