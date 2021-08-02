from konlpy.tag import Okt
import pandas as pd
import numpy as np
import re
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

file_name = '../csvfile/보석십자수2021-07-06.csv'

df = pd.read_csv(file_name)

#상위 200개 본문들 tokenized( 형태소로)
okt = Okt()
df = df.iloc[:2]
posts = df['Post']
post_list = [re.sub(r"[^0-9가-힣?.!,¿]+", " ", post) for post in posts]
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
tokenized_posts = []
for post in post_list:
    tokenized_post = okt.morphs(post)
    tokenized_post = [token for token in tokenized_post if token not in stopwords]
    tokenized_posts.append(tokenized_post)

#각 본문에 대해서 벡터화
documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(tokenized_posts)]
model_doc = Doc2Vec(documents, vector_size=100, window=2, min_count=1, workers=4)

post_vector_list = []

for i in range(len(model_doc.dv)):
    post_vector_list.append(model_doc.dv[i])
post_vector_list = np.asarray(post_vector_list)

#LSTM 정답 구하기
y_numerator = df['Sympathy num'] + df['Comment num']
y_demonitator = [] # 나중에 구하자.

y = y_numerator
y

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM
x = post_vector_list
x = x.reshape((x.shape[0],x.shape[1],1))

model = Sequential()
model.add(LSTM(10,activation='relu'))
model.add(Dense(5))
model.add(Dense(1))

model.compile(optimizer='adam',loss='mse')
model.fit(x,y,epochs=100,batch_size=1)

