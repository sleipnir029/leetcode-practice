#!/usr/bin/env bash
# Start a problem the honest way: scaffold the think-log, then FREEZE it with a commit
# BEFORE you write any code. The commit proves the plan landed before the SOLVE COMMIT, and that
# the plan wasn't blank. It cannot prove the plan came before the solving itself — that happens on
# leetcode.com, which this repo can't see. A scaffold for your own honesty, not a proof.
#
# Usage:  ./think.sh <leetcode-id>      e.g.  ./think.sh 1768
set -euo pipefail
cd "$(dirname "$0")"

# make sure the commit-msg guard is active (idempotent self-install; hooks dir is tracked)
[ "$(git config core.hooksPath 2>/dev/null)" = ".githooks" ] || git config core.hooksPath .githooks
# git silently *ignores* a non-executable hook (it only prints a hint), so the guard can
# vanish without a word after a clone or a chmod. Re-assert the bit every run.
[ -x .githooks/commit-msg ] || chmod +x .githooks/commit-msg

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
# A pipe/non-tty run would sail past `read` and (under `set -e`) exit before committing —
# silently freezing nothing, which you'd only discover when the solve commit is refused hours
# later. Fail loudly and early instead.
if [ ! -t 0 ]; then
  echo "  ✗ Not a terminal — nothing frozen. Run ./think.sh in a real shell, not a pipe." >&2
  exit 1
fi
read -r -p "  Written your pre-code plan? Press Enter to FREEZE it with a commit... " _

# The freeze is only worth something if there's a plan in it. An untouched template is a
# commit that satisfies the hook and measures nothing, so refuse it.
# The template line carries a trailing "← name the actual pattern…" hint, so "unfilled" means
# nothing but that hint. Delete the hint verbatim rather than everything after the arrow — a plan
# typed OVER the hint (which is what the hint invites) must still count as filled.
# `|| true` matters: under `set -e` a grep miss would kill the script here, silently freezing
# nothing — the exact failure the tty guard above exists to prevent.
line=$(grep -m1 'reaching for:' "$log" || true)
plan=$(printf '%s\n' "$line" \
  | sed 's/.*reaching for:\*\*//; s/← name the actual pattern, or write "none — flailing"//' \
  | tr -d '[:space:]')
if [ -z "$plan" ]; then
  echo "  ✗ 'The approach I'm reaching for:' is still blank — nothing frozen." >&2
  echo "    Name the pattern you're reaching for, or write \"none — flailing\". Then re-run." >&2
  exit 1
fi

# scope both the check and the commit to the think-log: an unrelated staged file must not get
# swept into a "frozen before coding" commit, and must not make an unchanged log look changed
git add "$log"
if git diff --cached --quiet -- "$log"; then
  echo "  (nothing new to commit — already frozen)"
else
  git commit -q -o "$log" -m "think-log $id: frozen before coding"
  echo "  ✅ Frozen at $(git log -1 --format=%cd --date=format:'%Y-%m-%d %H:%M:%S'). Now go solve on LeetCode."
fi
