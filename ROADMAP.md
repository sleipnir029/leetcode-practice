# Roadmap — LeetCode 75 is month one, not the whole thing

The independent review made one thing clear: **finishing LeetCode 75 makes you interview-*capable*,
not interview-*ready*.** LC75 is 22 easy + 53 medium + **zero hard**. It builds your pattern
vocabulary — the recognition reflex that makes an unseen problem feel familiar. That's necessary
and it's month one. Real interview loops also throw harder variants, two-patterns-composed
problems, a live human, and (for many roles) system-design and behavioral rounds. This file is the
plan for after the 75, so you pace the whole thing instead of thinking the finish line is at 75.

Don't start month two until the LC75 dashboard shows: **optimal-first ≥ ~60%** (note: this is a
trailing-10-problem window, not a 75-problem average, and the last 10 are the hardest sections —
so read it alongside the per-pattern table, not alone), **retention ≥ ~80%**,
and no red gap flags. If you finish the 75 problems but those are shaky, the right move is a second
pass over your weakest patterns (the dashboard's "Needs attention" list), not new material.

The retention figure counts only reviews at a week or longer, so it means what the gate needs it to
mean: recall that survived a real gap. (It used to pool every rung equally, which let a blank mint
its own easy next-day retests and dilute the number upward — fixed.) The practical consequence is
that retention reads `—` for the first couple of weeks, until five reviews have come due at the
7-day rung or beyond. Don't read that dash as a problem; it's the metric refusing to guess.

---

## Month 1 — LeetCode 75 (where you are)
**Goal:** pattern vocabulary + the daily habit.
- One problem/day, solo-first, debrief, spaced review. Already built.
- Exit test: the three thresholds above.

## Month 2 — Depth + speed
**Goal:** handle mediums fast and start on hards; stop needing the full 45 minutes.
- **Extend to NeetCode 150** (superset of LC75 — you'll have ~75 done, ~75 new). Same daily loop,
  same dashboard. The new problems are the harder mediums and the composed ones.
- **Introduce hards, slowly:** one hard every 3rd day, untimed at first (a hard you grind for an
  hour teaches more than three you bounce off). Add a `hard` difficulty to the seed list when you
  get here — but this is not free: `build_dashboard.py` has `assert len(SEED) == 75`, and
  `validate()` rejects any id outside `SEED`. Those two block the build outright. The stats block,
  the difficulty chart and the `.easy`/`.medium` CSS then produce silently wrong output rather than
  failing — which is worse. All five need attention before a `hard` row or a NeetCode-150 id.
- **Start timing tighter:** mediums in 25 min, not 45. Speed comes from recognition, not rushing —
  so this is a *consequence* of month one working, not a thing to force.
- **Begin `/mock` weekly.** One live verbalized mock a week. This is the skill LC75 never touches.

## Month 3 — Interview simulation
**Goal:** perform under a human, on a clock, across a full loop.
- **Two-problem timed sessions**, 30–35 min each, back to back — interview stamina is its own skill.
- **`/mock` 2–3×/week**, escalating: interviewer interrupts more, gives fewer hints, pushes on
  "why that data structure" and "what's the complexity of that line."
- **Company-tagged sets** for the places you're actually applying (LeetCode's company filter) —
  pattern *frequency* differs by company, and this is where that matters.
- **System design + behavioral** if the roles need them. Different prep entirely (design: a
  handful of canonical problems + a framework; behavioral: ~8 STAR stories). Out of scope for this
  repo, but don't discover you need them the week before an onsite.

## Ongoing, all three months
- **Never stop the reviews.** Retention is the whole game; the dashboard now measures it (pass/blank).
  A leaking retention rate means slow down new problems and clear the queue.
- **Redo in C++** once a pattern is solid in Python — add `solution.cpp` beside `solution.py`; the
  side-by-side diff is the lesson about memory and pointers you wanted.
- **Mock feedback feeds back.** Recurring communication weaknesses go in `mistakes.md` as a
  freeform line. They can't be a `mistakes` tag in `progress.json` — that array is validated
  against a fixed vocabulary and `communication` isn't in it. Give mocks their own file if you
  want a trend.

---

*This is a sketch, not a contract. Adjust the pace to your actual interview timeline — if a loop is
6 weeks out, compress; if it's 6 months out, go deeper on understanding. The one non-negotiable is
that "finished LC75" and "ready to interview" are different milestones.*
