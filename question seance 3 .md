# Réponses aux questions - Séance 3

## Partie A - Découvrir pandas

1. **Qu'est-ce qu'un DataFrame? Une Series?**
   - Un **DataFrame** est une structure de données bidimensionnelle, c'est-à-dire un tableau avec des lignes et des colonnes nommées.
   - Une **Series** est une structure unidimensionnelle, correspondant à une seule colonne du tableau munie de son index.

2. **Pourquoi utiliser pandas plutôt que des boucles et le module csv? Que signifie « vectorisation »?**
   - Pandas est nettement plus rapide et concis que des boucles Python associées au module `csv`.
   - La **vectorisation** consiste à appliquer une opération mathématique ou logique directement sur l'ensemble d'une colonne (ou d'un tableau) en une seule instruction, sans écrire de boucle `for` explicite. Ces opérations sont exécutées par des routines sous-jacentes optimisées en langage C.

3. **Pourquoi déconseille-t-on `iterrows()`?**
   - On déconseille `iterrows()` car cette fonction parcourt le DataFrame ligne par ligne en instanciant un nouvel objet `Series` à chaque étape. Cela détruit le mécanisme de vectorisation et rend l'exécution extrêmement lente sur de grands jeux de données.

4. **Comment pandas représente-t-il les valeurs manquantes (NaN)? Conséquences sur les moyennes?**
   - Pandas représente les valeurs manquantes par l'indicateur `NaN` (*Not a Number*).
   - Par défaut, les fonctions statistiques de pandas (comme `.mean()`) ignorent automatiquement les valeurs `NaN`, calculant ainsi la moyenne uniquement sur les données valides existantes.

---

## Partie B - Nettoyer, consolider et analyser

1. **C'est quoi le forward-fill? Quelle hypothèse fait-on en l'utilisant?**
   - Le **forward-fill** (`ffill`) est une méthode d'imputation qui consiste à combler une valeur manquante en propageant la dernière valeur valide connue précédente.
   - En l'utilisant pour des taux financiers, on fait l'hypothèse que le taux de change reste inchangé pendant les jours non ouvrés (week-ends et jours fériés) où les marchés sont fermés.

2. **À quoi sert `resample`? Que signifie une moyenne mobile?**
   - `resample` permet de modifier la fréquence temporelle d'une série temporelle (par exemple, agréger des données journalières en données mensuelles).
   - Une **moyenne mobile** consiste à calculer la moyenne des données sur une fenêtre glissante de $N$ périodes (ex. 20 jours). Cela permet de lisser les fluctuations de court terme et de faire ressortir la tendance générale.

---

## Partie C - Les jointures

1. **Rappelez les quatre types de jointure (inner, left, right, outer) : que garde chacune ?**
   - **`inner`** : Ne conserve que les lignes dont la clé est présente dans les deux tables (intersection).
   - **`left`** : Conserve toutes les lignes de la table de gauche.
   - **`right`** : Conserve toutes les lignes de la table de droite.
   - **`outer`** : Conserve l'ensemble des lignes des deux tables (union).

2. **Sur quelle colonne (clé) joint-on ? Que devient une ligne sans correspondance dans l’autre table ?**
   - On joint sur une colonne commune (ou sur l'index de date) appelée la **clé**.
   - Lorsqu'une ligne n'a pas de correspondance dans l'autre table, les colonnes importées de la table absente sont remplies avec des valeurs `NaN`.

3. **Pour réunir deux séries de taux sur la même période, quelle jointure choisir et pourquoi ?**
   - On choisit une jointure **`inner`** (ou `left` si l'index temporel est déjà harmonisé) afin de ne conserver que les dates où les taux sont effectivement disponibles pour les deux devises, garantissant une comparaison rigoureuse.

4. **Quelle différence entre `merge` et `concat` ? Dans quel cas utiliser l’un ou l’autre ?**
   - **`merge`** réalise une jointure relationnelle basée sur l'appariement des valeurs d'une colonne clé. On l'utilise pour combiner des jeux de données ayant une référence commune (ex. la date).
   - **`concat`** empile simplement des tables les unes sous les autres (sur les lignes) ou les unes à côté des autres (sur les colonnes) sans chercher de correspondance de valeurs. On l'utilise pour assembler des jeux de données partageant la même structure.

---

## Partie D - Un peu de numpy (et aperçu de polars)

1. **Différence entre une liste Python et un tableau numpy (`ndarray`) ? C’est quoi un `dtype` ? Le `broadcasting` ?**
   - Une liste Python peut contenir des objets de types différents stockés de manière dispersée en mémoire. Un **`ndarray`** est un tableau de taille fixe contenant des éléments d'un type unique stockés de façon contiguë en mémoire.
   - Le **`dtype`** (*data type*) indique le type exact des éléments contenus dans le tableau (ex. `float64`, `int32`).
   - Le **`broadcasting`** est la capacité de numpy à effectuer automatiquement des opérations arithmétiques entre des tableaux de dimensions différentes (ex. multiplier un tableau par un nombre scalaire).

2. **Pourquoi numpy est-il plus rapide que des boucles Python ?**
   - Numpy s'appuie sur du code C compilé sous-jacent, exploite la contiguïté mémoire des données et évite le surcoût lié au typage dynamique de Python à chaque itération.

3. **Différences entre pandas et polars (langage d’implémentation, usage des cœurs, évaluation paresseuse) ? Quand choisir l’un ou l’autre ?**
   - **Pandas** est écrit en C/Python, s'exécute principalement sur un seul cœur CPU et utilise une évaluation immédiate (*eager evaluation*).
   - **Polars** est écrit en Rust, est nativement multithreadé (utilise tous les cœurs CPU) et prend en charge l'évaluation paresseuse (*lazy evaluation*), ce qui lui permet d'optimiser le plan de requête avant l'exécution.
   - **Quand choisir ?** Utiliser Pandas pour des scripts d'analyse classiques ou de petits jeux de données. Choisir Polars pour traiter de très grands volumes de données nécessitant des performances et une vitesse d'exécution maximales.