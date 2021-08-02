#!/usr/bin/env python
# -*- coding: utf-8 -*-
import eunjeon
from eunjeon import Mecab
from collections import Counter
import pandas as pd
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt 
import re

def onlytext(temp):
    temp = temp.replace("\u200b"," ").replace("\t"," ").replace("\n"," ").replace("#"," ")
    temp = re.sub(r'[^가-힣 ]','',temp)
    return temp

# keyword_list = ['다이소', '생각','주문', '디즈니', '액자', '큐빅', '해바라기', '선물', '그림','아이','구매','주문','배송','시작','내돈내산','내돈','내산']
# minus_list = ['러브','페인','생활','아이','취미','사용','추천','정말','제품']
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
# score_list=[]
# nounlist=[]
# verb_list=[]
# josa_list=[]
# adjective_list=[]
# punctuation_list=[]
# exclamation_list=[]
# foreign_list=[]
def isNaN(num):
    return num != num
# okt = Twitter()
# okt.add_dictionary('내돈내산', 'Noun')
# okt.add_dictionary('내돈', 'Noun')s
# okt.add_dictionary('내산', 'Noun')
# okt.add_dictionary('리얼', 'Noun')
# okt.add_dictionary('리뷰', 'Noun')
# ss.add_dictionary('집순이', 'Noun')
mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
# all_noun_dict={}
def getWordFrequencyListFromCSV_notad(data):
    #data = pd.read_csv(csv_name+".csv")
    text_list=[]
    all_noun_list=[]
    all_text=""
    num=-1
    count=0
    for post in data['Post']:
        num+=1
        #not 광고
        #if 직접
        if isNaN(data['AD'][num]):
            count+=1
            post += str(data['Title'][num])
            post = onlytext(post)
            text_list.append(str(post))
            all_text = all_text + str(post)
    
    print(count)
    text_list.append(all_text)
    
    for text in text_list:
        
        if isNaN(text):
            print("2")
            continue
        temp_X = mecab.morphs(text) # 토큰화
        noun = [word for word in temp_X if not word in stopwords if not len(word)<2] # 불용어 제거
        noun_len = len(noun)
        count = Counter(noun)
        noun_list = count.most_common(100)
        noun_dict = dict()
        for item,num in noun_list:
            noun_dict[item] = round(num/noun_len,10)*100
        all_noun_list.append(noun_dict)
        # for v in noun_list:
        #     print(v)

        # print("-"*50)
        
    return all_noun_list

def getWordFrequencyListFromCSV_ad(data):
    #data = pd.read_csv(csv_name+".csv")
    text_list=[]
    all_noun_list=[]
    all_text=""
    num=-1
    count=0
    for post in data['Post']:
        num+=1
        #not 광고
        #if 직접
        if not isNaN(data['AD'][num]):
            count+=1
            post += str(data['Title'][num])
            post = onlytext(post)
            text_list.append(str(post))
            all_text = all_text + str(post)
    
    print(count)
    text_list.append(all_text)
    
    for text in text_list:
        
        if isNaN(text):
            print("2")
            continue
        temp_X = mecab.morphs(text) # 토큰화
        noun = [word for word in temp_X if not word in stopwords if not len(word)<2] # 불용어 제거
        noun_len = len(noun)
        count = Counter(noun)
        noun_list = count.most_common(100)
        noun_dict = dict()
        for item,num in noun_list:
            noun_dict[item] = round(num/noun_len,10)*100
        all_noun_list.append(noun_dict)
        # for v in noun_list:
        #     print(v)

        # print("-"*50)
        
    return all_noun_list

# csv_name = './crawler/보석십자수2021-07-13'
# data = pd.read_csv(csv_name+".csv")
# # csv_name = './crawler/DIY2021-07-13'
# # data2 = pd.read_csv(csv_name+".csv")
# # data = pd.concat([data2,data1],ignore_index=True)
# # print(data)
# word_frequency_list = getWordFrequencyListFromCSV(data)
# for i in word_frequency_list[-1]:
#     word_frequency_list[-1][i] = round(word_frequency_list[-1][i],4)
# print(word_frequency_list[-1])
# total_word_frequency = word_frequency_list[-1]
# total_word_frequency_s = pd.Series(total_word_frequency)

######################################################################

# wc = WordCloud(font_path='font/NanumGothic.ttf', \
# 	background_color="white", \
# 	width=1000, \
# 	height=1000, \
# 	max_words=100, \
# 	max_font_size=300, \
#     colormap = 'Set1'
#     )
    

# wc.generate_from_frequencies(word_frequency_list[-1])
# wc.to_file('notad_wordcloud.png')

#print(sorted([f.name for f in fm.fontManager.ttflist if f.name.startswith('Nanum')]))


#######################################################################
# mpl.rc('font',family='NanumGothic')
# mpl.rc('axes',unicode_minus=False)

# plt.figure(figsize=(100,100))
# total_word_frequency_s.plot(kind = 'bar')
# plt.show()