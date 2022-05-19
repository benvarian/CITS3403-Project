from asyncore import read
from random import randint
from datetime import date
from datetime import datetime
import pandas

def scrambledLetters(mode):
    try:
        if checkTime(mode):
            if mode == "speed":
                f = open("./app/game/sletters.txt", "w")
            else:
                f = open("./app/game/nletters.txt", "w")
            letters = letterstoUse()
            for letter in letters:
                f.write(letter[0] + " " + str(letter[1])+"\n")
            f.close()
            return letters
        else:
            if mode == "speed":
                f = open("./app/game/sletters.txt", "r")
            else:
                f = open("./app/game/nletters.txt", "r")
            lines = f.readlines()
            letters = []
            for line in lines:
                line = line.strip('\n')
                letters.append((line.split(" ")))
            f.close()
            return letters
    except:
        if mode == "speed":
            f = open("./app/game/sletters.txt", "w")
        else:
            f = open("./app/game/nletters.txt", "w")
        letters = letterstoUse()
        for letter in letters:
            f.write(letter[0] + " " + str(letter[1])+"\n")
        f.close()
        return letters

def checkTime(mode):
    pathname = "./app/game/last_update"
    if mode == "speed":
        pathname += "s.txt"
    else:
        pathname += "n.txt"
    try:
        f_read = open(pathname , 'r')
        last_date_string = f_read.read()
        last_date = datetime.strptime(last_date_string, "%d-%m-%Y")
        last_date = datetime.date(last_date)
        f_read.close()
        if date.today() > last_date:
            f_write =  open(pathname , 'w')
            new_date = date.today()
            new_date_string = new_date.strftime("%d-%m-%Y")
            f_write.write(new_date_string)
            f_write.close()
            return True
        return False
    except: 
        f = open(pathname, 'w')
        new_date = date.today()
        new_date_string = new_date.strftime("%d-%m-%Y")
        f.write(new_date_string)
        f.close()
        return True

def letterstoUse():
    vowels = {"A":1, "E":1, "I":1, "O":1, "U":1}
    rare_consonants = {"F":4, "J":8, "K":5, "Q":10, "V":4, "X":8, "Z":10}
    common_consonants = {"B":3, "C":3, "D":2, "G":2,"L":1, "H":4, "M":3, "N":1, "P":3, "R":1, "S":1, "T":1, "Y":4, "W":4}
    
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
    while len(consonantList) < 4:
        randomNum = randint(0,13)
        ckeysList = list(common_consonants.keys())
        letter = ckeysList[randomNum]
        if letter not in consonantCheckList:
            consonantList.append([letter, common_consonants[letter]])
            consonantCheckList.append(letter)   
        
    randomNum = randint(0,6)
    keyList = list(rare_consonants.keys())
    rareLetter = keyList[randomNum]
    consonantList.append([rareLetter, rare_consonants[rareLetter]])

    letters = vowelList + consonantList
    return letters

def checkWordExists(word):
    filename = '../Scrambled/words_file.csv'
    wordLower = word.lower()
    data = pandas.read_csv(filename, header=0)
    myData = list(data.values)
    if wordLower in myData:
        return True
    return False

def adminOverwrite(letters, mode):
    alphabet = {"A":1, "E":1, "I":1, "O":1, "U":1,"F":4, "J":8, "K":5,
     "Q":10, "V":4, "X":8, "Z":10, "B":3, "C":3, "D":2, "G":2,"L":1,
      "H":4, "M":3, "N":1, "P":3, "R":1, "S":1, "T":1, "Y":4, "W":4}
    if mode == "normal": 
        f = open("./app/game/nletters.txt", "w")
    else:
        f = open("./app/game/sletters.txt", "w")
    for letter in letters:
        f.write(letter + " " + str(alphabet[letter])+"\n")
    f.close()