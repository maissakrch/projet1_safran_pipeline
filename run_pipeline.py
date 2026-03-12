import subprocess
from logger import log

log("🚀 Démarrage du pipeline complet")

try:
    log("▶️ Étape 1 : Collecte des données")
    subprocess.run(["python", "src/collect_data.py"], check=True)
    log("✔️ Collecte terminée")
except Exception as e:
    log(f"❌ Erreur dans la collecte : {e}")

try:
    log("▶️ Étape 2 : Agrégation & nettoyage")
    subprocess.run(["python", "src/aggregate_data.py"], check=True)
    log("✔️ Agrégation terminée")
except Exception as e:
    log(f"❌ Erreur dans l’agrégation : {e}")

try:
    log("▶️ Étape 3 : Import dans la base finale")
    subprocess.run(["python", "src/import_to_db.py"], check=True)
    log("✔️ Import SQL terminé")
except Exception as e:
    log(f"❌ Erreur dans l’import SQL : {e}")

log("🎉 Pipeline terminé avec succès")
