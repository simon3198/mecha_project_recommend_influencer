# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

choice = input('[보석십자수, 미니어처, 펀치니들, 3d펜, 3d프린터, 가죽공예, 가방만들기, 양모펠트, 프랑스자수, 스크래치북, LED조명, 무드등, 칼림바, 오르골, 발난로, 우산, 캡슐세제, 전자저울, 산소포화도측정기, 소음측정기, 거리측정기, 온습도계, 적외선온도계, 높이측정기, 타이머, 유수분측정기, 아두이노, 라즈베리파이, 마이크로비트, 휴대용선풍기, 스피커, 디퓨저, 기저귀, 파우치, 운동화, 청소세제, 로봇청소기, 전동칫솔, 수납박스, 청소포, 에어프라이어, 거북목베개, 컵홀더, 공기청정기, 진공청소기, 자외선차단제, 섬유유연제, 가습기, 마우스패드]\n========================================================================\n 다음 이이템 들 중 하나를 고르시오 : ')

influencer_item_df = pd.read_csv('./blogger score/all item matrixs_final.csv')
training_item_df = pd.read_csv('./blogger score/all item matrixs_train.csv')

influencer_item_df = influencer_item_df.append(training_item_df)
influencer_item_df.drop_duplicates(['blog id'],inplace=True)
save_df = influencer_item_df

itemcharacter_df = pd.read_csv('./datas/item_source.csv')
itemcharacter_df = itemcharacter_df.rename(columns={'Unnamed: 0':'character'})
itemcharacter_df = itemcharacter_df.set_index('character').T
itemcharacter_df.fillna(0,inplace=True)

itemcharacter_df.columns = list(map(lambda x: x.replace(' ',''),itemcharacter_df.columns.values))
influencer_item_df.columns = list(map(lambda x: x.replace(' ',''),influencer_item_df.columns.values))

def cos_sim(_A,_B):
    return np.dot(_A,_B)/(np.linalg.norm(_A)*np.linalg.norm(_B))

def combi2(_df):
    new_df = _df.copy()
    for i in range(len(_df)):
        for j in range(i,len(_df)):
            i_df = _df.iloc[i,:]
            j_df = _df.iloc[j,:]
            new_df = new_df.append(i_df+j_df,ignore_index=True)
    return new_df
itemcharacter_df = combi2(itemcharacter_df)
item_simil = cosine_similarity(itemcharacter_df.T)
item_simil_df = pd.DataFrame(item_simil,columns=itemcharacter_df.columns,index=itemcharacter_df.columns)
np.fill_diagonal(item_simil_df.values,0)
influencer_item_df = influencer_item_df.drop(['weeklyview','2021postnum','5yearspostnum'],axis=1)
influencer_item_df = influencer_item_df.set_index('blogid')

def isNaN(_n):
    return _n!=_n

def dropNaN(_row):
    output_list = []
    for idx,score in enumerate(_row):
        if idx==0:
            nickname=score
            continue
        if isNaN(score) is not True:
            output_list.append((idx,score))
    return (nickname,output_list)

def getItemScoreTuple(_df):
    return _df.apply(dropNaN,axis=1)

influencer_item_score_tuple = getItemScoreTuple(influencer_item_df)

def getKSimilItems(_df,_itemname,k):
    return _df[_itemname].sort_values(ascending=False)[:k]
def getKSimilItems_index(_df,_itemnameindex,k):
    return _df.iloc[_itemnameindex].sort_values(ascending=False)[:k]

def getIndexFromItemName(_df,_itemname):
    columns = _df.columns.values.tolist()
    return columns.index(_itemname)

def getTopKscore(_iindex_score_list,_k):
    content_dict = dict()
    for index,score in _iindex_score_list:
        #-1을 해주는 이유는 influencer_item_df의 index는 blog id때문에 column이 하나 더 추가 되었기 때문.
        ksimil_index_items = getKSimilItems_index(item_simil_df,index,_k)
        for simil_index,simil_value in zip(ksimil_index_items.index,ksimil_index_items.values):
            if simil_index in content_dict:
                content_dict[simil_index].append(score*simil_value)
            else:
                content_dict[simil_index] = [score*simil_value]
    
    for idx,value in content_dict.items():
        content_dict[idx] = np.mean(value)
        
    for index,score in _iindex_score_list:
        if item_simil_df.columns.values[index-1] in content_dict.keys():
            del content_dict[item_simil_df.columns.values[index-1]]
    return content_dict

def contentFill(_df,_influencer_item_score_tuple,_k):
    df_len = len(influencer_item_df.index)
    for i in range(df_len):
        top_k_dict = getTopKscore(_influencer_item_score_tuple[i][1],_k)
        for item_name,score in top_k_dict.items():
            _df.iloc[i,getIndexFromItemName(_df,item_name)] = score  
    
    return _df

output = contentFill(influencer_item_df,influencer_item_score_tuple,5)
output.to_csv('./datas/content_filled_final.csv')

df = output
df = df.replace(0, np.NaN)

inf_data=pd.DataFrame(data=df.T)
inf_data_dic=inf_data.to_dict()

# dictionary에 nan값 함수 
def dropna(data):
    for i in data:
        for j in data[i]:
            name=i
            item_data=j
            value=data[i][j]
        data[i]={item_data: value for item_data, value in data[i].items() if pd.isnull(value)==False}
    return data

# 딕셔너리 nan 값 제거 
inf_data_dic_drop=dropna(inf_data_dic)

import math
def sim_pearson(data, n1, n2): 
    #구현
    sumX=0
    sumY=0
    sumSqX=0 # x 제곱합 
    sumSqY=0 # y 제곱합 
    sumXY=0 #XY 합
    global cnt
    cnt =0
    for i in data[n1]:
        if i in data[n2]:
            sumX+=data[n1][i]
            sumY+=data[n2][i]
            sumSqX+=pow(data[n1][i],2)
            sumSqY+=pow(data[n2][i],2)
            sumXY+=(data[n1][i])*(data[n2][i])
            cnt+=1
            global num # 전역변수 선언
            global den # 전역변수 선언
            num=sumXY-((sumX*sumY)/cnt)
            den= (sumSqX-(pow(sumX,2)/cnt))*(sumSqY-(pow(sumY,2)/cnt))
    return num/math.sqrt(den+0.00001) # 분모=0방지

def top_match(data, name, rank=3, simf=sim_pearson):
    #sim_pearson함수를 simf라는 이름으로 사용하겠다.    
    #구현부분 
    simList=[]
    for i in data:
        if name!=i: #자기 자신을 제외
            simList.append((simf(data, name, i),i))
    simList.sort() #오름차순
    simList.reverse() #역순(내림차순)
    return simList[:rank]

def recommendation(data,person,simf=sim_pearson ):
    try:
        res=top_match(data, person, len(data))
    #     print(res)
        simSum=0 #상관계수(유사도)의 합
        score_dic={} 
        sim_dic={} # 유사도 합을 저장하기 위한 dic 
        myList=[]
        for sim, name in res: 
            if sim<0 : continue # 유사도가 양수인 경우만 처리를 하도록 하겠음 
            for item_data in data[name]:
                if item_data not in data[person]:
                    simSum+=sim*data[name][item_data]
                    score_dic.setdefault(item_data,0) #key가 없으면 초기화하지만 key가 있으면 냅둔다.
                    score_dic[item_data]+=simSum
                    sim_dic.setdefault(item_data,0)
                    sim_dic[item_data]+=sim
                simSum=0 
        for key in score_dic: 
            score_dic[key]=score_dic[key]/sim_dic[key] 
            df[key][person]=score_dic[key]
    except:
        pass

i=0
for person in df.index:
    recommendation(inf_data_dic_drop,person)

df['weekly view']= list(save_df['weeklyview'])
df['2021 post num']= list(save_df['2021postnum'])
df['5years post num']= list(save_df['5yearspostnum'])

df=df[['weekly view', '2021 post num', '5years post num',
       '보석십자수', '미니어처', '펀치니들', '3d펜', '3d프린터', '가죽공예', '가방만들기', '양모펠트',
       '프랑스자수', '스크래치북', 'LED조명', '무드등', '칼림바', '오르골', '발난로', '우산', '캡슐세제',
       '전자저울', '산소포화도측정기', '소음측정기', '거리측정기', '온습도계', '적외선온도계', '높이측정기', '타이머',
       '유수분측정기', '아두이노', '라즈베리파이', '마이크로비트', '휴대용선풍기', '스피커', '디퓨저', '기저귀',
       '파우치', '운동화', '청소세제', '로봇청소기', '전동칫솔', '수납박스', '청소포', '에어프라이어', '거북목베개',
       '컵홀더', '공기청정기', '진공청소기', '자외선차단제', '섬유유연제', '가습기', '마우스패드'
       ]]

filtered = pd.read_csv('./datas/filtered blogger.csv')

new_df = pd.DataFrame(columns=['weekly view', '2021 post num', '5years post num',
       '보석십자수', '미니어처', '펀치니들', '3d펜', '3d프린터', '가죽공예', '가방만들기', '양모펠트',
       '프랑스자수', '스크래치북', 'LED조명', '무드등', '칼림바', '오르골', '발난로', '우산', '캡슐세제',
       '전자저울', '산소포화도측정기', '소음측정기', '거리측정기', '온습도계', '적외선온도계', '높이측정기', '타이머',
       '유수분측정기', '아두이노', '라즈베리파이', '마이크로비트', '휴대용선풍기', '스피커', '디퓨저', '기저귀',
       '파우치', '운동화', '청소세제', '로봇청소기', '전동칫솔', '수납박스', '청소포', '에어프라이어', '거북목베개',
       '컵홀더', '공기청정기', '진공청소기', '자외선차단제', '섬유유연제', '가습기', '마우스패드'
       ])

for blog_id in filtered['0']:
    new_df = new_df.append(df.loc[blog_id])

choice = choice.replace(' ','')

over_1000 = new_df['weekly view'] >=1000

new_df=new_df[over_1000]

new_df.to_csv('./datas/recommender_final.csv')

new_df = new_df[['weekly view', '2021 post num', '5years post num',choice]]

new_df.sort_values(by=choice,inplace=True,ascending=False)
# new_df.reset_index(inplace=True)

new_df.to_csv('./datas/recommender_final_score.csv')

new_df.sort_values(by='weekly view',inplace=True,ascending=False)

new_df.to_csv('./datas/recommender_final_weekview.csv')