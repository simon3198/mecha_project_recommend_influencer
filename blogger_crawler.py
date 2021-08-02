from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from ast import literal_eval
import re
from urllib import parse

def blog_crawler(blogid):
    page_num=0
    post_list =[]
    while True:
        flg=0
        page_num+=1
        link = f'https://blog.naver.com/PostTitleListAsync.naver?blogId={blogid}&viewdate=&currentPage={page_num}&categoryNo=0&parentCategoryNo=&countPerPage=30'
        response = requests.get(link)
        html = response.content
        soup = bs(html,'html.parser')
        soup = str(soup.text)
        for i in range(30):
            flag =re.search('"addDate":"(.+?)"', soup)
            try:
                logno = re.search('"logNo":"(.+?)"', soup).group(1)
            except:
                print(soup)
            try:
                date = re.search('"addDate":"(.+?)"',soup).group(1)
            except:
                flg=1
                break
            date = date[:4]
            try:
                if int(date)<2016:
                    flg=1
                    break
            except:
                pass
            title = re.search('"title":"(.+?)"', soup).group(1)
            title = parse.unquote(title)
            title = title.replace('+','')
            title = title.replace(' ','')
            soup = soup[flag.end():]
            link_ = f'https://blog.naver.com/{blogid}?Redirect=Log&logNo={logno}'
            post_list.append([link_,title])
        if flg ==1:
            break

    blogger_df = pd.DataFrame(post_list,columns=['Link','Title'])
    blogger_df.to_csv('./blogger all post/'+blogid+'.csv')
    return blogger_df

# https://report.revu.net/service/campaigns/428897



# blogger_list =['duswk75','amaim30','kyakya_4001']
# for blogger in blogger_list:
#     blog_crawler(blogger)