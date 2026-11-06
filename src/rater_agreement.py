import sqlite3
import pandas as pd

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
board = board[board["annotations"] >= 20].round(2)

print("Overall average agreement:", round(pairs["similarity"].mean(), 2))
print()
print("Lowest agreement raters:")
print(board.sort_values("avg_agreement").head(10))
print()
print("Rater 31:")
print(board.loc[[31]])