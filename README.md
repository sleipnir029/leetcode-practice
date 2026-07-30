# leetcode-practice

Working through the [LeetCode 75 study plan](https://leetcode.com/studyplan/leetcode-75/) —
75 problems, 22 sections, 22 Easy / 53 Medium — one problem a day.

This is a study system, not just a submissions archive. The goal isn't a solved count; it's
being able to look at an unfamiliar problem and know which pattern it wants, and to explain
*why* one solution costs more memory than another when it comes up in a real conversation.

**Progress:** open [`dashboard.html`](dashboard.html) in a browser.

**LC75 is month one, not the finish line** — the full arc (hards, mock interviews, system design)
is in [`ROADMAP.md`](ROADMAP.md).

---

## The daily loop

### 0. Start the problem — `./think.sh <id>`  (required, ~1 min)

Run `./think.sh <id>` (e.g. `./think.sh 1768`). It scaffolds today's think-log, opens it, and —
once you've written your **pre-code plan** in the top half — commits it. It refuses to freeze an
untouched template, and refuses to run outside a terminal, so what gets committed has content in it.

This isn't just a convention: a git `commit-msg` hook (`.githooks/commit-msg`, auto-activated by
`think.sh`) **refuses** a `solve: <id>` commit unless the matching `think-log <id>` commit already
exists. (If you `git commit --no-verify` past it, recognition for that problem is scored `unknown`.)

What that buys you, precisely: the plan commit came before the solve commit, and the plan wasn't
blank. It is **not** proof the plan came before the *solving* — that happens on leetcode.com, which
this repo can't see. The gate is a subject-line match, so `Solve: 1768` or `solve:1768` slip past it
entirely. It's a scaffold for your own honesty, not a proof, and it only works if you actually run
it first.

### 1. Solo — timer on, no help

| Difficulty | Think | Code | Total |
|---|---|---|---|
| Easy | 15 min | 15 min | 30 min |
| Medium | 15–20 min | 25 min | 45 min |

The **think** phase is the top half of the think-log — the approach in plain English, written and
**frozen** (step 0) *before* you type any code. If the sentence is fuzzy, the code will be too —
and in an interview the narration is half of what's being graded.

When the timer ends, stop. Solved, timed out, or wrong — all three are valid outcomes and all
three feed the same debrief.

No asking Claude for hints while the clock runs. That rule is written into `CLAUDE.md`, which is
instruction, not machinery — nothing can stop you asking, so this one is on you.

### 2. Debrief — `/debrief <id>`

**The floor:** on a night when the full debrief isn't happening, the sanctioned minimum is steps
**2, 4 and 7** — complexity, trigger, re-implement from blank — about 35 minutes, committed with
`min` in the message. A minimum day beats a skipped day. Step 7 is never optional; if you're too
tired to re-implement, don't log the problem at all and take it cold another day.

Paste the problem and your attempt. Seven steps, in order:

1. Explain your own code back, line by line
2. State the time/space complexity — your guess first
3. Brute force → optimal ladder, and the insight that removes each nested loop
4. Name the pattern, and the **trigger** — the phrase in the problem that should have fired it
5. Trade-offs: when would the "worse" solution actually win in a real system?
6. Quiz, with the code hidden
7. Re-implement from a blank file — that's the version that gets committed

Step 7 is the one that does the work. Reading a solution feels like learning and isn't.

### 3. Review — `/due`

**Clear the queue each day** — reviews before the new problem. With clean recall it peaks at about
3 reviews/day (first reached around day 39). It grows with your *blank rate*, not your calendar:
every blank resets that problem to box 1 and starts its ladder over, so at a 20% blank rate the peak
is nearer 7/day, and worse if you're often rating confidence ≤ 2. A long queue is a retention
signal, not a discipline one. A review-only day still keeps your streak.

Every solved problem comes back on four rungs — **1, 7, 30, then 90 days** — each measured from
the *previous review*, not from the solve date (so in calendar terms: +1, +8, +38, +128). A blank
resets it to rung one. Anything you rated confidence ≤ 2 comes back twice as fast. A review takes ~10 minutes and does **not** use up the day's new
problem.

### 4. Mock interview — `/mock` (as needed)

The daily loop builds silent, written problem-solving. Interviews are verbal and live. `/mock`
runs a real mock: you talk through a problem out loud while the AI plays an interviewer that
interrupts, probes your reasoning, and rations hints — then scores you on communication,
clarifying questions, complexity, and composure, not just correctness. Separate from the daily
problem; do a few in the weeks before interviews.

---

## How the dashboard reads you

Beyond counts, the dashboard evaluates *how you think*, not just *what you finished*. Three fields
recorded honestly during each debrief drive it:

- **approach** — how optimal the code you brought is: `optimal / suboptimal / brute / stuck`
  (judged from the attempt you bring to the debrief. Note the file that gets *committed* is the
  step-7 re-implementation, written after the debrief — so if you want the score to be re-auditable
  later, save the raw attempt too). A `stuck` attempt is logged but does **not** count as solved:
  it stays out of the 75 count and comes back around as a fresh cold attempt.
- **recognized** — did you name the pattern *before* coding: `self / hinted / missed`. This one
  can **only** come from the frozen top half of your **think-log** — written and committed by
  `./think.sh <id>` before you type any code (what pattern you reached for, whether you peeked at a
  hint). No frozen note → scored `unknown` and left out of the rate, never guessed from your code.
  See `templates/think-log.md`.
- **mistakes** — tagged from a fixed list, so recurring bugs become countable

> **Why the think-log matters:** you solve on LeetCode, not with me, so your code is all I see —
> and code shows the *result*, not what you were thinking at minute 3. The frozen note is the only
> honest way to measure whether you *recognised* the pattern before coding — a strong signal for
> how well a problem will transfer, and a useful complement to the optimal-first north-star. Two
> lines is enough. Because it's committed before you code, it can't be quietly rewritten later to
> flatter you — which is the entire point.

From those it computes the signals that actually matter for interviews:

- **Optimal-first rate** — do you find the key insight yourself, or reach working code and need
  help to optimize? This is *the* number.
- **Pattern recognition rate** — how often you see the pattern before the hint.
- **Needs attention** — your weakest logged attempts, ranked, with the reason (a `stuck` attempt
  stays visible here even though it doesn't count as solved).
- **Recurring mistakes** — the bug category to drill.
- **Pattern mastery** — per-pattern optimal-code %, recognition %, confidence, weakest first.
  (Optimal-*code*, not optimal-first: it scores the solution regardless of how you got there.)
- **Diagnosis** — those numbers turned into a plain-language read at the top of the page.

Every rate stays silent until it has 5 data points *of its own kind* — 5 attempts with a frozen
think-log for optimal-first *and* recognition, 5 reviews taken a week or more apart for retention.
At one problem a day, a rate over three problems is noise, and the dashboard won't pretend
otherwise.

Two things to know about how they're bounded. The optimal-first hero and the diagnosis text print
their `n`; the recognition and retention **tiles show only a percentage**, so check the diagnosis for
the count behind them. And the **per-pattern** table has a lower floor of its own — 3 attempts,
because with 22 sections most patterns never reach 5 — below which it prints the raw count
(`1/2`) instead of a percentage.

**Retention counts reviews at a week or longer**, not next-day retests. That's deliberate: a blank
resets a problem to the 1-day rung, so counting every rung equally meant a bad stretch generated its
own cheap wins and the number drifted *up* as recall got worse. Excluding the 1-day rung costs you
nothing — next-day recall was never the thing worth measuring — but it does mean retention stays `—`
for the first couple of weeks, until you have five reviews at real intervals.

At **10 / 20 / 35 / 50 / 65 / 75** solved, `ASSESSMENT.md` gets a written milestone review that
reads your actual pre-code plans and judges whether the reasoning is sharpening — the part no
number can see. Trigger it anytime with `/assess`.

### Reading it comfortably

The dashboard is built for readability:

- **Text size** — `A− / A / A+` in the top bar scales the whole page; your choice is remembered.
  (The baseline is already 18px, so `A−` does nothing until you've gone up first.)
- **Light / dark** — toggle in the top bar, also remembered; both are high-contrast.
- **Every chart's numbers are readable as text** — a "Show these numbers as a table" link under
  each chart (the per-section chart is the exception: its table is always open, directly below it),
  since a column of numbers is often clearer than a plotted line. Charts are backed by `aria-label`s and
  the page uses proper headings, so a screen reader can navigate it.
- **Colour is never the only signal** — the diagnosis uses ▲ good / ● watch / ▼ gap icons and
  words, not just colour, on a colourblind-safe palette.
- **Guidance is on the page** — every section carries a plain-language lead saying what it shows,
  and the diagnosis has a "what this means / what to do" legend, so nothing is cryptic.

---

## Layout

```
dashboard.html          progress, review queue, mind map — regenerate, don't edit
build_dashboard.py      the generator; also holds the 75-problem seed list
progress.json           one record per logged attempt — the source of truth
patterns.md             trigger → pattern glossary; the most reusable file here
mistakes.md             recurring error log
templates/think-log.md  the pre-code freeze; `./think.sh <id>` copies it into the problem folder
templates/notes.md      copy this into each new problem folder after the debrief
solutions/<nn-section>/<lc-id>-<slug>/{think-log.md,solution.py,notes.md}
```

Regenerate the dashboard after any change to `progress.json`:

```sh
python3 build_dashboard.py          # generator: stdlib only, no dependencies
python3 build_dashboard.py --test   # self-checks: review-date math, metrics, escaping, freshness
```

Problem statements aren't copied into this repo — `notes.md` links to LeetCode and carries my
own restatement instead, which is its own comprehension check.

Python now. Once the patterns are solid, the same problems get redone in C++ as `solution.cpp`
beside the Python file — the side-by-side diff is the point.

---

## Sections

`01-array-string` · `02-two-pointers` · `03-sliding-window` · `04-prefix-sum` ·
`05-hash-map-set` · `06-stack` · `07-queue` · `08-linked-list` · `09-binary-tree-dfs` ·
`10-binary-tree-bfs` · `11-bst` · `12-graphs-dfs` · `13-graphs-bfs` · `14-heap` ·
`15-binary-search` · `16-backtracking` · `17-dp-1d` · `18-dp-multidimensional` ·
`19-bit-manipulation` · `20-trie` · `21-intervals` · `22-monotonic-stack`

---

## The one rule that keeps this alive

One problem a day. Miss a day and the streak resets — that's the entire penalty. There is no
catch-up, no doubling up, no debt. Systems like this die from the guilt of a backlog, not from
the missed day.

A review day counts as a practice day, so clearing `/due` keeps the streak alive — the dashboard
tells you to clear reviews before starting something new, and it would be perverse to zero your
streak for obeying it. And next to the streak is **days practised**, which only ever goes up: a
reset costs you the streak, not the record of the work.
