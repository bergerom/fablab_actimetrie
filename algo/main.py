# Algorithme de detection de groupe par detection de regard
# ==== Cas 4 personnes ====
# Partie Calcul

# On utilise les biblioteques SciKit-learn et HMMlearn
# pour appliquer l'algorithme de Viterbi.
from hmmlearn import hmm
import numpy as np
from sklearn.preprocessing import normalize
from numpy.random import randint

#==============================================================================#
#                           Initialisation                                     #
#==============================================================================#

# Dans le cas de 4 personnes (A,B,C et D) on a 4 groupes possibles
# On represente un groupe de personne entre parenthese
# (AB)(CD) signifie 2 groupes composes respectivement de A,B et de C,D
states = ["(ABCD)", "(AB)(CD)", "(AC)(BD)", "(AD)(CB)"]
n_states = len(states)

# On doit creer toutes les observations possibles
# On utilise un code pour les representer :
# Code d'une observation :
# A=1, B=2, C=3, D=4
# Code = [0-4][0-4][0-4][0-4]
# chiffre 1 = A regarde A/B/C/D/rien(0)
# chiffre 2 = B regarde ...
observations = []
for n0 in range(0, 5):
    for n1 in range(0, 5):
        for n2 in range(0, 5):
            for n3 in range(0, 5):
                if (n3 != 4 and n2 != 3 and n1 != 2 and n0 != 1):
                    observations.append(n3 + n2 * 10 + n1 * 100 + n0 * 1000)

# On a besoin de fonctions nous permettant d'acceder a un chiffre du code
def getN0(n):
    return n / 1000

def getN1(n):
    a = getN0(n)
    return (n - a * 1000) / 100

def getN2(n):
    a = getN0(n)
    b = getN1(n)
    return (n - a * 1000 - b * 100) / 10

def getN3(n):
    a = getN0(n)
    b = getN1(n)
    c = getN2(n)
    return n - a * 1000 - b * 100 - c * 10

#Retourne qui regarde y dans x
def getNassociatedWith(x, y):
    if (y == 1):
        return getN0(x)
    if (y == 2):
        return getN1(x)
    if (y == 3):
        return getN2(x)
    if (y == 4):
        return getN3(x)

# Cette fonction calcule un vecteur de probabilite des observations dans le cas
# ou il y a 2 groupes (b11,b12)(b21,b22)
# Cela nous permet de remplir la matrice d'emission par la suite
def probGroupe2(observations, b11, b12, b21, b22):
    tab = []
    pGroupe = 0.9 # Poid pour 2 personnes d'un meme groupe
    pNon = 0.1    # Poid sinon
    for x in observations:
        regardeParb11 = getNassociatedWith(x, b11)
        regardeParb12 = getNassociatedWith(x, b12)
        regardeParb21 = getNassociatedWith(x, b21)
        regardeParb22 = getNassociatedWith(x, b22)
        
        p = 1
        # Pour chaque observation onn regarde si chaque chiffre regarde 
        # une personne qui est dans son groupe
        # Si oui, on multiplie notre "pseudo-probabilite" par 0.9
        # Si non, par 0.1
        # on obtient un resultat par observation
        # On normalise le vecteur,
        # on obtient un vecteur de probabilite coherent
        if (regardeParb11 == b12):
            p = p * pGroupe
        else:
            p = p * pNon
        
        if (regardeParb12 == b11):
            p = p * pGroupe
        else:
            p = p * pNon
        
        if (regardeParb21 == b22):
            p = p * pGroupe
        else:
            p = p * pNon
            
        if (regardeParb22 == b21):
            p = p * pGroupe
        else:
            p = p * pNon
    
        tab.append(float(p))
    
    # Respect des contraintes de type de HMM
    tab = np.asarray(tab)
    tab = normalize(tab.reshape(1,-1),  norm="l1")
    tab = tab[0]
    tab = np.array(tab)
    return tab
        
n_observations = len(observations)

# Vecteurs de probabilite de chaque etat au depart
# On considere ici que chaque etat est initialement equiprobable
start_probability = np.array([0.25, 0.25, 0.25, 0.25])

# Matrice de transition de la chaine de Markov
# Represente les probabilite de changement d'etat
# On prend ici une probabilite de rester dans l'etat precedent de 0.9
transition_probability = np.array([
                                  [0.9, 0.03, 0.03, 0.04],
                                  [0.03, 0.9, 0.04, 0.03],
                                  [0.03, 0.04, 0.9, 0.03],
                                  [0.04, 0.03, 0.03, 0.9]
                                  ])

# Matrice representant les probabilites de chaque observations
# pour chaque etat initialement
emission_probability = np.array([
                                np.full(n_observations, 1.0 / n_observations),
                                probGroupe2(observations, 1, 2, 3, 4),
                                probGroupe2(observations, 1, 3, 2, 4),
                                probGroupe2(observations, 1, 4, 3, 2)
                                ])

# On definit notre chaine de Markov
model = hmm.MultinomialHMM(n_components=n_states)
model.startprob_ = (start_probability)
model.transmat_ = (transition_probability)
model.emissionprob_ = (emission_probability)

#==============================================================================#
#                           Tests d'observations                               #
#==============================================================================#


# Test de donnees parfaites (AB)(CD)
# On trouve l'indice corespondant au code 2143 = aPB, bpA, cPd, dPc
indice = 0
for i in range(0, len(observations)-1):
    if (observations[i] == 2143):
        indice = i
test1 = []
for i in range(0, 99):
    test1.append([indice])

# Test d'observations aleatoires
test2 = []
for i in range(0, 200):
    test2.append([randint(0,len(observations) - 1)])

# Test aleatoire compose de :
# 25% de 2143 = parfait (AB)(CD)
# 25% de 3412 = parfait (AC)(BD)
# 50% de 4321 = parfait (AD)(BC)
test3 = []
for i in range(0, len(observations) -1):
    if (observations[i] == 3412):
        i2 = i
    if (observations[i] == 4321):
        i3 = i
for i in range(0, 500):
    r = randint(1,101)
    if (r < 25):
        test3.append([indice])
    elif (r<50 & r>50):
        test3.append([i2])
    else:
        test3.append([i3])


#==============================================================================#
#                           Calcul et affichage                                #
#==============================================================================#


# Calcul des resultats de test
logprob, result = model.decode(test1, algorithm="viterbi")
logprob, result2 = model.decode(test2, algorithm="viterbi")
logprob, result3 = model.decode(test3, algorithm="viterbi")

# Affichage des resultats
print ""
print "Cas parfait (AB)(CD)              : " + (states[result[len(result) - 1]])
print "Cas observations aleatoire        : " + (states[result2[len(result2) - 1]])
print "Cas aleatoire a majorite (AD)(CB) : " + (states[result3[len(result3) - 1]])
print ""