<!-- Session skill router. Schema: skill-router/v1. Inject at session start. -->
# Skill router

> Fail closed: activate a skill only when a trigger below matches. Vetoes are
> absolute and outrank any trigger match. If this router is missing or stale,
> fall back to manual invoke. State which skills are applied in the first
> line of the first substantive response.

| Skill | Trigger | Vetoes |
|---|---|---|
| `reasoning-doctrine` | any nontrivial task: analysis, planning, implementation, debugging, document work, review, multi-stage work | trivial factual answer; simple formatting |
| `governed-operator` | work that touches shared state, spans agents or seats, or involves planning, architecture, code or config change, review, dispatch, or a canonical record | quick factual question; trivial one-off answer |
| `ship-it-or-fix-it` | the operator explicitly sets maximum assurance (G2) for the task, names this skill, or resumes a work unit already recorded at G2 | NEVER auto-activate on task class (security, auth, payments, migrations, production); if G2 seems warranted and the operator has not said so, ask once |
| `grilling` | the user asks to stress-test a plan, decision, or idea, uses a 'grill' trigger phrase, or a convergence packet is about to be assembled | none |
| `unslop` | prose is written or edited for any surface: reply, doc, handoff, convergence packet, `SKILL.md` body, PR description, commit message | none |

