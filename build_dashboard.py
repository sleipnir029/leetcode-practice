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
    None until two full windows of data exist — a single window has nothing to
    compare against, and inventing a direction there would be the small-n lie."""
    chron = _chron(solved)
    if len(chron) < 2 * MIN_RATE_N:
        return None
    recent, prior = chron[-window:], chron[-2 * window:-window]
    if not prior:
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
    if not prior:
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


def build(progress, today):
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
        "solved": len(progress),
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
    """Numbers → a coach's read. Each flag is (level, text); level ∈ good/watch/gap.
    Everything n-guarded so nothing speaks before there's data to stand on."""
    flags = []
    n = len(solved)
    if n < MIN_RATE_N:
        flags.append(("watch", f"Building baseline — {MIN_RATE_N - n} more solves before the "
                               f"evaluation kicks in. Rates over {n} problems would just be noise."))
        return flags

    ofr = optimal_first_rate(solved)
    if ofr:
        pct = round(100 * ofr[0])
        t = trend(solved, lambda e: e.get("approach") == "optimal")
        arrow = {"up": " (rising)", "down": " (slipping)", "flat": ""}.get(t, "")
        if pct >= 60:
            flags.append(("good", f"Optimal-first {pct}% (n={ofr[1]}){arrow} — you're finding the "
                                  f"key insight yourself, not just grinding brute force."))
        else:
            flags.append(("gap", f"Optimal-first {pct}% (n={ofr[1]}){arrow} — you reach working "
                                 f"code but often miss the optimizing insight. That's the interview gap."))

    rec = recognition_rate(solved)
    if rec:
        pct = round(100 * rec[0])
        t = trend(solved, lambda e: e.get("recognized") == "self")
        arrow = {"up": " and rising", "down": " and slipping", "flat": ""}.get(t, "")
        level = "good" if pct >= 60 else "watch"
        flags.append((level, f"Pattern recognition {pct}%{arrow} — how often you name the pattern "
                             f"before coding, not after the hint."))

    tax = mistake_taxonomy(solved)
    if tax:
        top, cnt = max(tax.items(), key=lambda kv: kv[1])
        total = sum(tax.values())
        if cnt >= 3 and cnt / total >= 0.3:
            flags.append(("watch", f"Recurring bug: {top} ({cnt} of {total} logged mistakes) — "
                                   f"worth a targeted drill."))

    st = solve_time_trend(solved, "medium")
    if st and st[2] == "down":
        flags.append(("good", f"Mediums are getting faster: median {round(st[1])}→{round(st[0])} min."))
    elif st and st[2] == "up":
        flags.append(("watch", f"Mediums slowing: median {round(st[1])}→{round(st[0])} min — "
                               f"harder sections, or fatigue?"))

    overdue = [p for p in problems if p["overdue"] and p["overdue"] > 0]
    if len(overdue) >= 3:
        flags.append(("watch", f"{len(overdue)} reviews overdue — retention decays without them; "
                               f"clear the queue before new problems."))
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
:root{color-scheme:dark}
body{margin:0;padding:2rem;background:#0b0f19;color:#e5e7eb;
 font:15px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
.wrap{max-width:1100px;margin:0 auto}
h1{font-size:1.5rem;margin:0 0 .25rem}
h2{font-size:1rem;text-transform:uppercase;letter-spacing:.08em;color:#9ca3af;
 margin:2.5rem 0 .75rem;border-bottom:1px solid #1f2937;padding-bottom:.4rem}
.sub{color:#6b7280;margin:0 0 2rem}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:.75rem}
.card{background:#111827;border:1px solid #1f2937;border-radius:10px;padding:.9rem 1rem}
.card .n{font-size:1.7rem;font-weight:600;line-height:1.1}
.card .l{font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:#6b7280;margin-top:.2rem}
.bar{height:8px;background:#1f2937;border-radius:99px;overflow:hidden;margin:.6rem 0 0}
.bar>i{display:block;height:100%;background:linear-gradient(90deg,#10b981,#34d399)}
.next{background:#111827;border:1px solid #10b981;border-radius:10px;padding:1rem;margin-top:1rem}
.next b{color:#34d399}
table{width:100%;border-collapse:collapse;font-size:.9rem}
th{text-align:left;color:#6b7280;font-weight:500;font-size:.75rem;text-transform:uppercase;
 letter-spacing:.05em;padding:.4rem .6rem;border-bottom:1px solid #1f2937}
td{padding:.45rem .6rem;border-bottom:1px solid #131a29}
tr:hover td{background:#111827}
a{color:#60a5fa;text-decoration:none}a:hover{text-decoration:underline}
.easy{color:#34d399}.medium{color:#fbbf24}
.pill{background:#1f2937;border-radius:99px;padding:.1rem .55rem;font-size:.75rem;color:#9ca3af}
.late{color:#f87171;font-weight:600}
.empty{color:#6b7280;font-style:italic;padding:1rem 0}
.scroll{overflow-x:auto}
.mini{height:6px;background:#1f2937;border-radius:99px;width:150px;display:inline-block;
 vertical-align:middle;overflow:hidden}
#sections td:nth-child(2){width:160px}
#sections td:nth-child(3){width:60px;color:#9ca3af}
#sections th:first-child,#sections td:first-child{width:200px}
.mini>i{display:block;height:100%;background:#10b981}
.dots{letter-spacing:2px;color:#4b5563}
.mermaid{background:#0d1220;border:1px solid #1f2937;border-radius:10px;padding:1rem;
 overflow-x:auto;text-align:center}
.charts{display:grid;grid-template-columns:2fr 1fr;gap:1rem}
@media(max-width:720px){.charts{grid-template-columns:1fr}}
.chartbox{background:#0d1220;border:1px solid #1f2937;border-radius:10px;padding:1rem;position:relative}
.chartbox h3{margin:0 0 .75rem;font-size:.8rem;font-weight:500;color:#9ca3af;
 text-transform:uppercase;letter-spacing:.05em}
.cwrap{position:relative;height:260px}
.section-chart{margin-top:1rem}.section-chart .cwrap{height:560px}
.chart-empty{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 color:#4b5563;font-style:italic;font-size:.9rem;pointer-events:none}
.diag{display:flex;flex-direction:column;gap:.5rem;margin:1rem 0}
.flag{border-left:3px solid;border-radius:6px;padding:.6rem .9rem;background:#111827;font-size:.92rem}
.flag.good{border-color:#10b981}.flag.watch{border-color:#fbbf24}.flag.gap{border-color:#f87171}
.flag .tag{font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;font-weight:600;
 margin-right:.5rem}
.flag.good .tag{color:#34d399}.flag.watch .tag{color:#fbbf24}.flag.gap .tag{color:#f87171}
.rategrid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem}
@media(max-width:560px){.rategrid{grid-template-columns:1fr}}
.reason{color:#9ca3af;font-size:.85rem}
</style></head><body><div class="wrap">
<h1>LeetCode 75</h1>
<p class="sub">One problem a day. Solo first, debrief after. Missing a day costs a number, nothing else.</p>

<div class="stats">
  <div class="card"><div class="n" id="s-solved"></div><div class="l">solved / 75</div>
    <div class="bar"><i id="s-bar"></i></div></div>
  <div class="card"><div class="n" id="s-streak"></div><div class="l">day streak</div></div>
  <div class="card"><div class="n" id="s-easy"></div><div class="l">easy</div></div>
  <div class="card"><div class="n" id="s-medium"></div><div class="l">medium</div></div>
  <div class="card"><div class="n" id="s-due"></div><div class="l">due for review</div></div>
</div>
<div class="next">Next up: <b id="s-next"></b></div>

<h2>Diagnosis — your read</h2>
<div class="diag" id="diag"></div>

<h2>Cognition — the interview signals</h2>
<div class="rategrid">
  <div class="chartbox"><h3>Optimal-first rate</h3>
    <div class="cwrap"><canvas id="c-opt"></canvas>
      <div class="chart-empty" id="e-opt"></div></div></div>
  <div class="chartbox"><h3>Pattern recognition rate</h3>
    <div class="cwrap"><canvas id="c-rec"></canvas>
      <div class="chart-empty" id="e-rec"></div></div></div>
</div>

<h2>Needs attention</h2>
<div id="attention"></div>

<h2>Recurring mistakes</h2>
<div class="chartbox"><div class="cwrap" style="height:220px"><canvas id="c-mist"></canvas>
  <div class="chart-empty" id="e-mist">no mistakes logged yet</div></div></div>

<h2>Pattern mastery</h2>
<div class="scroll"><table id="mastery"></table></div>

<h2>Charts</h2>
<div class="charts">
  <div class="chartbox"><h3>Cumulative progress</h3>
    <div class="cwrap"><canvas id="c-cum"></canvas>
      <div class="chart-empty" id="e-cum">no problems solved yet</div></div></div>
  <div class="chartbox"><h3>Difficulty</h3>
    <div class="cwrap"><canvas id="c-diff"></canvas>
      <div class="chart-empty" id="e-diff">nothing solved yet</div></div></div>
</div>
<div class="chartbox section-chart"><h3>Section completion</h3>
  <div class="cwrap"><canvas id="c-sec"></canvas></div></div>

<h2>Review queue</h2>
<div id="queue"></div>

<h2>Mind map — section → pattern → problem</h2>
<pre class="mermaid">__MERMAID__</pre>

<h2>Sections</h2>
<div class="scroll"><table id="sections"></table></div>

<h2>Solved log</h2>
<div class="scroll"><div id="log"></div></div>
</div>
<script>
const PROBLEMS = __PROBLEMS__;
const STATS = __STATS__;

const $ = id => document.getElementById(id);
const lc = p => `https://leetcode.com/problems/${p.slug}/`;
const notes = p => `solutions/${p.section}/${p.id}-${p.slug}/notes.md`;
const due = PROBLEMS.filter(p => p.overdue !== null);

$('s-solved').textContent = `${STATS.solved}/${STATS.total}`;
$('s-bar').style.width = (100 * STATS.solved / STATS.total) + '%';
$('s-streak').textContent = STATS.streak;
$('s-easy').textContent = `${STATS.easy}/${STATS.easyTotal}`;
$('s-medium').textContent = `${STATS.medium}/${STATS.mediumTotal}`;
$('s-due').textContent = due.length;
$('s-next').textContent = STATS.next;

// diagnosis flags
$('diag').innerHTML = (STATS.diagnosis || []).map(([lvl, text]) =>
  `<div class="flag ${lvl}"><span class="tag">${lvl}</span>${text}</div>`).join('')
  || '<p class="empty">No read yet.</p>';

// attention list — weakest solved problems first
const att = PROBLEMS.filter(p => p.solved && p.attention > 0)
  .sort((a, b) => b.attention - a.attention).slice(0, 8);
$('attention').innerHTML = att.length
  ? '<div class="scroll"><table><tr><th>#</th><th>Problem</th><th>Why</th>' +
    '<th>Pattern</th><th>Notes</th></tr>' +
    att.map(p => `<tr><td>${p.id}</td>
      <td><a href="${lc(p)}" target="_blank">${p.title}</a></td>
      <td class="reason">${p.reason}</td>
      <td><span class="pill">${p.pattern || '—'}</span></td>
      <td><a href="${notes(p)}">notes</a></td></tr>`).join('') + '</table></div>'
  : '<p class="empty">Nothing flagged — either too early, or everything solid.</p>';

// pattern mastery table
const pm = STATS.patternMastery || [];
$('mastery').innerHTML = pm.length
  ? '<tr><th>Pattern</th><th>Solved</th><th>Optimal-first</th><th>Recognized</th><th>Avg conf</th></tr>' +
    pm.map(r => `<tr><td>${r.pattern}</td><td>${r.n}</td>
      <td>${r.optimal}%</td><td>${r.recog}%</td>
      <td class="dots">${'●'.repeat(Math.round(r.conf)) + '○'.repeat(5 - Math.round(r.conf))}</td></tr>`
    ).join('')
  : '<tr><td class="empty">No patterns logged yet.</td></tr>';

if (!due.length) {
  $('queue').innerHTML = '<p class="empty">Nothing due. Do the next new problem.</p>';
} else {
  due.sort((a, b) => b.overdue - a.overdue);
  $('queue').innerHTML = '<div class="scroll"><table><tr><th>#</th><th>Problem</th>' +
    '<th>Pattern</th><th>Due</th><th>Notes</th></tr>' +
    due.map(p => `<tr><td>${p.id}</td>
      <td><a href="${lc(p)}" target="_blank">${p.title}</a></td>
      <td><span class="pill">${p.pattern || '—'}</span></td>
      <td class="${p.overdue > 0 ? 'late' : ''}">${p.overdue > 0 ? p.overdue + 'd overdue' : 'today'}</td>
      <td><a href="${notes(p)}">notes</a></td></tr>`).join('') + '</table></div>';
}

const secs = [...new Set(PROBLEMS.map(p => p.section))];
$('sections').innerHTML = '<tr><th>Section</th><th>Progress</th><th></th><th>Confidence</th></tr>' +
  secs.map(s => {
    const m = PROBLEMS.filter(p => p.section === s);
    const d = m.filter(p => p.solved);
    const c = d.length ? (d.reduce((a, p) => a + p.confidence, 0) / d.length) : 0;
    return `<tr><td>${s.slice(3).replace(/-/g, ' ')}</td>
      <td><span class="mini"><i style="width:${100 * d.length / m.length}%"></i></span></td>
      <td>${d.length}/${m.length}</td>
      <td class="dots">${c ? '●'.repeat(Math.round(c)) + '○'.repeat(5 - Math.round(c)) : '—'}</td></tr>`;
  }).join('');

const solved = PROBLEMS.filter(p => p.solved).sort((a, b) => b.date.localeCompare(a.date));
$('log').innerHTML = solved.length
  ? '<table><tr><th>Date</th><th>#</th><th>Problem</th><th>Diff</th><th>Solo</th>' +
    '<th>Min</th><th>Pattern</th><th>Notes</th></tr>' +
    solved.map(p => `<tr><td>${p.date}</td><td>${p.id}</td>
      <td><a href="${lc(p)}" target="_blank">${p.title}</a></td>
      <td class="${p.diff}">${p.diff}</td><td>${p.solo}</td><td>${p.minutes}</td>
      <td><span class="pill">${p.pattern || '—'}</span></td>
      <td><a href="${notes(p)}">notes</a></td></tr>`).join('') + '</table>'
  : '<p class="empty">Nothing yet. Day 1 is 1768. Merge Strings Alternately.</p>';

// ---- charts ----
Chart.defaults.color = '#9ca3af';
Chart.defaults.borderColor = '#1f2937';
Chart.defaults.font.family = 'ui-sans-serif, system-ui, sans-serif';
Chart.defaults.animation = false;  // static dashboard — no need to redraw every frame
const GREEN = '#10b981', AMBER = '#fbbf24', GHOST = '#1f2937';

const solvedChron = PROBLEMS.filter(p => p.solved).sort((a, b) => a.date.localeCompare(b.date));

// 1. cumulative progress — running total by date
if (solvedChron.length) {
  $('e-cum').style.display = 'none';
  const dates = [...new Set(solvedChron.map(p => p.date))];
  let run = 0;
  const cum = dates.map(d => run += solvedChron.filter(p => p.date === d).length);
  new Chart($('c-cum'), {
    type: 'line',
    data: {labels: dates, datasets: [{
      data: cum, borderColor: GREEN, backgroundColor: 'rgba(16,185,129,.15)',
      fill: true, tension: .25, pointRadius: 3, pointBackgroundColor: GREEN}]},
    options: {maintainAspectRatio: false, plugins: {legend: {display: false}},
      scales: {y: {beginAtZero: true, suggestedMax: Math.max(5, ...cum), ticks: {precision: 0}}}}
  });
}

// 2. difficulty donut — solved easy / solved medium / remaining
if (STATS.solved) {
  $('e-diff').style.display = 'none';
  new Chart($('c-diff'), {
    type: 'doughnut',
    data: {labels: ['Easy', 'Medium', 'Left'],
      datasets: [{data: [STATS.easy, STATS.medium, STATS.total - STATS.solved],
        backgroundColor: [GREEN, AMBER, GHOST], borderColor: '#0d1220', borderWidth: 2}]},
    options: {maintainAspectRatio: false, cutout: '62%',
      plugins: {legend: {position: 'bottom', labels: {boxWidth: 12}}}}
  });
}

// 3. section completion — solved stacked over remaining, one bar per section
{
  const secs = [...new Set(PROBLEMS.map(p => p.section))];
  const label = s => s.slice(3).replace(/-/g, ' ');
  const done = secs.map(s => PROBLEMS.filter(p => p.section === s && p.solved).length);
  const tot = secs.map(s => PROBLEMS.filter(p => p.section === s).length);
  new Chart($('c-sec'), {
    type: 'bar',
    data: {labels: secs.map(label), datasets: [
      {label: 'solved', data: done, backgroundColor: GREEN},
      {label: 'remaining', data: tot.map((t, i) => t - done[i]), backgroundColor: GHOST}]},
    options: {maintainAspectRatio: false, indexAxis: 'y',
      scales: {x: {stacked: true, ticks: {precision: 0}}, y: {stacked: true}},
      plugins: {legend: {position: 'top', labels: {boxWidth: 12}}}}
  });
}

// 4 & 5. cognition trend lines — only when enough data, else a "need k more" note
const cs = STATS.cognitionSeries || {labels: []};
function trendLine(canvasId, emptyId, series, colour) {
  const need = STATS.minRateN - STATS.solved;
  if (!series || !series.length) {
    $(emptyId).textContent = need > 0
      ? `need ${need} more solve${need > 1 ? 's' : ''} before this is meaningful`
      : 'not enough data yet';
    return;
  }
  $(emptyId).style.display = 'none';
  new Chart($(canvasId), {
    type: 'line',
    data: {labels: cs.labels, datasets: [{
      data: series, borderColor: colour, backgroundColor: colour + '26',
      fill: true, tension: .3, pointRadius: 2}]},
    options: {maintainAspectRatio: false, plugins: {legend: {display: false}},
      scales: {y: {min: 0, max: 100, ticks: {callback: v => v + '%'}}}}
  });
}
trendLine('c-opt', 'e-opt', cs.optimal, '#34d399');
trendLine('c-rec', 'e-rec', cs.recognition, '#818cf8');

// 6. mistake taxonomy — horizontal bar
const mist = STATS.mistakes || {};
const mkeys = Object.keys(mist);
if (mkeys.length) {
  $('e-mist').style.display = 'none';
  new Chart($('c-mist'), {
    type: 'bar',
    data: {labels: mkeys, datasets: [{data: mkeys.map(k => mist[k]),
      backgroundColor: '#f87171'}]},
    options: {maintainAspectRatio: false, indexAxis: 'y',
      plugins: {legend: {display: false}}, scales: {x: {ticks: {precision: 0}}}}
  });
}

mermaid.initialize({startOnLoad: true, theme: 'dark',
  themeVariables: {background: '#0d1220', fontSize: '13px'}});
</script></body></html>
"""


def render(problems, stats):
    return (TEMPLATE
            .replace("__MERMAID__", mermaid(problems))
            .replace("__PROBLEMS__", json.dumps(problems))
            .replace("__STATS__", json.dumps(stats)))


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

    # diagnosis: silent-ish baseline below MIN_RATE_N, real flags above
    assert diagnosis([mk(i) for i in range(3)], [])[0][0] == "watch"
    flags = diagnosis([mk(i) for i in range(8)], [])
    assert any("Optimal-first" in f[1] for f in flags)

    # build() surfaces the eval fields onto stats and problems
    _, st2 = build([mk(i) for i in range(6)], t)
    assert st2["optimalFirst"]["n"] == 6 and st2["optimalFirst"]["rate"] == 1.0
    assert isinstance(st2["diagnosis"], list) and st2["diagnosis"]
    print("all checks passed")


if __name__ == "__main__":
    if "--test" in sys.argv:
        demo()
        sys.exit(0)
    progress = json.loads((ROOT / "progress.json").read_text())
    problems, stats = build(progress, date.today())
    (ROOT / "dashboard.html").write_text(render(problems, stats))
    print(f"dashboard.html — {stats['solved']}/{stats['total']} solved, "
          f"{stats['streak']} day streak, next: {stats['next']}")
