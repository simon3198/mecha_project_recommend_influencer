import pandas as pd
from Naver_Blog_Crawler import NaverBlogCrawler

link_list=['https://blog.naver.com/flute8248/222597337658']
crawler = NaverBlogCrawler(_blog_url_list = link_list)
df = crawler.getPostDataFrame_blogUrls()
df.to_csv('test.csv')