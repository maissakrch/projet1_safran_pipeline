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
pip install pandas requests beautifulsoup4 python-dotenv
```

### Exécution
```bash
python src/collect_data.py
```

---

## 3. Requêtes SQL (C2)

### Requête principale — collecte depuis source.db

```sql
SELECT * FROM capteurs;
```

**Justification :** Collecte exhaustive de toutes les mesures capteurs NASA.
Pas de filtre appliqué à ce stade : le nettoyage est délégué à C3 (aggregate_data.py).
Pas de jointure nécessaire : la table `capteurs` est la seule table de la base source.

### Requêtes API — base finale final.db

```sql
-- Récupération paginée
SELECT * FROM mesures LIMIT ?;

-- Filtrage par unité moteur (requête paramétrée)
SELECT * FROM mesures WHERE unit = ?;

-- Statistiques globales
SELECT COUNT(*) as total FROM mesures;
SELECT COUNT(DISTINCT unit) as nb_unites FROM mesures;
```

**Optimisations appliquées :**
- Requêtes paramétrées (protection injection SQL)
- Pagination via LIMIT pour éviter les surcharges mémoire
- COUNT sur colonnes indexées

---

## 4. Agrégation et nettoyage (C3)

### Script : `src/aggregate_data.py`

### Opérations réalisées

| Opération | Méthode | Justification |
|-----------|---------|---------------|
| Suppression colonnes vides | `dropna(axis=1, how="all")` | Fichiers NASA contiennent 2 colonnes vides |
| Suppression lignes vides | `dropna(how="all")` | Éviter les enregistrements inutiles |
| Gestion valeurs manquantes | `fillna(mean())` | Imputation par moyenne pour stabiliser les données numériques |
| Harmonisation des types | `astype(str)` sur colonnes object | Éviter les erreurs lors de la fusion multi-sources |
| Fusion multi-sources | `pd.concat()` | Centralisation en un dataset unique |

### Résultat
- Fichier : `data/processed/final_clean_data.csv`
- Données propres, normalisées, prêtes pour import SQL

### Exécution
```bash
python src/aggregate_data.py
```

---

## 5. Base de données finale (C4)

### Modélisation Merise
- MCD : `docs/merise_mcd.png`
- MPD : `docs/merise_mpd.png`

### Entité principale : `mesures`

| Colonne | Type | Description |
|---------|------|-------------|
| unit | INTEGER | Identifiant unité moteur |
| time | INTEGER | Cycle temporel |
| op_setting_1 | REAL | Paramètre opérationnel 1 |
| op_setting_2 | REAL | Paramètre opérationnel 2 |
| op_setting_3 | REAL | Paramètre opérationnel 3 |
| sensor_1 … sensor_21 | REAL | Valeurs capteurs |
| source | TEXT | Origine de la donnée |

### Choix technique
SQLite choisi pour sa simplicité de déploiement local, sans serveur,
adapté au volume de données (~120 000 lignes) et aux contraintes du projet.

### Script d'import
```bash
python src/import_to_db.py
```

---

## 6. RGPD

Les données utilisées dans ce pipeline sont :
- Des données techniques de capteurs moteurs (NASA CMAPSS)
- Des données publiques Wikipedia
- Des données fictives (JSONPlaceholder)

**Aucune donnée personnelle n'est collectée, stockée ou traitée.**
Le registre des traitements de données personnelles est donc vide.
Aucune procédure de tri RGPD n'est nécessaire dans le cadre de ce projet.

---

## 7. API REST (C5)

### Stack technique
- Framework : FastAPI 
- Documentation : Swagger UI (OpenAPI 3.1)
- Base de données : SQLite (final.db)

### Authentification
Toutes les routes protégées (sauf `/`) requièrent une clé API dans le header :