import sqlite3
import pandas as pd
from logger import log


df = pd.read_csv("data/raw/train_FD001.csv")

conn = sqlite3.connect("data/raw/source.db")
df.to_sql("capteurs", conn, if_exists="replace", index=False)
conn.close()

print("✔️ Base SQL créée : source.db avec table 'capteurs'")
