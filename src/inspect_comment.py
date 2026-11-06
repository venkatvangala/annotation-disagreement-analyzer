import sys
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/annotations.db")
df = pd.read_sql_query(
    "SELECT * FROM annotations WHERE id = ?", conn, params=(sys.argv[1],)
)
emotions = df.columns[df.columns.get_loc("admiration"):]

print("TEXT:", df["text"].iloc[0])
print()
for _, row in df.iterrows():
    chosen = [e for e in emotions if row[e] == 1]
    print(row["rater_id"], "->", ", ".join(chosen))
conn.close()