import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger import log

# ---------------------------------------------------------
# Source : Wikipedia — Liste de moteurs d'avion à réaction
# Contexte Safran : données publiques sur les moteurs aéro
# ---------------------------------------------------------

URL = "https://en.wikipedia.org/wiki/CFM_International_CFM56"
def scrape_moteurs_wikipedia():
    log("🌐 Scraping Wikipedia — moteurs aéro...")

    headers = {"User-Agent": "Mozilla/5.0 (compatible; SafranPipelineBot/1.0)"}
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Récupère le premier tableau de la page
    tables = soup.find_all("table", {"class": "infobox"})
    table = tables[0] if tables else None

    if table is None:
        log("⚠️ Aucun tableau trouvé sur la page Wikipedia.")
        return pd.DataFrame()

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            rows.append(cells)

    # Ajuste les colonnes si nécessaire
    df = pd.DataFrame(rows)
    if len(headers) == df.shape[1]:
        df.columns = headers

    log(f"✔️ Scraping terminé : {len(df)} lignes récupérées")
    return df


if __name__ == "__main__":
    df = scrape_moteurs_wikipedia()
    if not df.empty:
        df.to_csv("data/processed/scrape_data.csv", index=False)
        log("💾 Fichier créé : data/processed/scrape_data.csv")
        print(df.head())