#!/bin/bash
# Team Hub Memory light — session-scoped write-duty tooth.
# Locked by thm-light--convergence-v3 (operator lock 2026-08-15).
# Mode: "$1" = baseline (SessionStart) | check (Stop).
# Predicate: tree changed vs THIS session's baseline AND the designated memory
# record is not among the changes AND no reminder issued yet this session.
# Fail-open by design: any error exits 0 silently (the tooth never blocks work).

set -u
cd "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || exit 0
MEMORY_RECORD="memory/01-latest-handoff.md"
INPUT=$(cat 2>/dev/null || true)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("session_id",""))
except Exception: print("")' 2>/dev/null)
[ -z "$SESSION_ID" ] && exit 0
STATE_DIR="${TMPDIR:-/tmp}/thm-tooth"
mkdir -p "$STATE_DIR" 2>/dev/null || exit 0
BASE="$STATE_DIR/$SESSION_ID.baseline"
RECBASE="$STATE_DIR/$SESSION_ID.record"
MARK="$STATE_DIR/$SESSION_ID.reminded"

STATUS=$(git status --porcelain --untracked-files=all 2>/dev/null) || exit 0
HASH=$(printf '%s' "$STATUS" | shasum -a 256 | cut -d' ' -f1)
if [ -f "$MEMORY_RECORD" ]; then RECHASH=$(shasum -a 256 "$MEMORY_RECORD" 2>/dev/null | cut -d' ' -f1); else RECHASH=ABSENT; fi

case "${1:-}" in
  baseline)
    printf '%s' "$HASH" > "$BASE" 2>/dev/null
    printf '%s' "$RECHASH" > "$RECBASE" 2>/dev/null
    ;;
  check)
    [ -f "$MARK" ] && exit 0
    [ -f "$BASE" ] || exit 0
    OLD=$(cat "$BASE" 2>/dev/null)
    [ "$HASH" = "$OLD" ] && exit 0
    OLDREC=$(cat "$RECBASE" 2>/dev/null || printf ABSENT)
    # Locked semantic: remind only if THIS SESSION did not update the record.
    # Deletion is not an update: record ABSENT now but present at baseline also reminds.
    if [ "$RECHASH" = "$OLDREC" ] || { [ "$RECHASH" = ABSENT ] && [ "$OLDREC" != ABSENT ]; }; then
      touch "$MARK" 2>/dev/null
      printf '{"systemMessage": "MEMORY TOOTH: this session changed files in this repo but did not update %s. Before ending substantive work: rotate the current record into memory/archive/<date>-handoff.md and write the new latest (light profile) — or state why no update is owed."}\n' "$MEMORY_RECORD"
    fi
    ;;
esac
exit 0
