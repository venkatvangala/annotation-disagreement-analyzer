import sqlite3
from collections import defaultdict

conn = sqlite3.connect("data/annotations.db")
conn.row_factory = sqlite3.Row
cur = conn.execute("SELECT * FROM annotations")
cols = [c[0] for c in cur.description]
emotions = cols[cols.index("admiration"):]

by_comment = defaultdict(list)
for row in cur:
    by_comment[row["id"]].append(frozenset(e for e in emotions if row[e] == 1))
conn.close()

def jaccard(a, b):
    u = a | b
    return len(a & b) / len(u) if u else 1.0

zero = total = 0
for labels in by_comment.values():
    if len(labels) < 3:
        continue
    total += 1
    sims = [jaccard(labels[i], labels[j])
            for i in range(len(labels)) for j in range(i + 1, len(labels))]
    if sum(sims) == 0:
        zero += 1

print("Comments with 3+ raters:", total)
print("With zero agreement:", zero, f"({zero / total:.1%})")