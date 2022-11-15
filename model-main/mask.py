import numpy as np
import torch


def nopeak_mask(size):
    np_mask = np.triu(np.ones((1, size, size)), k=1).astype('uint8')
    np_mask = (torch.from_numpy(np_mask) == 0).cuda()
    return np_mask

def create_masks(src, tgt):
    src_mask = torch.from_numpy(src != "[PAD]").unsqueeze(-2).cuda()

    if tgt is not None:
        tgt_mask = torch.from_numpy((tgt != "[PAD]")).unsqueeze(-2).cuda()
        size = tgt.shape[1]
        np_mask = nopeak_mask(size)
        tgt_mask = tgt_mask & np_mask
    else:
        tgt_mask = None
    return src_mask, tgt_mask