import utils
from nagisa.tagger import Tagger

version = '0.1.2'
# Initialize instance
tagger  = Tagger()
# Functions
wakati  = tagger.wakati
tagging = tagger.tagging
filter  = tagger.filter
extract = tagger.extract
postagging = tagger.postagging
