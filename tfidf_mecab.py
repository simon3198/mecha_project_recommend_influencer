#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eunjeon import Mecab
from konlpy.tag import Okt
import pandas as pd # 데이터프레임 사용을 위해
from math import log # IDF 계산을 위해
import io
import re
import pandas as pd


def onlytext(temp):
  temp = temp.replace("\u200b"," ").replace("\t"," ").replace("\n"," ").replace("#"," ")
  temp = re.sub(r'[^가-힣 ]','',temp)
  temp = temp.replace('페인팅','페인')
  temp = temp.replace('페인','페인팅')
  temp = temp.replace('하루 클래스','하루클래스')
  temp =temp.replace('아이 러브','아이러브')
  temp = temp.replace('러브 페인팅','러브페인팅')
  return temp

def isnan(temp):
  return temp != temp

def tf(t, d):
    return d.count(t)

def idf(N,t,docs):
    df = 0
    for doc in docs:
        df += t in doc
    return log(N/(df + 1))

def tfidf(idf_,t, d):
    return tf(t,d)* idf_['IDF'][t]

def tfidf_ad(train_data):
  docs=[]
  num =-1
  for i in train_data['Post']:
    num+=1
    #not 직접
    #if 광고
    if isnan(train_data['AD'][num]):
      continue
    i = onlytext(i)
    if isnan(i):
      continue
    docs.append(i)
  mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')

  vocab = list(set(w for doc in docs for w in mecab.morphs(doc) if len(w)>1))
  vocab.sort()
  N = len(docs) # 총 문서의 수
  result = []
  for i in range(N): # 각 문서에 대해서 아래 명령을 수행
      result.append([])
      d = docs[i]
      for j in range(len(vocab)):
          t = vocab[j]
          result[-1].append(tf(t, d))

  result_idf = []
  for j in range(len(vocab)):
      t = vocab[j]
      result_idf.append(idf(N,t,docs))

  idf_ = pd.DataFrame(result_idf, index = vocab, columns = ["IDF"])
  idf_.sort_values(by='IDF')

  result = []
  for i in range(N):
      result.append([])
      d = docs[i]
      for j in range(len(vocab)):
          t = vocab[j]

          result[-1].append(tfidf(idf_,t,d))

  tfidf_ = pd.DataFrame(result, columns = vocab)

  tfidf_ = tfidf_.append(tfidf_.mean(),ignore_index=True)
  return dict(tfidf_.iloc[-1].sort_values(ascending=False).head(20))


def tfidf_notad(train_data):
  docs=[]
  num =-1
  for i in train_data['Post']:
    num+=1
    #not 직접
    #if 광고
    if not isnan(train_data['AD'][num]):
      continue
    i = onlytext(i)
    if isnan(i):
      continue
    docs.append(i)
  mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')

  vocab = list(set(w for doc in docs for w in mecab.morphs(doc) if len(w)>1))
  vocab.sort()
  N = len(docs) # 총 문서의 수
  result = []
  for i in range(N): # 각 문서에 대해서 아래 명령을 수행
      result.append([])
      d = docs[i]
      for j in range(len(vocab)):
          t = vocab[j]
          result[-1].append(tf(t, d))

  result_idf = []
  for j in range(len(vocab)):
      t = vocab[j]
      result_idf.append(idf(N,t,docs))

  idf_ = pd.DataFrame(result_idf, index = vocab, columns = ["IDF"])
  idf_.sort_values(by='IDF')

  result = []
  for i in range(N):
      result.append([])
      d = docs[i]
      for j in range(len(vocab)):
          t = vocab[j]

          result[-1].append(tfidf(idf_,t,d))

  tfidf_ = pd.DataFrame(result, columns = vocab)

  tfidf_ = tfidf_.append(tfidf_.mean(),ignore_index=True)
  return dict(tfidf_.iloc[-1].sort_values(ascending=False).head(20))




# import matplotlib.pyplot as plt
# import matplotlib
# import matplotlib as mpl
# from matplotlib import font_manager, rc

# font_path = "C:/Windows/Fonts/NanumGothic.ttf"
# font = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font)

# plt.figure(figsize=(12,12))
# tfidf_.iloc[-1].sort_values(ascending=False).head(50).plot(kind='barh')
# plt.xlabel('tfidf mean')
# plt.title('광고 글 morphs tfidf')
# plt.xlim(0.6,1.8)
# plt.show()