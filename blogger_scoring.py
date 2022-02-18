import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm.notebook import tqdm
from kobert import get_tokenizer
from kobert import get_pytorch_kobert_model
import pandas as pd
import datetime
import kss
import re

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
sent_path = './model/sentiment_model.pt'
subj_path = '/model/subjetive_model.pt'
#데이터 셋을 BERT모델에 알맞은 형태로 변경
class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len, pad, pair):
        transform = nlp.data.BERTSentenceTransform(bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]
    
    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))
    
    def __len__(self):
        return len(self.labels)

#BERT 모델
#sentiment predict를 위해서는 num_classes를 3으로 설정해준다
#objective/subjective predict를 위해서는 num_classes를 2로 설정해준다.
#default는 3으로 되어있다
class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=3,
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size, num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)
        
    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()
    
    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)        


def load_model(model_path, num_classes:int = 2):
    model = BERTClassifier(bertmodel, num_classes=num_classes, dr_rate=0.5).to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

class Scorer:

    def __init__(self, blogger_name, sentiment_model, subjective_model, tokenizer):
        file_path = f"./blogger detail/{blogger_name}.csv"
        self.blogger_name = blogger_name
        self.df=  pd.read_csv(file_path, index_col = 0)
        self.tok = tokenizer
        self.sentiment_model = sentiment_model
        self.subjective_model = subjective_model

    def row_func(self, row):
        year, month, day, _ = row.split(".")
        return datetime.date(int(year), int(month), int(day))
    
    def preprocessing(self, sentence):
        sentence = re.sub("[^ ㄱ-ㅎ가-힣a-zA-Z0-9]","",sentence)
        return sentence

    def split_post(self, post):
        sentences = []
        print("---spliting---")
        for sentence in kss.split_sentences(post):
            sentences.append(sentence)
        print("---split finish!---")
        return sentences

    def bertToTorch(self, _data, device):
        token_ids, valid_length, segment_ids, label = _data
        token_ids = torch.tensor([token_ids])
        segment_ids = torch.tensor([segment_ids])
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)
        valid_length = torch.IntTensor([valid_length.item()])
        return token_ids, valid_length, segment_ids

    def toBertDataset(self, post):
        max_len = 64
        post = [[sent,'1'] for sent in post]
        bertdataset = BERTDataset(post, 0, 1, self.tok, max_len, True, False)
        return bertdataset

    def scoring_func(self, _predicted):
        predicted = _predicted.cpu().detach().numpy()
        predicted_value = np.argmax(predicted)
        return predicted_value

    def predict_label(self, _bertdataset, _model, score_func):
        predicted_labels = []
        for bs in _bertdataset:
            token_ids, valid_length, segment_ids = self.bertToTorch(bs, device)
            predicted = _model(token_ids, valid_length, segment_ids)
            predicted_value = score_func(predicted)
            predicted_labels.append(predicted_value)
        
        predicted_labels = predicted_labels
        return predicted_labels

    def scoring(self):
        dates = df['Posting Date']
        dates = dates.apply(self.row_func)

        df['Posting Date'] = dates
        df = df.sort_values(by=['Posting Date'], ascending=False)

        if len(df) > 90:
            df = df[:90]

        posts = df['Post']
        posts = posts.apply(self.preprocessing)
        df['Post'] = posts
        
        posts = df['Post'].apply(self.split_post)
        posts_sentiments = []
        posts_subjectives = []

        for post in posts:

            post_bert = self.toBertDataset(post)
            predicted_sentiments = self.predict_label(post_bert, self.sentiment_model, self.scoring_func)
            predicted_subjectives = self.predict_label(post_bert, self.subjective_model, self.scoring_func)

            posts_sentiments.append(predicted_sentiments)
            posts_subjectives.append(predicted_subjectives)

        posts = posts.values
        after_predicted = []
        for post, sentiments, subjectives in zip(posts, posts_sentiments, posts_subjectives):
            after_predicted.append([(sentence, sentiment, subjective) for sentence, sentiment, subjective in zip(post, sentiments, subjectives)])

        df['AP'] = after_predicted

        file_path = f'./datas/{self.blogger_name}.csv'
        df.to_csv(file_path)
        print(f"{self.blogger_name} saving finish!")
        
if __name__ == '__main__':
    #KoBERT 모델과 KoBERT vocabulary를 다운받는다.
    bertmodel, vocab = get_pytorch_kobert_model(cachedir=".cache")

    blogger_list = ['rilrastory']
    sentiment_model = load_model(sent_path, 3)
    subjective_model = load_model(subj_path, 2)

    tokenizer = get_tokenizer()
    tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False) 
    for blogger_name in blogger_list:
        scorer = Scorer(blogger_name, sentiment_model, subjective_model, tok)
        scorer.scoring()


















