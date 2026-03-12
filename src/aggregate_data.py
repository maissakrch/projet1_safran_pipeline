import pandas as pd
import os
from logger import log


# ---------------------------------------------------------
# 1. Charger les données collectées
# ---------------------------------------------------------

def load_all_sources():
    def load_if_exists(path):
        return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

    df_api = load_if_exists("data/processed/api_data.csv")
    df_csv = load_if_exists("data/processed/csv_data.csv")
    df_sql = load_if_exists("data/processed/sql_data.csv")
    df_big = load_if_exists("data/processed/bigdata.csv")

    return df_api, df_csv, df_sql, df_big

# ---------------------------------------------------------
# 2. Nettoyage des données
# ---------------------------------------------------------

def clean_dataframe(df):
    if df.empty:
        return df

    # Supprimer colonnes vides
    df = df.dropna(axis=1, how="all")

    # Supprimer lignes vides
    df = df.dropna(how="all")

    # Remplacer valeurs manquantes par la moyenne
    df = df.fillna(df.mean(numeric_only=True))

    # Harmoniser les types
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str)

    return df

# ---------------------------------------------------------
# 3. Fusionner toutes les sources
# ---------------------------------------------------------

def merge_sources(df_api, df_csv, df_sql, df_big):
    dfs = [df for df in [df_api, df_csv, df_sql, df_big] if not df.empty]
    df_merged = pd.concat(dfs, ignore_index=True)
    return df_merged

# ---------------------------------------------------------
# POINT D’ENTRÉE
# ---------------------------------------------------------

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DE L’AGRÉGATION & NETTOYAGE")

    df_api, df_csv, df_sql, df_big = load_all_sources()

    df_api = clean_dataframe(df_api)
    df_csv = clean_dataframe(df_csv)
    df_sql = clean_dataframe(df_sql)
    df_big = clean_dataframe(df_big)

    df_final = merge_sources(df_api, df_csv, df_sql, df_big)

    df_final.to_csv("data/processed/final_clean_data.csv", index=False)

    print(f"✔️ Données nettoyées et fusionnées : {len(df_final)} lignes")
    print("💾 Fichier créé : data/processed/final_clean_data.csv")
