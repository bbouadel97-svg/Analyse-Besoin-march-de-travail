import pandas as pd
import sqlite3

# 1. Configuration et Connexion
DB_NAME = 'C:\\Users\\User\\OneDrive\\Bureau\\dossier test\\BMO_Analyse_Projet.db'
CSV_FOLDER = 'C:\\Users\\User\\OneDrive\\Bureau\\dossier test\\'

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print("Connexion à la base de données réussie.\n")
except Exception as e:
    print(f"Erreur de connexion : {e}")
    exit()

# 2. Lecture et traitement de tous les fichiers CSV (2018 à 2025)
all_dataframes = []

for annee in range(2018, 2026):  # 2018 à 2025 inclus
    csv_file = f'{CSV_FOLDER}DATA{annee}.csv'
    
    try:
        print(f"Lecture du fichier DATA{annee}.csv...")
        df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
        print(f"  ✓ Fichier lu. Nombre de lignes : {len(df)}")
        all_dataframes.append(df)
    except FileNotFoundError:
        print(f"  ✗ Erreur: Le fichier DATA{annee}.csv n'a pas été trouvé.")
    except Exception as e:
        print(f"  ✗ Erreur lors de la lecture de DATA{annee}.csv : {e}")

# 3. Combiner tous les DataFrames
if all_dataframes:
    df_combined = pd.concat(all_dataframes, ignore_index=True)
    print(f"\n✓ Tous les fichiers ont été combinés. Total de lignes : {len(df_combined)}")
else:
    print("\n✗ Aucun fichier CSV n'a pu être lu.")
    conn.close()
    exit()

# --- FONCTIONS D'INSERTION DANS L'ORDRE ---

def insert_regions(dataframe, cursor, conn):
    print("\n--- 1/5 Insertion REGION ---")
    df_region = dataframe[['REG', 'NOM_REG']].drop_duplicates().dropna(subset=['REG', 'NOM_REG'])
    sql_insert = "INSERT OR IGNORE INTO REGION (code_region, nom_region) VALUES (?, ?)"
    data_to_insert = [(row['REG'], row['NOM_REG']) for _, row in df_region.iterrows()]
    cursor.executemany(sql_insert, data_to_insert)
    conn.commit()
    print(f"Insertion de {len(df_region)} régions uniques terminée.")

def insert_familles(dataframe, cursor, conn):
    print("\n--- 2/5 Insertion FAMILLE_METIER ---")
    df_famille = dataframe[['Famille_met', 'Lbl_fam_met']].drop_duplicates().dropna(subset=['Famille_met'])
    sql_insert = "INSERT OR IGNORE INTO FAMILLE_METIER (code_famille, libelle_famille) VALUES (?, ?)"
    data_to_insert = [(row['Famille_met'], row['Lbl_fam_met']) for _, row in df_famille.iterrows()]
    cursor.executemany(sql_insert, data_to_insert)
    conn.commit()
    print(f"Insertion de {len(df_famille)} familles de métiers uniques terminée.")

def insert_departements(dataframe, cursor, conn):
    print("\n--- 3/5 Insertion DEPARTEMENT ---")
    df_departement = dataframe[['Dept', 'NomDept', 'REG']].drop_duplicates().dropna(subset=['Dept'])
    sql_insert = "INSERT OR IGNORE INTO DEPARTEMENT (code_departement, nom_departement, code_region_fk) VALUES (?, ?, ?)"
    data_to_insert = [(row['Dept'], row['NomDept'], row['REG']) for _, row in df_departement.iterrows()]
    cursor.executemany(sql_insert, data_to_insert)
    conn.commit()
    print(f"Insertion de {len(df_departement)} départements uniques terminée.")

def insert_metiers(dataframe, cursor, conn):
    print("\n--- 4/5 Insertion METIER ---")
    df_metier = dataframe[['Code métier BMO', 'Nom métier BMO', 'Famille_met']].drop_duplicates().dropna(subset=['Code métier BMO'])
    sql_insert = "INSERT OR IGNORE INTO METIER (code_metier, nom_metier, code_famille_fk) VALUES (?, ?, ?)"
    data_to_insert = [(row['Code métier BMO'], row['Nom métier BMO'], row['Famille_met']) for _, row in df_metier.iterrows()]
    cursor.executemany(sql_insert, data_to_insert)
    conn.commit()
    print(f"Insertion de {len(df_metier)} métiers uniques terminée.")

def insert_analyse(dataframe, cursor, conn):
    print("\n--- 5/5 Insertion ANALYSE (Faits) ---")
    # Sélection et renommage des colonnes pour correspondre aux noms de la table SQL
    df_analyse = dataframe[[
        'annee', 'met', 'xmet', 'Code métier BMO', 'Dept'
    ]].rename(columns={
        'met': 'projets_totaux',
        'xmet': 'projets_difficiles',
        'Code métier BMO': 'code_metier_fk',
        'Dept': 'code_departement_fk'
    }).dropna(subset=['code_metier_fk', 'code_departement_fk'])
    
    # Supprimer les doublons basés sur la clé primaire composite
    df_analyse = df_analyse.drop_duplicates(subset=['annee', 'code_metier_fk', 'code_departement_fk'])
    
    sql_insert = """
    INSERT OR REPLACE INTO ANALYSE (annee, projets_totaux, projets_difficiles, code_metier_fk, code_departement_fk)
    VALUES (?, ?, ?, ?, ?)
    """   
    data_to_insert = df_analyse[[
        'annee', 'projets_totaux', 'projets_difficiles', 'code_metier_fk', 'code_departement_fk'
    ]].values.tolist()
    
    cursor.executemany(sql_insert, data_to_insert)
    conn.commit()
    print(f"Insertion de {len(data_to_insert)} lignes d'analyse terminée.")

if __name__ == '__main__':
    insert_regions(df_combined, cursor, conn)
    insert_familles(df_combined, cursor, conn)
    insert_departements(df_combined, cursor, conn) # Dépend de REGION
    insert_metiers(df_combined, cursor, conn)     # Dépend de FAMILLE_METIER
    insert_analyse(df_combined, cursor, conn)     # Dépend de METIER et DEPARTEMENT
    
    conn.close()
    print("\n✅ Processus d'intégration des données terminé.")
