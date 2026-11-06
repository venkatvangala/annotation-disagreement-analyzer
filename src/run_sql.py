import sys
import sqlite3
import pandas as pd

pd.set_option("display.max_colwidth", 60)
pd.set_option("display.width", 200)

sql = open(sys.argv[1], encoding="utf-8").read()
conn = sqlite3.connect("data/annotations.db")
print(pd.read_sql_query(sql, conn))
conn.close()