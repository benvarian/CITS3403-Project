from random import randint
from string import ascii_lowercase
import json
from nltk.corpus import words

def letterstoUse():
    vowels = {"A":1, "E":1, "I":1, "O":1, "U":1}
    consonants = {"B":3, "C":3, "D":2, "F":4, "G":2, "J":8, "H":4, "K":5, "L":1,
                 "M":3, "N":1, "P":3, "Q":10, "R":1, "S":1, "T":1, "V":4, 
                 "Y":4, "W":4, "X":8, "Z":10}    
    
    vowelList = []
    vowelCheckList = []
    while len(vowelList) < 3:
        randomNum = randint(0,4)
        vkeysList = list(vowels.keys())
        letter = vkeysList[randomNum]
        if letter not in vowelCheckList:
            vowelList.append([letter, vowels[letter]])
            vowelCheckList.append(letter)
            
    consonantList = []
    consonantCheckList = []
    while len(consonantList) < 5:
        randomNum = randint(0,20)
        ckeysList = list(consonants.keys())
        letter = ckeysList[randomNum]
        if letter not in consonantCheckList:
            consonantList.append([letter, consonants[letter]])
            consonantCheckList.append(letter)        
    
    letters = vowelList + consonantList
    return letters

def checkWordExists(word):
    if word in words.words():
        return 0
    else:
        return 1

