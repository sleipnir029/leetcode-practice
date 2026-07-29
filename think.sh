#!/usr/bin/env bash
# Start a problem the honest way: scaffold the think-log, then FREEZE it with a commit
# BEFORE you write any code. The commit timestamp is the proof your plan predated your
# solution — that's what makes the recognition score trustworthy instead of honor-system.
#
# Usage:  ./think.sh <leetcode-id>      e.g.  ./think.sh 1768
set -euo pipefail
cd "$(dirname "$0")"

# make sure the commit-msg guard is active (idempotent self-install; hooks dir is tracked)
[ "$(git config core.hooksPath 2>/dev/null)" = ".githooks" ] || git config core.hooksPath .githooks

id="${1:-}"
[ -z "$id" ] && { echo "usage: ./think.sh <leetcode-id>   (e.g. ./think.sh 1768)"; exit 1; }

# resolve section + slug from the single source of truth (SEED in build_dashboard.py)
info="$(python3 - "$id" <<'PY'
import sys, build_dashboard as b
i = int(sys.argv[1])
row = next((r for r in b.SEED if r[0] == i), None)
if not row:
    sys.exit(f"id {i} is not a LeetCode 75 problem")
print(row[3], b.slug(row[1]))
PY
)" || { echo "$info"; exit 1; }

section="${info%% *}"; slug="${info#* }"
dir="solutions/$section/$id-$slug"
log="$dir/think-log.md"

mkdir -p "$dir"
if [ ! -f "$log" ]; then
  sed "s/<id>/$id/; s/<title>/$slug/" templates/think-log.md > "$log"
fi

# open it however this machine opens files; non-fatal if that fails
( ${EDITOR:-open} "$log" >/dev/null 2>&1 & ) || true

cat <<MSG

  Think-log: $log

  Fill the TOP half NOW — before you write a single line of code on LeetCode.
  Restate it, name the pattern you're reaching for (or "none — flailing"), be honest.

MSG
read -r -p "  Written your pre-code plan? Press Enter to FREEZE it with a commit... " _

git add "$log"
if git diff --cached --quiet; then
  echo "  (nothing new to commit — already frozen)"
else
  git commit -q -m "think-log $id: frozen before coding"
  echo "  ✅ Frozen at $(git log -1 --format=%cd --date=format:'%Y-%m-%d %H:%M:%S'). Now go solve on LeetCode."
fi
