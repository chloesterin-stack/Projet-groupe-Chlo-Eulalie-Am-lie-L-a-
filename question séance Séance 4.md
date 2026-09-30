# Notes — Séance 4

Python idiomatique, programmation orientée objet, matplotlib et finalisation du projet.

---

## Partie A — Python plus idiomatique

### 1. C'est quoi une compréhension de liste ? Quel avantage par rapport à une boucle `for` classique ?

Une compréhension de liste est une syntaxe compacte pour construire une nouvelle liste à partir d'un itérable, en une seule expression :

```python
taux = [1.08, 1.09, 1.11]

# boucle classique
doubles = []
for x in taux:
    doubles.append(x * 2)

# compréhension
doubles = [x * 2 for x in taux]

# avec condition
positifs = [x for x in variations if x > 0]
```

Avantages : le code est plus court et plus lisible (l'intention est visible d'un coup d'œil), il n'y a pas de liste vide à initialiser ni de `append`, et c'est en général un peu plus rapide. Il existe aussi des compréhensions de dictionnaire : `{date: taux for date, taux in zip(dates, taux)}`. Il faut éviter les compréhensions trop imbriquées, qui deviennent illisibles : dans ce cas, une boucle classique est préférable.

### 2. À quoi servent `enumerate` et `zip` ?

- `enumerate(liste)` permet de parcourir une liste en récupérant à la fois l'indice et la valeur, sans gérer un compteur à la main :

  ```python
  for i, taux in enumerate(liste_taux):
      print(i, taux)
  ```

- `zip(a, b)` associe deux (ou plus) listes élément par élément, en s'arrêtant à la plus courte :

  ```python
  for date, taux in zip(dates, liste_taux):
      print(date, taux)
  ```

### 3. Comment trier une liste selon un critère (`sorted` avec `key`) ?

`sorted(iterable, key=fonction)` renvoie une nouvelle liste triée ; la fonction `key` est appliquée à chaque élément pour calculer la valeur de comparaison. L'option `reverse=True` inverse l'ordre. La liste d'origine n'est pas modifiée (contrairement à `liste.sort()`).

```python
donnees = [("2026-01-02", 1.09), ("2026-01-01", 1.08), ("2026-01-03", 1.11)]
par_taux = sorted(donnees, key=lambda t: t[1], reverse=True)
```

### 4. C'est quoi une f-string ? Comment afficher un nombre à deux décimales ?

Une f-string est une chaîne de caractères préfixée par `f` dans laquelle on insère directement des variables ou des expressions entre accolades `{}`. On peut ajouter un format après `:`.

```python
taux = 1.08456
print(f"Le taux est {taux:.2f}")   # Le taux est 1.08
print(f"Variation : {var:+.2%}")   # pourcentage avec signe
print(f"Date : {date:%d/%m/%Y}")   # formatage d'une date
```

`:.2f` signifie « nombre flottant avec 2 chiffres après la virgule ».

### 5. C'est quoi une fonction lambda ?

Une lambda est une petite fonction anonyme, écrite sur une seule ligne avec `lambda arguments: expression`. Elle est utile quand on a besoin d'une fonction simple et jetable, typiquement comme argument de `sorted`, `map` ou `filter` :

```python
carre = lambda x: x ** 2
list(map(lambda x: x * 100, variations))      # applique une fonction à chaque élément
list(filter(lambda x: x > 0, variations))     # garde les éléments qui vérifient la condition
```

Elle ne peut contenir qu'une seule expression. Dès que la logique devient plus complexe, on utilise une vraie fonction définie avec `def`.

---

## Partie B — La programmation orientée objet

### 1. C'est quoi une classe ? Un objet ? Une instance ? À quoi sert `self` ?

- Une **classe** est un modèle (un plan) qui décrit des données (attributs) et des comportements (méthodes). Exemple : `SerieTaux`.
- Un **objet** est une réalisation concrète de ce modèle. Un objet est une **instance** de sa classe : les deux mots sont quasiment synonymes. `usd = SerieTaux("USD", dates, taux)` crée une instance de `SerieTaux`.
- `self` est le premier paramètre de chaque méthode d'instance : il représente l'objet sur lequel la méthode est appelée. Il permet d'accéder à ses attributs (`self.devise`) et à ses autres méthodes. Python le passe automatiquement : `usd.moyenne()` équivaut à `SerieTaux.moyenne(usd)`.

```python
class SerieTaux:
    def __init__(self, devise, dates, taux):
        self.devise = devise
        self.dates = dates
        self.taux = taux

    def moyenne(self):
        return sum(self.taux) / len(self.taux)

    def variation(self):
        return (self.taux[-1] - self.taux[0]) / self.taux[0]

    def taux_a(self, date):
        return dict(zip(self.dates, self.taux))[date]
```

### 2. À quoi sert `__init__` ?

`__init__` est le constructeur : c'est la méthode appelée automatiquement à la création d'une instance (`SerieTaux(...)`). Elle initialise les attributs de l'objet à partir des paramètres reçus, pour que l'objet soit dans un état valide dès sa création.

### 3. Différence entre un attribut de classe et un attribut d'instance ?

- Un **attribut d'instance** est défini dans `__init__` via `self.x = ...` : il est propre à chaque objet (le taux de l'USD n'est pas celui du GBP).
- Un **attribut de classe** est défini directement dans le corps de la classe : il est partagé par toutes les instances (par exemple une constante `BASE = "EUR"`).

Piège : déclarer une liste (ou un dictionnaire) mutable en attribut de classe fait que toutes les instances partagent la même liste, comme pour les dictionnaires en séance 1.

```python
class Mauvais:
    taux = []                 # attribut de classe, partagé !

a, b = Mauvais(), Mauvais()
a.taux.append(1.08)
print(b.taux)                 # [1.08] : b est aussi modifié

class Bon:
    def __init__(self):
        self.taux = []        # attribut d'instance, propre à chaque objet
```

### 4. Qu'apporte une dataclass par rapport à une classe écrite entièrement à la main ?

Le décorateur `@dataclass` (module `dataclasses`) génère automatiquement `__init__`, `__repr__` (affichage lisible) et `__eq__` (comparaison) à partir des attributs annotés. On écrit donc beaucoup moins de code répétitif :

```python
from dataclasses import dataclass, field

@dataclass
class SerieTaux:
    devise: str
    dates: list[str]
    taux: list[float] = field(default_factory=list)

    def moyenne(self):
        return sum(self.taux) / len(self.taux)
```

On note `field(default_factory=list)` pour les valeurs par défaut mutables, ce qui évite justement le piège du partage entre instances.

---

## Partie C — Visualiser avec matplotlib

### 1. Différence entre la figure et les axes ? Pourquoi préférer `fig, ax = plt.subplots()` à l'usage direct de `pyplot` ?

- La **figure** (`Figure`) est le conteneur global : la fenêtre ou l'image entière, avec sa taille et sa résolution.
- Les **axes** (`Axes`) sont la zone de dessin proprement dite : la courbe, les graduations, le titre, les légendes d'axes. Une figure peut contenir plusieurs axes (plusieurs graphiques côte à côte).

`fig, ax = plt.subplots()` crée explicitement les deux objets, ce qui rend le code plus clair et plus contrôlable : on sait toujours sur quel graphique on agit (`ax.plot`, `ax.set_title`), on gère facilement plusieurs graphiques (`plt.subplots(1, 2)`) et le code est plus facile à réutiliser dans des fonctions. L'interface `pyplot` directe (`plt.plot(...)`) repose sur un état global implicite (« la figure courante »), source de confusion dès que l'on a plusieurs graphiques.

```python
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(dates, taux, label="USD")
ax.set_title("Évolution EUR/USD")
ax.set_xlabel("Date")
ax.set_ylabel("Taux")
ax.legend()
fig.savefig("graphiques/usd.png", dpi=150)
```

### 2. Quel type de graphique pour quel type de donnée ?

- **Série temporelle** (évolution dans le temps) : graphique en courbe (`ax.plot`), avec la date en abscisse.
- **Distribution** (répartition des valeurs, par exemple les variations quotidiennes) : histogramme (`ax.hist`), éventuellement boîte à moustaches (`boxplot`).
- **Comparaison** entre catégories ou entre devises : plusieurs courbes sur le même graphique (si les échelles sont comparables), ou diagramme en barres (`ax.bar`) pour comparer des valeurs agrégées (moyennes, variations totales).
- **Relation entre deux variables** : nuage de points (`ax.scatter`).

### 3. Comment sauvegarder une figure en PNG ?

Avec `fig.savefig("chemin/nom.png")` (ou `plt.savefig`), à appeler avant `plt.show()`. On peut régler la résolution avec `dpi=150` et couper les marges inutiles avec `bbox_inches="tight"`. Le format est déduit de l'extension du fichier. Il est ensuite conseillé de fermer la figure avec `plt.close(fig)` pour libérer la mémoire.

---

## Partie D — Assembler et finaliser

### 1. À quoi sert `argparse` ? Pourquoi une ligne de commande plutôt que des `input()` ?

`argparse` est le module de la bibliothèque standard qui lit et valide les arguments passés en ligne de commande, et génère automatiquement l'aide (`--help`) et les messages d'erreur. Avec des sous-commandes, on obtient un outil unique :

```bash
python -m src.main extraire --devise USD
python -m src.main analyser --devise USD
python -m src.main graphiques --devises USD GBP
```

Avantages par rapport à `input()` : le programme peut être lancé sans interaction (scripts, automatisation, tâches planifiées), il est reproductible (la commande exacte peut être documentée dans le README), les paramètres sont validés et documentés, et il est plus facile à tester.

### 2. Que fait exactement `if __name__ == "__main__"` ?

Quand un fichier est exécuté directement (`python fichier.py`), Python affecte à `__name__` la valeur `"__main__"`. Quand il est importé comme module, `__name__` vaut le nom du module. La condition permet donc d'exécuter du code seulement lorsque le fichier est lancé comme script, et pas quand il est simplement importé : on peut ainsi réutiliser les fonctions d'un fichier dans un autre sans déclencher son programme principal.

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

### 3. C'est quoi un module ? Un package ?

- Un **module** est un fichier `.py` contenant des fonctions, classes et variables, que l'on peut importer avec `import` (par exemple `src/analyse.py`).
- Un **package** est un dossier contenant des modules, généralement avec un fichier `__init__.py`, qui permet d'organiser le code en ensembles cohérents (`src/` avec `extraction.py`, `analyse.py`, `graphiques.py`, `cli.py`).

### 4. Que doit contenir un bon README ? À quoi servent `requirements.txt` et `.gitignore` ?

**README.md** : c'est la page d'accueil du dépôt. Il doit contenir :
- le titre et une description du projet (objectif, contexte),
- les prérequis et les instructions d'installation (création de l'environnement virtuel, `pip install -r requirements.txt`),
- des exemples de commandes d'utilisation avec les résultats attendus,
- la structure du dépôt,
- les auteurs (le groupe) et éventuellement la licence.

**requirements.txt** : liste les dépendances Python avec leurs versions (`pip freeze > requirements.txt`), afin que n'importe qui puisse recréer le même environnement avec `pip install -r requirements.txt`.

**.gitignore** : liste les fichiers et dossiers que Git ne doit pas suivre : environnement virtuel (`.venv/`), `__pycache__/`, fichiers temporaires, secrets et clés d'API (`.env`), données volumineuses ou générées. Cela garde le dépôt propre et évite de publier des informations sensibles.