from copyreg import pickle
from dataset import LanguageDataset
import os
import pickle

from tokenizer import Language, Tokenizer

data = LanguageDataset.read_data(
    os.path.join("C:\\Users\\Steven\\Desktop\\ML","english.txt"), 
    os.path.join("C:\\Users\\Steven\\Desktop\\ML","french.txt")
)

unique = set()
unique = unique.union(["[CLS]", "[SEP]", "[PAD]"])
counter = 0

en_tokenizer = Tokenizer(Language.EN)
fr_tokenizer = Tokenizer(Language.FR)

for en_sentence in data[0]:
    tokens = en_tokenizer.tokenize(en_sentence)
    unique = unique.union(tokens)

for fr_sentence in data[1]:
    tokens = fr_tokenizer.tokenize(fr_sentence)
    unique = unique.union(tokens)

map = { u: i+1 for i, u in enumerate(unique) }

with open("mapped.pkl", 'wb') as f:
    pickle.dump(map, f)