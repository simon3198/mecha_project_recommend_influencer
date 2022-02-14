# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import ast
from blogger_crawler import blog_crawler
from Naver_Blog_Crawler import NaverBlogCrawler
from score_for_blogger import score_blogger
import re
import requests
import xml.etree.ElementTree as ET

#DIY,컴퓨터부품, 커넥터 제거 52-3=49
item_list = ['보석십자수', '미니어처', '펀치 니들', '3d펜', '3d프린터', '가죽공예', '가방 만들기', '양모펠트', '프랑스 자수', '스크래치 북','LED조명', '무드등', '칼림바', '오르골', '발난로', '우산', '캡슐 세제','전자저울', '산소포화도 측정기', '소음 측정기', '거리 측정기', '온습도계', '적외선 온도계', '높이 측정기', '타이머', '유수분 측정기','아두이노', '라즈베리 파이', '마이크로 비트','휴대용선풍기','스피커','디퓨저','기저귀','파우치','운동화','청소세제','로봇청소기','전동칫솔','수납박스','청소포','에어프라이어','거북목베개','컵홀더','공기청정기','진공청소기','자외선차단제','섬유유연제','가습기','마우스패드']
print(len(item_list))
blogger_list = pd.read_csv('./crawler/revu_id_list.csv')
blogger_list = blogger_list['0'].tolist()
print(len(blogger_list))
final_score_list=[]
for blogger_name in blogger_list:
    try:
        blog_category =''
        is_notad = 2
        post_num, data = blog_crawler(blogger_name)

        final_df={}
        category = []
        if data['Link'].count() <= 100:
            continue
        link_list=[]
        for item in item_list:
            item = item.replace(' ','')
            item_bool = data['Title'].apply(lambda x: item in x)
            item_df = data[item_bool]
            # final_df = final_df.join(pd.Series(list(item_df['Link'])).rename(item), how='right')
            final_df[item] = list(item_df['Link'])
            # link_list.extend(list(item_df['Link']))
        # link_df = pd.DataFrame(link_list,columns=['Link'])
        # link_df.to_csv('./blogger score/'+blogger_name+'.csv')
        score_list=[]
        for item in item_list:
            temp = item.replace(' ','')
            url_list = final_df[temp]
            
            num =-1
            if len(url_list)>0:
                crawler = NaverBlogCrawler(_blog_url_list = url_list)
                df = crawler.getPostDataFrame_blogUrls()
                ad, score = score_blogger(item,df)
                # if ad == 1 and is_notad==2:
                #     is_notad=1
                # if ad == 0 and is_notad!=0:
                #     is_notad = 0
                score_list.append(score)
            else:
                score_list.append(None)
        viewer_num_url = f'https://blog.naver.com/NVisitorgp4Ajax.nhn?blogId={blogger_name}'
        viewer_num_response = requests.get(viewer_num_url)
        viewer_num_list = [int(node.get("cnt")) for node in ET.fromstring(viewer_num_response.text)]
        week_view = np.mean(np.array(viewer_num_list))

        # score_list.append(is_notad)
        score_list.append(week_view)
        score_list.append(post_num)
        score_list.append(data['Link'].count())
        # score_df = pd.DataFrame([score_list],columns=item_list+['weekly view','post num','5 years post num'])
        score_list.insert(0,blogger_name)
        final_score_list.append(score_list)
        #  score_df.to_csv('./blogger score/'+blogger_name+'.csv')
    except:
        print(blogger_name)
        pass

item_list.insert(0,'blog id')
final_score_df = pd.DataFrame(final_score_list,columns=item_list+['weekly view','2021 post num','5years post num'])
final_score_df = final_score_df.set_index('blog id')
final_score_df.to_csv('./blogger score/all item matrixs__.csv')