import pandas as pd

# ==== A.1 - Les compréhensions ====

df = pd.read_csv("donnees/eur_usd_2026.csv")
taux_liste = df["taux_usd"].tolist()

# --- Façon "classique" (boucle for) ---
variations_boucle = []
for i in range(1, len(taux_liste)):
    variations_boucle.append(taux_liste[i] - taux_liste[i - 1])

# --- Façon "compréhension de liste" (équivalent, plus court) ---
variations_comprehension = [taux_liste[i] - taux_liste[i - 1] for i in range(1, len(taux_liste))]

print("Identiques ?", variations_boucle == variations_comprehension)
print("5 premières variations :", variations_comprehension[:5])

# --- Compréhension de dictionnaire ---
dates = df["date"].tolist()
dict_taux = {date: taux for date, taux in zip(dates, taux_liste)}
print("Premier élément du dictionnaire :", list(dict_taux.items())[0])

# ==== A.2 - enumerate, zip, sorted ====

# enumerate : parcourir avec l'indice ET la valeur
for i, taux in enumerate(taux_liste[:5]):
    print(f"Jour {i} : {taux}")

# zip : associer deux listes élément par élément
for date, taux in zip(dates[:5], taux_liste[:5]):
    print(date, "->", taux)

# sorted avec key : trier une liste de couples selon un critère précis
couples = list(zip(dates, taux_liste))
couples_tries = sorted(couples, key=lambda c: c[1])  # trie par taux croissant

print("\n5 taux les plus bas :")
for date, taux in couples_tries[:5]:
    print(date, taux)

# ==== A.3 - f-strings, lambda, map/filter ====

# f-string : formater un nombre avec 2 décimales
exemple_taux = taux_liste[0]
print(f"Taux formaté : {exemple_taux:.2f}")

# lambda : une fonction "anonyme", écrite en une ligne
double = lambda x: x * 2
print("Double de 5 :", double(5))

# map : applique une fonction à CHAQUE élément d'une liste
taux_doubles = list(map(lambda x: x * 2, taux_liste[:5]))
print("Taux doublés (5 premiers) :", taux_doubles)

# filter : ne garde que les éléments qui vérifient une condition
taux_eleves = list(filter(lambda x: x > 1.18, taux_liste))
print("Nombre de jours où taux > 1.18 :", len(taux_eleves))  

# ==== B.1 - Votre première classe ====

class SerieTaux:
    """Représente la série de taux de change d'une devise."""

    def __init__(self, nom_devise, dates, taux):
        self.nom_devise = nom_devise   # attribut d'instance
        self.dates = dates
        self.taux = taux

    def moyenne(self):
        """Calcule la moyenne des taux."""
        return sum(self.taux) / len(self.taux)

    def variation(self):
        """Calcule la variation en % entre le premier et le dernier taux."""
        return (self.taux[-1] / self.taux[0] - 1) * 100

    def taux_a_date(self, date_recherchee):
        """Renvoie le taux à une date donnée, ou None si non trouvée."""
        for date, taux in zip(self.dates, self.taux):
            if date == date_recherchee:
                return taux
        return None


# Test
serie_usd = SerieTaux("USD", dates, taux_liste)
print("Devise :", serie_usd.nom_devise)
print("Moyenne :", serie_usd.moyenne())
print("Variation :", serie_usd.variation())
print("Taux au 2026-01-02 :", serie_usd.taux_a_date("2026-01-02"))

# ==== B.2 - Plusieurs objets et attribut de classe vs instance ====

df_gbp = pd.read_csv("donnees/eur_gbp_2026.csv")
dates_gbp = df_gbp["date"].tolist()
taux_gbp_liste = df_gbp["taux_gbp"].tolist()

serie_gbp = SerieTaux("GBP", dates_gbp, taux_gbp_liste)

print("USD moyenne :", serie_usd.moyenne())
print("GBP moyenne :", serie_gbp.moyenne())


# Démonstration du piège : liste mutable en attribut de CLASSE
class Exemple:
    historique = []  # attribut de CLASSE (partagé par TOUTES les instances !)

    def __init__(self, valeur):
        self.valeur = valeur  # attribut d'INSTANCE (propre à chaque objet)
        Exemple.historique.append(valeur)

a = Exemple(1)
b = Exemple(2)
print("Historique partagé :", Exemple.historique)  # [1, 2] : les deux objets ont modifié la MÊME liste

# ==== B.3 - Les dataclasses ====

from dataclasses import dataclass

@dataclass
class SerieTauxSimple:
    nom_devise: str
    dates: list
    taux: list

    def moyenne(self):
        return sum(self.taux) / len(self.taux)


serie_test = SerieTauxSimple("USD", dates, taux_liste)
print(serie_test)                  # affichage automatique, sans __repr__ à écrire !
print("Moyenne :", serie_test.moyenne())

# ==== C.1 - Une première courbe ====

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(dates, taux_liste)
ax.set_title("Évolution du taux EUR/USD en 2026")
ax.set_xlabel("Date")
ax.set_ylabel("Taux EUR/USD")

# Pour ne pas surcharger l'axe des dates, on n'affiche qu'une date sur 20
ax.set_xticks(range(0, len(dates), 20))
ax.set_xticklabels([dates[i] for i in range(0, len(dates), 20)], rotation=45)

fig.tight_layout()
fig.savefig("graphique_eur_usd.png")
print("Graphique sauvegardé : graphique_eur_usd.png")

# ==== C.2 - Plusieurs graphiques (subplots) ====

variations_pourcent = [(taux_liste[i] - taux_liste[i-1]) / taux_liste[i-1] * 100
                        for i in range(1, len(taux_liste))]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Graphique 1 : comparaison des deux devises (série temporelle)
ax1.plot(dates, taux_liste, label="EUR/USD")
ax1.plot(dates_gbp, taux_gbp_liste, label="EUR/GBP")
ax1.set_title("Comparaison EUR/USD vs EUR/GBP")
ax1.set_xlabel("Date")
ax1.set_ylabel("Taux")
ax1.legend()
ax1.set_xticks(range(0, len(dates), 30))
ax1.set_xticklabels([dates[i] for i in range(0, len(dates), 30)], rotation=45)

# Graphique 2 : histogramme des variations quotidiennes (distribution)
ax2.hist(variations_pourcent, bins=20)
ax2.set_title("Distribution des variations quotidiennes EUR/USD")
ax2.set_xlabel("Variation (%)")
ax2.set_ylabel("Nombre de jours")

fig.tight_layout()
fig.savefig("graphiques_comparaison.png")
print("Graphique sauvegardé : graphiques_comparaison.png")