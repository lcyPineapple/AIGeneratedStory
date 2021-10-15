# This program contains a trigram Markov model which is used to
# generate a AI created story. The model uses
# by Sir Arthur Conan Doyle.
# AUTHOR: LEIKA YAMADA
# DATE: 8/15/2021

from random import randint
import math

# Global Variables
markovCount = 0
uniGramMap = {}
biGramMap = {}
triGramMap = {}

def getCount():
    return markovCount

def addCount():
    global markovCount
    markovCount += 1

class Node:
    def __init__(self, current, nextNode, nextWiNode, value):
        self.current = current
        # Next Wi-1 possibility
        self.nextNode = nextNode
        # next Wi possibility
        self.nextWiNode = nextWiNode
        self.value = value

# This method stores word frequencies in a map
# It will be used to calculate P(Word)
# Param: string, the word to add as the key in map
def uniGram(word):
    global uniGramMap
    if word in uniGramMap:
        uniGramMap[word] = uniGramMap[word] + 1
    else:
        uniGramMap[word] = 1

# This method stores bigram frequencies in a map
# It will be used to calculate P(Word|Word-1)
# Param: string, Word - 1 = wordi
#      : string, Word
def biGram(wordi, word):
    global biGramMap
    flag = True
    if wordi in biGramMap:
        node = biGramMap[wordi]
        while flag:
            if node.current == word:
                node.value = node.value + 1
                flag = False
            elif node.nextNode is None:
                newNode = Node(word, None, None, 1)
                node.nextNode = newNode
                flag = False
            else:
                node = node.nextNode
    else:
        myNode = Node(word, None, None, 1)
        biGramMap[wordi] = myNode

# This method stores trigram frequencies in a map
# It will be used to calculate P(Word|Word-1, Word-2)
# Param: string, Word - 2 = worditwo
#        string, Word - 1 = wordi
#      : string, Word
def triGram(worditwo, wordi, word):
    global triGramMap
    flag = True
    flagB = True
    if worditwo in triGramMap:
        node = triGramMap[worditwo]
        while flag:
            if node.current == wordi:
                internalNode = node.nextWiNode
                while flagB:
                    if internalNode.current == word:
                        internalNode.value = internalNode.value + 1
                        flagB = False
                    elif internalNode.nextNode is None:
                        newNode = Node(word, None, None, 1)
                        internalNode.nextNode = newNode
                        flagB = False
                    else:
                        internalNode = internalNode.nextNode
                flag = False
            elif node.nextNode is None:
                mynewWi = Node(word, None, None, 1)
                newNode = Node(wordi, None, mynewWi, 1)
                node.nextNode = newNode
                flag = False
            else:
                node = node.nextNode
    else:
        myWi = Node(word, None, None, 1)
        myNode = Node(wordi, None, myWi, None)
        triGramMap[worditwo] = myNode

# Test biGram by printing results to console
def printbiDict():
    print(biGramMap.values())
    for x in biGramMap.values():
        print('newList')
        flag = True
        myNode = x
        while flag:
            print(myNode.current)
            print(myNode.value)
            if myNode.nextNode is None:
                flag = False
            else:
                myNode = myNode.nextNode
    print(biGramMap.keys())

# Test triGram by printing results to console
def printTriDict():
    print(triGramMap.values())
    for x in triGramMap.values():
        print('newList---------------------------------')
        flag = True
        myNode = x
        while flag:
            print("SECOND WORD IN SERIES--------------")
            print(myNode.current)
            nodea = x.nextWiNode
            flagB = True
            while flagB:
                print("Here>")
                print(nodea.current)
                print(nodea.value)
                if nodea.nextNode is None:
                    flagB = False
                else:
                    nodea = nodea.nextNode
            if myNode.nextNode is None:
                flag = False
            else:
                myNode = myNode.nextNode
    print(triGramMap.keys())

def triTest():
    for x in triGramMap.values():
        flag = True
        curr = x
        while flag:
            if curr.nextNode != None:
                print(curr.current)
                print(curr.nextWiNode.current)
                curr = curr.nextNode
                print(curr.current)
                print(curr.nextWiNode.current)
                print(curr.nextWiNode.value)
            else:
                flag = False
# This method returns the probability of the word occuring in text
# P(Word) = Count(word) / Count(TotalWords)

# This method selects the first word in the sentence
# using the unigramMap
# return: string, the first word of a sentence.
def selectOne():
    size = len(uniGramMap.keys())
    # generate random integer
    value = randint(1, size)
    index = 1
    for x in uniGramMap.keys():
        if index == value:
            if x == ".":
                return selectOne()
            return x
        index += 1
# This method selects the second word in the sentence
# It uses the biGram and unigram probabilties to select
# the most likely word to follow the first word
# Using markov biGram equation :
#   MAX [For All Wi in W : (P(wi)P(wi|wi-1))]
# Param: string, wiONe previous word
#        int, totalWords total words in model
def selectTwo(wiOne, totalWords):
    word = ""
    max = 1000
    for x in uniGramMap.keys():
        freqX = uniGramMap[x]
        #log of probability for word to appear
        pwi = math.log(freqX/totalWords, 2)
        #log of probability for word to appear, given prev word
        pwiGivenFreq = 0
        pwiGivenWOne = 0
        if wiOne in biGramMap.keys():
            node = biGramMap[wiOne]
            flag = True
            while flag:
                if node.current == x:
                    pwiGivenFreq = node.value
                    flag = False
                elif node.nextNode is not None:
                    node = node.nextNode
                else:
                    flag = False
        if pwiGivenFreq != 0:
            pwiGivenWOne = math.log(pwiGivenFreq / freqX, 2)
            finalProbability = pwi + pwiGivenWOne
            if max < finalProbability or max == 1000:
                max = finalProbability
                word = x
    if max == 1000:
        print("Cop out")
        word = selectOne()
    return word

# This method selects the third word in the sentence
# It uses the trigram model to select
# the most likely word to follow the first word
# Using markov triGram equation :
#   MAX [For All Wi in W : (P(wi)P(wi|wi-1))P(wi|wi-1, wi-2))]
# Param: string, wiTwo two words previous
#        string, wiONe previous word
#        int, totalWords total words in model
# Returns: Most likely word
def selectThree(wiTwo, wiOne, totalWords):
    word = ""
    max = 1000
    for x in uniGramMap.keys():
        pOne = p(x, totalWords)
        pTwo = p2(wiOne, x)
        pThree = p3(wiTwo, wiOne, x)
        probability = 0
        if pOne != 0 and pTwo != 0 and pThree != 0:
            probability = pOne + pTwo + pThree
            if max == 1000 or max < probability:
                max = probability
                word = x
    if max == 1000:
        word = selectOne()
    return word

# Find prob(word) = wordCount/totalWords
def p(word, totalWords):
        freqX = uniGramMap[word]
        #log of probability for word to appear
        pwi = math.log(freqX/totalWords, 2)
        return pwi

# Find prob(word|prevWord)
def p2(wordPrev, word):
        pwiGivenFreq = countTwoSeq(wordPrev, word)
        pwiGivenWOne = 0
        freqX = uniGramMap[wordPrev]
        if pwiGivenFreq != 0:
            pwiGivenWOne = math.log(pwiGivenFreq / freqX, 2)
        return pwiGivenWOne

# Find count(prevWord, word)
def countTwoSeq(wordPrev, word):
        pwiGivenFreq = 0
        if wordPrev in biGramMap.keys():
            node = biGramMap[wordPrev]
            flag = True
            while flag:
                if node.current == word:
                    pwiGivenFreq = node.value
                    flag = False
                elif node.nextNode is not None:
                    node = node.nextNode
                else:
                    flag = False
        return pwiGivenFreq

# Find count(prevprevWord,prevword, word)
def countThreeSeq(wordPrevPrev, wordPrev, word):
        freq = 0
        if wordPrevPrev in triGramMap.keys():
            node = triGramMap[wordPrevPrev]
            flag = True
            while flag:
                if node.current == wordPrev:
                    flagB = True
                    myNode = node.nextWiNode
                    while flagB:
                        if myNode.current == word:
                            freq = myNode.value
                            flagB = False
                        elif myNode.nextNode is not None:
                            myNode = myNode.nextNode
                        else:
                            flagB = False
                    flag = False
                elif node.nextNode is not None:
                    node = node.nextNode
                else:
                    flag = False
        return freq
# Find prob(word|prevWord, prevprevWord)
#   = count(prevprevWord, prevWord, word) / count(prevprevword, prevword)
def p3(wordPrevPrev, wordPrev, word):
    denominator = countTwoSeq(wordPrevPrev, wordPrev)
    numerator = countThreeSeq(wordPrevPrev, wordPrev, word)
    probability = 0
    if numerator != 0 and denominator != 0:
        probability = math.log(numerator / denominator, 2)
    return probability