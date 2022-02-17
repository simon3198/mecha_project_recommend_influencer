# -*- coding: utf-8 -*-
from typing import final
from eunjeon import Mecab
from collections import Counter
import pandas as pd
import numpy as np
import re
import ast

def isNaN(num):
    return num != num

def onlytext(temp):
    temp = temp.replace("\u200b"," ").replace("\t"," ").replace("\n"," ").replace("#"," ")
    temp = re.sub(r'[^가-힣 ]','',temp)
    return temp

def list2dic(temp):
    res ={}
    n = int(len(temp)/2)
    for i in range(n):
        res[temp[i*2+1]] = round(float(temp[2*i+2]),4)
    return res

def standard(temp):
    a=np.array(temp)
    mean = np.mean(temp)
    std = np.std(temp)
    for i in range(len(temp)):
        temp[i] = (temp[i]-mean)/std
    return temp,mean,std

def score_blogger(itemname,data):
    threshold_data = pd.read_csv('./threshold/threshold_'+itemname+'.csv')
    threshold_data = threshold_data.loc[0]

    threshold_list=[]
    threshold_list.append(ast.literal_eval(threshold_data['keyword']))
    threshold_list.append(ast.literal_eval(threshold_data['tfidf']))
    threshold_list.append(ast.literal_eval(threshold_data['paragraph']))
    threshold_list.append(ast.literal_eval(threshold_data['image']))
    threshold_list.append(ast.literal_eval(threshold_data['video']))
    threshold_list.append(ast.literal_eval(threshold_data['gif']))
    threshold_list.append(ast.literal_eval(threshold_data['sticker']))
    threshold_list.append([threshold_data['grammer mean'],threshold_data['grammer std']])
    threshold_list.append([threshold_data['imgwrd mean'],threshold_data['imgwrd std']])


    keyword_data = pd.read_csv('write.csv',header=None, error_bad_lines=False)
    keyword_data.set_index(0, inplace = True)

    ad_keyword_list = keyword_data.loc[itemname+'ad']
    notad_keyword_list = keyword_data.loc[itemname+'notad']
    tfidf_ad_keyword_list = keyword_data.loc[itemname+'tfidf_ad']
    tfidf_ad_keyword_list = list2dic(tfidf_ad_keyword_list)
    tfidf_notad_keyword_list = keyword_data.loc[itemname+'tfidf_notad']
    tfidf_notad_keyword_list= list2dic(tfidf_notad_keyword_list)

    mecab = Mecab()
    all_noun_dict={}
    text_list=[]
    all_noun_list=[]
    final_list=[]
    all_text=""
    num_=-1
    count=0
    post_df_idx=0
    ad = 1
    #############################################################
    for post in data['Post']:
        num_+=1
        post = onlytext(post)
        text_list.append(str(post))
        text = str(post)
        all_text = all_text + str(post)
        if isNaN(text):
            continue
        temp_X = mecab.morphs(text)
        noun = [word for word in temp_X if len(word)>1] # 불용어 제거
        noun_len = len(noun)
        
        ########################################################
        #keyword score calculation
        score=0
        for keyword in notad_keyword_list:
            for i in noun:
                if keyword == i:
                    score +=1
        for keyword in ad_keyword_list:
            for i in noun:
                if keyword == i:
                    score -=1
        score /= noun_len
        score *=100
        keyword_score=score
        score=0

        ########################################################
        #itidf keyword score calculation
        temp_score=0
        for keyword in tfidf_notad_keyword_list.keys():
            for i in noun:
                if keyword == i:
                    temp_score += tfidf_notad_keyword_list[keyword]
        for keyword in tfidf_ad_keyword_list.keys():
            for i in noun:
                if keyword == i:
                    temp_score -= tfidf_ad_keyword_list[keyword]
        ###########################################################
        #grammer score
        grammer = mecab.pos(text)
        grammer_length = len(grammer)
        noun_=0
        josa=0
        verb=0
        adjective=0
        exclamation=0
        for i in grammer:
            if i[1] in ['NNG','NNP','NNB','NNBC','NR','NP']:
                noun_+=1
            elif i[1] in ['Josa','JKS','JKC','JKG' ,'JKO','JKB','JKV','JKQ','JX','JC']:
                josa+=1
            elif i[1] in ['VV', 'VA', 'VX', 'VCP', 'VCN']:
                verb+=1
            elif i[1] in['MM','MAG','MAJ']:
                adjective+=1
            elif i[1] in 'IC':
                exclamation+=1
        noun_ /= grammer_length
        josa /= grammer_length
        verb /= grammer_length
        adjective /= grammer_length
        exclamation /= grammer_length
        #######################################################################
        # 명사/조사 가  2.4 이상이면 직접후기글과 비슷하다
        temp = round(noun_/josa,2)
        temp = (temp-threshold_list[7][0])/threshold_list[7][1]

        # 이미지당 글자 수 계산
        if data['Image num'][num_]!=0:
            imgwrd_score= (data['Paragraph num'][num_]/data['Image num'][num_])
        else:
            imgwrd_score=100
        imgwrd_score = (imgwrd_score-threshold_list[8][0])/threshold_list[8][1]

        # video score 많을 수록 감점
        if data['Video num'][num_]>0:
            score += 10

        post_df_idx+=1
        # if not isNaN(data['AD'][num_]) and ad ==1:
        #     ad = 0
        
        final_list.append([text,score,data['Image num'][num_],data['Video num'][num_],data['Comment num'][num_],
                           keyword_score,temp_score,
                           temp,int(data['Paragraph num'][num_]),data['gif num'][num_],
                           data['sticker num'][num_],imgwrd_score])

    final_score=0
    for i in range(len(final_list)):
        #keyword score
        final_list[i][1]+=((final_list[i][5]-threshold_list[0][1])/threshold_list[0][0])*8
        #tfidf score
        final_list[i][1]+=((final_list[i][6]-threshold_list[1][1])/threshold_list[1][0])*8
        #greammer score
        if final_list[i][7]<1.96 and final_list[i][7]>0:
            final_list[i][1] += 5
        #paragraph num score
        final_list[i][1]+=((final_list[i][8]-threshold_list[2][1])/threshold_list[2][0])*18
        #image num score
        final_list[i][1]+=((final_list[i][2]-threshold_list[3][1])/threshold_list[3][0])*25
        #imgwrd num score
        if final_list[i][-1]>-1.96 and final_list[i][-1]<0:
            final_list[i][1] += 7
        if final_list[i][-1]>=0 and final_list[i][-1]<0.5:
            final_list[i][1] += 5
        if final_list[i][-1]>=0.5 or final_list[i][-1]<=-1.96:
            final_list[i][1] += 3
        #video num score
        final_list[i][1]-=((final_list[i][3]-threshold_list[4][1])/threshold_list[4][0])*5
        #gif num score
        final_list[i][1]+=((final_list[i][-3]-threshold_list[5][1])/threshold_list[5][0])*13
        #sticker num score
        final_list[i][1]+=((final_list[i][-2]-threshold_list[6][1])/threshold_list[6][0])*10
        
        final_score += final_list[i][1]
    if len(final_list)!=0:
        final_score/=len(final_list)
    if final_score>=100:
        final_score = 95
    return final_score



