# Projet d'Analyse BMO (Besoin en Main-d'Œuvre)

## 📊 Objectif de l'étude

Comparer les résultats du BMO sur plusieurs années (2021-2025) pour observer les tendances d'évolution des métiers et identifier quelles familles professionnelles recrutent le plus chaque année.

## 🎯 Ce que permet cette analyse

- **Anticiper les difficultés de recrutement à venir** : Identifier les métiers en tension
- **Améliorer l'orientation des demandeurs d'emploi** : Diriger vers des formations adaptées aux besoins du marché
- **Informer les décideurs** : Fournir des données sur les métiers porteurs et les dynamiques régionales
- **Suivre l'évolution du marché du travail** : Observer les tendances dans le temps

## 📁 Structure du projet

### Base de données
- **BMO_Analyse_Projet.db** : Base SQLite contenant les données d'analyse
- **Tables** :
  - `REGION` : Les régions françaises
  - `FAMILLE_METIER` : Les familles professionnelles
  - `METIER` : Les métiers détaillés
  - `DEPARTEMENT` : Les départements
  - `ANALYSE` : Table de faits contenant les projets de recrutement par année

### Scripts Python

#### 1. `creer_bdd.py`
Crée la base de données SQLite avec toutes les tables nécessaires.

```bash
python creer_bdd.py
```

#### 2. `TEST.py`
Script principal pour importer les données CSV (2018-2025) dans la base de données.
- Lit tous les fichiers DATA*.csv
- Insère les données dans les tables appropriées
- Gère les relations entre les tables

```bash
python TEST.py
```

#### 3. `Requete_tension_de_travail.py`
Analyse des métiers en tension (taux de difficulté de recrutement).
- Permet de choisir une année spécifique ou toutes les années
- Affiche les top 5 métiers avec le plus haut taux de tension
- Calcul : (Projets Difficiles / Total Projets) × 100

```bash
python Requete_tension_de_travail.py
```

#### 4. `executer_demande_travail.py`
Analyse de l'évolution de la demande de travail par région.
- Choix d'une année spécifique ou vue globale
- Classement des régions par volume de projets
- Suivi des tendances régionales

```bash
python executer_demande_travail.py
```

#### 5. `requete_concentration.py`
Identifie les départements avec la plus forte concentration du métier le plus en tension.
- Analyse géographique des difficultés de recrutement
- Focus sur les métiers critiques

```bash
python requete_concentration.py
```

### Fichiers SQL

- **Tension.sql** : Requêtes d'analyse du taux de tension par métier
- **Requête_demande_detravail** : Requêtes d'évolution de la demande par région

## 📈 Données sources

Les fichiers CSV contiennent les données BMO de 2018 à 2025 :
- `DATA2018.csv` à `DATA2025.csv`

**Colonnes principales** :
- `annee` : Année de l'enquête
- `Code métier BMO` / `Nom métier BMO` : Identification du métier
- `Famille_met` / `Lbl_fam_met` : Famille professionnelle
- `Dept` / `NomDept` : Département
- `REG` / `NOM_REG` : Région
- `met` : Nombre total de projets de recrutement
- `xmet` : Nombre de projets difficiles à recruter

## 🔧 Prérequis

```bash
pip install pandas sqlite3
```

## 🚀 Démarrage rapide

1. **Créer la base de données** :
   ```bash
   python creer_bdd.py
   ```

2. **Importer les données** :
   ```bash
   python TEST.py
   ```

3. **Lancer une analyse** :
   ```bash
   python Requete_tension_de_travail.py
   ```

## 📊 Exemples d'analyses

### Métiers en tension 2025
Les 5 métiers avec le plus haut taux de tension :
1. Techniciens télécoms et courants faibles (84,4%)
2. Charpentiers (83,3%)
3. Techniciens en maintenance électrique (82,7%)
4. Couvreurs (82,2%)
5. Techniciens en froid et climatisation (81,2%)

### Régions les plus demandeuses (2025)
1. Île-de-France : 207 638 projets
2. Occitanie : 115 639 projets
3. Provence-Alpes-Côte d'Azur : 114 415 projets

## 📝 Auteur

Projet d'analyse des données BMO - Étude des tendances du marché du travail en France

## 📄 Licence

Données sources : Enquête BMO (Besoin en Main-d'Œuvre)
