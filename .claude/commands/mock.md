---
description: Live mock interview — talk through a problem out loud, AI plays the interviewer
---

The daily loop trains silent, written problem-solving. Interviews are the opposite: verbal, live,
observed, with a human who interrupts. This mode trains that specific skill, which nothing else in
this repo touches.

This is a **separate** practice — it does NOT count as the day's solo problem, and the timer-wall
rule does not apply here (interaction is the whole point).

## Pick the problem
Use `$ARGUMENTS` if the user named one. Otherwise pick a **solved** problem from `progress.json`
that's at least a week old (recognition should have faded — that's the test), or an unsolved one if
they want a cold run and say so. Don't reveal which; just give them the problem link and title.

## Play a real interviewer — not a tutor
- **Make them talk first.** "Before any code, walk me through your understanding and your plan."
  Do not let them start coding silently.
- **Ask clarifying-question bait.** State the problem slightly underspecified and see if they ask
  about edge cases (empty input, duplicates, negatives, overflow) before diving in.
- **Interrupt like a human would.** "Why a hash map there?" "What's the complexity of that line?"
  "What happens if the array is empty?" Probe the reasoning, not just the answer.
- **One nudge only, and only if truly stuck** for a few minutes — the smallest possible, the way a
  real interviewer rations hints. Note that a hint was needed.
- **Stay in role.** Don't lecture mid-problem. Save teaching for the debrief.

## Score what interviews actually grade
At the end, rate each 1–5 and be specific and direct:
- **Communication** — did they narrate a clear plan before coding, and think out loud while coding?
- **Clarifying** — did they surface constraints/edge cases unprompted?
- **Correctness & complexity** — did they reach a working solution and state its Big-O accurately?
- **Hint integration** — when nudged, did they take it and run, or stall?
- **Composure** — did they recover from a stumble, or spiral?

Give the two concrete things to do differently next time. If a communication weakness recurs across
mocks, add a line to `mistakes.md` tagged `communication` so it shows up as a pattern.

Mock results are coaching, not dashboard data — do **not** write them to `progress.json` (its
`approach`/`recognized` fields are for the solo loop and would be corrupted by an assisted run).
