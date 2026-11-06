import pandas as pd

BASE = "https://storage.googleapis.com/gresearch/goemotions/data/full_dataset/"
files = ["goemotions_1.csv", "goemotions_2.csv", "goemotions_3.csv"]

df = pd.concat([pd.read_csv(BASE + f) for f in files], ignore_index=True)

print(df.shape)
print(df.columns.tolist())
print(df.head())

# keep all raters for 3000 randomly chosen comments
ids = df["id"].drop_duplicates().sample(3000, random_state=1)
sample = df[df["id"].isin(ids)]
sample.to_csv("data/raw_sample.csv", index=False)
print("Saved rows:", sample.shape[0])