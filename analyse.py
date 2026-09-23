import pandas as pd
import json

# ==== A.1 - Charger et inspecter ====

df = pd.read_csv("donnees/eur_usd_2026.csv")

print("--- head() : 5 premières lignes ---")
print(df.head())

print("\n--- describe() : statistiques descriptives ---")
print(df.describe())

print("\n--- dtypes : type de chaque colonne ---")
print(df.dtypes)

# ==== A.2 - Sélectionner et filtrer ====

taux = df["taux_usd"]   # une Series : une seule colonne extraite du DataFrame

# Filtre : on ne garde que les lignes où le taux dépasse 1.18
df_filtre = df[df["taux_usd"] > 1.18]
print("\n--- Lignes où le taux dépasse 1.18 ---")
print(df_filtre)

# Comparaison avec tes fonctions de la séance 2
print("\nMoyenne (pandas) :", taux.mean())
print("Minimum (pandas) :", taux.min())
print("Maximum (pandas) :", taux.max())

# ==== B.1 - Combler les trous (forward-fill) ====

df["date"] = pd.to_datetime(df["date"])   # convertit le texte en vraie date
df = df.set_index("date")                  # la date devient l'index du tableau

calendrier_complet = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")
df = df.reindex(calendrier_complet)
df = df.ffill()

print("\n--- Après reindex + forward-fill (10 premières lignes) ---")
print(df.head(10))

# ==== B.2 - Analyser ====

# Variation en % entre le premier et le dernier taux de la période
variation_pct = (df["taux_usd"].iloc[-1] / df["taux_usd"].iloc[0] - 1) * 100
print(f"\nVariation sur la période : {variation_pct:.2f} %")

# Moyenne mobile sur 7 jours
df["moyenne_mobile_7j"] = df["taux_usd"].rolling(window=7).mean()
print("\n--- Moyenne mobile 7 jours (10 dernières lignes) ---")
print(df[["taux_usd", "moyenne_mobile_7j"]].tail(10))

# Rééchantillonnage mensuel : moyenne par mois
df_mensuel = df["taux_usd"].resample("ME").mean()
print("\n--- Moyenne mensuelle (resample) ---")
print(df_mensuel)

# ==== C.1 - Récupérer une deuxième devise (GBP) ====

import urllib.request
import ssl
import certifi
import csv as csv_module

ssl_context = ssl.create_default_context(cafile=certifi.where())

url_gbp = "https://api.frankfurter.app/2026-01-01..2026-09-01?from=EUR&to=GBP"
requete_gbp = urllib.request.Request(url_gbp, headers={"User-Agent": "Mozilla/5.0"})

with urllib.request.urlopen(requete_gbp, context=ssl_context) as reponse_api:
    donnees_gbp = json.loads(reponse_api.read())

with open("donnees/eur_gbp_2026.csv", "w", newline="") as f:
    writer = csv_module.writer(f)
    writer.writerow(["date", "taux_gbp"])
    for date, valeurs in sorted(donnees_gbp["rates"].items()):
        writer.writerow([date, valeurs["GBP"]])

print("Fichier eur_gbp_2026.csv créé.")

# ==== C.1 - Réunir les deux devises avec merge ====

df_usd = pd.read_csv("donnees/eur_usd_2026.csv")
df_gbp = pd.read_csv("donnees/eur_gbp_2026.csv")

df_combine = pd.merge(df_usd, df_gbp, on="date", how="inner")

print("\n--- Jointure USD + GBP (head) ---")
print(df_combine.head())
print("\nNombre de lignes df_usd :", len(df_usd))
print("Nombre de lignes df_gbp :", len(df_gbp))
print("Nombre de lignes après merge :", len(df_combine))

# ==== C.2 - Les 4 types de jointure ====

gauche = pd.DataFrame({"cle": [1, 2], "valeur_gauche": ["a", "b"]})
droite = pd.DataFrame({"cle": [2, 3], "valeur_droite": ["x", "y"]})

print("\n--- inner ---")
print(pd.merge(gauche, droite, on="cle", how="inner"))

print("\n--- left ---")
print(pd.merge(gauche, droite, on="cle", how="left"))

print("\n--- right ---")
print(pd.merge(gauche, droite, on="cle", how="right"))

print("\n--- outer ---")
print(pd.merge(gauche, droite, on="cle", how="outer"))

# ==== D.1 / D.2 - numpy ====

tableau_taux = df_usd["taux_usd"].to_numpy()

print("\n--- numpy ---")
print("Type du tableau :", type(tableau_taux))
print("dtype :", tableau_taux.dtype)
print("Moyenne (numpy) :", tableau_taux.mean())
print("Écart-type (numpy) :", tableau_taux.std())

variations = tableau_taux[1:] - tableau_taux[:-1]
print("Variations jour à jour (5 premières) :", variations[:5])

# Broadcasting : l'opération s'applique à chaque élément du tableau
taux_en_pourcent = tableau_taux * 100
print("Taux en pourcent (5 premiers) :", taux_en_pourcent[:5])

# ==== D.3 - Aperçu de polars ====

import time
import polars as pl

df_polars = pl.read_csv("donnees/eur_usd_2026.csv")

debut = time.time()
moyenne_polars = df_polars["taux_usd"].mean()
duree_polars = time.time() - debut

debut = time.time()
moyenne_pandas = df_usd["taux_usd"].mean()
duree_pandas = time.time() - debut

print("\n--- polars vs pandas ---")
print(f"polars : moyenne={moyenne_polars}, durée={duree_polars:.6f}s")
print(f"pandas : moyenne={moyenne_pandas}, durée={duree_pandas:.6f}s")