import torch
import torch.nn.functional as F
import pytorch_lightning as pl
import numpy as np

from torch.utils.data import DataLoader

from dataset import LanguageDataset
from mask import create_masks
from model import Transformer

import torchtext

D_MODEL = 300
HEADS = 8
N = 6
MAX_TOKEN_LEN = 128

model_en = torchtext.vocab.FastText("en")
model_fr = torchtext.vocab.FastText("fr")

model_en.stoi["[PAD]"] = len(model_en.vectors)
model_en.stoi["[CLS]"] = len(model_en.vectors) + 1
model_en.stoi["[SEP]"] = len(model_en.vectors) + 2

model_en.itos.append("[PAD]")
model_en.itos.append("[CLS]")
model_en.itos.append("[SEP]")

model_fr.stoi["[PAD]"] = len(model_fr.vectors)
model_fr.stoi["[CLS]"] = len(model_fr.vectors) + 1
model_fr.stoi["[SEP]"] = len(model_fr.vectors) + 2

model_fr.itos.append("[PAD]")
model_fr.itos.append("[CLS]")
model_fr.itos.append("[SEP]")

pad_tensor = torch.zeros(1, 300) + 0.1
start_tensor = torch.zeros(1, 300) + 0.2
end_tensor = torch.zeros(1, 300) + 0.3

model_en.vectors = torch.cat((model_en.vectors, pad_tensor, start_tensor, end_tensor))
model_fr.vectors = torch.cat((model_fr.vectors, pad_tensor, start_tensor, end_tensor))

class TransformerModel(pl.LightningModule):
    def __init__(self, transformer):
        super().__init__()
        self.model = transformer

        for p in self.model.parameters():
            if p.dim() > 1:
                torch.nn.init.xavier_uniform_(p)
    
    def forward(self, src, tgt, src_mask, trg_mask):
        return self.model(src, tgt, src_mask, trg_mask)
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.0001, betas=(0.9, 0.98), eps=1e-9)
        
    def training_step(self, batch, batch_idx):
        src = np.array(batch['src']).transpose((1,0))
        tgt = np.array(batch['tgt']).transpose((1,0))
        src_tr = batch['src_tr']
        tgt_tr = batch['tgt_tr']
        tgt_comp = batch['tgt_comp']

        src_mask, tgt_mask = create_masks(src, tgt)
        y_pred = self(src_tr, tgt_tr, src_mask, tgt_mask)
        y_pred = torch.permute(y_pred, (0, 2, 1))
        loss = F.cross_entropy(y_pred, tgt_comp)
        return loss

def train():
    dataset = LanguageDataset("C:\\Users\\Steven\\Desktop\\ML", MAX_TOKEN_LEN, model_en, model_fr)
    train_loader = DataLoader(dataset=dataset, batch_size=2)
    trainer = pl.Trainer(max_epochs=1, accelerator='gpu', devices='1')
    model = TransformerModel(
        Transformer(
            len(model_en.vectors),
            len(model_fr.vectors),
            D_MODEL,
            HEADS,
            N,
            MAX_TOKEN_LEN
        )       
    )

    trainer.fit(model, train_dataloaders=train_loader)

if __name__ == '__main__':
    train()