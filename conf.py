##conf.py
import os
path = os.path.dirname(__file__)
vaultPath = path + "\\vault\\"
meaningsPath = [path + "\\meanings\\tarotMeanings.tsv"]
imgPath = path + "\\images\\tarot\\"
deckPrefsPath = path + "\\settings\\deckPrefs.txt"
talkingChannelsPath = path + "\\settings\\talkingChannels.txt"
layoutsPath = path + "\\meanings\\layouts"
sigilImagesPath = path + "\\images\\"


defaultDeck = "Biddy"
defaultArt = "Biddy"
deckChoices = ["Biddy"]
artChoices = ["Biddy"]
layoutChoices = ["spiral", "rect", "geomabet", "querty"]
