# governed-agent-skills — latest handoff (Team Hub Memory light)

**2026-08-15 · drafted by claude-code (rollout slice) · first light-profile record**

## Current state
Branch `main`, tracking `origin/main`; clean at last commit — the only uncommitted files are this rollout's memory scaffolding (`AGENTS.md`, `CLAUDE.md`, `.claude/`, `memory/`), pending operator commit. Last commit `4ac7829` (2026-08-07): "v1.4.0: add write-maintainable-code, the minimum-sufficient implementation lens." Version 1.4.0 (`plugin.json`). A plugin/marketplace package of governed agent skills shipping: 4 full skills (`skills/`) — `governed-operator` (constitution: seats, gates, role integrity), `reasoning-doctrine` (working method: stage loop, anti-drift), `write-maintainable-code` (minimum-sufficient implementation lens), `run-review-repair-loop` (bounded self-review, 1-5 scoring); 2 universal starters (`universal-starter/`) for skill-less surfaces; 1 enforcement pattern (`destructive-command-guard/`, dependency-free Python pre-execution hook with test suite and per-surface adapters). `.claude-plugin/` holds the Claude Code plugin manifest (marketplace `ezra-governed`). Note: `skills/find-a-way/agents/` exists on disk but is empty and untracked by git — not shipped repo content. Install model (`INSTALL.md`): one tier per skill only (full or starter, never both); routes are Claude Code plugin install or manual copy, zip upload for Claude web/desktop/API, `.agents/skills/` for Codex, pasted project instructions elsewhere. README (as of 2026-08-07) marks Claude Code plugin and GitHub Copilot CLI "verified in practice"; VS Code/Codex/Cursor/ChatGPT desktop documented-only or unverified; manual copy verified on Kimi, Grok, Antigravity.

## Decisions made, with why
v1.4.0 added `write-maintainable-code`, scoped to load only after outcome/scope/authority are fixed (per its frontmatter and README's load-order note). Preceding commits (`a9ceb5f`, `968069f`) split README install-route labels into "documented" vs. "verified in practice." `destructive-command-guard` commits show the same pattern: a Kimi desktop result was recorded negative, then removed from the shipped list (`8cbb720`, "Ship only live-verified surfaces") — a stated policy of shipping only what's been run live.

## Next actions
Operator-stated (2026-08-16, not yet evidenced in the repo): updates to the skill set are already in the pipeline — this repo is actively evolving, which is why it carries memory. A session picking up that work should update this record with the specific slate. Standing continuity worth tracking here that git history does not hold: the per-surface verified-vs-documented matrix (README) and any feedback from the repo's consumers. Next action belongs to the operator's roadmap.

## Files & surfaces
`README.md`, `INSTALL.md`, `LICENSE`, `plugin.json` (top level); `.claude-plugin/` (marketplace + plugin manifests); `skills/` (4 skill folders, `SKILL.md` + optional `references/`); `universal-starter/` (2 files); `destructive-command-guard/` (core, adapters, tests, README); `assets/social-preview.png`.

## Constraints
This record is continuity, not authority — verify against the repo before acting on it (LSN-018). Project continuity of this kind never enters CIL.

## Verification performed
Read `README.md` and `INSTALL.md` in full; read `plugin.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`; ran `git status`, `git log --oneline` (19 commits), `git log -1` for exact last-commit hash/date; listed top-level and `skills/` contents; confirmed `skills/find-a-way/` is untracked/empty via `git ls-files`; read SKILL.md frontmatter for all four shipped skills.
