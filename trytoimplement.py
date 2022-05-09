import random
from string import ascii_lowercase
import enchant
import json

def letterstoUse():
   
    a = []

    vowels = ["a", "e", "i", "o", "u"]

    random.shuffle(vowels)

    i = 0

    while i < 3:
        a.append(vowels[i])
        i += 1

    j = 0

    constants = ["b", "c", "d", "f", "g", "j", "k", "l",
                 "m", "n", "p", "q", "s", "t", "v", "x", "z"]

    while j < 2:
        random.shuffle(constants)
        a.append(constants[j])
        j += 1

    checkarray(a)
    return a


def checkarray(a):
    for x in range(5):
        if a[x-1] == a[x]:
            a[x] = random.choice(ascii_lowercase)
    y = json.dumps(a)
    print(y)
    return y 

def checkword(word):
    dictionary = enchant.Dict("en_US")
    if dictionary.check(word):
        return 0  # if word is a valid word
    else:
        return 1 # if word isnt a valid word


letterstoUse()
checkword("USER INPUT")
