import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import sqlite3
import pandas as pd
from logger import log

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

app = FastAPI(
    title="Safran Data Pipeline API",
    description="API REST pour accéder aux données capteurs du pipeline Safran",
    version="1.0.0"
)

DB_PATH = "data/final.db"
API_KEY = "safran-secret-key-2024"  # À mettre dans .env en production
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# ---------------------------------------------------------
# AUTHENTIFICATION
# ---------------------------------------------------------

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        log("❌ Tentative d'accès non autorisé à l'API")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API invalide ou manquante"
        )
    return api_key

# ---------------------------------------------------------
# UTILITAIRE DB
# ---------------------------------------------------------

def query_db(query, params=None):
    conn = sqlite3.connect(DB_PATH)
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ---------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------

@app.get("/", tags=["Status"])
def root():
    """Vérifie que l'API est opérationnelle."""
    log("✔️ Ping API")
    return {"message": "API du pipeline Safran opérationnelle"}

@app.get(
    "/mesures",
    tags=["Mesures"],
    summary="Récupérer un échantillon de mesures",
    description="Retourne les N premières mesures de la base finale. Par défaut 100 lignes."
)
def get_all_mesures(
    limit: int = 100,
    api_key: str = Depends(verify_api_key)
):
    log(f"📊 GET /mesures — limit={limit}")
    df = query_db(f"SELECT * FROM mesures LIMIT {limit}")
    return df.to_dict(orient="records")

@app.get(
    "/mesures/{unit_id}",
    tags=["Mesures"],
    summary="Récupérer les mesures d'une unité moteur",
    description="Retourne toutes les mesures associées à l'unité moteur spécifiée."
)
def get_mesures_by_unit(
    unit_id: int,
    api_key: str = Depends(verify_api_key)
):
    log(f"📊 GET /mesures/{unit_id}")
    # Requête paramétrée pour éviter les injections SQL
    df = query_db("SELECT * FROM mesures WHERE unit = ?", params=(unit_id,))
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune mesure trouvée pour l'unité {unit_id}"
        )
    return df.to_dict(orient="records")

@app.get(
    "/stats",
    tags=["Statistiques"],
    summary="Statistiques générales sur les mesures",
    description="Retourne le nombre total de mesures et le nombre d'unités moteur distinctes."
)
def get_stats(api_key: str = Depends(verify_api_key)):
    log("📊 GET /stats")
    df_count = query_db("SELECT COUNT(*) as total FROM mesures")
    df_units = query_db("SELECT COUNT(DISTINCT unit) as nb_unites FROM mesures")
    return {
        "total_mesures": int(df_count["total"][0]),
        "nb_unites": int(df_units["nb_unites"][0])
    }