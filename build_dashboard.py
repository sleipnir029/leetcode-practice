#!/usr/bin/env python3
"""Regenerate dashboard.html from progress.json. Stdlib only, no server.

Usage:  python3 build_dashboard.py
        python3 build_dashboard.py --test    # run self-checks
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent

# The official LeetCode 75 study plan, in plan order.
# (leetcode_id, title, difficulty, section)
SEED = [
    (1768, "Merge Strings Alternately", "easy", "01-array-string"),
    (1071, "Greatest Common Divisor of Strings", "easy", "01-array-string"),
    (1431, "Kids With the Greatest Number of Candies", "easy", "01-array-string"),
    (605, "Can Place Flowers", "easy", "01-array-string"),
    (345, "Reverse Vowels of a String", "easy", "01-array-string"),
    (151, "Reverse Words in a String", "medium", "01-array-string"),
    (238, "Product of Array Except Self", "medium", "01-array-string"),
    (334, "Increasing Triplet Subsequence", "medium", "01-array-string"),
    (443, "String Compression", "medium", "01-array-string"),
    (283, "Move Zeroes", "easy", "02-two-pointers"),
    (392, "Is Subsequence", "easy", "02-two-pointers"),
    (11, "Container With Most Water", "medium", "02-two-pointers"),
    (1679, "Max Number of K-Sum Pairs", "medium", "02-two-pointers"),
    (643, "Maximum Average Subarray I", "easy", "03-sliding-window"),
    (1456, "Maximum Number of Vowels in a Substring of Given Length", "medium", "03-sliding-window"),
    (1004, "Max Consecutive Ones III", "medium", "03-sliding-window"),
    (1493, "Longest Subarray of 1's After Deleting One Element", "medium", "03-sliding-window"),
    (1732, "Find the Highest Altitude", "easy", "04-prefix-sum"),
    (724, "Find Pivot Index", "easy", "04-prefix-sum"),
    (2215, "Find the Difference of Two Arrays", "easy", "05-hash-map-set"),
    (1207, "Unique Number of Occurrences", "easy", "05-hash-map-set"),
    (1657, "Determine if Two Strings Are Close", "medium", "05-hash-map-set"),
    (2352, "Equal Row and Column Pairs", "medium", "05-hash-map-set"),
    (2390, "Removing Stars From a String", "medium", "06-stack"),
    (735, "Asteroid Collision", "medium", "06-stack"),
    (394, "Decode String", "medium", "06-stack"),
    (933, "Number of Recent Calls", "easy", "07-queue"),
    (649, "Dota2 Senate", "medium", "07-queue"),
    (2095, "Delete the Middle Node of a Linked List", "medium", "08-linked-list"),
    (328, "Odd Even Linked List", "medium", "08-linked-list"),
    (206, "Reverse Linked List", "easy", "08-linked-list"),
    (2130, "Maximum Twin Sum of a Linked List", "medium", "08-linked-list"),
    (104, "Maximum Depth of Binary Tree", "easy", "09-binary-tree-dfs"),
    (872, "Leaf-Similar Trees", "easy", "09-binary-tree-dfs"),
    (1448, "Count Good Nodes in Binary Tree", "medium", "09-binary-tree-dfs"),
    (437, "Path Sum III", "medium", "09-binary-tree-dfs"),
    (1372, "Longest ZigZag Path in a Binary Tree", "medium", "09-binary-tree-dfs"),
    (236, "Lowest Common Ancestor of a Binary Tree", "medium", "09-binary-tree-dfs"),
    (199, "Binary Tree Right Side View", "medium", "10-binary-tree-bfs"),
    (1161, "Maximum Level Sum of a Binary Tree", "medium", "10-binary-tree-bfs"),
    (700, "Search in a Binary Search Tree", "easy", "11-bst"),
    (450, "Delete Node in a BST", "medium", "11-bst"),
    (841, "Keys and Rooms", "medium", "12-graphs-dfs"),
    (547, "Number of Provinces", "medium", "12-graphs-dfs"),
    (1466, "Reorder Routes to Make All Paths Lead to the City Zero", "medium", "12-graphs-dfs"),
    (399, "Evaluate Division", "medium", "12-graphs-dfs"),
    (1926, "Nearest Exit from Entrance in Maze", "medium", "13-graphs-bfs"),
    (994, "Rotting Oranges", "medium", "13-graphs-bfs"),
    (215, "Kth Largest Element in an Array", "medium", "14-heap"),
    (2336, "Smallest Number in Infinite Set", "medium", "14-heap"),
    (2542, "Maximum Subsequence Score", "medium", "14-heap"),
    (2462, "Total Cost to Hire K Workers", "medium", "14-heap"),
    (374, "Guess Number Higher or Lower", "easy", "15-binary-search"),
    (2300, "Successful Pairs of Spells and Potions", "medium", "15-binary-search"),
    (162, "Find Peak Element", "medium", "15-binary-search"),
    (875, "Koko Eating Bananas", "medium", "15-binary-search"),
    (17, "Letter Combinations of a Phone Number", "medium", "16-backtracking"),
    (216, "Combination Sum III", "medium", "16-backtracking"),
    (1137, "N-th Tribonacci Number", "easy", "17-dp-1d"),
    (746, "Min Cost Climbing Stairs", "easy", "17-dp-1d"),
    (198, "House Robber", "medium", "17-dp-1d"),
    (790, "Domino and Tromino Tiling", "medium", "17-dp-1d"),
    (62, "Unique Paths", "medium", "18-dp-multidimensional"),
    (1143, "Longest Common Subsequence", "medium", "18-dp-multidimensional"),
    (714, "Best Time to Buy and Sell Stock with Transaction Fee", "medium", "18-dp-multidimensional"),
    (72, "Edit Distance", "medium", "18-dp-multidimensional"),
    (338, "Counting Bits", "easy", "19-bit-manipulation"),
    (136, "Single Number", "easy", "19-bit-manipulation"),
    (1318, "Minimum Flips to Make a OR b Equal to c", "medium", "19-bit-manipulation"),
    (208, "Implement Trie (Prefix Tree)", "medium", "20-trie"),
    (1268, "Search Suggestions System", "medium", "20-trie"),
    (435, "Non-overlapping Intervals", "medium", "21-intervals"),
    (452, "Minimum Number of Arrows to Burst Balloons", "medium", "21-intervals"),
    (739, "Daily Temperatures", "medium", "22-monotonic-stack"),
    (901, "Online Stock Span", "medium", "22-monotonic-stack"),
]
assert len(SEED) == 75, f"seed list has {len(SEED)} problems, expected 75"
assert len({p[0] for p in SEED}) == 75, "duplicate problem id in seed list"

INTERVALS = [1, 7, 30]  # days after solve date

# --- evaluation layer ---
# Guards so the dashboard doesn't lie at small n. At 1 problem/day a "rate" over
# 3 points is noise; below MIN_RATE_N we show "need k more" instead of a number.
MIN_RATE_N = 5
WINDOW = 10
MISTAKE_TAGS = ["off-by-one", "edge-empty", "wrong-complexity", "wrong-ds",
                "premature-code", "logic", "syntax"]


def _chron(progress):
    """Solved entries oldest-first. Everything downstream assumes this order."""
    return sorted(progress, key=lambda e: e["date"])


def rate(solved, pred, window=WINDOW):
    """(fraction matching pred, n) over the most recent `window` solved entries,
    or None when there isn't enough data to be honest about."""
    recent = _chron(solved)[-window:]
    if len(recent) < MIN_RATE_N:
        return None
    return sum(1 for e in recent if pred(e)) / len(recent), len(recent)


def optimal_first_rate(solved, window=WINDOW):
    return rate(solved, lambda e: e.get("approach") == "optimal", window)


def recognition_rate(solved, window=WINDOW):
    return rate(solved, lambda e: e.get("recognized") == "self", window)


def trend(solved, pred, window=WINDOW):
    """up / flat / down comparing the last `window` to the window before it.
    None unless BOTH windows hold at least MIN_RATE_N samples — a direction drawn
    from a 1-2 problem prior window is exactly the small-n lie we promise not to
    tell. The old `len(chron) < 2*MIN_RATE_N` guard let the prior window shrink to
    1 sample between 11 and 19 solves (window > MIN_RATE_N), so it's replaced by
    checking each slice after the fact."""
    chron = _chron(solved)
    recent, prior = chron[-window:], chron[-2 * window:-window]
    if len(recent) < MIN_RATE_N or len(prior) < MIN_RATE_N:
        return None
    r = sum(1 for e in recent if pred(e)) / len(recent)
    p = sum(1 for e in prior if pred(e)) / len(prior)
    if r - p > 0.1:
        return "up"
    if p - r > 0.1:
        return "down"
    return "flat"


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    if not n:
        return 0
    mid = n // 2
    return xs[mid] if n % 2 else (xs[mid - 1] + xs[mid]) / 2


def solve_time_trend(solved, diff, window=WINDOW):
    """(recent median minutes, prior median, direction) for one difficulty,
    or None below MIN_RATE_N. 'down' in minutes is improvement."""
    chron = [e for e in _chron(solved) if e.get("minutes")]
    chron = [e for e in chron if _diff_of(e) == diff]
    if len(chron) < MIN_RATE_N:
        return None
    recent = chron[-window:]
    prior = chron[-2 * window:-window]
    rm = _median([e["minutes"] for e in recent])
    if len(prior) < MIN_RATE_N:   # no direction off a thin prior window (same guard as trend)
        return rm, None, None
    pm = _median([e["minutes"] for e in prior])
    direction = "down" if rm < pm - 2 else "up" if rm > pm + 2 else "flat"
    return rm, pm, direction


_SEED_DIFF = {pid: diff for pid, _t, diff, _s in SEED}


def _diff_of(entry):
    return _SEED_DIFF.get(entry["id"], "")


def mistake_taxonomy(solved):
    """{tag: count} across every solved entry, tags in fixed vocabulary order."""
    counts = {t: 0 for t in MISTAKE_TAGS}
    for e in solved:
        for m in e.get("mistakes", []):
            if m in counts:
                counts[m] += 1
    return {t: c for t, c in counts.items() if c}


def attention_score(entry, overdue):
    """Higher = needs work. A weighted sum, not a model — every term is a thing
    the debrief actually observed."""
    s = 0
    c = entry.get("confidence", 3)
    s += 2 if c <= 2 else 1 if c == 3 else 0
    if entry.get("solo") in ("timeout", "wrong"):
        s += 2
    ap = entry.get("approach")
    s += 2 if ap in ("brute", "stuck") else 1 if ap == "suboptimal" else 0
    if overdue and overdue > 0:
        s += 1
    if not entry.get("reviews"):
        s += 1  # solved once, never revisited
    return s


def attention_reason(entry):
    c = entry.get("confidence", 3)
    ap = entry.get("approach")
    if ap in ("brute", "stuck"):
        return "only reached " + ap
    if entry.get("solo") in ("timeout", "wrong"):
        return "failed solo (" + entry["solo"] + ")"
    if c <= 2:
        return "low confidence"
    if ap == "suboptimal":
        return "suboptimal approach"
    if not entry.get("reviews"):
        return "never reviewed"
    return "needs a pass"


def slug(title):
    # apostrophes vanish rather than becoming separators: "1's" -> "1s", matching LC's own urls
    title = title.replace("'", "")
    keep = [c.lower() if c.isalnum() else "-" for c in title]
    out = "".join(keep)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def next_review(entry, today):
    """Next due date, or None if the problem has graduated past the last interval.

    reviews = list of dates already completed. confidence<=2 halves the interval
    so shaky problems come back sooner.
    """
    done = len(entry.get("reviews", []))
    if done >= len(INTERVALS):
        return None
    gap = INTERVALS[done]
    if entry.get("confidence", 3) <= 2:
        gap = max(1, gap // 2)
    last = entry.get("reviews", [None])[-1] if done else entry["date"]
    return date.fromisoformat(last) + timedelta(days=gap)


def streak(dates, today):
    """Consecutive days ending today or yesterday. Yesterday still counts —
    today isn't over yet, and a streak that dies at midnight is a punishment."""
    days = set(dates)
    if not days:
        return 0
    cur = today if today.isoformat() in days else today - timedelta(days=1)
    n = 0
    while cur.isoformat() in days:
        n += 1
        cur -= timedelta(days=1)
    return n


def validate(progress):
    """Fail loud with a human-readable message on bad progress.json, instead of a
    raw traceback (the file is hand-edited daily, so typos are expected). Checks:
    known id, no duplicate ids, parseable ISO date. Returns progress unchanged."""
    seen = set()
    for i, e in enumerate(progress):
        where = f"entry #{i + 1}"
        if "id" not in e or "date" not in e:
            raise ValueError(f"{where} in progress.json is missing 'id' or 'date'.")
        if e["id"] not in _SEED_DIFF:
            raise ValueError(f"{where}: id {e['id']} is not a LeetCode 75 problem. "
                             f"Check the number against the seed list.")
        if e["id"] in seen:
            raise ValueError(f"{where}: id {e['id']} appears twice. One record per problem.")
        seen.add(e["id"])
        try:
            date.fromisoformat(e["date"])
        except (ValueError, TypeError):
            raise ValueError(f"{where} (id {e['id']}): date {e['date']!r} is not YYYY-MM-DD.")
        for r in e.get("reviews", []):
            try:
                date.fromisoformat(r)
            except (ValueError, TypeError):
                raise ValueError(f"{where} (id {e['id']}): review date {r!r} is not YYYY-MM-DD.")
    return progress


def build(progress, today):
    validate(progress)
    by_id = {e["id"]: e for e in progress}
    problems = []
    for pid, title, diff, section in SEED:
        e = by_id.get(pid)
        due = next_review(e, today) if e else None
        overdue = (today - due).days if due and due <= today else None
        problems.append({
            "id": pid, "title": title, "diff": diff, "section": section,
            "slug": slug(title),
            "solved": bool(e),
            "pattern": (e or {}).get("pattern", ""),
            "confidence": (e or {}).get("confidence", 0),
            "date": (e or {}).get("date", ""),
            "minutes": (e or {}).get("minutes", 0),
            "solo": (e or {}).get("solo", ""),
            "approach": (e or {}).get("approach", ""),
            "recognized": (e or {}).get("recognized", ""),
            "mistakes": (e or {}).get("mistakes", []),
            "reviews": (e or {}).get("reviews", []),
            "due": due.isoformat() if due else "",
            "overdue": overdue,
            "attention": attention_score(e, overdue) if e else 0,
            "reason": attention_reason(e) if e else "",
        })
    stats = {
        # derived from rendered problems, not len(progress), so solved == easy+medium always
        "solved": sum(1 for p in problems if p["solved"]),
        "total": len(SEED),
        "easy": sum(1 for p in problems if p["solved"] and p["diff"] == "easy"),
        "easyTotal": sum(1 for p in SEED if p[2] == "easy"),
        "medium": sum(1 for p in problems if p["solved"] and p["diff"] == "medium"),
        "mediumTotal": sum(1 for p in SEED if p[2] == "medium"),
        "streak": streak([e["date"] for e in progress], today),
        "days": len({e["date"] for e in progress}),
        "today": today.isoformat(),
    }
    nxt = next((p for p in problems if not p["solved"]), None)
    stats["next"] = f'{nxt["id"]}. {nxt["title"]} ({nxt["diff"]})' if nxt else "all 75 done"

    # cognition rates for the header + trend charts
    ofr = optimal_first_rate(progress)
    rec = recognition_rate(progress)
    stats["optimalFirst"] = {"rate": round(ofr[0], 2), "n": ofr[1]} if ofr else None
    stats["recognition"] = {"rate": round(rec[0], 2), "n": rec[1]} if rec else None
    stats["minRateN"] = MIN_RATE_N
    stats["diagnosis"] = diagnosis(progress, problems)
    stats["mistakes"] = mistake_taxonomy(progress)
    stats["cognitionSeries"] = cognition_series(progress)
    stats["patternMastery"] = pattern_mastery(problems)
    return problems, stats


def cognition_series(solved, window=WINDOW):
    """Per-solve rolling rates, so the trend charts have a line to draw.
    Point i = rate over the window ending at solve i. Empty below MIN_RATE_N."""
    chron = _chron(solved)
    if len(chron) < MIN_RATE_N:
        return {"labels": [], "optimal": [], "recognition": []}
    labels, opt, rec = [], [], []
    for i in range(MIN_RATE_N, len(chron) + 1):
        win = chron[max(0, i - window):i]
        labels.append(chron[i - 1]["date"])
        opt.append(round(100 * sum(1 for e in win if e.get("approach") == "optimal") / len(win)))
        rec.append(round(100 * sum(1 for e in win if e.get("recognized") == "self") / len(win)))
    return {"labels": labels, "optimal": opt, "recognition": rec}


def pattern_mastery(problems):
    """Per pattern: how many, avg confidence, self-recognition %, optimal-first %.
    Sorted weakest first — the 'what am I lacking' view."""
    out = {}
    for p in problems:
        if not p["solved"] or not p["pattern"]:
            continue
        out.setdefault(p["pattern"], []).append(p)
    rows = []
    for pat, ps in out.items():
        n = len(ps)
        rows.append({
            "pattern": pat, "n": n,
            "conf": round(sum(p["confidence"] for p in ps) / n, 1),
            "recog": round(100 * sum(1 for p in ps if p["recognized"] == "self") / n),
            "optimal": round(100 * sum(1 for p in ps if p["approach"] == "optimal") / n),
        })
    rows.sort(key=lambda r: (r["optimal"], r["conf"]))
    return rows


def diagnosis(solved, problems):
    """Numbers → a coach's read. Each flag is (level, observation, action);
    level ∈ good/watch/gap. Everything n-guarded so nothing speaks before there's
    data to stand on. The action is the 'what to do about it' the observation implies."""
    flags = []
    n = len(solved)
    if n < MIN_RATE_N:
        left = MIN_RATE_N - n
        flags.append((
            "watch",
            f"Building your baseline. You've logged {n} of the {MIN_RATE_N} solves needed before "
            f"the evaluation can say anything trustworthy.",
            f"Just keep going — {left} more problem{'s' if left != 1 else ''} and the real numbers "
            f"(optimal-first rate, pattern recognition, recurring bugs) switch on. A rate over "
            f"{n} problem{'s' if n != 1 else ''} would be noise, so it stays quiet on purpose."))
        return flags

    ofr = optimal_first_rate(solved)
    if ofr:
        pct = round(100 * ofr[0])
        t = trend(solved, lambda e: e.get("approach") == "optimal")
        arrow = {"up": ", and rising", "down": ", and slipping lately", "flat": ""}.get(t, "")
        # tiers match the hero tile exactly (good >=60, watch 40-59, gap <40)
        if pct >= 60:
            flags.append((
                "good",
                f"You reach the optimal idea on your own {pct}% of the time (last {ofr[1]} problems)"
                f"{arrow}. That's the skill interviews actually test — you're not just grinding brute "
                f"force and waiting for the trick.",
                "Keep pushing the think-phase before you code. When you do miss optimal, that problem "
                "is the one worth re-solving."))
        else:
            level = "watch" if pct >= 40 else "gap"
            flags.append((
                level,
                f"You reach the optimal idea on your own {pct}% of the time (last {ofr[1]} problems)"
                f"{arrow}. Usually you get to working code but stop before the insight that removes "
                f"the extra time or space. That gap is the single biggest interview risk.",
                "In the think-phase, after you have any working idea, spend two more minutes on one "
                "question: 'what am I recomputing, and can I store it?' That question unlocks most "
                "optimal solutions on this list."))

    rec = recognition_rate(solved)
    if rec:
        pct = round(100 * rec[0])
        t = trend(solved, lambda e: e.get("recognized") == "self")
        arrow = {"up": ", trending up", "down": ", trending down", "flat": ""}.get(t, "")
        if pct >= 60:
            flags.append((
                "good",
                f"You name the right pattern before coding {pct}% of the time{arrow}. Recognition is "
                f"the thing that makes an unseen problem feel familiar.",
                "Keep reading the Trigger line in patterns.md before each session — it's paying off."))
        else:
            flags.append((
                "watch",
                f"You spot the pattern before coding {pct}% of the time{arrow} — more often you find "
                f"it only after the hint. Recognition is what turns a scary unseen problem into a "
                f"familiar one.",
                "Before each session, spend 60 seconds re-reading the Trigger column in patterns.md. "
                "You're training the 'this smells like a two-pointer problem' reflex."))

    tax = mistake_taxonomy(solved)
    if tax:
        top, cnt = max(tax.items(), key=lambda kv: kv[1])
        total = sum(tax.values())
        if cnt >= 3 and cnt / total >= 0.3:
            flags.append((
                "watch",
                f"One bug keeps coming back: {top} ({cnt} of your {total} logged mistakes). It's not "
                f"bad luck at this point — it's a habit.",
                f"Before you hit run, do a 30-second check aimed only at {top}. Naming the specific "
                f"failure mode is how you stop repeating it."))

    st = solve_time_trend(solved, "medium")
    if st and st[2] == "down":
        flags.append((
            "good",
            f"Mediums are getting faster: your median dropped from {round(st[1])} to {round(st[0])} "
            f"minutes. Speed here is recognition plus fewer false starts, not rushing.",
            "Nothing to fix — this is exactly the curve you want."))
    elif st and st[2] == "up":
        flags.append((
            "watch",
            f"Mediums are taking longer: median up from {round(st[1])} to {round(st[0])} minutes. "
            f"Could be harder sections (graphs/DP are genuinely tougher) or fatigue.",
            "If it's the harder sections, that's expected — don't read it as regression. If it's "
            "fatigue, a rest day beats a bad session."))

    overdue = [p for p in problems if p["overdue"] and p["overdue"] > 0]
    if len(overdue) >= 3:
        flags.append((
            "watch",
            f"{len(overdue)} reviews are overdue. Spaced repetition only works if the repetitions "
            f"actually happen — a solved problem you never revisit fades within weeks.",
            "Run /due and clear the queue before starting a new problem. Reviews take ~10 minutes "
            "and don't use up your daily problem."))
    return flags


def mermaid(problems):
    """Section -> Pattern -> Problem. Only solved problems get a pattern node;
    unsolved sections still appear so the map shows the whole territory."""
    lines = ["graph LR"]
    sections = list(dict.fromkeys(p["section"] for p in problems))
    for si, sec in enumerate(sections):
        sid = f"S{si}"
        members = [p for p in problems if p["section"] == sec]
        done = sum(1 for p in members if p["solved"])
        lines.append(f'  {sid}["{sec[3:].replace("-", " ")}<br/>{done}/{len(members)}"]')
        lines.append(f"  class {sid} {'secdone' if done == len(members) else 'sec'}")
        patterns = list(dict.fromkeys(p["pattern"] for p in members if p["solved"] and p["pattern"]))
        for pi, pat in enumerate(patterns):
            pid_ = f"P{si}_{pi}"
            lines.append(f'  {pid_}("{pat}")')
            lines.append(f"  class {pid_} pat")
            lines.append(f"  {sid} --> {pid_}")
            for p in members:
                if p["solved"] and p["pattern"] == pat:
                    lines.append(f'  {pid_} --> N{p["id"]}["{p["id"]}"]')
                    lines.append(f"  class N{p['id']} done")
        unsolved = [p for p in members if not p["solved"]]
        if unsolved:
            lines.append(f'  {sid} -.-> U{si}["{len(unsolved)} unsolved"]')
            lines.append(f"  class U{si} todo")
    lines.append("  classDef sec fill:#1f2937,stroke:#4b5563,color:#e5e7eb")
    lines.append("  classDef secdone fill:#065f46,stroke:#10b981,color:#d1fae5")
    lines.append("  classDef pat fill:#312e81,stroke:#6366f1,color:#e0e7ff")
    lines.append("  classDef done fill:#064e3b,stroke:#10b981,color:#a7f3d0")
    lines.append("  classDef todo fill:#111827,stroke:#374151,color:#4b5563")
    return "\n".join(lines)


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LeetCode 75 — progress</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
/* ---- theme tokens (validated data-viz palette) ---- */
:root{
  --scale:1;
  --page:#0d0d0d; --surface:#1a1a19; --surface-2:#232320;
  --ink:#ffffff; --ink-2:#e6e5dd; --muted:#a9a89f;
  --grid:#2c2c2a; --axis:#3a3a37; --border:rgba(255,255,255,.14);
  --good:#22c55e; --watch:#fab219; --gap:#f16b6b;
  --s-blue:#3987e5; --s-aqua:#1baf7a; --s-violet:#9085e9; --s-gray:#3a3a37;
  --good-ink:#4ade80; --watch-ink:#fbbf24; --gap-ink:#f87171;
  --link:#6aa6f2;
}
:root[data-theme="light"]{
  --page:#f4f3ef; --surface:#ffffff; --surface-2:#f7f6f2;
  --ink:#0b0b0b; --ink-2:#2b2b28; --muted:#5c5b56;
  --grid:#e1e0d9; --axis:#c3c2b7; --border:rgba(11,11,11,.16);
  --good:#0a8f0a; --watch:#b47600; --gap:#c62f2f;
  --s-blue:#256abf; --s-aqua:#0f8a5f; --s-violet:#4a3aa7; --s-gray:#c3c2b7;
  --good-ink:#0a7a0a; --watch-ink:#8a5a00; --gap-ink:#b02525;
  --link:#1a5fb4;
}
*{box-sizing:border-box}
html{font-size:calc(18px * var(--scale))}
body{margin:0;padding:0 0 4rem;background:var(--page);color:var(--ink);
 font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.7;
 -webkit-font-smoothing:antialiased}
.wrap{max-width:1000px;margin:0 auto;padding:0 1.25rem}
a{color:var(--link);text-decoration:underline;text-underline-offset:2px}
a:hover{text-decoration:none}
:focus-visible{outline:3px solid var(--s-blue);outline-offset:2px;border-radius:4px}

/* ---- sticky toolbar ---- */
.bar{position:sticky;top:0;z-index:50;background:var(--page);
 border-bottom:1px solid var(--border);padding:.6rem 0;margin-bottom:1.5rem}
.bar .wrap{display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
.bar h1{font-size:1.35rem;margin:0;flex:1;min-width:12ch}
.ctrl{display:flex;align-items:center;gap:.35rem}
.ctrl .cl{font-size:.8rem;color:var(--muted);margin-right:.15rem}
.btn{font:inherit;font-size:.95rem;background:var(--surface);color:var(--ink);
 border:2px solid var(--border);border-radius:8px;padding:.35rem .7rem;cursor:pointer;
 min-width:2.6rem;min-height:2.6rem;line-height:1}
.btn:hover{border-color:var(--s-blue)}
.btn[aria-pressed="true"]{background:var(--s-blue);border-color:var(--s-blue);color:#fff}

h2{font-size:1.5rem;margin:2.75rem 0 .35rem;padding-top:.5rem}
h2 .num{color:var(--muted);font-weight:600;font-size:1rem;margin-left:.5rem}
.lead{color:var(--ink-2);font-size:1.02rem;margin:.35rem 0 1.1rem;max-width:68ch}

/* ---- guidance box ---- */
.guide{background:var(--surface-2);border:1px solid var(--border);border-radius:12px;
 padding:1rem 1.15rem;margin:0 0 1.25rem;max-width:72ch}
.guide dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:.35rem .9rem}
.guide dt{font-weight:700;color:var(--muted);font-size:.85rem;text-transform:uppercase;
 letter-spacing:.04em;white-space:nowrap;padding-top:.1rem}
.guide dd{margin:0;color:var(--ink-2)}

/* ---- hero + stat tiles ---- */
.hero{background:var(--surface);border:1px solid var(--border);border-radius:16px;
 padding:1.5rem 1.6rem;margin-bottom:1.25rem;display:flex;gap:1.5rem;align-items:center;
 flex-wrap:wrap}
.hero .fig{font-size:4.5rem;font-weight:700;line-height:1;letter-spacing:-.02em}
.hero .fig.good{color:var(--good-ink)} .hero .fig.gap{color:var(--gap-ink)}
.hero .fig.watch{color:var(--watch-ink)} .hero .fig.none{color:var(--muted);font-size:2.2rem}
.hero .side{flex:1;min-width:16ch;max-width:60ch}
.hero .side .t{font-size:1.15rem;font-weight:600;margin-bottom:.2rem}
.hero .side .d{color:var(--ink-2)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.9rem;
 margin-bottom:1.25rem}
.tile{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:1.1rem 1.2rem;
 display:flex;flex-direction:column}
.tile .v{font-size:2.4rem;font-weight:700;line-height:1.05}
.tile .k{font-size:.95rem;color:var(--muted);margin-top:.25rem}
.tile .track{height:.6rem;background:var(--surface-2);border-radius:99px;overflow:hidden;margin-top:auto;
 border:1px solid var(--border)}
.tile .track>i{display:block;height:100%;background:var(--good)}

.next{background:var(--surface);border:2px solid var(--good);border-radius:14px;
 padding:1.1rem 1.3rem;margin-bottom:.5rem;font-size:1.15rem;max-width:72ch}
.next b{color:var(--good-ink)}

/* ---- diagnosis ---- */
.diag{display:flex;flex-direction:column;gap:.85rem;margin-bottom:.5rem}
.flag{background:var(--surface);border:1px solid var(--border);border-left-width:6px;
 border-radius:12px;padding:1rem 1.2rem}
.flag.good{border-left-color:var(--good)} .flag.watch{border-left-color:var(--watch)}
.flag.gap{border-left-color:var(--gap)}
.flag .hd{display:flex;align-items:center;gap:.5rem;font-weight:700;margin-bottom:.35rem;font-size:1.05rem}
.flag .ic{font-size:1.15rem;line-height:1}
.flag.good .ic,.flag.good .lv{color:var(--good-ink)}
.flag.watch .ic,.flag.watch .lv{color:var(--watch-ink)}
.flag.gap .ic,.flag.gap .lv{color:var(--gap-ink)}
.flag .lv{text-transform:uppercase;letter-spacing:.05em;font-size:.8rem}
.flag .obs{color:var(--ink);max-width:70ch} .flag .act{color:var(--ink-2);margin-top:.5rem;max-width:70ch}
.flag .act b{color:var(--ink)}

/* ---- charts ---- */
.chartbox{background:var(--surface);border:1px solid var(--border);border-radius:14px;
 padding:1.1rem 1.2rem;margin-bottom:1.25rem}
.chartbox h3{margin:0 0 .8rem;font-size:1.05rem}
.cwrap{position:relative;height:300px}
.cwrap.tall{height:600px} .cwrap.short{height:240px}
.chart-empty{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 color:var(--muted);font-size:1.05rem;text-align:center;padding:1rem}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem}
@media(max-width:720px){.grid2{grid-template-columns:1fr}}

/* ---- tables ---- */
details{margin-top:.85rem}
summary{cursor:pointer;color:var(--link);font-size:.95rem;padding:.3rem 0}
.scroll{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:1rem;font-variant-numeric:tabular-nums}
caption{text-align:left;color:var(--muted);font-size:.9rem;padding:.4rem 0}
th{text-align:left;color:var(--ink-2);font-weight:700;padding:.55rem .7rem;
 border-bottom:2px solid var(--border);white-space:nowrap}
td{padding:.55rem .7rem;border-bottom:1px solid var(--grid)}
th.num,td.num{text-align:right;font-variant-numeric:tabular-nums}
tbody tr:hover td{background:var(--surface-2)}
.tblcard{background:var(--surface);border:1px solid var(--border);border-radius:14px;
 padding:.5rem 1rem 1rem;margin-bottom:1.25rem}
.pill{display:inline-block;background:var(--surface-2);border:1px solid var(--border);
 border-radius:99px;padding:.1rem .6rem;font-size:.85rem;color:var(--ink-2)}
.easy{color:var(--good-ink);font-weight:600}.medium{color:var(--s-blue);font-weight:600}
:root[data-theme="light"] .medium{color:#1a5fb4}
.late{color:var(--gap-ink);font-weight:700}
.empty{color:var(--muted);padding:.75rem 0}
.reason{color:var(--ink-2)}
.dots{letter-spacing:2px;font-size:1.1rem}
.dots .on{color:var(--good-ink)} .dots .off{color:var(--axis)}
.bars{display:inline-flex;align-items:center;gap:.5rem}
.bars .track{height:.7rem;width:8rem;background:var(--surface-2);border:1px solid var(--border);
 border-radius:99px;overflow:hidden} .bars .track>i{display:block;height:100%;background:var(--good)}
.mermaid{background:var(--surface);border:1px solid var(--border);border-radius:14px;
 padding:1rem;overflow-x:auto;text-align:center}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
</style></head><body>

<div class="bar"><div class="wrap">
  <h1>LeetCode 75</h1>
  <div class="ctrl"><span class="cl">Text size</span>
    <button class="btn" id="tminus" aria-label="Decrease text size">A−</button>
    <button class="btn" id="treset" aria-label="Reset text size">A</button>
    <button class="btn" id="tplus" aria-label="Increase text size">A＋</button>
  </div>
  <div class="ctrl"><span class="cl">Theme</span>
    <button class="btn" id="theme" aria-pressed="false" aria-label="Toggle light and dark theme">Dark</button>
  </div>
</div></div>

<main class="wrap" id="main">
<p class="lead">One problem a day. Solo first with the timer, debrief after. This page reads
your <b>learning</b>, not just your solve count — how often you reach the optimal idea yourself,
whether you spot the pattern before coding, and what to work on next. Every number waits until it
has enough data to be honest.</p>

<div class="next" id="next"></div>
<div class="tiles" id="tiles"></div>

<h2>The one number that matters most</h2>
<p class="lead">In an interview, the test isn't "did you solve it" — it's "did you find the
efficient idea yourself." This is the share of your recent solo attempts that reached the optimal
approach <em>before</em> any help.</p>
<div class="hero" id="hero-opt"></div>
<div class="grid2">
  <div class="chartbox"><h3>Optimal-first, over time</h3>
    <div class="cwrap" role="img" aria-label="Line chart of optimal-first rate over recent solves. Numbers in the table below.">
      <canvas id="c-opt" aria-hidden="true"></canvas><div class="chart-empty" id="e-opt"></div></div>
    <details id="d-opt"><summary>Show these numbers as a table</summary>
      <div class="scroll"><table id="t-opt"></table></div></details>
  </div>
  <div class="chartbox"><h3>Pattern recognition, over time</h3>
    <div class="cwrap" role="img" aria-label="Line chart of pattern-recognition rate over recent solves. Numbers in the table below.">
      <canvas id="c-rec" aria-hidden="true"></canvas><div class="chart-empty" id="e-rec"></div></div>
    <details id="d-rec"><summary>Show these numbers as a table</summary>
      <div class="scroll"><table id="t-rec"></table></div></details>
  </div>
</div>

<h2>Your read right now</h2>
<div class="guide"><dl>
  <dt>What</dt><dd>A plain-language summary of what the numbers below are saying today.</dd>
  <dt>Colour</dt><dd><b style="color:var(--good-ink)">▲ Good</b> = keep doing it.
    <b style="color:var(--watch-ink)">● Watch</b> = worth attention.
    <b style="color:var(--gap-ink)">▼ Gap</b> = the thing to fix first.</dd>
</dl></div>
<div class="diag" id="diag"></div>

<h2>Needs attention <span class="num">weakest first</span></h2>
<p class="lead">Your solved problems, ranked by how much they still need work — low confidence,
a failed solo attempt, a brute-force-only solution, or an overdue review. Start reviews here.</p>
<div class="tblcard scroll"><table id="attention"><caption>Ranked most-to-least in need of a revisit.</caption></table></div>

<h2>Recurring mistakes</h2>
<p class="lead">The bug categories you actually hit, counted. A tall bar isn't bad luck — it's a
habit worth a targeted 30-second check before you run your code.</p>
<div class="chartbox"><div class="cwrap short" role="img" aria-label="Bar chart of mistake counts by category. Numbers in the table below.">
  <canvas id="c-mist" aria-hidden="true"></canvas><div class="chart-empty" id="e-mist">No mistakes logged yet.</div></div>
  <details id="d-mist"><summary>Show these numbers as a table</summary>
    <div class="scroll"><table id="t-mist"></table></div></details>
</div>

<h2>Pattern mastery <span class="num">weakest first</span></h2>
<p class="lead">Per pattern: how often you reached optimal, how often you recognised it, and your
average confidence. Low rows are patterns you've technically solved but haven't truly internalised.</p>
<div class="tblcard scroll"><table id="mastery"></table></div>

<h2>Progress</h2>
<p class="lead">How far through the 75 you are, and the easy/medium split. 53 of the 75 are
Medium, so most days are the longer session — pace accordingly.</p>
<div class="grid2">
  <div class="chartbox"><h3>Solved over time</h3>
    <div class="cwrap" role="img" aria-label="Cumulative solved count over time. Numbers in the table below.">
      <canvas id="c-cum" aria-hidden="true"></canvas><div class="chart-empty" id="e-cum">Nothing solved yet.</div></div>
    <details id="d-cum"><summary>Show these numbers as a table</summary>
      <div class="scroll"><table id="t-cum"></table></div></details>
  </div>
  <div class="chartbox"><h3>Difficulty</h3>
    <div class="cwrap" role="img" aria-label="Breakdown of solved easy, solved medium, and remaining problems. Numbers in the table below.">
      <canvas id="c-diff" aria-hidden="true"></canvas><div class="chart-empty" id="e-diff">Nothing solved yet.</div></div>
    <details id="d-diff"><summary>Show these numbers as a table</summary>
      <div class="scroll"><table id="t-diff"></table></div></details>
  </div>
</div>

<h2>Sections <span class="num">22 topics</span></h2>
<p class="lead">Completion across the study plan's own 22 sections, in order. The dots show your
average confidence where you've solved something.</p>
<div class="chartbox"><div class="cwrap tall" role="img" aria-label="Bar chart of solved vs remaining problems per section. Numbers in the table below.">
  <canvas id="c-sec" aria-hidden="true"></canvas></div></div>
<div class="tblcard scroll"><table id="sections"></table></div>

<h2>Review queue</h2>
<p class="lead">Spaced repetition: each solved problem returns at +1 day, +7 days, +30 days
(sooner if you were shaky). Clearing these matters more than a new problem — retention decays
without them.</p>
<div id="queue"></div>

<h2>Mind map <span class="num">section → pattern → problem</span></h2>
<p class="lead">How the pieces connect. The middle layer — the pattern — is what transfers to an
unseen interview question. Filled nodes are solved; ghosted ones are still ahead.</p>
<pre class="mermaid">__MERMAID__</pre>

<h2>Solved log</h2>
<div class="tblcard scroll"><table id="log"></table></div>
</main>

<script>
const PROBLEMS = __PROBLEMS__;
const STATS = __STATS__;
const $ = id => document.getElementById(id);
const lc = p => `https://leetcode.com/problems/${p.slug}/`;
const notes = p => `solutions/${p.section}/${p.id}-${p.slug}/notes.md`;
const cssv = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const secName = s => s.slice(3).replace(/-/g, ' ');
const confDots = c => { const n = Math.round(c);
  return `<span class="dots" aria-label="${n} of 5">${'●'.repeat(n)}`.replace(/●/g,'<span class="on">●</span>')
    + `${'○'.repeat(5-n)}`.replace(/○/g,'<span class="off">○</span>') + '</span>'; };

/* ---------- text size + theme controls ---------- */
let scale = parseFloat(localStorage.getItem('lc75-scale') || '1');
function applyScale(){ document.documentElement.style.setProperty('--scale', scale);
  localStorage.setItem('lc75-scale', scale); }
applyScale();
// floor at 1 = the 18px accessible baseline; A- never goes below it, A is the reset
$('tminus').onclick = () => { scale = Math.max(1, +(scale-0.1).toFixed(2)); applyScale(); redraw(); };
$('tplus').onclick  = () => { scale = Math.min(1.7, +(scale+0.1).toFixed(2)); applyScale(); redraw(); };
$('treset').onclick = () => { scale = 1; applyScale(); redraw(); };

const prefLight = matchMedia('(prefers-color-scheme: light)').matches;
let theme = localStorage.getItem('lc75-theme') || (prefLight ? 'light' : 'dark');
function applyTheme(){ document.documentElement.setAttribute('data-theme', theme);
  const b = $('theme'); b.textContent = theme === 'dark' ? 'Dark' : 'Light';
  b.setAttribute('aria-pressed', theme === 'light'); localStorage.setItem('lc75-theme', theme); }
applyTheme();
$('theme').onclick = () => { theme = theme === 'dark' ? 'light' : 'dark'; applyTheme(); redraw(); };

/* ---------- static content ---------- */
$('next').innerHTML = `Next up: <b>${STATS.next}</b>`;

const tiles = [
  {v:`${STATS.solved}/${STATS.total}`, k:'solved', bar:100*STATS.solved/STATS.total},
  {v:STATS.recognition ? Math.round(100*STATS.recognition.rate)+'%' : '—', k:'pattern recognition'},
  {v:STATS.streak, k:'day streak'},
  {v:PROBLEMS.filter(p=>p.overdue!==null).length, k:'reviews due'},
];
$('tiles').innerHTML = tiles.map(t => `<div class="tile"><div class="v">${t.v}</div>
  <div class="k">${t.k}</div>${t.bar!=null?`<div class="track"><i style="width:${t.bar}%"></i></div>`:''}</div>`).join('');

// hero — optimal first
(function(){
  const o = STATS.optimalFirst;
  if (!o){ const need = STATS.minRateN - STATS.solved;
    $('hero-opt').innerHTML = `<div class="fig none">not yet</div><div class="side">
      <div class="t">Need ${need} more solve${need!==1?'s':''}</div>
      <div class="d">A rate over ${STATS.solved} problem${STATS.solved!==1?'s':''} would be noise.
      This switches on at ${STATS.minRateN} solved.</div></div>`; return; }
  const pct = Math.round(100*o.rate);
  const lvl = pct>=60 ? 'good' : pct>=40 ? 'watch' : 'gap';
  const msg = pct>=60 ? "You're finding the efficient idea yourself. That's the interview skill."
    : "You reach working code but often need help to optimise. Closing this is the priority.";
  $('hero-opt').innerHTML = `<div class="fig ${lvl}">${pct}%</div><div class="side">
    <div class="t">of your last ${o.n} solo attempts reached optimal first</div>
    <div class="d">${msg}</div></div>`;
})();

// diagnosis
const ICON = {good:'▲', watch:'●', gap:'▼'};
$('diag').innerHTML = (STATS.diagnosis||[]).map(([lvl,obs,act]) =>
  `<div class="flag ${lvl}"><div class="hd"><span class="ic">${ICON[lvl]}</span>
     <span class="lv">${lvl}</span></div>
   <div class="obs">${obs}</div>${act?`<div class="act"><b>Do this:</b> ${act}</div>`:''}</div>`
).join('') || '<p class="empty">No read yet.</p>';

// attention
const att = PROBLEMS.filter(p=>p.solved && p.attention>0)
  .sort((a,b)=>b.attention-a.attention).slice(0,8);
$('attention').innerHTML = att.length
  ? '<thead><tr><th>#</th><th>Problem</th><th>Why it needs work</th><th>Pattern</th><th>Notes</th></tr></thead><tbody>'
    + att.map(p=>`<tr><td>${p.id}</td>
      <td><a href="${lc(p)}" target="_blank" rel="noopener">${p.title}</a></td>
      <td class="reason">${p.reason}</td><td><span class="pill">${p.pattern||'—'}</span></td>
      <td><a href="${notes(p)}">notes</a></td></tr>`).join('') + '</tbody>'
  : '<tbody><tr><td class="empty">Nothing flagged — either too early, or everything is solid.</td></tr></tbody>';

// pattern mastery
const pm = STATS.patternMastery||[];
$('mastery').innerHTML = pm.length
  ? '<thead><tr><th>Pattern</th><th class="num">Solved</th><th class="num">Optimal-first</th><th class="num">Recognised</th><th>Avg confidence</th></tr></thead><tbody>'
    + pm.map(r=>`<tr><td>${r.pattern}</td><td class="num">${r.n}</td><td class="num">${r.optimal}%</td>
      <td class="num">${r.recog}%</td><td>${confDots(r.conf)}</td></tr>`).join('') + '</tbody>'
  : '<tbody><tr><td class="empty">No patterns logged yet.</td></tr></tbody>';

// sections table
const secs = [...new Set(PROBLEMS.map(p=>p.section))];
$('sections').innerHTML = '<thead><tr><th>Section</th><th>Progress</th><th class="num">Done</th><th>Avg confidence</th></tr></thead><tbody>'
  + secs.map(s=>{ const m=PROBLEMS.filter(p=>p.section===s), d=m.filter(p=>p.solved);
    const c=d.length?d.reduce((a,p)=>a+p.confidence,0)/d.length:0;
    return `<tr><td>${secName(s)}</td>
      <td><span class="bars"><span class="track"><i style="width:${100*d.length/m.length}%"></i></span></span></td>
      <td class="num">${d.length}/${m.length}</td><td>${c?confDots(c):'<span class="empty">—</span>'}</td></tr>`;
  }).join('') + '</tbody>';

// review queue
const due = PROBLEMS.filter(p=>p.overdue!==null).sort((a,b)=>b.overdue-a.overdue);
$('queue').innerHTML = due.length
  ? '<div class="tblcard scroll"><table><thead><tr><th>#</th><th>Problem</th><th>Pattern</th><th>Due</th><th>Notes</th></tr></thead><tbody>'
    + due.map(p=>`<tr><td>${p.id}</td>
      <td><a href="${lc(p)}" target="_blank" rel="noopener">${p.title}</a></td>
      <td><span class="pill">${p.pattern||'—'}</span></td>
      <td class="${p.overdue>0?'late':''}">${p.overdue>0?p.overdue+' days overdue':'today'}</td>
      <td><a href="${notes(p)}">notes</a></td></tr>`).join('') + '</tbody></table></div>'
  : '<p class="empty">Nothing due. Do the next new problem.</p>';

// solved log
const log = PROBLEMS.filter(p=>p.solved).sort((a,b)=>b.date.localeCompare(a.date));
$('log').innerHTML = log.length
  ? '<thead><tr><th>Date</th><th>#</th><th>Problem</th><th>Diff</th><th>Solo</th><th>Approach</th><th>Min</th><th>Pattern</th><th>Notes</th></tr></thead><tbody>'
    + log.map(p=>`<tr><td>${p.date}</td><td>${p.id}</td>
      <td><a href="${lc(p)}" target="_blank" rel="noopener">${p.title}</a></td>
      <td class="${p.diff}">${p.diff}</td><td>${p.solo}</td><td>${p.approach||'—'}</td>
      <td>${p.minutes}</td><td><span class="pill">${p.pattern||'—'}</span></td>
      <td><a href="${notes(p)}">notes</a></td></tr>`).join('') + '</tbody>'
  : '<tbody><tr><td class="empty">Nothing yet. Day 1 is 1768. Merge Strings Alternately.</td></tr></tbody>';

/* ---------- charts (theme + size aware; rebuilt on any control change) ---------- */
let charts = [];
function fillTable(id, head, rows){
  // first column is the label; the rest are numeric -> right-aligned tabular
  const cls = i => i === 0 ? '' : ' class="num"';
  $(id).innerHTML = rows.length
    ? '<thead><tr>'+head.map((h,i)=>`<th${cls(i)}>${h}</th>`).join('')+'</tr></thead><tbody>'
      + rows.map(r=>'<tr>'+r.map((c,i)=>`<td${cls(i)}>${c}</td>`).join('')+'</tr>').join('') + '</tbody>'
    : '<tbody><tr><td class="empty">No data yet.</td></tr></tbody>';
}
function need(id, txt){ const e=$(id); if(e) e.textContent = txt; }

function draw(){
  charts.forEach(c=>c.destroy()); charts=[];
  const ink=cssv('--ink-2'), muted=cssv('--muted'), grid=cssv('--grid');
  const blue=cssv('--s-blue'), aqua=cssv('--s-aqua'), violet=cssv('--s-violet'),
        gray=cssv('--s-gray'), good=cssv('--good'), gap=cssv('--gap');
  Chart.defaults.color = ink;
  Chart.defaults.borderColor = grid;
  Chart.defaults.font.family = 'system-ui, sans-serif';
  Chart.defaults.font.size = Math.round(16 * scale);  // >= body text, scales with the control
  Chart.defaults.animation = false;
  const pctScale = {min:0,max:100,ticks:{callback:v=>v+'%'},grid:{color:grid}};
  const solved = PROBLEMS.filter(p=>p.solved).sort((a,b)=>a.date.localeCompare(b.date));

  // cumulative
  if (solved.length){ $('e-cum').style.display='none';
    const dates=[...new Set(solved.map(p=>p.date))]; let run=0;
    const cum=dates.map(d=>run+=solved.filter(p=>p.date===d).length);
    charts.push(new Chart($('c-cum'),{type:'line',
      data:{labels:dates,datasets:[{data:cum,borderColor:blue,backgroundColor:blue+'22',
        fill:true,tension:.25,pointRadius:4,pointBackgroundColor:blue,borderWidth:2}]},
      options:{maintainAspectRatio:false,plugins:{legend:{display:false}},
        scales:{y:{beginAtZero:true,ticks:{precision:0},grid:{color:grid}},x:{grid:{color:grid}}}}}));
    fillTable('t-cum',['Date','Total solved'],dates.map((d,i)=>[d,cum[i]]));
  }

  // difficulty — horizontal stacked bar w/ labels + table
  if (STATS.solved){ $('e-diff').style.display='none';
    charts.push(new Chart($('c-diff'),{type:'bar',
      data:{labels:['Problems'],datasets:[
        {label:'Easy solved',data:[STATS.easy],backgroundColor:aqua},
        {label:'Medium solved',data:[STATS.medium],backgroundColor:blue},
        {label:'Remaining',data:[STATS.total-STATS.solved],backgroundColor:gray}]},
      options:{indexAxis:'y',maintainAspectRatio:false,
        scales:{x:{stacked:true,grid:{color:grid},ticks:{precision:0}},y:{stacked:true,grid:{display:false}}},
        plugins:{legend:{position:'bottom',labels:{boxWidth:14,padding:14}}}}}));
    fillTable('t-diff',['Group','Count'],[
      ['Easy solved',`${STATS.easy} of ${STATS.easyTotal}`],
      ['Medium solved',`${STATS.medium} of ${STATS.mediumTotal}`],
      ['Remaining',STATS.total-STATS.solved]]);
  }

  // section completion
  { const done=secs.map(s=>PROBLEMS.filter(p=>p.section===s&&p.solved).length);
    const tot=secs.map(s=>PROBLEMS.filter(p=>p.section===s).length);
    charts.push(new Chart($('c-sec'),{type:'bar',
      data:{labels:secs.map(secName),datasets:[
        {label:'solved',data:done,backgroundColor:good},
        {label:'remaining',data:tot.map((t,i)=>t-done[i]),backgroundColor:gray}]},
      options:{indexAxis:'y',maintainAspectRatio:false,
        scales:{x:{stacked:true,grid:{color:grid},ticks:{precision:0}},y:{stacked:true,grid:{display:false}}},
        plugins:{legend:{position:'top',labels:{boxWidth:14,padding:14}}}}}));
  }

  // cognition trend lines
  const cs = STATS.cognitionSeries||{labels:[]};
  function trendLine(cid,eid,tid,series,colour,label){
    const gap2 = STATS.minRateN - STATS.solved;
    if(!series||!series.length){
      need(eid, gap2>0 ? `Needs ${gap2} more solve${gap2!==1?'s':''} before this means anything.`
        : 'Not enough data yet.');
      fillTable(tid,['Date',label],[]); return; }
    $(eid).style.display='none';
    charts.push(new Chart($(cid),{type:'line',
      data:{labels:cs.labels,datasets:[{data:series,borderColor:colour,backgroundColor:colour+'22',
        fill:true,tension:.3,pointRadius:3,borderWidth:2}]},
      options:{maintainAspectRatio:false,plugins:{legend:{display:false}},
        scales:{y:pctScale,x:{grid:{color:grid}}}}}));
    fillTable(tid,['Date',label],cs.labels.map((d,i)=>[d,series[i]+'%']));
  }
  trendLine('c-opt','e-opt','t-opt',cs.optimal,cssv('--good'),'Optimal-first');
  trendLine('c-rec','e-rec','t-rec',cs.recognition,violet,'Recognised');

  // mistakes
  const mist=STATS.mistakes||{}, mk=Object.keys(mist);
  if(mk.length){ $('e-mist').style.display='none';
    charts.push(new Chart($('c-mist'),{type:'bar',
      data:{labels:mk,datasets:[{data:mk.map(k=>mist[k]),backgroundColor:gap}]},
      options:{indexAxis:'y',maintainAspectRatio:false,plugins:{legend:{display:false}},
        scales:{x:{ticks:{precision:0},grid:{color:grid}},y:{grid:{display:false}}}}}));
    fillTable('t-mist',['Mistake','Count'],mk.map(k=>[k,mist[k]]));
  } else { fillTable('t-mist',['Mistake','Count'],[]); }
}

// every control change (theme OR text size) rebuilds both charts and the mind map,
// so nothing stays frozen at its initial size/colour. Charts are cheap; the mermaid
// re-render is debounced so rapid A+/A- clicks don't overlap runs (which reject).
let mermaidTimer = null;
function redraw(){ draw(); clearTimeout(mermaidTimer); mermaidTimer = setTimeout(drawMermaid, 120); }
function drawMermaid(){
  document.querySelectorAll('.mermaid').forEach(el=>{
    if(el.dataset.src) el.textContent=el.dataset.src; el.removeAttribute('data-processed'); });
  mermaid.initialize({startOnLoad:false, theme: theme==='dark'?'dark':'neutral',
    themeVariables:{fontSize: Math.round(16*scale)+'px'}});
  try { const r = mermaid.run({querySelector:'.mermaid'}); if (r && r.catch) r.catch(()=>{}); }
  catch(e){ /* mermaid re-render race — the previous render stays visible */ }
}
document.querySelectorAll('.mermaid').forEach(el=>el.dataset.src=el.textContent);
draw();
drawMermaid();
</script></body></html>
"""


def _js(obj):
    """JSON safe to inline inside a <script> block: neutralise `</script>`,
    stray `</`, and the two line-separator chars JSON allows raw but JS forbids
    in string literals. Without this, a pattern containing `</` blanks the page."""
    return (json.dumps(obj).replace("</", "<\\/")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def render(problems, stats):
    return (TEMPLATE
            .replace("__MERMAID__", mermaid(problems))
            .replace("__PROBLEMS__", _js(problems))
            .replace("__STATS__", _js(stats)))


def demo():
    """Self-checks for the only non-trivial logic here: review dates and streaks."""
    t = date(2026, 8, 1)
    # first review = solve date + 1
    assert next_review({"date": "2026-08-01", "confidence": 4, "reviews": []}, t) == date(2026, 8, 2)
    # second = last review + 7
    assert next_review({"date": "2026-08-01", "confidence": 4,
                        "reviews": ["2026-08-02"]}, t) == date(2026, 8, 9)
    # third = last review + 30
    assert next_review({"date": "2026-08-01", "confidence": 4,
                        "reviews": ["2026-08-02", "2026-08-09"]}, t) == date(2026, 9, 8)
    # graduated after 3 reviews
    assert next_review({"date": "2026-08-01", "confidence": 4,
                        "reviews": ["a", "b", "c"]}, t) is None
    # low confidence halves the gap (7 -> 3), and never goes below 1
    assert next_review({"date": "2026-08-01", "confidence": 2,
                        "reviews": ["2026-08-02"]}, t) == date(2026, 8, 5)
    assert next_review({"date": "2026-08-01", "confidence": 1, "reviews": []}, t) == date(2026, 8, 2)

    assert streak([], t) == 0
    assert streak(["2026-08-01"], t) == 1
    assert streak(["2026-07-31"], t) == 1                      # yesterday still counts
    assert streak(["2026-07-30"], t) == 0                      # two days ago does not
    assert streak(["2026-08-01", "2026-07-31", "2026-07-30"], t) == 3
    assert streak(["2026-08-01", "2026-07-30"], t) == 1        # gap breaks it

    assert slug("Best Time to Buy and Sell Stock with Transaction Fee") == \
        "best-time-to-buy-and-sell-stock-with-transaction-fee"
    assert slug("Implement Trie (Prefix Tree)") == "implement-trie-prefix-tree"
    assert slug("Longest Subarray of 1's After Deleting One Element") == \
        "longest-subarray-of-1s-after-deleting-one-element"

    probs, st = build([], t)
    assert st["solved"] == 0 and st["next"].startswith("1768.")
    probs, st = build([{"id": 1768, "date": "2026-08-01", "confidence": 3,
                        "pattern": "two-index-interleave", "minutes": 20,
                        "solo": "solved", "reviews": []}], t)
    assert st["solved"] == 1 and st["easy"] == 1 and st["next"].startswith("1071.")
    assert [p for p in probs if p["id"] == 1768][0]["due"] == "2026-08-02"

    # --- evaluation layer ---
    ids = [p[0] for p in SEED]

    def mk(i, approach="optimal", recognized="self", mistakes=None, conf=4,
           solo="solved", minutes=30, reviews=None):
        return {"id": ids[i], "date": f"2026-08-{i + 1:02d}", "confidence": conf,
                "pattern": "p", "minutes": minutes, "solo": solo, "approach": approach,
                "recognized": recognized, "mistakes": mistakes or [],
                "reviews": reviews if reviews is not None else []}

    # rate: None below MIN_RATE_N, real fraction above
    assert optimal_first_rate([mk(i) for i in range(4)]) is None
    r = optimal_first_rate([mk(i, approach="optimal" if i < 3 else "brute") for i in range(6)])
    assert r == (3 / 6, 6), r
    assert recognition_rate([mk(i, recognized="self" if i % 2 else "missed")
                             for i in range(6)])[0] == 0.5

    # trend: needs two full-ish windows; None with one
    small = [mk(i) for i in range(6)]
    assert trend(small, lambda e: e["approach"] == "optimal") is None
    improving = [mk(i, approach="brute") for i in range(10)] + \
                [mk(10 + i, approach="optimal") for i in range(10)]
    assert trend(improving, lambda e: e["approach"] == "optimal", window=10) == "up"

    # mistake taxonomy counts across entries, ignores unknown tags
    tax = mistake_taxonomy([mk(0, mistakes=["off-by-one", "logic"]),
                            mk(1, mistakes=["off-by-one", "bogus"])])
    assert tax == {"off-by-one": 2, "logic": 1}, tax

    # attention: weak brute-force timeout outranks a clean confident solve
    weak = attention_score({"confidence": 1, "solo": "timeout", "approach": "brute",
                            "reviews": []}, overdue=3)
    strong = attention_score({"confidence": 5, "solo": "solved", "approach": "optimal",
                             "reviews": ["x"]}, overdue=None)
    assert weak > strong and strong == 0, (weak, strong)

    # solve-time trend: 'down' is improvement
    slower_then_faster = [mk(i, minutes=50) for i in range(10)] + \
                         [mk(10 + i, minutes=30) for i in range(10)]
    st_med = solve_time_trend([{**e, "id": 11} for e in slower_then_faster], "medium", window=10)
    assert st_med[2] == "down", st_med

    # pattern_mastery sorts weakest (lowest optimal%) first
    pm = pattern_mastery([
        {"solved": True, "pattern": "strong", "confidence": 5, "recognized": "self", "approach": "optimal"},
        {"solved": True, "pattern": "weak", "confidence": 2, "recognized": "missed", "approach": "brute"},
    ])
    assert pm[0]["pattern"] == "weak", pm

    # diagnosis: silent-ish baseline below MIN_RATE_N, real flags above.
    # Each flag is (level, observation, action) — action must be present.
    base = diagnosis([mk(i) for i in range(3)], [])
    assert base[0][0] == "watch" and len(base[0]) == 3 and base[0][2]
    flags = diagnosis([mk(i) for i in range(8)], [])
    assert any("optimal idea on your own" in f[1] for f in flags)
    assert all(len(f) == 3 and f[2] for f in flags)  # every flag has an action

    # trend must NOT declare a direction off a thin prior window (the 11-19 solve bug):
    # 11 solves, window 10 -> prior window is 1 sample -> must return None, not "up".
    eleven = [mk(i, approach="brute") for i in range(1)] + \
             [mk(1 + i, approach="optimal") for i in range(10)]
    assert trend(eleven, lambda e: e["approach"] == "optimal", window=10) is None
    # only once both windows have >= MIN_RATE_N does a direction appear
    twenty = [mk(i, approach="brute") for i in range(10)] + \
             [mk(10 + i, approach="optimal") for i in range(10)]
    assert trend(twenty, lambda e: e["approach"] == "optimal", window=10) == "up"
    # solve_time_trend likewise: thin prior -> no direction
    st_thin = solve_time_trend([{**mk(i, minutes=30), "id": 11} for i in range(11)], "medium", window=10)
    assert st_thin[2] is None, st_thin

    # validate() rejects bad data with a clear message instead of crashing later
    for bad, needle in [
        ([{"id": 99999, "date": "2026-08-01"}], "not a LeetCode 75"),
        ([{"id": 1768, "date": "08/01/2026"}], "not YYYY-MM-DD"),
        ([{"id": 1768, "date": "2026-08-01"}, {"id": 1768, "date": "2026-08-02"}], "twice"),
        ([{"id": 1768}], "missing"),
    ]:
        try:
            validate(bad); assert False, f"validate accepted {bad}"
        except ValueError as ex:
            assert needle in str(ex), (needle, str(ex))

    # build() surfaces the eval fields onto stats and problems; solved == easy+medium
    _, st2 = build([mk(i) for i in range(6)], t)
    assert st2["optimalFirst"]["n"] == 6 and st2["optimalFirst"]["rate"] == 1.0
    assert st2["solved"] == st2["easy"] + st2["medium"] == 6
    assert isinstance(st2["diagnosis"], list) and st2["diagnosis"]

    # render() neutralises </script> in user fields so the page can't be broken
    html = render(*build([mk(0, mistakes=["</script><b>x"])], t))
    assert "</script><b>x" not in html and "<\\/script>" in html
    print("all checks passed")


if __name__ == "__main__":
    if "--test" in sys.argv:
        demo()
        sys.exit(0)
    try:
        progress = json.loads((ROOT / "progress.json").read_text())
    except json.JSONDecodeError as ex:
        sys.exit(f"progress.json is not valid JSON: {ex}. "
                 f"A trailing comma or an unquoted value is the usual cause.")
    try:
        problems, stats = build(progress, date.today())
    except ValueError as ex:
        sys.exit(f"progress.json: {ex}")
    (ROOT / "dashboard.html").write_text(render(problems, stats))
    print(f"dashboard.html — {stats['solved']}/{stats['total']} solved, "
          f"{stats['streak']} day streak, next: {stats['next']}")
