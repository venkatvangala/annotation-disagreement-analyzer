import sqlite3
import pandas as pd

df = pd.read_csv("data/raw_sample.csv")
conn = sqlite3.connect("data/annotations.db")
df.to_sql("annotations", conn, if_exists="replace", index=False)
conn.close()
print("Loaded", len(df), "rows into annotations.db")