entier = 25
decimal = 3.14
texte = "Chloé"
booleen = True
liste = [1, 2, 3]
dictionnaire = {"nom": "Chloé", "age": 20}

# On affiche la valeur ET son type
print(entier, type(entier))
print(decimal, type(decimal))
print(texte, type(texte))
print(booleen, type(booleen))
print(liste, type(liste))
print(dictionnaire, type(dictionnaire))

# ==== A.4 - Les opérations ====

# Opérations arithmétiques
a = 10
b = 3
print(a + b)   # addition
print(a - b)   # soustraction
print(a * b)   # multiplication
print(a / b)   # division (résultat décimal)
print(a // b)  # division entière
print(a % b)   # modulo (reste de la division)
print(a ** b)  # puissance

# Chaînes de caractères
prenom = "Chloé"
nom = "Sterin"
nom_complet = prenom + " " + nom
print(nom_complet)
print(nom_complet.upper())
print(nom_complet.split(" "))

# Listes
fruits = ["pomme", "banane"]
fruits.append("kiwi")
print(fruits)
print(len(fruits))
print(fruits[0])

# Dictionnaires
personne = {"nom": "Chloé"}
print(personne["nom"])
personne["age"] = 20
print(personne)

# Comparaisons
print(a == b)
print(a != b)
print(a > b)
print(a <= b)

# Opérateurs booléens
print(True and False)
print(True or False)
print(not True)

# ==== A.5 - Les conditions ====

taux = 1.08

if taux > 1:
    print("au-dessus de 1")
elif taux == 1:
    print("égal à 1")
else:
    print("en-dessous de 1")

    # ==== C.1 - Explorer un dictionnaire ====

reponse = {
    "amount": 1.0,
    "base": "EUR",
    "date": "2024-01-02",
    "rates": {"USD": 1.0956},
}

# 1. Afficher la valeur associée à une clé (la date, puis le taux USD dans rates)
print(reponse["date"])
print(reponse["rates"]["USD"])

# 2. Ajouter une clé qui existe déjà, puis afficher le dictionnaire
reponse["date"] = "2099-01-01"
print(reponse)

# 3. Copier le dictionnaire, modifier la copie, afficher l'original : est-il modifié ?
copie = reponse.copy()
copie["date"] = "2050-05-05"
print("original :", reponse["date"])
print("copie :", copie["date"])

# Maintenant on modifie la partie imbriquée (rates) de la copie
copie["rates"]["USD"] = 999
print("original rates :", reponse["rates"])
print("copie rates :", copie["rates"])

import copy

reponse2 = {
    "amount": 1.0,
    "base": "EUR",
    "date": "2024-01-02",
    "rates": {"USD": 1.0956},
}

copie_profonde = copy.deepcopy(reponse2)
copie_profonde["rates"]["USD"] = 999
print("original rates :", reponse2["rates"])
print("copie profonde rates :", copie_profonde["rates"])

# ==== C.2 - Appeler l'API pour de vrai ====

import urllib.request
import json
import ssl
import certifi

# Corrige le problème de certificat SSL sur Mac
ssl_context = ssl.create_default_context(cafile=certifi.where())

url = "https://api.frankfurter.app/latest?from=EUR&to=USD"
requete = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(requete, context=ssl_context) as reponse_api:
    donnees = json.loads(reponse_api.read())

print(donnees)
print("Date :", donnees["date"])
print("Taux USD :", donnees["rates"]["USD"])


# ==== C.2.2 - Série sur une période ====

import csv
from pathlib import Path

url_serie = "https://api.frankfurter.app/2026-01-01..2026-09-01?from=EUR&to=USD"

requete_serie = urllib.request.Request(
    url_serie,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(requete_serie, context=ssl_context) as reponse_api:
    donnees_serie = json.loads(reponse_api.read())

# Créer les dossiers cache/ et donnees/ s'ils n'existent pas
Path("cache").mkdir(exist_ok=True)
Path("donnees").mkdir(exist_ok=True)

# 1. Enregistrer la réponse brute dans cache/ (format JSON)
with open("cache/eur_usd_2026.json", "w") as f:
    json.dump(donnees_serie, f, indent=2)

print("Nombre de jours reçus :", len(donnees_serie["rates"]))

# 2. Convertir en CSV propre dans donnees/
with open("donnees/eur_usd_2026.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "taux_usd"])
    for date, valeurs in sorted(donnees_serie["rates"].items()):
        writer.writerow([date, valeurs["USD"]])

print("Fichier CSV créé avec succès.")