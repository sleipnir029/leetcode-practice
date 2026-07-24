---
description: Post-mortem a problem you just attempted — 7-step debrief, quiz, re-implement, log
---

The user has finished their timer on problem **$ARGUMENTS** and is bringing their attempt.
Their code follows, or is already in the working tree.

**First, ask for their think-note** if they didn't paste one — the 2–3 lines they jotted while
solving on LeetCode (restatement, the pattern they reached for *before* coding, whether they
looked at any hint/editorial). This is the ONLY valid source for the `recognized` score; I can't
read pre-code thinking from finished code. If they have no note this time, that's fine — score
`recognized: unknown` (not a guess), mention it's left out of the recognition rate, and remind
them the think-note is what unlocks that metric. Don't nag beyond one line.

Run the debrief protocol in `CLAUDE.md`. All 7 steps, in order, no skipping:

1. Read back — they explain their own code, step by step.
2. Complexity — their guess first, then correct.
3. Brute force → optimal ladder — every rung, and the insight that removes each loop.
4. Pattern + the trigger phrase that should have fired it.
5. Trade-offs — when does the worse solution win, in a real system?
6. Quiz — 3–5 questions, code hidden, one "what breaks if…" mutation. Ask for confidence 1–5.
7. Re-implement from blank. That version is what gets saved.

Do it conversationally — one step at a time, wait for their answer before moving on. Do not
dump all seven at once, and do not give away step 3 or 4 while still in step 1 or 2.

If they haven't actually attempted it yet, stop: refer them to the timer wall rule.

While debriefing, decide the three evaluation fields honestly (`approach`, `recognized`,
`mistakes`) — see the debrief protocol in `CLAUDE.md`. Score the solo attempt straight; "brute"
and "stuck" are recorded as-is.

When step 7 is done, run the logging checklist in `CLAUDE.md` (progress.json with all fields →
patterns.md → mistakes.md → `python3 build_dashboard.py` → commit → milestone check).
