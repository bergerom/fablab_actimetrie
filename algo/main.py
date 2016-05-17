# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from hmmlearn import hmm
import numpy as np
from sklearn.preprocessing import normalize


states = ["(ABCD)", "(AB)(CD)", "(AC)(BD)", "(AD)(CB)"]
n_states = len(states)

#Code d'une observation :
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

def probGroupe2(observations, b11, b12, b21, b22):
    tab = []
    pGroupe = 0.9
    pNon = 0.1
    for x in observations:
        regardeParb11 = getNassociatedWith(x, b11)
        regardeParb12 = getNassociatedWith(x, b12)
        regardeParb21 = getNassociatedWith(x, b21)
        regardeParb22 = getNassociatedWith(x, b22)
        
        p = 1
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
    tab = np.asarray(tab)
    tab = normalize(tab.reshape(1,-1),  norm="l1")
    tab = tab[0]
    tab = np.array(tab)
    return tab
        
n_observations = len(observations)

start_probability = np.array([0.25, 0.25, 0.25, 0.25])

transition_probability = np.array([
                                  [0.9, 0.03, 0.03, 0.04],
                                  [0.03, 0.9, 0.04, 0.03],
                                  [0.03, 0.04, 0.9, 0.03],
                                  [0.04, 0.03, 0.03, 0.9]
                                  ])

emission_probability = np.array([
                                np.full(n_observations, 1.0 / n_observations),
                                probGroupe2(observations, 1, 2, 3, 4),
                                probGroupe2(observations, 1, 3, 2, 4),
                                probGroupe2(observations, 1, 4, 3, 2)
                                ])
                                



#test de donnees parfaites (AB)(CD)
#On trouve l'indice corespondant au code 2143 = aPB, bpA, cPd, dPc
#indice = 0
#for i in range(0, len(observations)-1):
#    if (observations[i] == 3412):
#        indice = i
#test = [[indice], [indice], [95], [95]]
#
##test = np.full(50, i)
##test = np.array(test).reshape((len(test),1))
#
#model = hmm.MultinomialHMM(n_components=n_states)
#model.startprob_ = (start_probability)
#model.transmat_ = (transition_probability)
#model.emissionprob_ = (emission_probability)
##X, Z = model.sample(100)
#X, Z = model.sample(100)
#
#remodel = hmm.MultinomialHMM(n_components=n_states)
#remodel.startprob_ = (start_probability)
#remodel.transmat_ = (transition_probability)
#remodel.emissionprob_ = (emission_probability)
#remodel.fit(X)  
#Z2 = remodel.predict(X)

#print "Groupe :"," ".join(map(lambda x: states[x], result))


#remodel = hmm.MultinomialHMM(n_components=n_states, startprob_prior=start_probability, transmat_prior=transition_probability, n_iter=100)
#remodel.fit(test)
#
#result = remodel.decode((test,1))
#print(result)



#test de donnees parfaites (AB)(CD)
#On trouve l'indice corespondant au code 2143 = aPB, bpA, cPd, dPc
indice = 0
for i in range(0, len(observations)-1):
    if (observations[i] == 2143):
        indice = i
test = [[indice], [indice], [indice], [42],[42],[42],[42],[42], [indice], [indice], [indice]]
print(observations[42])
#test = np.full(50, i)
#test = np.array(test).reshape((len(test),1))

model = hmm.MultinomialHMM(n_components=n_states)
model.startprob_ = (start_probability)
model.transmat_ = (transition_probability)
model.emissionprob_ = (emission_probability)

#X, Z = model.sample(100)
logprob, result = model.decode(test, algorithm="viterbi")
print "Groupe :"," ".join(map(lambda x: states[x], result))

