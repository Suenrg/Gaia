import os
from tarotFuncs import *


class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = {}

    def addCard(self, card):
        self.cards.append(card)



def loadDecks(paths):
    decks = {}
    cards = {}
    for i in paths:
        deckName = ""
        with open(i, errors="ignore") as f:
            for line in f:
                if (line.startswith("Name")):
                    deckName=(line.split("\t")[1]).replace("\n", "")
                else:
                    line = line.replace("\n", "")
                    splat = line.split("\t")
                    newCard = Card(splat[0], splat[1], splat[2], splat[3], splat[4], splat[5])
                    cards[newCard.name] = newCard
        decks[deckName] = cards

    return decks

# ##main
# meaningsPath = [os.path.dirname(__file__)+"\\meanings\\tarotMeanings.tsv"]
# imgPath = os.path.dirname(__file__)+"\\images\\tarot\\"

# decks = loadDecks(meaningsPath)
# print(decks)
