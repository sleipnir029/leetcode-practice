---
description: Today's spaced-repetition review queue — quiz, re-solve, log
---

Read `progress.json` and work out what's due today (intervals D+1, D+7, D+30; `confidence <= 2`
halves the gap — the logic lives in `next_review()` in `build_dashboard.py`, so read that rather
than reimplementing the arithmetic).

Show the queue, most overdue first. Then for each problem the user wants to review:

1. Show only the **title and the trigger line from `notes.md`** — never `solution.py`.
2. Ask them to state the approach from memory, out loud, before touching a keyboard.
3. If it's shaky, they re-solve it from blank (~10 min). If it's solid, one quiz question is enough.
4. Ask for a fresh confidence 1–5.

Then log the **outcome**, not just that a review happened. Append to that entry's `reviews` array
an object `{"date": "<today>", "result": "pass"|"blank", "confidenceWas": <their confidence going
INTO this review, 1-5>}`:
- **pass** — they recalled the approach and (if re-solved) got it right without help.
- **blank** — they couldn't recall it, or needed the notes/a hint. Score this honestly; a blank
  resets the problem to box 1 (retest tomorrow, and the 7/30/90-day intervals must be re-earned).
- **`confidenceWas`** — snapshot their confidence *before* this review, so overconfidence stays
  visible even after you lower their confidence below. Don't skip it on blanks especially.

Then update `confidence`, note any miss in `mistakes.md`, run `python3 build_dashboard.py`, and
commit `review: <id> <slug> (<pass|blank>, confidence <n>)`.

Review does **not** consume the day's new problem — say so if they seem to think it does.

If nothing is due, say so in one line and point them at the next unsolved problem.
