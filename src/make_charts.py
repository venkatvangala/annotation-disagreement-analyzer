import os
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("images", exist_ok=True)

conn = sqlite3.connect("data/annotations.db")
df = pd.read_sql_query("SELECT * FROM annotations", conn)
conn.close()

emotions = list(df.columns[df.columns.get_loc("admiration"):])
df["labels"] = df[emotions].apply(
    lambda r: frozenset(e for e in emotions if r[e] == 1), axis=1
)

def jaccard(a, b):
    union = a | b
    return len(a & b) / len(union) if union else 1.0

rows = []
for cid, g in df.groupby("id"):
    items = list(zip(g["rater_id"], g["labels"]))
    for i, (r1, l1) in enumerate(items):
        for j, (r2, l2) in enumerate(items):
            if i != j:
                rows.append((r1, jaccard(l1, l2)))

pairs = pd.DataFrame(rows, columns=["rater_id", "similarity"])
board = pairs.groupby("rater_id")["similarity"].mean().to_frame("avg_agreement")
board["annotations"] = df.groupby("rater_id").size()
board["avg_labels"] = df.assign(n=df["labels"].apply(len)).groupby("rater_id")["n"].mean()
board = board[board["annotations"] >= 20]
overall = pairs["similarity"].mean()

# Chart 1: labels per item vs agreement, one dot per rater
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(board["avg_labels"], board["avg_agreement"],
           s=board["annotations"] / 2, alpha=0.6)
ax.axhline(overall, linestyle="--", color="gray")
ax.text(board["avg_labels"].max(), overall + 0.005,
        f"overall avg {overall:.2f}", ha="right", color="gray")
for rid in [31, 79, 11]:
    if rid in board.index:
        ax.annotate(f"rater {rid}",
                    (board.loc[rid, "avg_labels"], board.loc[rid, "avg_agreement"]))
ax.set_xlabel("Average labels chosen per comment")
ax.set_ylabel("Average agreement with other raters (0-1)")
ax.set_title("Rater behavior vs agreement (dot size = number of annotations)")
fig.tight_layout()
fig.savefig("images/rater_scatter.png", dpi=150)

# Chart 2: distribution of rater agreement
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(board["avg_agreement"], bins=15)
ax.axvline(overall, linestyle="--", color="gray")
ax.set_xlabel("Average agreement with other raters (0-1)")
ax.set_ylabel("Number of raters")
ax.set_title("How much raters agree with each other")
fig.tight_layout()
fig.savefig("images/agreement_hist.png", dpi=150)

print("Saved 2 charts in images/")