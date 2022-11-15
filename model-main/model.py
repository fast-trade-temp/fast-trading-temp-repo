
import torch
import torch.nn as nn
import torch.nn.functional as F
import copy
import math

class MultiHeadedAttention(nn.Module):
    def __init__(self, heads, d_model, drop_p=0.1):
        super(MultiHeadedAttention, self).__init__()
        self.d_model = d_model
        self.d_k = d_model // heads
        self.heads = heads
        self.q_lin = nn.Linear(d_model, d_model)
        self.v_lin = nn.Linear(d_model, d_model)
        self.k_lin = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, d_model)
        self.attn = None
        self.dropout = nn.Dropout(drop_p)
        
    def forward(self, q, k, v, mask=None):
        batch_size = q.size(0)
        
        q = self.q_lin(q).view(batch_size, -1, self.heads, self.d_k)
        k = self.k_lin(k).view(batch_size, -1, self.heads, self.d_k)
        v = self.v_lin(v).view(batch_size, -1, self.heads, self.d_k)
        
        q = q.transpose(1,2)
        k = k.transpose(1,2)
        v = v.transpose(1,2)
        
        scores = attention(q, k, v, self.d_k, mask, self.dropout)
        
        concat = scores.transpose(1,2).contiguous().view(batch_size, -1, self.d_model)
        output = self.out(concat)
    
        return output

class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff=2048, dropout=0.1):
        super(FeedForward, self).__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        return self.w_2(self.dropout(F.relu(self.w_1(x))))

class PositionalEncoder(nn.Module):
    def __init__(self, d_model, seq_len):
        super(PositionalEncoder, self).__init__()
        self.d_model = d_model
        
        pe = torch.zeros(seq_len, d_model)
        for pos in range(seq_len):
            for i in range(0, d_model, 2):
                pe[pos, i] = math.sin(pos / (10000 ** (i/d_model)))
                pe[pos, i + 1] = math.cos(pos / (10000 ** (i/d_model)))
                
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
        
    def forward(self, x):
        x = x * math.sqrt(self.d_model) 
        seq_len = x.size(1)
        x = x + torch.autograd.Variable(self.pe[:,:seq_len], requires_grad=False).cuda()
        return x

class EncoderLayer(nn.Module):
    def __init__(self, d_model, heads, dropout = 0.1):
        super().__init__()
        self.norm_1 = torch.nn.LayerNorm(d_model)
        self.norm_2 = torch.nn.LayerNorm(d_model)
        self.attn = MultiHeadedAttention(heads, d_model)
        self.ff = FeedForward(d_model, dropout=dropout)
        self.dropout_1 = nn.Dropout(dropout)
        self.dropout_2 = nn.Dropout(dropout)
        
    def forward(self, x, mask):
        x2 = self.norm_1(x)
        x = x + self.dropout_1(self.attn(x2,x2,x2,mask))
        x2 = self.norm_2(x)
        x = x + self.dropout_2(self.ff(x2))
        return x
    
class DecoderLayer(nn.Module):
    def __init__(self, d_model, heads, dropout=0.1):
        super().__init__()
        self.norm_1 = torch.nn.LayerNorm(d_model)
        self.norm_2 = torch.nn.LayerNorm(d_model)
        self.norm_3 = torch.nn.LayerNorm(d_model)
        
        self.dropout_1 = nn.Dropout(dropout)
        self.dropout_2 = nn.Dropout(dropout)
        self.dropout_3 = nn.Dropout(dropout)
        
        self.attn_1 = MultiHeadedAttention(heads, d_model)
        self.attn_2 = MultiHeadedAttention(heads, d_model)
        self.ff = FeedForward(d_model, dropout=dropout)
        
    def forward(self, x, e_outputs, src_mask, trg_mask):
        x2 = self.norm_1(x)
        x = x + self.dropout_1(self.attn_1(x2, x2, x2, trg_mask))
        x2 = self.norm_2(x)
        x = x + self.dropout_2(self.attn_2(x2, e_outputs, e_outputs, src_mask))
        x2 = self.norm_3(x)
        x = x + self.dropout_3(self.ff(x2))
        return x

class Encoder(nn.Module):
    def __init__(self, d_model, N, heads, seq_len):
        super().__init__()
        self.N = N
        self.pe = PositionalEncoder(d_model, seq_len)
        self.layers = get_clones(EncoderLayer(d_model, heads), N)
        self.norm = torch.nn.LayerNorm(d_model)
        
    def forward(self, src, mask):
        x = self.pe(src)
        for i in range(self.N):
            x = self.layers[i](x, mask)
        return self.norm(x)
    
class Decoder(nn.Module):
    def __init__(self, d_model, N, heads, seq_len):
        super().__init__()
        self.N = N
        self.pe = PositionalEncoder(d_model, seq_len)
        self.layers = get_clones(DecoderLayer(d_model, heads), N)
        self.norm = torch.nn.LayerNorm(d_model)
        
    def forward(self, trg, e_outputs, src_mask, trg_mask):
        x = self.pe(trg)
        for i in range(self.N):
            x = self.layers[i](x, e_outputs, src_mask, trg_mask)
        return self.norm(x)

class Transformer(nn.Module):
    def __init__(self, src_vocab, trg_vocab, d_model, N, heads, seq_len):
        super().__init__()
        self.encoder = Encoder(d_model, N, heads, seq_len)
        self.decoder = Decoder(d_model, N, heads, seq_len)
        self.out = nn.Linear(d_model, trg_vocab)
        
    def forward(self, src, trg, src_mask, trg_mask):
        e_outputs = self.encoder(src, src_mask)
        d_output = self.decoder(trg, e_outputs, src_mask, trg_mask)
        output = self.out(d_output)
        return output

def attention(q, k, v, d_k, mask=None, dropout=None):
    scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        mask = mask.unsqueeze(1)
        scores = scores.masked_fill(mask == 0, -1e9)
    p_attn = scores.softmax(dim=-1)
    if dropout is not None:
        p_attn = dropout(p_attn)
    return torch.matmul(p_attn, v)

def get_clones(module, N):
    return nn.ModuleList([copy.deepcopy(module) for i in range(N)])