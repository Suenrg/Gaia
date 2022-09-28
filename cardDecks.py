class Card: #create the card class, for storing tarot card objects
    def __init__(self, name, icon, upright, reverse, upLong, revLong):
        self.name = name
        self.icon = icon
        self.upright = upright
        self.reverse = reverse
        self.upLong = upB
        self.revLong = revB
    def prints(self):
        print("Name: " + self.name +" Up: " + self.up + " rev: "+ self.rev + " gen: "+self.upB + ' revB: '+self.revB + ')



class Deck:
    def __init__(self, name):
        self.name = Name
        self.cards = {}

    def addCard(card):
        cards.append(card)



def loadDecks(paths):
    decks = {}
    for i in paths:
        with open(i, errors="ignore") as f:
            for line in f:
                # create card
    return decks
