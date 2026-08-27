# governed-agent-skills repository rules

This file governs the repository for all agents.

Standing environment skills (`governed-operator`, `reasoning-doctrine`) load
once at session start and remain active; do not copy or redefine them here.

## Repository rules

- Make the smallest safe change inside the authorized seam; do not widen scope
  or modify unrelated files.
- Skill bodies are the product. Keep each rule in exactly one place, prune
  stale lines, and write for the agent that loads the file.
