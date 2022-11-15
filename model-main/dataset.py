from tokenizer import Language, Tokenizer
from torch.utils.data import Dataset
import torch
import os
import numpy as np

class LanguageDataset(Dataset):

    def __init__(self, root_dir, max_token_len, model_en, model_fr):
        self.data = LanguageDataset.read_data(
            os.path.join(root_dir,"english_filtered.txt"), 
            os.path.join(root_dir,"french_filtered.txt")
        )
  
        self.max_token_len = max_token_len
        self.en_tokenizer = Tokenizer(Language.EN)
        self.fr_tokenizer = Tokenizer(Language.FR)
        self.en_vocab_size = len(self.en_tokenizer.nlp.vocab.vectors)
        self.fr_vocab_size = len(self.fr_tokenizer.nlp.vocab.vectors)
        
        self.model_en = model_en
        self.model_fr = model_fr


    def __len__(self):
        return len(self.data[0])

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        src = self.en_tokenizer.tokenize(self.data[0][idx])
        tgt = self.fr_tokenizer.tokenize(self.data[1][idx])

        src.append("[SEP]")
        src += ["[PAD]"] * (self.max_token_len - len(src))

        tgt.insert(0, "[CLS]")
        tgt.append("[SEP]")
        tgt += ["[PAD]"] * (self.max_token_len - len(tgt))

        src_transformed = torch.stack(tuple(self.model_en[token] for token in src))
        tgt_transformed = torch.stack(tuple(self.model_fr[token] for token in tgt))

        try:
            tgt_comp = np.array([self.model_fr.stoi[token] for token in tgt])
        except Exception as e:
            print(tgt)
            
        tgt_comp = np.roll(tgt_comp, -1)
        tgt_comp[-1] = self.model_fr.stoi["[PAD]"] 
        tgt_comp = torch.from_numpy(tgt_comp).type(torch.LongTensor)

        item = {
            'src': src,
            'tgt': tgt,
            'src_tr': src_transformed,
            'tgt_tr': tgt_transformed,
            'tgt_comp': tgt_comp
        }

        return item

    @staticmethod
    def read_data(src_dir, tgt_dir):
        try:
            src_data = open(src_dir, encoding="utf8").read().strip().split('\n')
            trg_data = open(tgt_dir, encoding="utf8").read().strip().split('\n')
            return (src_data, trg_data)
        except Exception as e:
            print("error: " + str(e))