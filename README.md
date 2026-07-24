# leetcode-practice

Working through the [LeetCode 75 study plan](https://leetcode.com/studyplan/leetcode-75/) —
75 problems, 22 sections, 22 Easy / 53 Medium — one problem a day.

This is a study system, not just a submissions archive. The goal isn't a solved count; it's
being able to look at an unfamiliar problem and know which pattern it wants, and to explain
*why* one solution costs more memory than another when it comes up in a real conversation.

**Progress:** open [`dashboard.html`](dashboard.html) in a browser.

---

## The daily loop

### 1. Solo — timer on, no help

| Difficulty | Think | Code | Total |
|---|---|---|---|
| Easy | 15 min | 15 min | 30 min |
| Medium | 15–20 min | 25 min | 45 min |

The **think** phase means writing the approach into `notes.md` in plain English *before* typing
any code. If the sentence is fuzzy, the code will be too — and in an interview the narration is
half of what's being graded.

When the timer ends, stop. Solved, timed out, or wrong — all three are valid outcomes and all
three feed the same debrief.

No asking Claude for hints while the clock runs. That rule is written into `CLAUDE.md` and it
gets enforced.

### 2. Debrief — `/debrief <id>`

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

Every solved problem comes back at **+1 day, +7 days, +30 days**. Anything you rated confidence
≤ 2 comes back twice as fast. A review takes ~10 minutes and does **not** use up the day's new
problem.

---

## How the dashboard reads you

Beyond counts, the dashboard evaluates *how you think*, not just *what you finished*. Three fields
recorded honestly during each debrief drive it:

- **approach** — where your *solo* attempt landed before help: `optimal / suboptimal / brute / stuck`
- **recognized** — did you name the pattern before coding: `self / hinted / missed`
- **mistakes** — tagged from a fixed list, so recurring bugs become countable

From those it computes the signals that actually matter for interviews:

- **Optimal-first rate** — do you find the key insight yourself, or reach working code and need
  help to optimize? This is *the* number.
- **Pattern recognition rate** — how often you see the pattern before the hint.
- **Needs attention** — your weakest solved problems, ranked, with the reason.
- **Recurring mistakes** — the bug category to drill.
- **Pattern mastery** — per-pattern optimal-first %, recognition %, confidence, weakest first.
- **Diagnosis** — those numbers turned into a plain-language read at the top of the page.

Every rate shows its `n` and stays silent until ~5 solves — at one problem a day, a rate over
three problems is noise, and the dashboard won't pretend otherwise.

At **10 / 20 / 35 / 50 / 65 / 75** solved, `ASSESSMENT.md` gets a written milestone review that
reads your actual pre-code plans and judges whether the reasoning is sharpening — the part no
number can see. Trigger it anytime with `/assess`.

---

## Layout

```
dashboard.html      progress, review queue, mind map — regenerate, don't edit
build_dashboard.py  the generator; also holds the 75-problem seed list
progress.json       one record per solved problem — the source of truth
patterns.md         trigger → pattern glossary; the most reusable file here
mistakes.md         recurring error log
templates/notes.md  copy this into each new problem folder
solutions/<nn-section>/<lc-id>-<slug>/{solution.py,notes.md}
```

Regenerate the dashboard after any change to `progress.json`:

```sh
python3 build_dashboard.py          # stdlib only, no dependencies
python3 build_dashboard.py --test   # self-checks on the review-date math
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
