# -*- coding: utf-8 -*-
from Naver_Blog_Crawler import NaverBlogCrawler
import time
import pandas as pd
from datetime import date

item_list = ['유수분 측정기','아두이노', '라즈베리 파이', '마이크로 비트', '컴퓨터 부품', '커넥터']
#'보석십자수', '미니어처', '펀치 니들', '3d펜', '3d프린터', '가죽공예', '가방 만들기', '양모펠트', '프랑스 자수', '스크래치 북', 'DIY','LED조명', '무드등', '칼림바', '오르골', '발난로', '우산','캡슐 세제','전자저울', '산소포화도 측정기', '소음 측정기', '거리 측정기', '온습도계', '적외선 온도계', '높이 측정기', '타이머', 
# item_list =['보석십자수']
for i in item_list:
    start = time.time()   
    crawler = NaverBlogCrawler(i)
    df = crawler.getPostDataFrame_FromItemName()
    post_df = crawler.getPostDataFrame_FromItemName()
    print("interval : ",time.time()-start)

    item_name=i
    item_name=item_name.replace("\"","")
    item_name=item_name.replace("+","")
    post_df.to_csv('./crawler/csvfile/'+item_name+date.today().isoformat()+'.csv')