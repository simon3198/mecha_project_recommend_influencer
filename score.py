from eunjeon import Mecab
from collections import Counter
import pandas as pd
import numpy as np
import re

def onlytext(temp):
    temp = temp.replace("\u200b"," ").replace("\t"," ").replace("\n"," ").replace("#"," ")
    temp = re.sub(r'[^가-힣 ]','',temp)
    return temp

# 빈 리스트 설정 + 키워드 리스트 설정
# keyword_list = ['다이소', '생각','주문', '디즈니', '액자', '큐빅', '해바라기', '선물', '그림','아이','구매','주문','배송','시작','내돈내산','내돈','내산']
# minus_list = ['러브','페인','생활','아이','취미','사용','추천','정말','제품']

#word frequency list
minus_list = ['페인팅', '생활', '취미', '아이', '더라구요', '고체', '비즈', '제품', '키트', '더라고요', '다양', '정말', '부터', '작품', '까지', '답니다', '붙이', '아서', '어서', '인테리어']
keyword_list = ['습니다', '입니다', '세요', '네요', '만들', '지만', '생각', '액자', '해서', '부분', '는데', '사용', '너무', '작업', '그림', '보다', '십자수', '완성', '이렇게', '보석']

#tfidf list
minus_dict_tfidf ={'공예': 1.6565380876805176, '구요': 1.5477083528105133, '고요': 1.5334047155347195, '도안': 1.5083661422926238, '페인': 1.508089270088575, '페인팅': 1.5048670926511774, '어요': 1.5039355765778932, '판매': 1.4191764396787392, '더라구요': 1.3970364031384148, '라구요': 1.394189703443211, '더라구': 1.3882237779480449, '라구': 1.3852719382846952, '비누': 1.3411725371420842, '더라고요': 1.3331414726296682, '러브': 1.3163923971613571, '아이러브': 1.3159702379249993, '더라고': 1.313712122519022, '만들': 1.3111273480161412, '아이러브페인팅': 1.298979276082331, '키트': 1.2680884032469106, '이러': 1.266304431300947, '캔들': 1.2611932912810568, '액자': 1.2460062603268167, '버스': 1.2372438768769545, '캔버스': 1.2283361669664365, '습니다': 1.2279750690240494, '붙이': 1.2063895256606074, '습니': 1.202084414260968, '아이': 1.198506531803969, '그림': 1.1640532101001162}
keyword_dict_tfidf={'니다': 1.606903691905675, '습니다': 1.5219040634376704, '습니': 1.5213921655252969, '어요': 1.4832103574031226, '만들': 1.336432369767162, '아이': 1.2961699706985828, '액자': 1.2519459776488826, '페인': 1.1301432715659903, '도안': 1.1191396151652284, '고요': 1.107375838594621, '큐빅': 1.0775354890142346, '만들기': 1.0707127281511584, '구요': 1.0312402438779593, '뜨개': 1.0236048439053533, '작업': 1.020897105002268, '더라': 1.0014193784510579, '가방': 0.9452786807493149, '사용': 0.945080915324915, '취미': 0.9377431710293702, '그림': 0.93022290686033, '붙이': 0.9253583959400897, '페인팅': 0.9152363400551377, '제품': 0.9078064613563507, '가죽': 0.9021868214542655, '공예': 0.9017193628140725, '작품': 0.890412374220934, '네요': 0.8836443927422628, '부분': 0.8808514854459975, '리어': 0.8760889773989764, '더라고요': 0.8740208673145219}

score_list=[]
keyword_score_list=[]
tfidf_score_list=[]
nounlist=[]
verb_list=[]
josa_list=[]
adjective_list=[]
exclamation_list=[]
def isNaN(num):
    return num != num

mecab = Mecab()
all_noun_dict={}
post_df = pd.DataFrame(columns=('Post','Image num','Video num','comment num','sympathy num','weekly view','score','AD','keyword score','tfidf score','josa','noun','noun/josa','paragraph num'))
csv_name = './crawler/보석십자수2021-07-15'
data = pd.read_csv(csv_name+".csv")
# csv_name = './crawler/DIY2021-07-22'
# data2 = pd.read_csv(csv_name+".csv")
# data = pd.concat([data2,data1],ignore_index=True)
text_list=[]
all_noun_list=[]
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
    count = Counter(noun)
    noun_list = count.most_common(50)
    noun_dict = dict()
    for item,num in noun_list:
        noun_dict[item] = round(num/noun_len,6)*100
    all_noun_list.append(noun_dict)
    ########################################################
    #keyword score calculation
    score=0
    for keyword in keyword_list:
        for i in noun:
            if keyword == i:
                score +=1
    for keyword in minus_list:
        for i in noun:
            if keyword == i:
                score -=1
    score /= noun_len
    score *=100
    keyword_score=score
    if score >5:
        score =1
    else:
        score =0
    ########################################################
    #itidf keyword score calculation
    # noun_set = set(noun)
    # noun_set = list(noun_set)
    temp_score=0
    for keyword in keyword_dict_tfidf.keys():
        for i in noun:
            if keyword == i:
                temp_score += keyword_dict_tfidf[keyword]
    for keyword in minus_dict_tfidf.keys():
        for i in noun:
            if keyword == i:
                temp_score -= minus_dict_tfidf[keyword]
    tfidf_score_list.append(temp_score)
    if temp_score > 1:
        score+=1
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
    nounlist.append(noun_)
    josa /= grammer_length
    josa_list.append(josa)
    verb /= grammer_length
    verb_list.append(verb)
    adjective /= grammer_length
    adjective_list.append(adjective)
    exclamation /= grammer_length
    exclamation_list.append(exclamation)
    #######################################################################
    # 명사/조사 가  2.4 이상이면 직접후기글과 비슷하다
    temp = round(noun_/josa,2)
    if temp>2.4:
        score +=1
    if int(data['Paragraph num'][num_])<300:
        score+=1
    print(score)
    score_list.append(score)
    post_df_idx+=1
    if isNaN(data['AD'][num_]):
        ad = 1
    else:
        ad = 0
    post_df.loc[post_df_idx] = [text,data['Image num'][num_],data['Video num'][num_],data['Comment num'][num_],data['Sympathy num'][num_],data['weekly viewer mean'][num_],score,ad,keyword_score,temp_score,josa,noun_,temp,int(data['Paragraph num'][num_])]
    keyword_score_list.append(keyword_score)
    print("-"*50)

for i in [score_list,keyword_score_list,tfidf_score_list,nounlist,verb_list,josa_list,adjective_list,exclamation_list]:
    a=np.array(i)
    avg = np.mean(a)
    print(avg)

post_df.to_csv('보석십자수 점수.csv')