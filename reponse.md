# Notes séance 1

## Partie A — Premiers pas en Python

### A.1 — Installer Python
1. Python est un langage de programmation interprété, polyvalent et facile à lire...
2. On installe Python en téléchargeant l'installeur sur python.org, ou via un gestionnaire de paquets (brew sur Mac). On vérifie l'installation avec `python3 --version` dans le terminal.
3. On peut lancer du code Python de deux façons : en tapant directement dans l'interpréteur interactif (terminal), ou en écrivant un script `.py` et en l'exécutant avec `python3 fichier.py`.

### A.3 — Les types de base
1. Les types de base en Python sont : int (entier), float (décimal), str (chaîne de caractères), bool (booléen), list (liste), dict (dictionnaire).

Le typage dynamique signifie qu'on n'a pas besoin de déclarer le type d'une variable à l'avance : Python le déduit automatiquement de la valeur assignée, et une variable peut changer de type au cours du programme.

### A.4 — Les opérations

Quelle est la différence entre un opérateur booléen et un opérateur logique ?

Un opérateur de comparaison (==, !=, <, >, <=, >=) compare deux valeurs et produit un résultat booléen (True ou False). Un opérateur logique (and, or, not) combine des valeurs booléennes déjà existantes entre elles pour en produire une nouvelle.

Exemple : a > b est une comparaison (elle crée un booléen). (a > b) and (c > d) utilise un opérateur logique (il combine deux booléens déjà créés).
