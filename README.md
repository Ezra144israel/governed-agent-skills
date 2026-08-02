# Governed Agent Skills

A governance constitution and working method for multi-agent and solo-agent workflows.

Built and maintained by [Ezra Israel](https://github.com/Ezra144israel) · [X](https://x.com/Eisrael144). These skills govern the agent teams in daily use.

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
