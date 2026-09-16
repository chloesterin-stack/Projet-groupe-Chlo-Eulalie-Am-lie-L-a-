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

### C.1 — Explorer un dictionnaire

Quand on affecte une valeur à une clé qui existe déjà dans un dictionnaire, la nouvelle valeur remplace l'ancienne (elle n'est pas dupliquée). Un dictionnaire ne peut avoir qu'une seule valeur associée à chaque clé.

### C.1 — Copie superficielle (.copy())

.copy() crée un nouveau dictionnaire, mais ne copie que le premier niveau. Les valeurs imbriquées (comme un dictionnaire à l'intérieur, ex: rates) ne sont pas dupliquées : l'original et la copie pointent vers le même sous-dictionnaire en mémoire. Modifier une clé imbriquée dans la copie modifie donc aussi l'original. C'est ce qu'on appelle une copie superficielle.

### C.1 — Copie profonde (copy.deepcopy())

copy.deepcopy() copie récursivement toutes les valeurs, y compris les dictionnaires imbriqués. L'original et la copie profonde sont donc complètement indépendants : modifier une clé imbriquée dans la copie n'affecte plus l'original.

Résumé mutabilité :
- Types mutables (modifiables après création) : list, dict — d'où le risque de la copie superficielle
- Types immuables (non modifiables) : int, float, str, bool, tuple — pas de risque de ce type avec eux, car réaffecter crée un nouvel objet plutôt que de modifier l'existant

### C.2 — Appeler l'API pour de vrai

Une API (Application Programming Interface) est une interface qui permet à un programme de demander des données ou des services à un autre programme via internet, sans avoir besoin de connaître son fonctionnement interne.

« Envoyer une requête » signifie envoyer une demande formatée (ici une URL) à un serveur, qui traite la demande et renvoie une réponse.

Le format JSON (JavaScript Object Notation) est un format de texte structuré pour échanger des données, très proche des dictionnaires Python (paires clé : valeur). En Python, le module json convertit ce texte en dictionnaire (json.loads) ou l'inverse (json.dumps).

Résultat obtenu le 2026-09-02 : 1 EUR = 1.1578 USD.

Difficulté rencontrée : erreur SSL CERTIFICATE_VERIFY_FAILED, corrigée en utilisant le module certifi pour fournir un contexte SSL valide. Puis erreur HTTP 403 Forbidden, corrigée en ajoutant un en-tête User-Agent à la requête pour éviter que le serveur ne bloque la requête par défaut de Python.

Pourquoi enregistrer la réponse dans un fichier (cache/) plutôt que rappeler l'API à chaque exécution ? Cela évite de solliciter inutilement le serveur à chaque test (respect du service, limite de requêtes), accélère l'exécution du programme (pas d'attente réseau), et permet de continuer à travailler même sans connexion internet ou si l'API est temporairement indisponible.

### C.2.2 — Série sur une période

On enregistre la réponse brute au format JSON dans cache/ pour garder une copie fidèle et complète de ce que l'API a renvoyé (utile en cas de problème ou pour retraiter les données différemment plus tard), puis on la transforme en un fichier CSV propre dans donnees/, plus simple à ouvrir dans un tableur ou à réutiliser dans d'autres scripts.

Résultat : 171 jours de taux EUR/USD récupérés entre le 1er janvier et le 1er septembre 2026.