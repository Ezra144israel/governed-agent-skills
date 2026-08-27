# governed-agent-skills

**Your agent isn't careless. It's grading its own homework.**

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![plugin](https://img.shields.io/badge/plugin-governed%40ezra--governed-blueviolet.svg)](#install-as-a-claude-code-plugin)
![version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![skills](https://img.shields.io/badge/skills-6-blue.svg)
![patterns](https://img.shields.io/badge/patterns-1-orange.svg)

Give your AI coding agents a constitution, a working method, an implementation
lens, planning discipline, test evidence standards, a maximum-assurance
convergence cycle, and an enforcement hook that blocks catastrophic shell
commands before they run. The agent that builds a thing is never the agent
that approves it.

![The governed loop](assets/how-it-works.svg)

Full picture, including when each skill loads: [docs/how-it-works.html](docs/how-it-works.html).

Built and maintained by [Ezra Israel](https://github.com/Ezra144israel) · [X](https://x.com/Eisrael144).

## Who this is for, and who it isn't

These skills were built to govern teams of coding agents: agents that
write code, review each other's work, and change repositories. That is
where the constitution and independent review earn their keep, when an
agent's mistake can reach a codebase, a deploy, or a canonical record.

If your agents do other work, such as marketing copy, listings, research,
design, or operations, most of this package is heavier than you need.
Take `reasoning-doctrine` (the working method: verify before asserting,
never build on unconfirmed facts, catch drift on long tasks; it applies
to any kind of work) and leave the constitution until
the day your agents touch real code.

An honest scope statement beats a broad one. If you install only one
skill from this repo, install `reasoning-doctrine`.

## What a "seat" is

A seat is a role an AI agent occupies for one session. It is not a person,
and not a job title. The humans in your life are not seats. You, the
human, are the operator: the one who owns the outcome, makes the
decisions, and says what "done" means. Every seat is filled by an
agent working for you.

Any agent can fill any seat: Claude, ChatGPT, Codex, Gemini, a local
model, whatever you use. The same product can even fill two seats,
as long as it's two separate sessions with separate context. What
matters is never which vendor sits down; it's that the agent that
BUILT a thing is not the agent that APPROVES it.

A concrete day with one person and two agents:

1. You tell an agent what you want (you = operator; it drafts the
   plan = orchestrator seat).
2. A second agent, or just a fresh session of the first, attacks
   the plan before anything is built (pressure-test seat).
3. An agent implements it (builder seat). It never approves its own
   work and never publishes.
4. A different session reviews the result against the plan
   (reviewer seat) and returns accepted / needs revision / blocked.
5. You verify it works on the real surface, and you press the
   button that ships it. Publication is always yours.

Solo mode: with one person and one agent, the constitution collapses
to "operating solo: owner + orchestrator", with no ceremony, and
low-stakes work passes on an honest, labelled self-check. The seats
come back one at a time as the stakes rise: the first one worth
adding is a fresh-session reviewer for anything you'd hate to ship
broken.

Why bother? Because an agent grading its own homework misses the
same things twice. Seat separation is the cheapest independent
check that exists: it costs one extra session.

## What's here

| Skill | What it does | Files |
|---|---|---|
| `skills/reasoning-doctrine/` | Stops drift. Frame, ground, converge, execute, verify. Every task. | `SKILL.md` + 4 references |
| `skills/governed-operator/` | The constitution. Seats, gates, and one rule above all: the builder never approves its own work. | `SKILL.md` |
| `skills/write-maintainable-code/` | The smallest change that truly does the job. Nothing speculative survives. | `SKILL.md` |
| `skills/portable-adaptive-planning/` | A plan is not permission. FINAL, then GO, and nothing runs without both. | `SKILL.md` + 1 reference |
| `skills/test-verification/` | Tests prove behavior, not internals. Green is not proof. | `SKILL.md` + 1 reference |
| `skills/ship-it-or-fix-it/` | On your say-so only. The acceptance oracle freezes before the code exists. | `SKILL.md` |

### Supported installation units

Skills install individually, with two exceptions that have required
companions:

- `reasoning-doctrine`, `write-maintainable-code`, `test-verification`, and
  `portable-adaptive-planning` each work alone;
- `governed-operator` requires `reasoning-doctrine`;
- `ship-it-or-fix-it` requires `governed-operator`, `reasoning-doctrine`, and
  `test-verification`;
- the full six-skill package.

### Patterns (enforcement)

Not skills. These are working code you install and wire, for the jobs
instructions cannot do.

| Pattern | Purpose |
|---|---|
| [`destructive-command-guard/`](destructive-command-guard/) | Pre-execution hook that denies catastrophic shell commands before your agent runs them. Works on Claude Code, Codex, and Antigravity from one file: it detects each surface's payload shape and answers in that surface's deny format. Python, no dependencies, with a regression suite and a built-in sentinel for proving it's live. |

## How to use

Two modes. Both work; pick per surface.

1. **Manual invoke** (default, zero setup): copy the skill directories into
   your agent's skills folder and invoke by name, or let the agent match on
   the skill descriptions. See [INSTALL.md](INSTALL.md).
2. **Progressive loading** (optional): route skills conditionally at session
   start with a small router and an `AGENTS.md` shim, so each skill loads
   only when its trigger fires. See [activation/](activation/) for example
   files; nothing activates by cloning this repo.

Recommended load order: `reasoning-doctrine` on any nontrivial task; add
`governed-operator` (it requires the method) before governed work; the
implementation lens after the outcome, acceptance evidence, scope, and
authority are fixed; independent review after the change.
`ship-it-or-fix-it` loads only on your explicit maximum-assurance
decision, never on task class alone.

## Install as a Claude Code plugin

```
/plugin marketplace add Ezra144israel/governed-agent-skills
/plugin install governed@ezra-governed
```

Skills load namespaced (e.g. `/governed:reasoning-doctrine`). Manual
installation, copying `skills/*` into `~/.claude/skills/`, works exactly
the same; see [INSTALL.md](INSTALL.md).

## Install in other agents

This repo also ships an [Agent Plugins](https://agent-plugins.org) manifest.
Route status is updated as surfaces are run in practice, not on
documentation:

- **Claude Code** (plugin route): verified in practice for v2.
- **GitHub Copilot CLI** (direct repo install): verified in practice on v1.x;
  not yet re-run on v2. Current CLI builds mark direct repo installs as
  deprecated; a marketplace-based route may be required in future versions.
- **VS Code** (Agent Plugins install): plugin installs and its skills list
  correctly on v1.x; chat-side invocation could not be attributed to the
  plugin. Not yet re-run on v2.
- **Codex / ChatGPT desktop, Cursor**: documented by their vendors, not yet
  run by the maintainer.
- **Manual copy** (folders under `skills/` into your agent's skills
  directory): verified in practice on Kimi, Grok, and Antigravity on v1.x;
  not yet re-run on v2.

Confirmations and failure reports on any route are welcome.

A note on what "verified" covers: skills are invoked when a request matches
their description; they are not command-level enforcement. For hard blocking
of destructive commands, see
[destructive-command-guard/](destructive-command-guard/).

**GitHub Copilot CLI:**

```
copilot plugin install Ezra144israel/governed-agent-skills
```

**VS Code (Copilot):** enable the `chat.plugins.enabled` setting, then Command
Palette → "Chat: Install Plugin From Source" → paste this repo's URL. (Preview
feature; may be disabled by your organization.)

**Cursor CLI:** run `agent`, then `/plugin`, paste this repo's URL, choose scope.

**Codex / ChatGPT desktop:**

```
codex plugin marketplace add Ezra144israel/governed-agent-skills
```

then `/plugins` → source "ezra-governed" → install "governed" → start a new
session.

**Cursor desktop and ChatGPT web:** not yet directly installable, because
these require marketplace/directory listing. Until then, manual install works
everywhere: copy any folder under `skills/` into your agent's skills
directory, respecting the installation units above.

## Credits

The writing standards applied while editing this package draw on skills by
other authors that are deliberately not republished here: `grilling` from
[mattpocock/skills](https://github.com/mattpocock/skills) (MIT) and `unslop`
from [cursor/plugins](https://github.com/cursor/plugins) (MIT, Lauren Tan).
Install those from their own repos.

## License

MIT
