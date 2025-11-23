import sqlite3

# Créer la connexion à la base de données
conn = sqlite3.connect('BMO_Analyse_Projet.db')
cursor = conn.cursor()

# Créer les tables
print("Création des tables...")

# Table REGION
cursor.execute('''
CREATE TABLE IF NOT EXISTS REGION (
    code_region VARCHAR(5) PRIMARY KEY, 
    nom_region VARCHAR(100) NOT NULL
)
''')

# Table FAMILLE_METIER
cursor.execute('''
CREATE TABLE IF NOT EXISTS FAMILLE_METIER (
    code_famille VARCHAR(10) PRIMARY KEY, 
    libelle_famille VARCHAR(255) NOT NULL
)
''')

# Table METIER
cursor.execute('''
CREATE TABLE IF NOT EXISTS METIER (
    code_metier VARCHAR(15) PRIMARY KEY, 
    nom_metier VARCHAR(255) NOT NULL,   
    code_famille_fk VARCHAR(10) NOT NULL,
    FOREIGN KEY (code_famille_fk) REFERENCES FAMILLE_METIER(code_famille)
)
''')

# Table DEPARTEMENT
cursor.execute('''
CREATE TABLE IF NOT EXISTS DEPARTEMENT (
    code_departement VARCHAR(5) PRIMARY KEY, 
    nom_departement VARCHAR(100) NOT NULL,  
    code_region_fk VARCHAR(5) NOT NULL,
    FOREIGN KEY (code_region_fk) REFERENCES REGION(code_region)
)
''')

# Table ANALYSE
cursor.execute('''
CREATE TABLE IF NOT EXISTS ANALYSE (
    annee INTEGER NOT NULL,
    projets_totaux INTEGER, 
    projets_difficiles INTEGER, 
    code_metier_fk VARCHAR(15) NOT NULL,
    code_departement_fk VARCHAR(5) NOT NULL,
    PRIMARY KEY (annee, code_metier_fk, code_departement_fk),
    FOREIGN KEY (code_metier_fk) REFERENCES METIER(code_metier),
    FOREIGN KEY (code_departement_fk) REFERENCES DEPARTEMENT(code_departement)
)
''')

# Valider les changements
conn.commit()

print("✓ Base de données créée avec succès!")
print("✓ Toutes les tables ont été créées:")
print("  - REGION")
print("  - FAMILLE_METIER")
print("  - METIER")
print("  - DEPARTEMENT")
print("  - ANALYSE")

# Fermer la connexion
conn.close()

print("\nLa base de données 'BMO_Analyse_Projet.db' est prête à être utilisée!")
