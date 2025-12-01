import sqlite3
import pandas as pd

# Configuration de l'affichage pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Connexion à la base de données
conn = sqlite3.connect('BMO_Analyse_Projet.db')

print("\n" + "="*80)
print("ANALYSE DES FAMILLES PROFESSIONNELLES QUI RECRUTENT LE PLUS")
print("="*80)

# === REQUÊTE 1 : Top 10 des familles par année ===
query_top_familles = """
SELECT
    T1.annee,
    T3.libelle_famille,
    SUM(T1.projets_totaux) AS Total_Projets,
    SUM(T1.projets_difficiles) AS Total_Difficiles,
    ROUND((CAST(SUM(T1.projets_difficiles) AS REAL) * 100) / SUM(T1.projets_totaux), 2) AS Taux_Tension_Pct
FROM
    ANALYSE T1
INNER JOIN
    METIER T2 ON T1.code_metier_fk = T2.code_metier
INNER JOIN
    FAMILLE_METIER T3 ON T2.code_famille_fk = T3.code_famille
GROUP BY
    T1.annee, T3.libelle_famille
ORDER BY
    T1.annee DESC, Total_Projets DESC;
"""

try:
    df_familles = pd.read_sql_query(query_top_familles, conn)
    
    # Afficher le top 10 par année
    annees = sorted(df_familles['annee'].unique(), reverse=True)
    
    for annee in annees:
        print(f"\n{'='*80}")
        print(f"ANNÉE {int(annee)} - TOP 10 FAMILLES PROFESSIONNELLES")
        print(f"{'='*80}\n")
        
        df_annee = df_familles[df_familles['annee'] == annee].head(10)
        
        for idx, row in df_annee.iterrows():
            rang = (idx % 10) + 1
            print(f"Rang {rang} : {row['libelle_famille']}")
            print(f"  → Projets totaux : {int(row['Total_Projets']):,}".replace(',', ' '))
            print(f"  → Projets difficiles : {int(row['Total_Difficiles']):,}".replace(',', ' '))
            print(f"  → Taux de tension : {row['Taux_Tension_Pct']}%")
            print()
    
    # === REQUÊTE 2 : Évolution d'une famille spécifique ===
    print("\n" + "="*80)
    print("ÉVOLUTION DES FAMILLES PROFESSIONNELLES SUR TOUTES LES ANNÉES")
    print("="*80 + "\n")
    
    # Obtenir les familles qui apparaissent dans le top 10 au moins une fois
    top_familles = df_familles.groupby('libelle_famille')['Total_Projets'].sum().nlargest(10).index.tolist()
    
    for famille in top_familles:
        print(f"\n--- {famille} ---")
        df_evolution = df_familles[df_familles['libelle_famille'] == famille].sort_values('annee')
        
        for _, row in df_evolution.iterrows():
            print(f"  {int(row['annee'])} : {int(row['Total_Projets']):,} projets (tension: {row['Taux_Tension_Pct']}%)".replace(',', ' '))
    
    # === REQUÊTE 3 : Croissance/Décroissance ===
    print("\n" + "="*80)
    print("FAMILLES EN CROISSANCE VS DÉCROISSANCE (2021 → 2025)")
    print("="*80 + "\n")
    
    query_evolution = """
    WITH Debut AS (
        SELECT
            T3.libelle_famille,
            SUM(T1.projets_totaux) AS Projets_2021
        FROM
            ANALYSE T1
        INNER JOIN METIER T2 ON T1.code_metier_fk = T2.code_metier
        INNER JOIN FAMILLE_METIER T3 ON T2.code_famille_fk = T3.code_famille
        WHERE T1.annee = (SELECT MIN(annee) FROM ANALYSE)
        GROUP BY T3.libelle_famille
    ),
    Fin AS (
        SELECT
            T3.libelle_famille,
            SUM(T1.projets_totaux) AS Projets_2025
        FROM
            ANALYSE T1
        INNER JOIN METIER T2 ON T1.code_metier_fk = T2.code_metier
        INNER JOIN FAMILLE_METIER T3 ON T2.code_famille_fk = T3.code_famille
        WHERE T1.annee = (SELECT MAX(annee) FROM ANALYSE)
        GROUP BY T3.libelle_famille
    )
    SELECT
        D.libelle_famille,
        D.Projets_2021,
        F.Projets_2025,
        (F.Projets_2025 - D.Projets_2021) AS Evolution,
        ROUND(((F.Projets_2025 - D.Projets_2021) * 100.0) / D.Projets_2021, 2) AS Evolution_Pct
    FROM
        Debut D
    INNER JOIN Fin F ON D.libelle_famille = F.libelle_famille
    WHERE D.Projets_2021 > 1000  -- Filtrer les familles avec volume significatif
    ORDER BY Evolution DESC;
    """
    
    df_evolution = pd.read_sql_query(query_evolution, conn)
    
    print("\n📈 TOP 5 FAMILLES EN CROISSANCE :\n")
    for idx, row in df_evolution.head(5).iterrows():
        print(f"{idx + 1}. {row['libelle_famille']}")
        print(f"   2021: {int(row['Projets_2021']):,} → 2025: {int(row['Projets_2025']):,}".replace(',', ' '))
        print(f"   Évolution: +{int(row['Evolution']):,} projets ({row['Evolution_Pct']:+.1f}%)".replace(',', ' '))
        print()
    
    print("\n📉 TOP 5 FAMILLES EN DÉCROISSANCE :\n")
    for idx, row in df_evolution.tail(5).iterrows():
        print(f"{idx + 1}. {row['libelle_famille']}")
        print(f"   2021: {int(row['Projets_2021']):,} → 2025: {int(row['Projets_2025']):,}".replace(',', ' '))
        print(f"   Évolution: {int(row['Evolution']):,} projets ({row['Evolution_Pct']:.1f}%)".replace(',', ' '))
        print()
    
    print("\n" + "="*80)
    print("ANALYSE TERMINÉE")
    print("="*80)
    
except Exception as e:
    print(f"Erreur lors de l'exécution de la requête : {e}")

conn.close()
