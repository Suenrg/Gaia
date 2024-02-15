##conf.py
import os
path = os.path.dirname(__file__)
vaultPath = path + "/vault/"
meaningsPath = [path + "/meanings/tarotMeanings.tsv"]
imgPath = path + "/images/tarot/"
deckPrefsPath = path + "/settings/deckPrefs"
talkingChannelsPath = path + "/settings/talkingChannels"
layoutsPath = path + "/meanings/layouts"
sigilImagesPath = path + "/images/"


defaultDeck = "Biddy"
defaultArt = "Biddy"
deckChoices = ["Biddy"]
artChoices = ["Biddy", "Rider Waite"]
# layoutChoices = ["spiral", "rect", "geomabet", "querty"]
