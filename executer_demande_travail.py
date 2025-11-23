import sqlite3
import pandas as pd

# Configuration de l'affichage pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Connexion à la base de données
conn = sqlite3.connect('BMO_Analyse_Projet.db')

# === CHOIX DE L'ANNÉE ===
print("\n=== Évolution de la Demande de Travail par Région ===")
print("\nAnnées disponibles : 2021, 2022, 2023, 2024, 2025")
print("Tapez le numéro de l'année souhaitée, ou appuyez sur Entrée pour toutes les années")

choix = input("\nVotre choix : ").strip()

if choix == "":
    ANNEE_SELECTIONNEE = None
else:
    try:
        ANNEE_SELECTIONNEE = int(choix)
        if ANNEE_SELECTIONNEE < 2021 or ANNEE_SELECTIONNEE > 2025:
            print("Année invalide. Affichage de toutes les années.")
            ANNEE_SELECTIONNEE = None
    except ValueError:
        print("Entrée invalide. Affichage de toutes les années.")
        ANNEE_SELECTIONNEE = None

# Construire la requête selon l'année sélectionnée
if ANNEE_SELECTIONNEE is None:
    # Requête pour toutes les années
    query = """
    SELECT
        T3.nom_region,
        T1.annee,
        SUM(T1.projets_totaux) AS Demande_Totale_Regionale
    FROM
        ANALYSE T1
    INNER JOIN
        DEPARTEMENT T2 ON T1.code_departement_fk = T2.code_departement
    INNER JOIN
        REGION T3 ON T2.code_region_fk = T3.code_region
    GROUP BY
        T3.nom_region, T1.annee
    ORDER BY
        T3.nom_region, T1.annee DESC;
    """
else:
    # Requête pour une année spécifique
    query = f"""
    SELECT
        T3.nom_region,
        T1.annee,
        SUM(T1.projets_totaux) AS Demande_Totale_Regionale
    FROM
        ANALYSE T1
    INNER JOIN
        DEPARTEMENT T2 ON T1.code_departement_fk = T2.code_departement
    INNER JOIN
        REGION T3 ON T2.code_region_fk = T3.code_region
    WHERE
        T1.annee = {ANNEE_SELECTIONNEE}
    GROUP BY
        T3.nom_region, T1.annee
    ORDER BY
        Demande_Totale_Regionale DESC;
    """

# Exécuter la requête
try:
    df_result = pd.read_sql_query(query, conn)
    
    if ANNEE_SELECTIONNEE is None:
        print("\n=== Résultats pour TOUTES les années ===\n")
        
        # Grouper par région pour un affichage plus lisible
        regions = df_result['nom_region'].unique()
        
        for region in regions:
            print(f"\n{'='*60}")
            print(f"Région: {region}")
            print(f"{'='*60}")
            
            df_region = df_result[df_result['nom_region'] == region]
            
            for idx, row in df_region.iterrows():
                print(f"  Année {int(row['annee'])}: {int(row['Demande_Totale_Regionale']):,} projets".replace(',', ' '))
        
        print(f"\n\n{'='*60}")
        print(f"Total: {len(df_result)} lignes retournées")
        print(f"Nombre de régions: {len(regions)}")
        print(f"{'='*60}")
    else:
        print(f"\n=== Résultats pour l'année {ANNEE_SELECTIONNEE} ===\n")
        
        for idx, row in df_result.iterrows():
            print(f"--- Rang {idx + 1} ---")
            print(f"Région: {row['nom_region']}")
            print(f"Année: {int(row['annee'])}")
            print(f"Demande Totale: {int(row['Demande_Totale_Regionale']):,} projets".replace(',', ' '))
            print()
        
        print(f"{len(df_result)} région(s) retournée(s)")
    
except Exception as e:
    print(f"Erreur lors de l'exécution de la requête : {e}")

conn.close()
