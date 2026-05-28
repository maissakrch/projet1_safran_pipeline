import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import pandas as pd
import sqlite3
from glob import glob
from logger import log
# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

API_URL = "https://jsonplaceholder.typicode.com/posts"
RAW_DATA_DIR = "data/raw/"
BIGDATA_DIR = "data/raw/bigdata/"
SQLITE_DB = "data/raw/source.db"

# ---------------------------------------------------------
# 1. Collecte depuis une API REST
# ---------------------------------------------------------

def collect_from_api():
    log("📡 Collecte depuis API REST...")
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    df_api = pd.DataFrame(data)
    log(f"✔️ API : {len(df_api)} lignes récupérées")
    return df_api

# ---------------------------------------------------------
# 2. Collecte depuis des fichiers CSV (NASA)
# ---------------------------------------------------------

def collect_from_csv():
    log("📁 Collecte depuis fichiers CSV NASA...")
    csv_files = glob(os.path.join(RAW_DATA_DIR, "*.csv"))

    if not csv_files:
        log("⚠️ Aucun fichier CSV trouvé dans data/raw/")
        return pd.DataFrame()

    df_list = [pd.read_csv(f) for f in csv_files]
    df_csv = pd.concat(df_list, ignore_index=True)
    log(f"✔️ CSV : {len(df_csv)} lignes récupérées")
    return df_csv

# ---------------------------------------------------------
# 3. Collecte depuis une base SQL (NASA)
# ---------------------------------------------------------

def collect_from_sql():
    log("🗄️ Collecte depuis base SQL NASA...")
    conn = sqlite3.connect(SQLITE_DB)
    # SELECT simple sur toute la table capteurs NASA
    # Pas de filtre ni jointure nécessaire : on collecte brut
    query = "SELECT * FROM capteurs;"
    df_sql = pd.read_sql_query(query, conn)
    conn.close()
    log(f"✔️ SQL : {len(df_sql)} lignes récupérées")
    return df_sql

# ---------------------------------------------------------
# 4. Collecte depuis une source "big data" simulée
# ---------------------------------------------------------

def collect_from_bigdata():
    log("📦 Collecte depuis source big data NASA...")
    big_files = glob(os.path.join(BIGDATA_DIR, "*.csv"))

    if not big_files:
        log("⚠️ Aucun fichier big data trouvé.")
        return pd.DataFrame()

    df_list = [pd.read_csv(f) for f in big_files]
    df_big = pd.concat(df_list, ignore_index=True)
    log(f"✔️ Big Data : {len(df_big)} lignes récupérées")
    return df_big

# ---------------------------------------------------------
# 5. Collecte depuis scraping Wikipedia (CFM56 — Safran)
# ---------------------------------------------------------

def collect_from_scraping():
    log("🌐 Collecte depuis scraping Wikipedia...")
    from scrape_data import scrape_moteurs_wikipedia
    df_scrape = scrape_moteurs_wikipedia()
    if df_scrape.empty:
        log("⚠️ Scraping : aucune donnée récupérée.")
    else:
        log(f"✔️ Scraping : {len(df_scrape)} lignes récupérées")
    return df_scrape

# ---------------------------------------------------------
# POINT D'ENTRÉE PRINCIPAL
# ---------------------------------------------------------

if __name__ == "__main__":
    log("🚀 DÉMARRAGE DE LA COLLECTE MULTI-SOURCES NASA")

    df_api = collect_from_api()
    df_csv = collect_from_csv()
    df_sql = collect_from_sql()
    df_big = collect_from_bigdata()
    df_scrape = collect_from_scraping()

    # Sauvegarde des données collectées
    os.makedirs("data/processed", exist_ok=True)
    df_api.to_csv("data/processed/api_data.csv", index=False)
    df_csv.to_csv("data/processed/csv_data.csv", index=False)
    df_sql.to_csv("data/processed/sql_data.csv", index=False)
    df_big.to_csv("data/processed/bigdata.csv", index=False)
    df_scrape.to_csv("data/processed/scrape_data.csv", index=False)

    log("💾 Données sauvegardées dans data/processed/")
    log("🎉 Collecte terminée.")