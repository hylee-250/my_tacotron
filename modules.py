import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F

class ReferenceEncoder(nn.Module):
    '''
    inputs: 가변 길이의 오디오 신호 (log-mel spectrogram)
    [N,Ty/r, n_mels*r]
    
    outputs: 고정된 길이의 벡터(reference embedding)
    [N, ref_enc_gru_size]
    
    '''
    def __init__(self,hparams):
        super().__init__()
        # K: convolution layer의 층 개수
        K = len(hparams.ref_enc_filters)
        # 6 layer convolution layer의 출력 채널
        filters = [1] + hparams.ref_enc_filters
        
        convs = [nn.Conv2d(in_channels=filters[i],
                           out_channels=filters[i+1],
                           kernel_size=(3,3),
                           stride=(2,2),
                           padding=(1,1)) for i in range(K)]

        self.convs = nn.ModuleList(convs)
        self.bns = nn.ModuleList(
            [nn.BatchNorm2d(num_features=hparams.ref_enc_filters[i])
             for i in range(K)])
        
        out_channels = self.calculate_channels(L = hparams.n_mel_channels,kernel_size=3,stride=2,pad=1,n_convs=K)
                
        self.gru = nn.GRU(input_size=hparams.ref_enc_filters[-1]*out_channels,
                          hidden_size=hparams.ref_enc_gru_size,
                          batch_first=True)
        self.n_mel_channels= hparams.n_mel_channels
        self.ref_enc_gru_size = hparams.ref_enc_gru_size
        
    def forward(self,inputs, input_lengths=None):
        out= inputs.view(inputs.size(0),1,-1,self.n_mel_channels)
        for conv, bn in zip(self.convs,self.bns):
            out = conv(out)
            out = bn(out)
            out = F.relu(out)
            
        out = out.transpose(1,2) # [N, Ty//2^K, 128, n_mels//2^K]
        N,T = out.size(0),out.size(1)
        out = out.contiguous().view(N,T,-1) #[N, Ty//2^K, 128*n_mels//2^K]
        
        if input_lengths is not None:
            input_lengths = torch.ceil(input_lengths.float() / 2 ** len(self))
            input_lengths = input_lengths.cpu().numpy().astype(int)
            out = nn.utils.rnn.pack_padded_sequence(
                out, input_lengths, batch_first=True, enforce_sorted=False)
    
        self.gru.flatten_parameters()
        _, out = self.gru(out)
        return out.squeeze(0)
    
    def calculate_channels(self, L, kernel_size, stride, pad, n_convs):
        for _ in range(n_convs):
            L = (L-kernel_size + 2 * pad) // stride +1
        return L
    
class STL(nn.Module):
    '''
    inputs --- [N, token_embedding_size//2]
    '''
    def __init__(self,hparams):
        super().__init__()
        self.embed = nn.Parameter(torch.FloatTensor(hparams.token_num,hparams.token_embedding_size // hparams.num_heads))
        d_q = hparams.ref_enc_gru_size
        d_k = hparams.token_embedding_size // hparams.num_heads
        self.attention = MultiHeadAttention(
            query_dim =d_q, key_dim=d_k, num_units=hparams.token_embedding_size,
            num_heads=hparams.num_heads)
        
        init.normal_(self.embed, mean=0, std=0.5)
    
    def forward(self,inputs):
        N = inputs.size(0)
        query = inputs.unsqueeze(1)
        keys = torch.tanh(self.embed).unsqueeze(0).expand(N,-1,-1) #[N,token_num, token_embedding_size // num_heads]
        style_embed = self.attention(query,keys)
        
        return style_embed
    
class MultiHeadAttention(nn.Module):
    '''
    input:
        query --- [N, T_q, query_dim]
        key --- [N, T_k, key_dim]
    output:
        out --- [N, T_q, num_units]
    '''
    def __init__(self,query_dim, key_dim, num_units, num_heads):
        super().__init__()
        self.num_units = num_units
        self.num_heads = num_heads
        self.key_dim = key_dim
        
        self.W_query = nn.Linear(in_features=query_dim,out_features=num_units,bias=False)
        self.W_key = nn.Linear(in_features=key_dim,out_features=num_units,bias=False)
        self.W_value = nn.Linear(in_features=key_dim,out_features=num_units,bias=False)
    
    def forward(self,query,key):
        querys = self.W_query(query)    # [N, T_q, num_units]
        keys = self.W_key(key)          # [N, T_k, num_units]
        values = self.W_value(key)
        
        split_size = self.num_units // self.num_heads
        querys = torch.stack(torch.split(querys,split_size,dim=2), dim=0)    # [h, N, T_q, num_units/h]
        keys = torch.stack(torch.split(keys, split_size,dim=2),dim=0)        # [h, N, T_k, num_units/h]
        values = torch.stack(torch.split(values,split_size, dim=2),dim=0)    # [h, N, T_k, num_units/h]
        
        scores = torch.matmul(querys, keys.transpose(2,3)) # [h, N, T_q, T_k]
        scores = scores / (self.key_dim ** 0.5)
        scores = F.softmax(scores, dim=3)
        
        # out = score * V
        out = torch.matmul(scores, values)  # [h,N,T_q, num_units/h]
        out = torch.cat(torch.split(out,1,dim=0), dim=3).squeeze(0) # [N, T_q, num_units]
        
        return out
            
class GST(nn.Module):
    def __init__(self,hparams):
        super().__init__()
        self.encoder = ReferenceEncoder(hparams)
        self.stl = STL(hparams)
        
    def forward(self, inputs, input_lengths=None):
        enc_out = self.encoder(inputs, input_lengths=input_lengths)
        style_embed = self.stl(enc_out)
        
        return style_embed