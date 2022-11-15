import spacy
import re
from enum import Enum

class Language(Enum):
    EN = "en_core_web_sm"
    FR = "fr_core_news_sm"

class Tokenizer():
    def __init__(self, language):
        self.nlp = spacy.load(language.value)
            
    def tokenize(self, sentence):
        sentence = re.sub(r"[\*\"“”\n\\…\+\-\/\=\(\)‘•:\[\]\|’;]", " ", str(sentence))
        sentence = re.sub(r"[ ]+", " ", sentence)
        sentence = re.sub(r"\!+", "!", sentence)
        sentence = re.sub(r"\,+", ",", sentence)
        sentence = re.sub(r"\?+", "?", sentence)
        sentence = re.sub(r"\u202f", "", sentence)
        sentence = re.sub(r"'", " ", sentence)
        sentence = re.sub(r"[0-9]","", sentence)
        sentence = sentence.lower()
        return [tok.text for tok in self.nlp.tokenizer(sentence) if tok.text != " "]