# Projet Python — Analyse de taux de change

Équipe : Chloé, Eulalie, Amélie, Léa

## Installation

pip3 install -r requirements.txt

## Utilisation

Le projet s'utilise via une ligne de commande unique (main.py) avec 3 sous-commandes :

python3 main.py extraire     # récupère les taux depuis l'API Frankfurter
python3 main.py analyser     # calcule moyenne, min, max, variation
python3 main.py graphiques   # génère les graphiques PNG

## Structure du projet

- `code.py`, `fonctions.py`, `recursivite.py` — séances 1 et 2 (bases Python, fonctions, récursivité)
- `analyse.py` — séance 3 (pandas, jointures, numpy, polars)
- `idiomatique.py` — séance 4 (compréhensions, classes, matplotlib)
- `main.py` — outil en ligne de commande (argparse)
- `donnees/` — fichiers CSV des taux de change
- `cache/` — réponses brutes de l'API (JSON)
- `docs/notes_seanceX.md` — réponses aux questions de chaque séance