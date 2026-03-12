import sqlite3
import pandas as pd
from logger import log


DB_PATH = "data/final.db"
CSV_PATH = "data/processed/final_clean_data.csv"

if __name__ == "__main__":
    print("🚀 Import des données dans la base finale...")

    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)

    df.to_sql("mesures", conn, if_exists="replace", index=False)

    conn.close()

    print("✔️ Base finale créée : data/final.db")
    print("✔️ Table 'mesures' importée avec succès")
