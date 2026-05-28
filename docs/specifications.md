# Spécifications Techniques — Pipeline de Données Industrielles Safran

## 1. Contexte et objectifs

**Projet :** Pipeline de données industrielles pour Safran Data Systems  
**Objectif :** Centraliser, nettoyer, normaliser et exposer les données capteurs avioniques  
**Dataset principal :** NASA CMAPSS (Turbofan Engine Degradation Simulation)

### Acteurs
- Équipes data/qualité/ingénierie Safran (consommateurs de l'API)
- Développeur data engineer (réalisateur du pipeline)

### Contraintes techniques
- Python 3.13
- Environnement local (macOS)
- Pas de cloud, stockage SQLite
- Données non personnelles (pas de RGPD applicable, voir section 6)

---

## 2. Sources de données (C1)

Le pipeline collecte depuis 5 sources hétérogènes :

| Source | Type | Description | Lignes collectées |
|--------|------|-------------|-------------------|
| JSONPlaceholder | API REST | Simulation API interne Safran | 100 |
| NASA CMAPSS CSV | Fichiers CSV | Données capteurs moteurs turbofan | 61 893 |
| SQLite source.db | Base de données SQL | Table capteurs NASA | 20 631 |
| data/raw/bigdata/ | Big Data simulé | Duplication fichiers NASA | 41 262 |
| Wikipedia CFM56 | Scraping web | Données moteur Safran/GE CFM56 | 9 |

### Scripts de collecte
- `src/collect_data.py` — orchestration de toutes les sources
- `src/scrape_data.py` — scraping Wikipedia
- `src/convert_nasa_to_csv.py` — conversion fichiers NASA .txt → .csv
- `src/create_sql_source.py` — création base SQLite source

### Dépendances
```bash