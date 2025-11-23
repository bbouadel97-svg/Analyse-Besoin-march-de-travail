import pandas as pd
import glob
import os

DATA_DIR = "C:\\Users\\User\\OneDrive\\Bureau\\dossier test\\file.csv"  # dossier contenant les fichiers excel

def read_bmo_files(data_dir=DATA_DIR):
    files = sorted(glob.glob(os.path.join(data_dir, "data.csv")))
    dfs = []
    for f in files:
        # essayer plusieurs sheets si nécessaire :
        df = pd.read_excel(f, sheet_name=0)
        # extraire année depuis le nom de fichier (ex: BMO_2019.xlsx)
        year = os.path.splitext(os.path.basename(f))[0].split("_")[-1]
        df['year'] = int(year)
        dfs.append(df)
    combined = pd.concat(dfs, ignore_index=True)
    return combined

df = read_bmo_files()

# --- Normalisation basique des noms de colonnes ---
# Adapter selon les colonnes présentes dans ton fichier
rename_map = {
    'Libellé métier': 'metier',
    'Famille professionnelle':'famille',
    'Région': 'region',
    'Nb recrutements': 'recrutements',
    'Nombre de projets de recrutement': 'recrutements'
}
df.rename(columns={c: rename_map.get(c, c) for c in df.columns}, inplace=True)

# Garder colonnes utiles (adapter si nécessaire)
cols_keep = [c for c in ['year','famille','metier','region','recrutements'] if c in df.columns]
df = df[cols_keep].copy()

# Nettoyage simple
df['famille'] = df['famille'].astype(str).str.strip().str.title()
df['metier'] = df['metier'].astype(str).str.strip().str.title()
df['recrutements'] = pd.to_numeric(df['recrutements'], errors='coerce').fillna(0).astype(int)

# Agrégation par famille et année
fam_year = df.groupby(['year','famille'], as_index=False)['recrutements'].sum()

# Calculer le total par année pour parts
total_year = fam_year.groupby('year')['recrutements'].sum().rename('total_annee').reset_index()
fam_year = fam_year.merge(total_year, on='year')
fam_year['part'] = fam_year['recrutements'] / fam_year['total_annee']

# Top familles par année
def top_families_by_year(df_fam_year, year, top_n=10):
    return df_fam_year[df_fam_year['year']==year].sort_values('recrutements', ascending=False).head(top_n)

print(top_families_by_year(fam_year, 2023, top_n=10))
