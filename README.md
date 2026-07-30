# leetcode-practice

A training system for the [LeetCode 75](https://leetcode.com/studyplan/leetcode-75/) — 75 problems,
22 sections, 22 Easy / 53 Medium. One problem a day.

This is not a submissions archive. The goal is to look at an unfamiliar problem and know which
pattern it wants, and to explain out loud why one solution costs more memory than another. The repo
exists to measure whether that's actually happening.

**Progress:** open [`dashboard.html`](dashboard.html) in a browser.
**After the 75:** [`ROADMAP.md`](ROADMAP.md).

---

## Quick start

```sh
./think.sh 1768        # 1. write your plan, freeze it
                       # 2. solve on LeetCode, timer on
/debrief 1768          # 3. post-mortem, re-implement, log
```

That's the whole loop. Everything below is detail to look up when you need it.

---

## The daily loop

### 0 · Start — `./think.sh <id>`

Scaffolds `think-log.md` in the problem folder, opens it, and commits it once you've filled in the
top half. Run it **before** you open the problem.

It refuses to freeze an untouched template, and refuses to run outside a terminal.

<details>
<summary>What the freeze does and doesn't prove</summary>

A `commit-msg` hook rejects a `solve: <id>` commit unless a matching `think-log <id>` commit already
exists. That proves the plan was committed before the solution was, and that it wasn't blank.

It does **not** prove the plan came before the *solving* — that happens on leetcode.com, which this
repo can't see. The gate is a subject-line match, so `Solve: 1768` or `solve:1768` slip past it.
Treat it as a scaffold for your own honesty, not a proof. It only measures something if you actually
fill it in first.

Bypassing with `git commit --no-verify` is fine; recognition for that problem is scored `unknown`.
</details>

### 1 · Solve — timer on, no help

| Difficulty | Think | Code | Total |
|---|---|---|---|
| Easy | 15 min | 15 min | 30 min |
| Medium | 15–20 min | 25 min | 45 min |

When the timer ends, stop. Solved, timed out, or wrong — all three feed the same debrief.

No asking Claude for hints while the clock runs. That rule lives in `CLAUDE.md`; it's instruction,
not machinery, so it's on you.

### 2 · Debrief — `/debrief <id>`

Seven steps, in order:

1. Explain your own code back, line by line
2. State the complexity — your guess first
3. Brute force → optimal ladder, and the insight that removes each loop
4. Name the pattern, and the **trigger** — the phrase that should have fired it
5. Trade-offs: when would the worse solution actually win?
6. Quiz, code hidden
7. **Re-implement from a blank file** — that version gets committed

Step 7 is the one that does the work. Reading a solution feels like learning and isn't.

> **Short on time?** The sanctioned minimum is steps **2, 4 and 7** — about 35 minutes, committed
> with `min` in the message. A minimum day beats a skipped day. Step 7 is never optional: if you're
> too tired to re-implement, don't log the problem at all and take it cold another day.

### 3 · Review — `/due`

Every solved problem returns on four rungs — **1, 7, 30, then 90 days** — each measured from the
*previous review*, not from the solve date. In calendar terms: **+1, +8, +38, +128**. Rating
confidence ≤ 2 halves the next gap. A blank resets that problem to the first rung.

Reviews come before the new problem, and they don't use up your daily problem. A review-only day
still counts toward your streak.

### 4 · Mock interview — `/mock` (occasional)

The daily loop trains silent, written problem-solving. Interviews are verbal and observed. `/mock`
plays an interviewer who interrupts, probes your reasoning and rations hints, then scores
communication and composure rather than just correctness. Separate from the daily problem; worth
doing in the weeks before a real loop.

---

## Commands

| Command | When | What it does |
|---|---|---|
| `./think.sh <id>` | Start of every problem | Scaffolds and freezes your pre-code plan |
| `/debrief <id>` | Right after the timer | 7-step post-mortem, scoring, logging |
| `/due` | Daily, before the new problem | Review queue — quiz, re-solve, record the outcome |
| `/mock [id]` | Occasionally | Live verbal mock interview |
| `/assess` | Automatic at milestones | Written read on whether your reasoning is sharpening |
| `python3 build_dashboard.py` | After any data change | Regenerates `dashboard.html` |
| `python3 build_dashboard.py --test` | Anytime | Self-checks: metrics, dates, escaping, doc drift |

---

## What the dashboard measures

Three fields per problem drive everything:

| Field | Values | Scored from |
|---|---|---|
| **`approach`** | `optimal` / `suboptimal` / `brute` / `stuck` | Your code. Hint-agnostic — reading the editorial and then writing an optimal solution is honestly `optimal` |
| **`recognized`** | `self` / `hinted` / `missed` / `unknown` | The **frozen top half** of your think-log, and nothing else. No frozen note → `unknown`, never inferred from finished code |
| **`mistakes`** | fixed tag list | The debrief |

From those:

- **Optimal-first rate** — the north star. A problem counts only if it was `optimal` **and** solved
  inside the timer **and** not reached off a hint. Everything else is real progress, but it isn't
  optimal-first.
- **Pattern recognition** — how often you named the pattern before coding.
- **Retention** — pass rate on reviews taken a week or more apart.
- **Needs attention** — your weakest logged attempts, ranked, with the reason.
- **Pattern mastery** — per pattern: optimal-code %, recognition %, confidence.
- **Diagnosis** — those numbers turned into a plain-language read at the top of the page.

### When each number appears

Every rate stays silent until it has five data points *of its own kind*:

| Rate | Needs |
|---|---|
| Optimal-first, recognition | 5 attempts **with a frozen think-log** |
| Retention | 5 reviews at a week-plus gap (so roughly two weeks in) |
| Per-pattern table | 3 attempts in that pattern — below that you get raw counts (`1/2`), not a percentage |

Skipping `./think.sh` costs you data, not credit: those problems sit outside optimal-first and
recognition entirely rather than being guessed in either direction.

### Two deliberate choices worth knowing

**A `stuck` attempt is logged but doesn't count as solved.** It stays out of the 75, stays visible
in "Needs attention", and comes back around as a fresh cold attempt.

**Retention ignores next-day retests.** A blank resets a problem to the first rung, which mints a
cheap retest; counting those let a bad stretch dilute itself, so the number read *better* as recall
got worse. Only genuine week-plus gaps count.

---

## Logging a solve

`/debrief` does this for you. The order matters.

1. Save `solution.py` and fill `notes.md` in `solutions/<nn-section>/<id>-<slug>/`
2. Append the entry to `progress.json`
3. Add a row to `patterns.md` — trigger first
4. Add to `mistakes.md` if anything was missed
5. `python3 build_dashboard.py`
6. Commit: `solve: <id> <slug> (<difficulty>, <solo-result>)`

A `progress.json` entry:

```json
{
  "id": 1768,
  "date": "2026-07-30",
  "pattern": "two-pointers",
  "solo": "solved",
  "minutes": 22,
  "confidence": 4,
  "approach": "optimal",
  "recognized": "self",
  "mistakes": [],
  "reviews": []
}
```

Title, difficulty and section are **not** stored — they come from the seed list by id, so they can't
drift. Every fixed-vocabulary field is validated: a typo fails the build with a readable message
instead of silently vanishing from a rate.

Reviews are appended to the same entry as
`{"date": "...", "result": "pass"|"blank", "confidenceWas": <1-5>}`.

---

## Layout

```
dashboard.html          the report — regenerate, don't edit
build_dashboard.py      the generator; also holds the 75-problem seed list
progress.json           one record per logged attempt — the source of truth
patterns.md             trigger → pattern glossary; the most reusable file here
mistakes.md             recurring error log
ASSESSMENT.md           milestone write-ups
ROADMAP.md              what comes after the 75
CLAUDE.md               the coaching rules
think.sh                starts a problem and freezes the plan
.githooks/commit-msg    refuses a solve commit with no frozen think-log
templates/              think-log.md (pre-code) and notes.md (post-debrief)
solutions/<nn-section>/<id>-<slug>/{think-log.md,solution.py,notes.md}
```

Problem statements aren't copied into this repo — `notes.md` links to LeetCode and carries your own
restatement, which is its own comprehension check.

---

## Troubleshooting

**`commit-msg: blocked — no frozen think-log for problem <id>`**
You skipped `./think.sh`. Either run it now, or `git commit --no-verify`. Either way, score
`recognized: unknown` for this problem.

**`dashboard.html is STALE`**
Run `python3 build_dashboard.py` and commit the result. The committed page is a build artifact, and
`--test` fails when it drifts from the generator.

**`progress.json: entry #N (id X): <field> must be one of ...`**
A typo in a validated field. The message names the field and the allowed values.

**`review dates must run forwards`**
Reviews must be appended in the order they happened, and can't predate the solve. Retention measures
the gap between consecutive reviews, so order changes the result.

**Retention still shows `—` after two weeks**
Expected. It only counts reviews at a week-plus gap, and early on every review is a next-day retest.

**The review queue is getting long**
Usually a high blank rate rather than skipped days — each blank restarts that problem's ladder.
Check the retention number first.

---

## The rules that keep this honest

1. **No hints while the timer runs.** A hint at minute 12 erases the session.
2. **You type every line of `solution.py`.** If the AI writes it, the repo measures nothing.
3. **Your guess first, correction second** — on the approach and on the complexity.
4. **Score straight.** Brute is `brute`. A flattered metric teaches nothing.
5. **One problem a day.** Miss a day and the streak resets — that's the entire penalty. No catch-up,
   no doubling up, no debt. These systems die from the guilt of a backlog, not from the missed day.

Next to the streak is **days practised**, which only ever goes up. A reset costs you the streak, not
the record of the work.

---

## Requirements

Python 3, standard library only — nothing to install. The dashboard pulls its chart and diagram
libraries from a CDN, so the charts need a connection; the tables and text work offline.
