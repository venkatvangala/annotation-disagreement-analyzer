import csv
import os
import sqlite3
from collections import defaultdict

os.makedirs("analysis", exist_ok=True)

conn = sqlite3.connect("data/annotations.db")
conn.row_factory = sqlite3.Row
cur = conn.execute("SELECT * FROM annotations")
columns = [c[0] for c in cur.description]
emotions = columns[columns.index("admiration"):]

by_comment = defaultdict(list)
for row in cur:
    labels = frozenset(e for e in emotions if row[e] == 1)
    by_comment[row["id"]].append((row["rater_id"], row["text"], labels))
conn.close()

def jaccard(a, b):
    union = a | b
    return len(a & b) / len(union) if union else 1.0

results = []
for cid, items in by_comment.items():
    if len(items) < 3:
        continue
    sims = [jaccard(items[i][2], items[j][2])
            for i in range(len(items)) for j in range(i + 1, len(items))]
    detail = " | ".join(
        f"rater {r}: " + (", ".join(sorted(l)) or "none") for r, _, l in items
    )
    results.append({
        "id": cid,
        "text": items[0][1],
        "raters": len(items),
        "avg_agreement": round(sum(sims) / len(sims), 2),
        "labels_by_rater": detail,
        "reason": "",
    })

results.sort(key=lambda r: r["avg_agreement"])
results = results[:25]

with open("analysis/disputed_comments.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    writer.writeheader()
    writer.writerows(results)

print("Saved", len(results), "comments to analysis/disputed_comments.csv")