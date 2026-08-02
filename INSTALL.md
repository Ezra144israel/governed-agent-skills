# Installation & Usage

These skills are plain-markdown instruction packages (`SKILL.md` plus optional
reference files). They work on any agent surface that can read markdown
instructions; the install path differs per surface.

**Pick one tier per skill.** Install either the full version (e.g.
`governed-operator-full/`) or the universal-starter version — never both.
The starters are self-contained condensations of the full skills; installing
both causes duplicate or conflicting triggering.

**Rename on install.** The repo folders carry a `-full` suffix for clarity.
When installing, use the canonical name from each file's frontmatter as the
folder name: `governed-operator`, `reasoning-doctrine`,
`run-review-repair-loop`.

---

# Before you install: check for conflicts with your existing setup

These skills are opinionated. If your environment already carries
instructions — a `CLAUDE.md`, an `AGENTS.md`, custom rules, other installed
skills, project instructions — some of them may contradict what these skills
mandate (who may commit, when tests are written, how reviews conclude, when
the agent asks vs. proceeds). An undetected conflict shows up later as
confusing agent behavior, and it will look like the skills are broken when
the real problem is two rulebooks disagreeing.

Two minutes of checking prevents that:

1. **Claude Code users:** run `/doctor` first to confirm your installation
   and settings are healthy before adding anything.
2. **Everyone:** before installing, have your agent read the skill files
   against your existing configuration and report contradictions. A
   paste-ready prompt:

```
Read the SKILL.md files in <path to this repo> but do not install or apply
them yet. Then read my existing configuration: CLAUDE.md / AGENTS.md /
project instructions / rules files / currently installed skills. List every
place where these skills would contradict, duplicate, or override something
I already have — especially rules about committing and pushing, test
ordering, review and approval, when to ask me vs. proceed, and output
format. For each conflict, tell me which side you would obey and why. Do
not resolve anything; just report.
```

3. **Decide the precedence yourself.** For each conflict, either remove your
   old rule, adapt the skill text, or write one line in your top-level
   instructions naming which source wins. An explicit precedence line beats
   two silently competing rules every time.

If the report comes back empty, install with confidence. If it doesn't,
you've just saved yourself a debugging session that would have been blamed
on the wrong thing.

---

## Claude Code (CLI)

Skills live as folders on disk. Claude Code discovers them automatically —
no configuration or upload step.

Personal (all your projects):

```
mkdir -p ~/.claude/skills
cp -r governed-operator-full ~/.claude/skills/governed-operator
cp -r reasoning-doctrine-full ~/.claude/skills/reasoning-doctrine
cp -r run-review-repair-loop-full ~/.claude/skills/run-review-repair-loop
```

Per-project (checked into one repo, applies only there): use
`.claude/skills/` at the repo root instead of `~/.claude/skills/`.

Verify: start a session and ask "what skills do you have available?" — the
three names should appear. Reference files under `references/` load
automatically when their trigger fires; don't flatten them.

## Claude web / desktop (claude.ai)

Requires a paid plan (Pro, Max, Team, or Enterprise) with code execution /
file creation enabled.

1. Zip each skill folder individually, with `SKILL.md` at the top level of
   the folder inside the zip (e.g. `governed-operator/SKILL.md`).
2. Go to **Settings → Features** (naming varies slightly by plan; look for
   Skills under Features or Capabilities).
3. Upload each zip. Skills are per-user — each team member uploads their own
   copy.

Verify: in a new chat, ask Claude to list its available skills.

## Claude API

Upload each skill as a zip via the Skills API (`/v1/skills`) with the
`skills-2025-10-02` beta header, enable the code execution tool, and pass the
returned `skill_id` in the `container` parameter of your requests. API skills
are workspace-wide but separate from claude.ai uploads — the two surfaces do
not sync.

## Codex (OpenAI)

Codex discovers skills from `SKILL.md` folders, in priority order:

- Repo-level: `.agents/skills/` (working directory, parents, or repo root)
- User-level: `~/.agents/skills/`
- Admin-level: `/etc/codex/skills/`

```
mkdir -p ~/.agents/skills
cp -r governed-operator-full ~/.agents/skills/governed-operator
cp -r reasoning-doctrine-full ~/.agents/skills/reasoning-doctrine
cp -r run-review-repair-loop-full ~/.agents/skills/run-review-repair-loop
```

Invoke explicitly with `$governed-operator` (or the `/skills` command), or
let Codex select a skill implicitly when a task matches its description. You
can also reference the skills from your `AGENTS.md` (e.g. "load
`governed-operator` before any multi-agent or review work") so they activate
by default.

## ChatGPT (web) and assistants without native skill support

No native `SKILL.md` mechanism. Two workable routes:

1. **Project instructions (recommended):** create a Project, paste the
   universal-starter text (`governed-operator-universal-SKILL.md` and
   `reasoning-doctrine-universal-SKILL.md`) into the project's custom
   instructions. The starters exist for exactly this — they are sized for an
   instruction slot.
2. **Attached files:** attach the full `SKILL.md` files to the Project and
   add one instruction line: "Before any multi-step or review work, read and
   apply the attached governed-operator and reasoning-doctrine files."

There is no automatic triggering on these surfaces — tell the assistant when
to apply a skill, or bind it in the project instructions.

## Other agents (Cursor, VS Code agents, custom frameworks)

Anything that accepts a system prompt, rules file, or context file can run
these: paste the universal starters into the rules/system layer, or point the
agent at the full files at session start. The skills are plain instructions —
no runtime, no dependencies.

---

# Activation — making the skills load every session

Installing puts the files where the agent can find them. On most surfaces
the agent still decides *whether* to load a skill by matching your request
against its description. For a constitution and working method, you usually
want them applied on every substantive session, not just when the agent
guesses well. Wire that per surface:

## Claude Code — SessionStart hook

Add a SessionStart hook that injects a standing instruction at the start of
every session. Create the hook script:

```bash
#!/bin/bash
# ~/.claude/hooks/load-governance.sh
jq -n '{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Standing instruction: before any nontrivial task, load and apply the reasoning-doctrine skill. Before any multi-agent, review, dispatch, or repo-mutating work, also load and apply the governed-operator skill. State which of the two are applied in the first line of your first substantive response."
  }
}'
```

Register it in `~/.claude/settings.json` (all projects) or
`.claude/settings.json` (one project):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/load-governance.sh"
          }
        ]
      }
    ]
  }
}
```

Make the script executable (`chmod +x ~/.claude/hooks/load-governance.sh`).
A lighter-weight alternative is putting the same standing instruction in
your `CLAUDE.md`, which is read every session — the hook is more reliable
because it survives memory-file edits and fires on resume and compaction too.

## Codex — AGENTS.md standing instruction

Codex reads `AGENTS.md` every session (`~/.codex/AGENTS.md` globally, or the
repo's `AGENTS.md`). Add the same standing instruction there:

```
Before any nontrivial task, load and apply $reasoning-doctrine.
Before any multi-agent, review, or repo-mutating work, also load and
apply $governed-operator. State which are applied in your first line.
```

## Claude web / desktop — Project instructions

Skills uploaded to claude.ai activate by description matching. To make them
deterministic, create a Project and put the standing instruction in the
project's custom instructions (same text as above, minus the `$` syntax).
Every chat in that project then starts under the rule.

## ChatGPT — Project instructions

Same pattern: the standing instruction lives in the Project's custom
instructions and binds every conversation in the project. Since there is no
skill registry, the instruction should point at the attached files or
pasted starter text explicitly.

## The load receipt (all surfaces)

Note the last line of each instruction above: the agent states which skills
it applied, in the first line of its first real response. That one line is
what makes activation verifiable instead of assumed — if the receipt is
missing or wrong, the wiring broke and you know immediately, before any
work was done under the wrong rules. Cheap, and worth keeping.

---

# Using the skills

## What each one is for

- **governed-operator** — the constitution. Defines four seats
  (Orchestrator, Pressure-Tester, Builder, Reviewer), five non-negotiable
  gates (ground before drafting; converge before building; dispatch a full
  outcome contract; independent final-state review; done = owner-verified),
  role integrity (whoever assembled it doesn't approve it), commit posture
  (workers never commit or push), and outcome-autonomy rules that keep
  governance from strangling throughput. Load it for any work that touches a
  repo, produces an artifact someone else consumes, or involves more than
  one agent.
- **reasoning-doctrine** — the working method for a single agent. A
  five-stage loop (frame, ground, converge, execute, verify), anti-drift
  re-anchoring, an effort dial so small tasks stay small, and honesty
  mechanics (mark every claim verified / inferred / unknown; never present a
  guess in a confident register). Load it for any nontrivial task, with or
  without the constitution.
- **run-review-repair-loop** — bounded self-review before handoff. The agent
  reviews its own diff, scores six categories 1–5 (overall = lowest score,
  never an average), repairs concrete findings, and repeats up to an
  iteration limit. The final score is evidence-backed self-assessment,
  explicitly not independent approval. Load it when an agent finishes a code
  change and before a second agent (or you) reviews it.

## Recommended load order

Constitution first, method second, review loop when there's a change to
review. Solo user with one assistant? Start with just
`reasoning-doctrine` — it stands alone. Add `governed-operator` when you
have two or more agents, or when you want seat separation between building
and approving. Add `run-review-repair-loop` when agents produce code.

## Things to know

- **Skills are instructions, not enforcement.** They shape behavior; they
  don't technically prevent an agent from committing or approving. Pair them
  with real permissions (branch protection, read-only tokens) for anything
  that matters.
- **Progressive loading is intentional.** `reasoning-doctrine`'s
  `references/` files load only when their trigger fires (a failure, a
  delegation, a retry). Don't paste them all into context up front — the
  structure exists to protect the context budget.
- **Adapt the vocabulary, keep the mechanisms.** Seat names, verdict labels,
  and return formats are conventions. Rename freely. The load-bearing parts
  are the separations: author ≠ approver, builder ≠ certifier, claim ≠
  verified claim.
- **Repository doctrine slots in.** `run-review-repair-loop` tells the agent
  to discover and apply your repo's own standards (a doctrine or rules file)
  before inventing a generic checklist. If your repo has a CONTRIBUTING.md,
  rules file, or internal standards doc, the loop will pick it up — name it
  in the dispatch if discovery is unreliable on your surface.
- **Narrow the triggers to your workload.** The skill descriptions are
  deliberately broad (`reasoning-doctrine` offers to load on every
  nontrivial task). If you run a large skill inventory or a
  non-engineering workload, edit the `description:` frontmatter so it
  fires where you want it — e.g. "research, money decisions, and
  pre-publish checks" — instead of everywhere. Narrowing a trigger is
  use, not misuse; the mechanisms don't change, only when they load.
- **Model-agnostic.** These run on any capable model. They were developed
  and are used daily across multiple vendors' models simultaneously.
