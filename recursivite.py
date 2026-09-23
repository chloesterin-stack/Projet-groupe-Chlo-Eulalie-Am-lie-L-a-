def factorielle(n):
    """Calcule n! (factorielle de n) de façon récursive."""
    if n == 0:          # cas de base : arrête la récursion
        return 1
    else:                # cas récursif : la fonction s'appelle elle-même
        return n * factorielle(n - 1)


# Test
print("5! =", factorielle(5))
print("0! =", factorielle(0))
print("10! =", factorielle(10))

import time
from functools import lru_cache

# ==== C.2 - Fibonacci récursif naïf ====

def fib_naive(n):
    """Calcule le n-ième nombre de Fibonacci, de façon récursive naïve (sans optimisation)."""
    if n <= 1:               # cas de base
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)   # cas récursif : deux appels !


# Mesure du temps pour des valeurs croissantes
print("=== Fibonacci naïf ===")
for n in [10, 20, 30, 33]:
    debut = time.perf_counter()
    resultat = fib_naive(n)
    duree = time.perf_counter() - debut
    print(f"fib_naive({n}) = {resultat}  |  temps : {duree:.4f} s")

  # ==== Fibonacci avec mémoïsation (lru_cache) ====

@lru_cache(maxsize=None)
def fib_memo(n):
    """Calcule le n-ième nombre de Fibonacci, avec mémoïsation (résultats mis en cache)."""
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


print("\n=== Fibonacci avec mémoïsation ===")
for n in [10, 20, 30, 33, 100]:
    debut = time.perf_counter()
    resultat = fib_memo(n)
    duree = time.perf_counter() - debut
    print(f"fib_memo({n}) = {resultat}  |  temps : {duree:.6f} s")


# ==== Fibonacci version itérative (sans récursion) ====

def fib_iteratif(n):
    """Calcule le n-ième nombre de Fibonacci, avec une boucle (sans récursion)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


print("\n=== Fibonacci itératif ===")
for n in [10, 20, 30, 33, 100]:
    debut = time.perf_counter()
    resultat = fib_iteratif(n)
    duree = time.perf_counter() - debut
    print(f"fib_iteratif({n}) = {resultat}  |  temps : {duree:.6f} s") 

  # ==== Test : RecursionError ====

def compte_recursif(n):
    """Fonction récursive sans limite raisonnable, pour observer la RecursionError."""
    return 1 + compte_recursif(n + 1)  # pas de cas de base : ne s'arrête jamais


try:
    compte_recursif(0)
except RecursionError as e:
    print("RecursionError interceptée :", e) 

 # ==== C.3 - Tableau comparatif des complexités ====

print("\n=== Comparaison des trois versions de Fibonacci ===")
print(f"{'n':<5}{'Naïf (s)':<15}{'Mémoïsé (s)':<15}{'Itératif (s)':<15}")

for n in [10, 20, 30, 33]:
    debut = time.perf_counter()
    fib_naive(n)
    t_naif = time.perf_counter() - debut

    debut = time.perf_counter()
    fib_memo(n)
    t_memo = time.perf_counter() - debut

    debut = time.perf_counter()
    fib_iteratif(n)
    t_iter = time.perf_counter() - debut

    print(f"{n:<5}{t_naif:<15.6f}{t_memo:<15.6f}{t_iter:<15.6f}")     