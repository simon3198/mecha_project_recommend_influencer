# -*- coding: utf-8 -*-
from typing import final
from eunjeon import Mecab
from collections import Counter
import pandas as pd
import numpy as np
import re

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

filename_list =['보석십자수2021-07-29','미니어처2021-07-26','펀치 니들2021-07-26','3d펜2021-07-26','3d프린터2021-07-26','가죽공예2021-07-26','가방 만들기2021-07-26','양모펠트2021-07-26','프랑스 자수2021-07-26','스크래치 북2021-07-26','DIY2021-07-27','LED조명2021-07-27','무드등2021-07-27','칼림바2021-07-27','오르골2021-07-27','발난로2021-07-27','우산2021-07-27','캡슐 세제2021-07-27','전자저울2021-07-27','산소포화도 측정기2021-07-27','소음 측정기2021-07-27','거리 측정기2021-07-27','온습도계2021-07-27','적외선 온도계2021-07-27','높이 측정기2021-07-27','타이머2021-07-27','아두이노2021-07-29','유수분 측정기2021-07-29']
# filename_list =['보석십자수2021-07-29']
for filename in filename_list:
    keyword_score_list=[]
    tfidf_score_list=[]
    grammer_score_list=[]
    paragraph_score_list=[]
    image_score_list=[]
    video_score_list=[]
    gif_score_list=[]
    imgwrd_score_list=[]
    sticker_score_list=[]
    item_name = filename[:-10]
    date_name = filename[-10:]
    data = pd.read_csv('./crawler/csvfile/'+filename+'.csv')

    keyword_data = pd.read_csv('write.csv',header=None, error_bad_lines=False)
    keyword_data.set_index(0, inplace = True)

    ad_keyword_list = keyword_data.loc[item_name+'ad']
    notad_keyword_list = keyword_data.loc[item_name+'notad']
    tfidf_ad_keyword_list = keyword_data.loc[item_name+'tfidf_ad']
    tfidf_ad_keyword_list = list2dic(tfidf_ad_keyword_list)
    tfidf_notad_keyword_list = keyword_data.loc[item_name+'tfidf_notad']
    tfidf_notad_keyword_list= list2dic(tfidf_notad_keyword_list)

    mecab = Mecab()
    all_noun_dict={}
    # post_df = pd.DataFrame(columns=('Post','score','Image num','Video num','comment num','sympathy num','weekly view','AD','keyword score','tfidf score','josa','noun','noun/josa','paragraph num'))

    text_list=[]
    all_noun_list=[]
    final_list=[]
    all_text=""
    num_=-1
    count=0
    post_df_idx=0
    #############################################################
    for post in data['Post']:
        num_+=1
        #not 직접
        #if 광고
        # if not isNaN(data['AD'][num_]):
        #     continue
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
        keyword_score_list.append(keyword_score)
        score=0
        # if score >5:
        #     score =1
        # else:
        #     score =0
        ########################################################
        #itidf keyword score calculation
        # noun_set = set(noun)
        # noun_set = list(noun_set)
        temp_score=0
        for keyword in tfidf_notad_keyword_list.keys():
            for i in noun:
                if keyword == i:
                    temp_score += tfidf_notad_keyword_list[keyword]
        for keyword in tfidf_ad_keyword_list.keys():
            for i in noun:
                if keyword == i:
                    temp_score -= tfidf_ad_keyword_list[keyword]
        tfidf_score_list.append(temp_score)
        # if temp_score > 2.5:
        #     score+=1
        ###########################################################
        # for v in noun_list:
        #     print(v)
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
        try:
            temp = round(noun_/josa,2)
        except:
            keyword_score_list.pop()
            tfidf_score_list.pop()
            continue
        grammer_score_list.append(temp)
        # if temp>2.4:
        #     score +=1
        # if int(data['Paragraph num'][num_])<300:
        #     score+=1
        paragraph_score_list.append(data['Paragraph num'][num_])
        image_score_list.append(data['Image num'][num_])
        video_score_list.append(data['Video num'][num_])
        gif_score_list.append(data['gif num'][num_])
        sticker_score_list.append(data['sticker num'][num_])
        if data['Image num'][num_]!=0:
            imgwrd_score_list.append(data['Paragraph num'][num_]/data['Image num'][num_])
        else:
            imgwrd_score_list.append(30)
        # video score
        if data['Video num'][num_]>0:
            score += 1
        if data['gif num'][num_]>0:
            score += 0.8
        if data['sticker num'][num_]>0:
            score += 0.8

        post_df_idx+=1
        if isNaN(data['AD'][num_]):
            ad = 1
        else:
            ad = 0
        # post_df.loc[post_df_idx] = [text,score,data['Image num'][num_],data['Video num'][num_],data['Comment num'][num_],data['Sympathy num'][num_],data['weekly viewer mean'][num_],ad,keyword_score,temp_score,josa,noun_,temp,int(data['Paragraph num'][num_])]
        final_list.append([text,score,data['Image num'][num_],data['Video num'][num_],data['Comment num'][num_],data['Sympathy num'][num_],data['weekly viewer mean'][num_],ad,keyword_score,temp_score,josa,noun_,temp,int(data['Paragraph num'][num_]),data['gif num'][num_],data['sticker num'][num_]])
    threshold_list=[]

    # temp_df = pd.DataFrame(columns=('Post','score','Image num','Video num','comment num','sympathy num','weekly view','AD','keyword score','tfidf score','josa','noun','noun/josa','paragraph num'))

    #중간값 구하기
    for i in [keyword_score_list,tfidf_score_list,paragraph_score_list,image_score_list,video_score_list,gif_score_list,sticker_score_list]:
        a=np.array(i)
        threshold_list.append([np.max(a)-np.min(a),np.min(a)])
    # temp_img = image_score_list
    # image_score_list_std,image_mean,image_std = standard(temp_img)
    temp_imgwrd = imgwrd_score_list
    imgwrd_score_list_std,imgwrd_mean,imgwrd_std = standard(temp_imgwrd)
    temp_grammer = grammer_score_list
    grammer_score_list_std,grammer_mean,grammer_std = standard(temp_grammer)

    for i in range(len(final_list)):
        #keyword score
        final_list[i][1]+=(final_list[i][8]-threshold_list[0][1])/threshold_list[0][0]
        #tfidf score
        final_list[i][1]+=(final_list[i][9]-threshold_list[1][1])/threshold_list[1][0]
        #greammer score
        if grammer_score_list_std[i]<1.96 and grammer_score_list_std[i]>0:
            final_list[i][1] = final_list[i][12]+1
        #paragraph num score
        final_list[i][1]+=1-((final_list[i][13]-threshold_list[2][1])/threshold_list[2][0])
        #image num score
        final_list[i][1]+=(final_list[i][2]-threshold_list[3][1])/threshold_list[3][0]
        #imgwrd num score
        if imgwrd_score_list_std[i]>-1.96 and imgwrd_score_list_std[i]<0:
            final_list[i][1] = final_list[i][1]+1
        #video num score
        final_list[i][1]-=((final_list[i][3]-threshold_list[4][1])/threshold_list[4][0])
        #gif num score
        final_list[i][1]+=-((final_list[i][-2]-threshold_list[5][1])/threshold_list[5][0])*0.2
        #sticker num score
        final_list[i][1]+=-((final_list[i][-1]-threshold_list[6][1])/threshold_list[6][0])*0.2

    # 평균과 표준편차 저장
    threshold_list.append(grammer_mean)
    threshold_list.append(grammer_std)
    threshold_list.append(imgwrd_mean)
    threshold_list.append(imgwrd_std)

    temp_df = pd.DataFrame(final_list,columns=('Post','score','Image num','Video num','comment num','sympathy num','weekly view','AD','keyword score','tfidf score','josa','noun','noun/josa','paragraph num','gif num','sticker num'))
    temp_df.to_csv('./score/'+item_name+' 점수.csv')

    threshold_df = pd.DataFrame([threshold_list],columns=('keyword','tfidf','paragraph','image','video','gif','sticker','grammer mean','grammer std','imgwrd mean','imgwrd std'))
    threshold_df.to_csv('./threshold/threshold_'+item_name+'.csv')

    # post_df.to_csv('보석십자수 점수.csv')


