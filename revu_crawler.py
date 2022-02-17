from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import date
import time
from bs4 import BeautifulSoup
import re
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from blogger_crawler import blog_crawler
from Naver_Blog_Crawler import NaverBlogCrawler
from score_for_blogger import score_blogger
import re
import requests
import xml.etree.ElementTree as ET
import sys

if __name__ == '__main__':
    
    id_list=[]

    link= input('revu link를 입력해주세요 : ')
    revu_id=input('revu id를 입력해주세요 : ')
    revu_pswd=input('revu password를 입력해주세요 : ')
    # link_list= ['https://report.revu.net/service/campaigns/422541']
    # ,'https://report.revu.net/service/campaigns/428897','https://report.revu.net/service/campaigns/422036','https://report.revu.net/service/campaigns/422023','https://report.revu.net/service/campaigns/420573','https://report.revu.net/service/campaigns/420573','https://report.revu.net/service/campaigns/420568','https://report.revu.net/service/campaigns/420183','https://report.revu.net/service/campaigns/418579','https://report.revu.net/service/campaigns/417204','https://report.revu.net/service/campaigns/415463','https://report.revu.net/service/campaigns/388108']

    # link = link_list[0]

    options = Options()
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome("./chromedriver")
    driver.get(link)
    driver.implicitly_wait(10)
    # wait=WebDriverWait(driver,5)

    
    revu_id = 'wc0426@naver.com'
    revu_pswd = 'sysy8659!'
    button = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[2]/span[1]')
    button[0].click()

    login = driver.find_elements_by_css_selector('.form-input')
    login[0].send_keys(revu_id)
    login[1].send_keys(revu_pswd)

    login_button = driver.find_element_by_css_selector('.btn.btn-revu')
    login_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div/div/div[2]')))
    try:
        notice_close = driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[2]')
        notice_close.click()
    except:
        pass

    influencer_choice = driver.find_element_by_class_name('client-pick')
    influencer_choice.click()
    more_button = driver.find_element_by_xpath('//*[@id="pick-list"]/div[3]/span')
    more_button.click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    num=29
    while True:
        num+=30
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,'requesting_'+str(num))))
        except:
            break
        try:
            more_button = driver.find_element_by_xpath('//*[@id="pick-list"]/div[3]/span')
            more_button.click()
        except:
            break
    blogger_list = driver.find_elements_by_css_selector('.media-title [href]')

    num=-1
    for blogger in blogger_list:
        num+=1
        temp = blogger.get_attribute('href')
        try:
            if 'blog.naver.com' in temp:
                temp = re.split('/',temp)[-1]
            else:
                temp = re.search('ttp://(.+?).blog.me', temp).group(1)
        except:
            continue
        id_list.append(temp)
        
        
    id_list = set(id_list)
    id_list = list(id_list)
    print(len(id_list))
    
    if len(id_list)==30:
        print('오류가 발생하였습니다. 다시 시도해주세요')
        sys.exit()
    
    id_list = pd.DataFrame(id_list)
    id_list.to_csv('./datas/revu_id_list.csv')

    #DIY,컴퓨터부품, 커넥터 제거 52-3=49
    item_list = ['보석십자수', '미니어처', '펀치 니들', '3d펜', '3d프린터', '가죽공예', '가방 만들기', '양모펠트', '프랑스 자수', '스크래치 북','LED조명', '무드등', '칼림바', 
                 '오르골', '발난로', '우산', '캡슐 세제','전자저울', '산소포화도 측정기', '소음 측정기', '거리 측정기', '온습도계', '적외선 온도계', '높이 측정기', '타이머', 
                 '유수분 측정기','아두이노', '라즈베리 파이', '마이크로 비트','휴대용선풍기','스피커','디퓨저','기저귀','파우치','운동화','청소세제','로봇청소기',
                 '전동칫솔','수납박스','청소포','에어프라이어','거북목베개','컵홀더','공기청정기','진공청소기','자외선차단제','섬유유연제','가습기','마우스패드']

    # blogger_list = pd.read_csv('./revu_id_list.csv')
    # blogger_list = blogger_list['0'].tolist()
    
    blogger_list=id_list
    
    final_score_list=[]

    #새로우 dataframe 만들기
    newdf = pd.DataFrame(columns=['comment num','comment detail','post num'])

    for blogger_name in blogger_list:
        try:
            blog_category =''
            is_notad = 2
            post_num, data = blog_crawler(blogger_name)

            category = []
            if data['Link'].count() <= 100:
                continue
            link_list=[]
            for item in item_list:
                item = item.replace(' ','')
                item_bool = data['Title'].apply(lambda x: item in x)
                item_df = data[item_bool]
                link_list.extend(list(item_df['Link']))
            final_df =  pd.DataFrame(link_list,columns=['Link'])
            
            score_list=[]
            
            crawler = NaverBlogCrawler(_blog_url_list = link_list)
            df = crawler.getPostDataFrame_blogUrls()
            data.rename(columns = {'Link' : 'Post URL'}, inplace = True)
            
            df = pd.merge(df,data,on='Post URL')
            df['Comment num'] = pd.to_numeric(df['Comment num'])
            for item in item_list:
                temp = item.replace(' ','')
                item_bool = df['Title'].apply(lambda x: temp in x)
                item_df = df[item_bool]
                
                if len(item_df)>0:
                    item_df.reset_index(inplace=True)
                    score = score_blogger(item,item_df)
                    score_list.append(score)
                else:
                    score_list.append(None)
                        
            comment_sum = df['Comment num'].sum()
            comment_list=[]

            for comment in df['Comment detail']:
                if comment != 0:
                    comment_list.extend(comment)
            newdf.loc[blogger_name]=[comment_sum,comment_list,len(df.index)]
            
            viewer_num_url = f'https://blog.naver.com/NVisitorgp4Ajax.nhn?blogId={blogger_name}'
            viewer_num_response = requests.get(viewer_num_url)
            viewer_num_list = [int(node.get("cnt")) for node in ET.fromstring(viewer_num_response.text)]
            week_view = np.mean(np.array(viewer_num_list))

            score_list.append(week_view)
            score_list.append(post_num)
            score_list.append(data['Post URL'].count())
            score_list.insert(0,blogger_name)
            final_score_list.append(score_list)
            print(blogger_name,'success')
        except:
            print(blogger_name,'failed')
            pass

    newdf.to_csv('./datas/blogger comment.csv')
    item_list.insert(0,'blog id')
    final_score_df = pd.DataFrame(final_score_list,columns=item_list+['weekly view','2021 post num','5years post num'])
    final_score_df = final_score_df.set_index('blog id')
    final_score_df.to_csv('./blogger score/all item matrixs_final.csv')