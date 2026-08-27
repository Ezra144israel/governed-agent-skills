#!/bin/bash
# SessionStart hook: inject the skill router as session context (Claude Code).
# Copy to ~/.claude/hooks/session-router.sh, place ROUTER.md beside it,
# chmod +x, and register via settings.example.json.
ROUTER="$(dirname "$0")/ROUTER.md"
[ -f "$ROUTER" ] || exit 0   # fail open: no router, no injection, manual invoke still works
jq -n --rawfile router "$ROUTER" '{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": $router
  }
}'
