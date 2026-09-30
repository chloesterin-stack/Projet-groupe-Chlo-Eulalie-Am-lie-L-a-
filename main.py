import argparse


def commande_extraire(args):
    print("Extraction des données en cours...")
    # Ici, on pourrait rappeler le code de la séance 1 (appel API)


def commande_analyser(args):
    print("Analyse des données en cours...")
    # Ici, on pourrait rappeler le code de fonctions.py / analyse.py


def commande_graphiques(args):
    print("Génération des graphiques en cours...")
    # Ici, on pourrait rappeler le code de idiomatique.py (matplotlib)


def main():
    parser = argparse.ArgumentParser(description="Outil d'analyse des taux de change")
    sous_parsers = parser.add_subparsers(dest="commande", required=True)

    sous_parsers.add_parser("extraire", help="Récupère les taux depuis l'API")
    sous_parsers.add_parser("analyser", help="Calcule les statistiques")
    sous_parsers.add_parser("graphiques", help="Génère les graphiques")

    args = parser.parse_args()

    if args.commande == "extraire":
        commande_extraire(args)
    elif args.commande == "analyser":
        commande_analyser(args)
    elif args.commande == "graphiques":
        commande_graphiques(args)


if __name__ == "__main__":
    main()