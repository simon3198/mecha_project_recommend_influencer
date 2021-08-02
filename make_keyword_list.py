# -*- coding: utf-8 -*-

from word_frequency import getWordFrequencyListFromCSV_ad as ad
from word_frequency import getWordFrequencyListFromCSV_notad as notad
import tfidf_mecab
from tfidf_mecab import tfidf_ad
from tfidf_mecab import tfidf_notad
import pandas as pd
import numpy as np
import csv
import re

def make_keywordlist(filename):
    res_notad={}
    res_ad={}
    data = pd.read_csv('./crawler/csvfile/'+filename+'.csv')
    item_name = filename[:-10]
    date_name = filename[-10:]

    ad_list = ad(data)

    notad_list = notad(data)
    
    ad_list = ad_list[-1]
    notad_list = notad_list[-1]

    for i in notad_list.keys():
        if i in ad_list.keys():
            res_notad[i]=round(notad_list[i]/ad_list[i],2) #높을수록 직접후기에 많이 나타나는 단어
            

    for i in ad_list.keys():
        if i in notad_list.keys():
            res_ad[i]=round(ad_list[i]/notad_list[i],2) #높을수록 광고에 많이 나타나는 단어

    ad_keywordlist = sorted(res_ad.items(), key = lambda item: item[1], reverse = True)
    ad_keyword_dict = list(dict(ad_keywordlist).keys())
    ad_keyword_dict = ad_keyword_dict[:20]
    ad_keyword_dict.insert(0,item_name+'ad')

    notad_keywordlist = sorted(res_notad.items(), key = lambda item: item[1], reverse = True)
    notad_keyword_dict = list(dict(notad_keywordlist).keys())
    notad_keyword_dict = notad_keyword_dict[:20]
    notad_keyword_dict.insert(0,item_name+'notad')

    for i in range(20):
        ad_keyword_dict.append(0)
        notad_keyword_dict.append(0)
##################################################
    #tfidf list
    ad_tfidf = tfidf_ad(data)
    notad_tfidf = tfidf_notad(data)

    temp_ad=[]
    temp_notad=[]
    for i in ad_tfidf:
        temp_ad.append(i)
        temp_ad.append(ad_tfidf[i])
    for i in notad_tfidf:
        temp_notad.append(i)
        temp_notad.append(notad_tfidf[i])
    # ad_tfidf= list(zip(ad_tfidf.keys(), ad_tfidf.values()))
    # notad_tfidf = list(zip(notad_tfidf.keys(), notad_tfidf.values()))

    temp_ad.insert(0,item_name+'tfidf_ad')
    temp_notad.insert(0,item_name+'tfidf_notad')

    f = open('write.csv','a', newline='')
    wr = csv.writer(f)
    wr.writerow(ad_keyword_dict)
    wr.writerow(notad_keyword_dict)
    wr.writerow(temp_ad)
    wr.writerow(temp_notad)
    f.close()

filename_list =['보석십자수2021-07-29','미니어처2021-07-26','펀치 니들2021-07-26','3d펜2021-07-26','3d프린터2021-07-26','가죽공예2021-07-26','가방 만들기2021-07-26','양모펠트2021-07-26','프랑스 자수2021-07-26','스크래치 북2021-07-26','DIY2021-07-27','LED조명2021-07-27','무드등2021-07-27','칼림바2021-07-27','오르골2021-07-27','발난로2021-07-27','우산2021-07-27','캡슐 세제2021-07-27','전자저울2021-07-27','산소포화도 측정기2021-07-27','소음 측정기2021-07-27','거리 측정기2021-07-27','온습도계2021-07-27','적외선 온도계2021-07-27','높이 측정기2021-07-27','타이머2021-07-27','유수분 측정기2021-07-29','아두이노2021-07-29']

for filename in filename_list:
    make_keywordlist(filename)




















# real = {'보석': 1.6314, '십자수': 1.5686, '어요': 1.2845, '만들': 1.2252, '는데': 0.8626, '습니다': 0.8305, '완성': 0.8278, '비즈': 0.8228, '에서': 0.7225, '어서': 0.6088, '해서': 0.549, '지만': 0.5471, '입니다': 0.5322, '아이': 0.4974, '네요': 0.4744, '시간': 0.4621, '사용': 0.451, '아요': 0.4311, '세요': 0.42, '액자': 0.4196, '취미': 0.4154, '너무': 0.4047, '면서': 0.3802, '하나': 0.3771, '생각': 0.3729, '합니다': 0.3484, '이렇게': 0.3473, '작업': 0.3419, '부분': 0.33, '붙이': 0.3254, '까지': 0.3159, '많이': 0.2891, '시작': 0.2822, '그림': 0.2764, '작품': 0.2718, '아서': 0.265, '보다': 0.263, '사진': 0.2619, '사이즈': 0.2535, '제품': 0.2481, '더라구요': 0.2393, '정도': 0.2309, '인테리어': 0.2297, '선물': 0.2255, '조금': 0.2251, '답니다': 0.2247, '으면': 0.2232, '그리고': 0.2182, '큐빅': 0.214, '부터': 0.2133, '가지': 0.2133, '정말': 0.2129, '다가': 0.2087, '느낌': 0.2048, '구성': 0.2041, '생활': 0.2029, '키트': 0.2018, '라고': 0.1968, '해요': 0.1956, '아니': 0.1953, '때문': 0.1949, '더라고요': 0.1945, '붙여': 0.193, '페인팅': 0.1926, '다고': 0.1918, '처음': 0.1914, '에요': 0.1899, '예쁘': 0.1884, '구매': 0.1884, ' 함께': 0.1876, '다양': 0.1853, '바로': 0.1838, '가능': 0.1838, '는데요': 0.1819, '주문': 0.18, '고체': 0.1784, '방법': 0.178, '제작': 0.178, '다른': 0.1765, '패키지': 0.1757, '컬러': 0.1719, '이나': 0.1711, '이번': 0.1708, '오늘': 0.1685, '색상': 0.1677, '해야': 0.165, '소품': 0.1639, '필요': 0.1616, '이런': 0.1604, '활용': 0.1597, '직접': 0.1597, '다는': 0.1593, '추천': 0.1593, '됩니다': 0.1585, '트레이': 0.1585, '요즘': 0.1581, '보이': 0.157, '다음': 0.1558, '가방': 0.1554, '만드': 0.1551}

# fake = {'보석': 1.7553, '십자수': 1.6673, '어요': 1.4489, '비즈': 1.3019, '만들': 1.0032, '완성': 0.8847, '는데': 0.8788, '아이': 0.8752, '에서': 0.8743, '취미': 0.7599, '어서': 0.7544, '시간': 0.567, '습니다': 0.5402, '해서': 0.5252, '지만': 0.468, '사용': 0.4625, '아요': 0.4625, '페인팅': 0.4494, '하나': 0.4358, '까지': 0.4253, '붙이': 0.4244, '면서': 0.4208, '너무': 0.4126, '생활': 0.3926, '더라구요': 0.3913, '제품': 0.3908, '액자': 0.3831, '네요': 0.3758, '이렇게': 0.3686, '작품': 
# 0.3686, '입니다': 0.3609, '러브': 0.3568, '작업': 0.3473, '시작': 0.3418, '아서': 0.34, '생각': 0.325, '부분': 0.32, '키트': 0.3064, '세요': 0.2996, '정말': 0.2973, '부터': 0.2946, '답니다': 0.2941, '고체': 0.2932, '그림': 0.2869, '인테리어': 0.2851, '캔버스': 0.281, '더라고요': 0.2764, '보다': 0.2751, '그리고': 0.261, '다양': 0.261}
# real_list = real.keys()
# res={}
# for i in real_list:
#     if i in fake.keys():
#         # res[i]=round(real[i]/fake[i],2) #높을수록 직접후기에 많이 나타나는 단어
#         res[i]=round(fake[i]/real[i],2) #높을수록 광고에 많이 나타나는 단어
# sorted_dict = sorted(res.items(), key = lambda item: item[1], reverse = True)
# print(sorted_dict)
# sorted_dict = dict(sorted_dict)
# print(sorted_dict.keys())


####################################################################
# from pandas.io.parsers import read_csv
# import pandas as pd

# data= pd.read_csv('./crawler/보석십자수2021-07-13.csv')

# def isNaN(temp):
#     return temp!=temp

# num=-1
# res=0
# count=0
# for post in data['Post']:
#     num+=1
#     #not 광고
#     #if 직접
#     if not isNaN(data['AD'][num]):
#         count+=1
#         res += data['Paragraph num'][num]/data['Image num'][num]s
# print(res/count)