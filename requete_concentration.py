import sqlite3
import pandas as pd

# Configuration de l'affichage pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Connexion à la base de données
conn = sqlite3.connect('BMO_Analyse_Projet.db')

# Objectif : Afficher les 5 départements où le métier le plus en tension génère le plus de projets difficiles
query = """
SELECT
    T3.nom_departement,
    T4.nom_region,
    T2.nom_metier,
    SUM(T1.projets_difficiles) AS Total_Projets_Difficiles
FROM
    ANALYSE T1
INNER JOIN
    METIER T2 ON T1.code_metier_fk = T2.code_metier
INNER JOIN
    DEPARTEMENT T3 ON T1.code_departement_fk = T3.code_departement
INNER JOIN
    REGION T4 ON T3.code_region_fk = T4.code_region
WHERE
    T2.nom_metier = 'Techniciens et agents de maîtrise en assistance et support technique client et en installation et maintenance télécoms et courants faibles'
    AND T1.annee = (SELECT MAX(annee) FROM ANALYSE) 
GROUP BY
    T3.nom_departement, T4.nom_region, T2.nom_metier
ORDER BY
    Total_Projets_Difficiles DESC
LIMIT 5;
"""

# Exécuter la requête
try:
    df_result = pd.read_sql_query(query, conn)
    
    print("\n=== Top 5 Départements - Concentration du Métier en Tension ===\n")
    
    for idx, row in df_result.iterrows():
        print(f"--- Rang {idx + 1} ---")
        print(f"Département: {row['nom_departement']}")
        print(f"Région: {row['nom_region']}")
        print(f"Métier: {row['nom_metier']}")
        print(f"Projets Difficiles: {int(row['Total_Projets_Difficiles'])}")
        print()
    
    print(f"{len(df_result)} département(s) retourné(s)")
    
except Exception as e:
    print(f"Erreur lors de l'exécution de la requête : {e}")

conn.close()