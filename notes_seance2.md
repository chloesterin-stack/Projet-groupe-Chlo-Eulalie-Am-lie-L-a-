# Notes — Séance 2 : Fonctions, gestion des erreurs, logging, récursivité

## Partie A — Les fonctions

**1. Pourquoi découper le code en fonctions ? Trois bénéfices concrets.**

- **Lisibilité** : un `main` de 100 lignes est difficile à suivre ; des fonctions bien nommées (`lire_csv_taux`, `calculer_moyenne`...) rendent le déroulement du programme évident sans avoir à lire tout le détail.
- **Réutilisabilité** : une fonction écrite une fois peut être appelée à plusieurs endroits (ou dans un autre script) sans dupliquer le code.
- **Testabilité et débogage** : on peut tester une fonction isolément avec des exemples simples, et si un bug apparaît, on sait exactement dans quelle fonction chercher plutôt que dans tout le programme.

**2. Différence entre un paramètre et la valeur de retour (`return`). Que renvoie une fonction sans `return` ?**

Un **paramètre** est une donnée qu'on donne *en entrée* à la fonction (ce qu'elle reçoit pour travailler). La **valeur de retour** (`return`) est ce que la fonction renvoie *en sortie*, une fois son traitement terminé — c'est ce résultat qu'on peut ensuite stocker dans une variable ou réutiliser.

Une fonction sans `return` renvoie automatiquement `None` (la valeur nulle de Python), même si elle fait des choses (par exemple un `print`) à l'intérieur.

**3. Qu'est-ce qu'une docstring et où la place-t-on ?**

Une docstring est une chaîne de caractères (entre triples guillemets `"""..."""`) placée juste après la ligne `def` d'une fonction, qui décrit ce qu'elle fait, ses paramètres et ce qu'elle renvoie. Elle sert de documentation : on peut la consulter avec `help(nom_fonction)` ou en survolant la fonction dans un éditeur de code.

**4. Différence entre une variable locale et une variable globale.**

Une **variable locale** est définie à l'intérieur d'une fonction : elle n'existe que pendant l'exécution de cette fonction et n'est pas accessible depuis l'extérieur. Une **variable globale** est définie en dehors de toute fonction, au niveau principal du script : elle est accessible partout dans le fichier, y compris à l'intérieur des fonctions (en lecture ; pour la modifier depuis une fonction, il faut le mot-clé `global`).

---

## Partie B — try/except et logging

**1. Pourquoi gérer les erreurs avec try/except ? Que se passe-t-il si une exception n'est pas gérée ? À quoi servent `else` et `finally` ?**

`try/except` permet d'anticiper qu'une opération peut échouer (appel réseau, fichier absent, conversion invalide...) et de réagir proprement (message clair, valeur par défaut) au lieu de laisser le programme planter. Si une exception n'est **pas** gérée, Python interrompt immédiatement l'exécution du programme et affiche une *traceback* (le message d'erreur avec la pile d'appels).

- `else` : bloc exécuté uniquement si **aucune** exception n'a été levée dans le `try` — utile pour du code qui ne doit s'exécuter qu'en cas de succès.
- `finally` : bloc exécuté **systématiquement**, qu'il y ait eu une erreur ou non — utile pour du nettoyage (fermer un fichier, une connexion...).

**2. Pourquoi un `except:` nu (sans préciser le type d'erreur) est-il déconseillé ?**

Un `except:` nu attrape **toutes** les exceptions possibles, y compris celles qu'on n'a pas anticipées et qui révèlent un vrai bug dans le code (par exemple une faute de frappe dans un nom de variable, qui lève une `NameError`). Ça masque le problème au lieu de le signaler, ce qui rend le programme difficile à déboguer. Il vaut mieux préciser le type d'erreur attendu (`except ValueError:`, `except urllib.error.HTTPError:`...) pour ne traiter que les cas prévus.

**3. C'est quoi `logging` ? Pourquoi le préférer à `print` ? Les niveaux de log et un usage de chacun.**

Le module `logging` de la bibliothèque standard permet d'enregistrer des messages de suivi d'exécution, avec un niveau de gravité, une date/heure automatique, et la possibilité de les rediriger vers un fichier plutôt que juste l'écran. Contrairement à `print`, on peut activer/désactiver certains niveaux de messages sans modifier le code, et garder une trace persistante (fichier `.log`) même après la fermeture du programme — utile pour comprendre un bug survenu en production.

Niveaux principaux, du moins au plus grave :
- `DEBUG` : informations très détaillées, utiles seulement en phase de développement (ex. valeur d'une variable à chaque itération)
- `INFO` : déroulement normal du programme (ex. "appel de l'API réussi")
- `WARNING` : quelque chose d'anormal mais non bloquant (ex. "aucune donnée reçue, valeur par défaut utilisée")
- `ERROR` : une erreur réelle qui empêche une opération de se terminer (ex. "impossible de joindre l'API")

---

## Partie C — Récursivité et complexité

**1. C'est quoi la récursivité ? Cas de base et cas récursif ? Que se passe-t-il si le cas de base est absent ?**

La récursivité est une technique où une fonction s'appelle elle-même pour résoudre un problème en le décomposant en sous-problèmes plus petits de même nature. Le **cas de base** est la condition qui arrête les appels récursifs (par exemple `n == 0` pour la factorielle) ; le **cas récursif** est celui où la fonction s'appelle elle-même sur une version réduite du problème.

Si le cas de base est absent (ou jamais atteint), la fonction s'appelle indéfiniment jusqu'à ce que Python lève une `RecursionError` (la pile d'appels dépasse la limite autorisée).

**2. Pourquoi utiliser la récursivité ? Est-elle toujours le meilleur choix ? Contre-exemple.**

Elle est souvent plus naturelle et lisible pour des problèmes définis eux-mêmes de façon récursive (parcours d'arbre, factorielle, certains algorithmes de tri comme le tri fusion). Mais elle n'est pas toujours le meilleur choix : elle consomme de la mémoire supplémentaire (une pile d'appels) et peut être nettement plus lente qu'une version itérative si elle recalcule plusieurs fois les mêmes sous-problèmes.

**Contre-exemple précis** : Fibonacci récursif naïf. `fibonacci_naif(n-1)` et `fibonacci_naif(n-2)` recalculent chacun de nombreux sous-résultats communs (par exemple `fibonacci(2)` est recalculé des milliers de fois pour un `n` un peu grand) — la version itérative donne exactement le même résultat, sans ce gaspillage, en une fraction du temps.

**3. C'est quoi la complexité temporelle ? La complexité spatiale ? O(n), O(n²), O(2ⁿ) ?**

- **Complexité temporelle** : le nombre d'opérations effectuées par un algorithme, en fonction de la taille `n` de l'entrée.
- **Complexité spatiale** : la quantité de mémoire supplémentaire utilisée, en fonction de `n`.

- `O(n)` : le nombre d'opérations croît proportionnellement à `n` (ex. une boucle simple qui parcourt une liste une fois).
- `O(n²)` : le nombre d'opérations croît comme le carré de `n` (ex. deux boucles imbriquées, chacune de taille `n`).
- `O(2ⁿ)` : le nombre d'opérations double à chaque unité supplémentaire de `n` — croissance extrêmement rapide (ex. Fibonacci récursif naïf, où chaque appel en génère deux autres).

**4. C'est quoi la mémoïsation ? Que fait `functools.lru_cache` ? Pourquoi Python limite-t-il la profondeur de récursion ?**

La mémoïsation consiste à stocker (mettre en cache) le résultat d'un calcul déjà effectué, pour le réutiliser directement si le même calcul est redemandé plus tard, au lieu de le refaire. Le décorateur `functools.lru_cache` automatise exactement ça : il intercepte les appels à la fonction décorée, vérifie si le résultat pour ces arguments est déjà en cache, et le renvoie directement si oui — sinon il calcule et l'ajoute au cache.

Python limite la profondeur de récursion (par défaut autour de 1000 appels imbriqués) car chaque appel de fonction consomme de la mémoire sur la pile d'appels (*call stack*) ; sans cette limite, une récursion infinie ou mal bornée pourrait faire planter l'interpréteur ou saturer la mémoire de la machine. La limite agit comme un garde-fou qui transforme un plantage silencieux en une erreur explicite (`RecursionError`).

---

## Tableau des mesures — comparaison des trois versions de Fibonacci

*(à compléter avec les résultats obtenus en exécutant `recursivite.py` sur ta machine — les temps varient selon le matériel)*

| n   | Temps naïf (s) | Temps mémoïsé (s) | Temps itératif (s) |
|-----|-----------------|---------------------|----------------------|
| 10  |                 |                     |                      |
| 20  |                 |                     |                      |
| 25  |                 |                     |                      |
| 30  |                 |                     |                      |
| 100 | *(non testé — trop lent)* |            |                      |
| 500 | *(non testé — trop lent)* |            |                      |

**Observation attendue** : le temps de la version naïve croît de façon exponentielle avec `n` (cohérent avec sa complexité O(2ⁿ)), tandis que les versions mémoïsée et itérative restent quasi instantanées même pour n=500, avec une complexité O(n). En mémoire, la version mémoïsée consomme davantage que l'itérative car elle garde en cache tous les résultats intermédiaires (complexité spatiale O(n) contre O(1) pour l'itérative, qui ne garde que les deux derniers termes).
