---
description: Post-mortem a problem you just attempted — 7-step debrief, quiz, re-implement, log
---

The user has finished their timer on problem **$ARGUMENTS** and is bringing their attempt.
Their code follows, or is already in the working tree.

**First, verify the frozen think-log.** Run `git log --format='%ci %s' | grep "think-log $ARGUMENTS"`
and confirm a `think-log <id>: frozen before coding` commit exists and predates this debrief (i.e.
the plan was committed before the solution). Read that committed think-log — its frozen top half is
the ONLY valid source for the `recognized` score; I can't read pre-code thinking from finished code.
If there is no frozen commit (they skipped `./think.sh`), or it was committed after the code, score
`recognized: unknown` — not a guess — say the freeze couldn't be verified, and remind them one line:
next time start with `./think.sh <id>` so recognition can be scored.

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

When step 7 is done, run the logging checklist in `CLAUDE.md` — all 7 steps. Step 1 is the one that
creates the files everything else reads: save the step-7 re-implementation to
`solutions/<nn-section>/<id>-<slug>/solution.py` and fill `notes.md` beside it. Then progress.json →
patterns.md → mistakes.md → `python3 build_dashboard.py` → commit → milestone check. `/due` quizzes
from `notes.md` and `/assess` reads it, so skipping step 1 leaves both with nothing.
