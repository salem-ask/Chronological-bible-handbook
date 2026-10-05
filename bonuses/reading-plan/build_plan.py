"""Build the 365-day chronological reading plan (HTML, then PDF via build-pdf.js).

    python3 bonuses/reading-plan/build_plan.py

Reads:
  chronological_order.py   the order of the readings
  kjv-chapter-words.json   KJV word count of every chapter (used to balance days)
  handbook-pages.json      Handbook page of each book (null = not supplied yet)
Writes:
  plan.json                the 365 days (for checking)
  reading-plan.html        printable document
"""
import html
import json
import os

from chronological_order import ORDER

HERE = os.path.dirname(os.path.abspath(__file__))
DAYS = 365
MAX_CHAPTERS_PER_DAY = 25

words = json.load(open(os.path.join(HERE, "kjv-chapter-words.json")))
pages = json.load(open(os.path.join(HERE, "handbook-pages.json")))

# ---------- 1. Flatten the order into chapters and check coverage ----------
chapters = []  # (period index, book, chapter, words, starts_segment)
for p, (_, readings) in enumerate(ORDER):
    for r in readings:
        book = r[0]
        nums = r[1] if isinstance(r[1], list) else list(range(r[1], r[2] + 1))
        for i, n in enumerate(nums):
            chapters.append((p, book, n, words[book][n - 1], i == 0))

seen = {}
for _, b, n, _, _ in chapters:
    seen[(b, n)] = seen.get((b, n), 0) + 1
expected = {(b, n + 1) for b, ws in words.items() for n in range(len(ws))}
missing = sorted(expected - set(seen))
dupes = sorted(k for k, v in seen.items() if v > 1)
assert not missing, "missing chapters: %s" % missing[:20]
assert not dupes, "duplicated chapters: %s" % dupes[:20]
assert len(chapters) == 1189

# ---------- 2. Split into 365 days of similar length (dynamic programming) ----------
total = sum(c[3] for c in chapters)
target = total / DAYS
N = len(chapters)
prefix = [0]
for c in chapters:
    prefix.append(prefix[-1] + c[3])

INF = float("inf")
# cost[d][i]: best cost covering the first i chapters in d days
cost = [[INF] * (N + 1) for _ in range(DAYS + 1)]
back = [[0] * (N + 1) for _ in range(DAYS + 1)]
cost[0][0] = 0
for d in range(1, DAYS + 1):
    lo = d  # at least one chapter per day
    hi = N - (DAYS - d)
    for i in range(lo, hi + 1):
        best, arg = INF, 0
        for j in range(max(d - 1, i - MAX_CHAPTERS_PER_DAY), i):
            prev = cost[d - 1][j]
            if prev == INF:
                continue
            w = prefix[i] - prefix[j]
            c = prev + (w - target) ** 2
            # small preference for starting a day where a new reading begins
            if not chapters[j][4]:
                c += (target * 0.08) ** 2
            if c < best:
                best, arg = c, j
        cost[d][i], back[d][i] = best, arg

bounds = []
i = N
for d in range(DAYS, 0, -1):
    j = back[d][i]
    bounds.append((j, i))
    i = j
bounds.reverse()

# ---------- 3. Format references ----------
SINGLE = {"Obadiah", "Philemon", "2 John", "3 John", "Jude"}


def fmt(chs):
    """[(book, ch), ...] -> 'Genesis 1–3; Psalms 56, 34'"""
    groups = []  # [book, [runs]]
    for b, n in chs:
        if groups and groups[-1][0] == b:
            runs = groups[-1][1]
            if runs[-1][1] + 1 == n:
                runs[-1][1] = n
            else:
                runs.append([n, n])
        else:
            groups.append([b, [[n, n]]])
    parts = []
    for b, runs in groups:
        if b in SINGLE:
            parts.append(b)
            continue
        nums = ", ".join(str(a) if a == z else "%d–%d" % (a, z) for a, z in runs)
        name = b
        if b == "Psalms" and len(runs) == 1 and runs[0][0] == runs[0][1]:
            name = "Psalm"
        parts.append("%s %s" % (name, nums))
    return "; ".join(parts)


days = []
first_seen = set()
for k, (a, z) in enumerate(bounds, 1):
    chs = chapters[a:z]
    w = sum(c[3] for c in chs)
    # Handbook reference: books that appear for the first time in the plan today
    starts = []
    for c in chs:
        if c[1] not in first_seen:
            first_seen.add(c[1])
            starts.append(c[1])
    days.append({
        "day": k,
        "period": ORDER[chs[0][0]][0],
        "reading": fmt([(c[1], c[2]) for c in chs]),
        "words": w,
        "handbook": [{"book": b, "page": pages.get(b)} for b in starts],
    })

json.dump(days, open(os.path.join(HERE, "plan.json"), "w"), indent=1, ensure_ascii=False)
ws = [d["words"] for d in days]
print("days:", len(days), "words/day: min %d, avg %d, max %d" % (min(ws), sum(ws) / len(ws), max(ws)))
print("minutes at 150 wpm: min %.1f, avg %.1f, max %.1f" % (min(ws) / 150, sum(ws) / len(ws) / 150, max(ws) / 150))

# ---------- 4. HTML ----------
e = html.escape


def hb_cell(items):
    out = []
    for it in items:
        page = str(it["page"]) if it["page"] else '<span class="blank">___</span>'
        out.append('<span class="hb">%s&nbsp;p.&nbsp;%s</span>' % (e(it["book"]), page))
    return "".join(out)


rows = []
current = None
for d in days:
    if d["period"] != current:
        current = d["period"]
        rows.append('<tr class="period"><th colspan="4" scope="colgroup">%s</th></tr>' % e(current))
    rows.append(
        '<tr><td class="chk"><span class="box"></span></td><td class="day">%d</td>'
        '<td class="ref">%s</td><td class="hbcol">%s</td></tr>'
        % (d["day"], e(d["reading"]), hb_cell(d["handbook"]))
    )

book_rows = []
for b in words:
    p = pages.get(b)
    book_rows.append('<li><span>%s</span><span class="dots"></span><span>p.&nbsp;%s</span></li>'
                     % (e(b), p if p else '<span class="blank">___</span>'))

period_rows = []
for p, (title, _) in enumerate(ORDER):
    ds = [d["day"] for d in days if d["period"] == title]
    if ds:
        period_rows.append("<li><strong>Days %d–%d</strong> %s</li>" % (ds[0], ds[-1], e(title)))

template = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
out = (template
       .replace("{{ROWS}}", "\n".join(rows))
       .replace("{{BOOKS}}", "\n".join(book_rows))
       .replace("{{PERIODS}}", "\n".join(period_rows)))
open(os.path.join(HERE, "reading-plan.html"), "w", encoding="utf-8").write(out)
print("wrote reading-plan.html")
