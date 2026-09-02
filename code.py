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