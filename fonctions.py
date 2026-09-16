import csv


def lire_csv(chemin):
    """Lit un fichier CSV de taux de change et renvoie une liste de couples (date, taux)."""
    donnees = []
    with open(chemin, newline="") as f:
        lecteur = csv.reader(f)
        next(lecteur)  # on saute la ligne d'en-tête
        for ligne in lecteur:
            date, taux = ligne
            donnees.append((date, float(taux)))
    return donnees


def moyenne(taux_liste):
    """Calcule la moyenne d'une liste de taux."""
    return sum(taux_liste) / len(taux_liste)


def min_max(taux_liste):
    """Renvoie un couple (taux minimum, taux maximum) d'une liste de taux."""
    return min(taux_liste), max(taux_liste)


# ==== Test des fonctions ====
donnees = lire_csv("donnees/eur_usd_2026.csv")
taux_liste = [taux for date, taux in donnees]

print("Nombre de valeurs :", len(taux_liste))
print("Moyenne :", moyenne(taux_liste))
print("Min, Max :", min_max(taux_liste))

# ==== B.1 / B.2 - Appel API protégé et journalisé ====
import urllib.request
import json
import ssl
import certifi
import logging

# Configuration du logging : écrit dans un fichier api.log
logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def recuperer_taux(url):
    """Appelle l'API de taux de change et renvoie le dictionnaire de la réponse, ou None en cas d'erreur."""
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        logging.info("Appel de l'API : %s", url)
        with urllib.request.urlopen(requete, context=ssl_context) as reponse_api:
            donnees = json.loads(reponse_api.read())
        logging.info("Réponse reçue avec succès.")
        return donnees

    except urllib.error.HTTPError as e:
        logging.error("Erreur HTTP %s : %s", e.code, e.reason)
        print(f"Erreur : le serveur a répondu avec le code {e.code}")

    except urllib.error.URLError as e:
        logging.error("Erreur réseau : %s", e.reason)
        print("Erreur : impossible de joindre le serveur (pas de connexion internet ?)")

    except json.JSONDecodeError:
        logging.warning("Réponse reçue mais illisible (pas du JSON valide).")
        print("Erreur : la réponse du serveur n'est pas lisible.")

    return None


# Test avec une URL valide
url_ok = "https://api.frankfurter.app/latest?from=EUR&to=USD"
resultat = recuperer_taux(url_ok)
print("Résultat (URL valide) :", resultat)

# Test avec une URL invalide, pour déclencher une erreur volontairement
url_cassee = "https://api.frankfurter.app/n-importe-quoi"
resultat_erreur = recuperer_taux(url_cassee)
print("Résultat (URL cassée) :", resultat_erreur)