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
print("\n=== Analyse du Taux de Tension par Métier ===")
print("\nAnnées disponibles : 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025")
print("Tapez le numéro de l'année souhaitée, ou appuyez sur Entrée pour toutes les années")

choix = input("\nVotre choix : ").strip()

if choix == "":
    ANNEE_SELECTIONNEE = None
else:
    try:
        ANNEE_SELECTIONNEE = int(choix)
        if ANNEE_SELECTIONNEE < 2018 or ANNEE_SELECTIONNEE > 2025:
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
        T2.nom_metier,
        T1.annee,
        SUM(T1.projets_totaux) AS Total_Projets,
        SUM(T1.projets_difficiles) AS Projets_Difficiles,
        ROUND((CAST(SUM(T1.projets_difficiles) AS REAL) * 100) / SUM(T1.projets_totaux), 2) AS Taux_Tension_Pct
    FROM
        ANALYSE T1
    INNER JOIN
        METIER T2 ON T1.code_metier_fk = T2.code_metier
    GROUP BY
        T2.nom_metier, T1.annee
    HAVING
        SUM(T1.projets_totaux) > 500
    ORDER BY
        T1.annee DESC, Taux_Tension_Pct DESC
    LIMIT 50;
    """
else:
    # Requête pour une année spécifique
    query = f"""
    SELECT
        T2.nom_metier,
        T1.annee,
        SUM(T1.projets_totaux) AS Total_Projets,
        SUM(T1.projets_difficiles) AS Projets_Difficiles,
        ROUND((CAST(SUM(T1.projets_difficiles) AS REAL) * 100) / SUM
        (T1.projets_totaux), 2) AS Taux_Tension_Pct
    FROM
        ANALYSE T1
    INNER JOIN
        METIER T2 ON T1.code_metier_fk = T2.code_metier
    WHERE
        T1.annee = {ANNEE_SELECTIONNEE}
    GROUP BY
        T2.nom_metier, T1.annee
    HAVING
        SUM(T1.projets_totaux) > 500
    ORDER BY
        Taux_Tension_Pct DESC
    LIMIT 5;
    """

# Exécuter la requête et afficher les résultats
try:
    df_result = pd.read_sql_query(query, conn)
    
    if ANNEE_SELECTIONNEE is None:
        print("\n=== Résultats pour TOUTES les années (Top 50) ===\n")
    else:
        print(f"\n=== Résultats pour l'année {ANNEE_SELECTIONNEE} (Top 5) ===\n")
    
    # Afficher chaque ligne séparément pour éviter la troncation
    for idx, row in df_result.iterrows():
        print(f"--- Rang {idx + 1} ---")
        print(f"Métier: {row['nom_metier']}")
        print(f"Année: {row['annee']}")
        print(f"Total Projets: {row['Total_Projets']}")
        print(f"Projets Difficiles: {row['Projets_Difficiles']}")
        print(f"Taux de Tension: {row['Taux_Tension_Pct']}%")
        print()
    
    print(f"{len(df_result)} ligne(s) retournée(s)")
except Exception as e:
    print(f"Erreur lors de l'exécution de la requête : {e}")

conn.close()
