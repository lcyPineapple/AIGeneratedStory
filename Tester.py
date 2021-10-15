# This is the driver file for the Sherlock Holms story generator
# This program uses a trigram Markov model and trains the model
# on "A Study in Scarlet" and "The Hound of the Baskervilles"
# by Sir Arthur Conan Doyle.
# AUTHOR: LEIKA YAMADA
# DATE: 8/15/2021

# Import the markov model
import re
import Markov

# Global Variables
start = 8
punctuations = '''!()-[]{};:'"\,<>/?@#$%^&*_~'''
STOP = '.'
storyLength = 2000
totalWords = 0
# Methods
#############################################################
# trainModel()
# This method parses the input file and reads the file into
# the trigram Markov model. It removes the title, date, chapter,
# chapter names and removes all punctuation. It also treats
# a period as a seperate word.
#############################################################
def trainModel(fileName):
    global totalWords
    file = open(fileName, "r")
    myList = file.readlines()
    file.close()
    index = start
    totalWords = 0
    # The current word
    wi = ""
    # wi - 1
    wione = ""
    # wi - 2
    witwo = ""
    while index < len(myList):
        myLine = myList[index]
        if "CHAPTER" in myLine:
            index += 2
        myLine = myList[index].lower()
        for x in myLine:
            if x in punctuations:
                myLine = myLine.replace(x, " ")
            if x in STOP:
                myLine = myLine.replace(x, " . ")
        words = myLine.split()
        #count = 0
        for word in words:
            wi = word
            Markov.uniGram(wi)
            if wione != "":
                Markov.biGram(wione, wi)
                if witwo != "":
                    Markov.triGram(witwo, wione, wi)
            witwo = wione
            wione = wi
            totalWords += 1
        index += 1
#############################################################
# writeStory()
# This method creates a file called ReadMe, in this file the
# trigram markov model is used to create an AI generated
# Sherlock holmes story.
#############################################################
def writeStory():
    outputFile = open("ReadMe.txt", "w")
    count = storyLength
    wTwo = ""
    wOne = ""
    word = ""
    while count > 0:
        if "" == wTwo:
            wTwo = Markov.selectOne()
            outputFile.write(wTwo.capitalize())
            outputFile.write(" ")
        elif "" == wOne:
            wOne = Markov.selectTwo(wTwo, totalWords)
            outputFile.write(wOne)
            outputFile.write(" ")
        else:
            word = Markov.selectThree(wTwo, wOne, totalWords)
            if word == "." or word == " .":
                wOne = ""
                wTwo = ""
            else:
                wTwo = wOne
                wOne = word
            outputFile.write(word)
            outputFile.write(" ")
        if(count % 10 == 0) and count < 1995:
            outputFile.write("\n")
        count = count - 1
    outputFile.close()

##########################################################
# This is the main method of the program.
# The program starts here:
#############################################################
#Modify in-file names here
print("Training Model Please Wait takes a min or two")
trainModel("houn.txt")
trainModel("stud.txt")
writeStory()


