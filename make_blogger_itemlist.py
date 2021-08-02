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

item_list = ['보석십자수', '미니어처', '펀치 니들', '3d펜', '3d프린터', '가죽공예', '가방 만들기', '양모펠트', '프랑스 자수', '스크래치 북', 'DIY','LED조명', '무드등', '칼림바', '오르골', '발난로', '우산', '캡슐 세제','전자저울', '산소포화도 측정기', '소음 측정기', '거리 측정기', '온습도계', '적외선 온도계', '높이 측정기', '타이머', '유수분 측정기']
#,'아두이노', '라즈베리 파이', '마이크로 비트', '컴퓨터 부품', '커넥터']

# blog_crawler(blogger_name)
blogger_list = ['amaim30', 'kyakya_4001', 'nora_nori', 'rin141206', 'vhglglgl', 'skyfox1011', 'miminimkkk', 'lim8419', 'shanesemi', 'yacomworld', 'lsogk70', 'songitktk', 'rudtj7177', 'skyjh0902', 'minica3892', 'tsslove', 'sunnybloger', 'syol07', 'namjji85', 'yoong4097', '11ansgallry', 'amoris1105', '33ehddks', 'bang_0215', 'dreamersr12', 'ooza-', 'popopo2013', 'rlagmltn2', 'uniqueplace_', 'sticky9', 'kwonsh0637', 'ue8755', 'codnjswhddn', 'yoon--sss', 'dmslse11', 'penguinnews', 'iletaittemps', 'alwayspurelu', 'arom0520', '83younsuk', 'jdmkr', 'aimi0803', 'chloeagit', 'rjy0626', '1127ye', 'starule', 'luna0723', 'zza344', 'didtks0590', 'hgy6908', 'jae2ee', 'alsl720', 'peach143', 'ilook2u', 'tjddk742', 'cey1996', '07min25', 'pian_oka', '3210dptmej', 'hoiyeji48', 'honeypigmom_', 'xnaxim', 'kyureegil', 'heemk0731', 'bak0866', 'hyebangee', 'aktf0910', 'khlee5260', 'threecolor_cat', 'dk1983', 'jhwood4736', 'googys', 'wmelon29', 'jinjunghan_na', 'mkil618', 'meruya9876', 'delphine0327', 'shin11109', 'cool7927', 'yibwa0912', 'heyji0303', 'hwajung319', 'dioni_', 'girlhj', 'codms86', 'ngfriend2002', 'sosoo101', 'slow6441', 'o_ogns07', 'ssb84351', 'bsh9240', 'april_record', 'lovelnr1103', 'alway0131', 'ys1104ys', 'shining1984', 'happycloud24', 'ahah3242', 'oboist1123', 'rlatnals6426', 'dlffldksk', 'mintnbambi', 'skawjd1112', 'cyber3578', 'ktaru', 'rilrastory', 'jae2653', 'greathead60', 'psj0914', 'langlang12', 'nwjoo98', 'meertd', 'genesis0821', 'sunju914', 'polaris_yh', 'chpc0313', 'bijoubitna', 'xuxis2', 'babb2011', 'caprisome', 'daily_something', 'dlahrwl', 'amelia421', 'hyetaeng', 'beautifuller', 'ssbling', 'sufreesia', 'jidud030512', 'mslink', 'hyey00n', 'hoegod6004', 'ewud09', 'bolgorog', 'masejin', 'seoji11', 'sophyhoney', 'oouoo4648', 'maymay123', 'eunjxx_108', 'ddalgi11', 'nagi_729', 'best4664', 'ringom0201', 'justdoitming', 'annau__u', 'lhk8787', 'yelloww613', 's98soon', 'raraann', 'kee5538', 'iamstar_', 'kimsej88', 'coco_9301', 'jkhn4325', 'hyewon_100588', 'wndud8354', 'sooyeon1202', 'ddiamosho', 'mg-shin', 'orangesirena', 'hr2love', 'leehaksoon', 'weiss2015', 'kindness89', 'lovmaria', 'pkloveletter', 'hyunadoo', 'fbwogus123', 'hosoo881020', 'silpid59', 'limbomee', 'osa3532', 'dailycindy', 'jo_penquin', 'dbqkffodyd', 'gomzzu', 'flostars', 'hyghhu', 'xkdidhqk11', 'janus0618', 'kkumiho', 'mint_always', 'seongminlove', 'wkdwlgp94', 'iso_sr', 'hbj0128', 'kbr0222', 'whrnjs4225', 'hhhh2346', 'skqusrudals12', 'crt4658', 'missj0322', 'dgnmm123', 'cyaflower', 'yaimn', '77ended', 'vividyg', 'hopuhope', 'gowjd1223', 'vjdud1222', 'kiho1030', 'damor1208', 'chry6295', 'daaah5', '05017491', 'ghkdwjddo202', '420dussssu', 'd_hye97', 'hwawoorok', 'rizotto1', 'ilov2h5691', 'jjanga1919', 'purplebora1018', 'lhr0905', 'thxjamie365', 'bebe9820', 'hark739', 'clamsh', 'sjsj_kim0228', 'pm0146', 'xo-elliott', 'seven-queen', 'jdbri1130', 'marilyn1', 'tnalalstn', 'odri1998', 'shinegirl05', 'good_coco', 'jieun2468jieun', 'x_x0319', 'ton53', 'xkralswo', 'k_sr0609', 'momokko', 'ha5807', 'nova007', 'gkffhzz', 'alsmekwyd', 'musicalyoon', 'tinynova', 'py2389', 'gng6679', 'kbearp', 'ksbeen0709', 'nam59887', 'jujuyeong', 'zzeeun', 'hwp1209', 'zellove12', 'soulmate1983', 'sesirlis', 'dnjswns15', 'glassr', 'sihyukumma14', 'yu_jin0415', 'wjddms0305', 'o_live_you', 'u_ulla', 'rhdnsnl88', 'rain8200', 'lovebookn', 'kej727_2', 'sj1229', 'takaraa', 'wlsdud8607', 'base02014', 'bluesoso', 'alfk8195', 'dudfla6771', 'yej45864586', 'njmjjang', 'lostpola79', 'lui14won', 'sdsd0536', 'darksea02', 'ty_hwang', 'thdud261', 'ceoseri', 'bo_angel', 'fairyasrai', 'ellew4902', 'kafer', 'quf4147', 'kies1614', 'hellomini486', 'ri_nyy', 'lamoon12', 'nadaumii', 'zizimi89', 'mkr4223', 'xogh0147', 'sji_eun', 'lillian1216', 'hongtaigne', 'lizela87', 'cm0103', 'yunkmink', 'rudals9703', 'lin100', 'xuanwo', 'pure_yeong0', 'disguise_126', 'kjtpntn', 'jieun_0216', 'kindmiso89', 'love_yulian', 'gkwls0320', 'audtjs1981', 'vov1077', 'hwiba0030', 'anue1123', 'lkjta55', 'changbum2', 'zasan77', 'xingyuner72', 'dbrkgus52', 'tncjq5', 'love3550', 'wltn786', 'kdseul33', 'asstarpine', '1223psy', 'kkso0503', '0525shj', 'sdm_bomi', 'ooheeya96', 'cuteboy0519', 'midihj', 'vyeon_', 'melonheads', 'yek867', 'delightplace', 'coolmikki', 'seanbyeol', 'inhey021', 'msunh']
final_score_list=[]
for blogger_name in blogger_list:
    # data = pd.read_csv('./blogger all post/'+blogger_name+'.csv')
    # 0->ad 1->notad
    is_notad = 2
    data = blog_crawler(blogger_name)
    final_df={}

    category = []
    for item in item_list:
        item = item.replace(' ','')
        item_bool = data['Title'].apply(lambda x: item in x)
        item_df = data[item_bool]
        # final_df = final_df.join(pd.Series(list(item_df['Link'])).rename(item), how='right')
        final_df[item] = list(item_df['Link'])

    score_list=[]
    for item in item_list:
        temp = item.replace(' ','')
        url_list = final_df[temp]
        
        num =-1
        
        if len(url_list)>0:
            crawler = NaverBlogCrawler(_blog_url_list = url_list)
            df = crawler.getPostDataFrame_blogUrls()
            ad,week_view, score = score_blogger(item,df)
            if ad == 1 and is_notad==2:
                is_notad=1
            if ad == 0 and is_notad!=0:
                is_notad = 0
            score_list.append(score)
        else:
            score_list.append(None)

    viewer_num_url = f'https://blog.naver.com/NVisitorgp4Ajax.nhn?blogId={blogger_name}'
    viewer_num_response = requests.get(viewer_num_url)
    viewer_num_list = [int(node.get("cnt")) for node in ET.fromstring(viewer_num_response.text)]
    week_view = np.mean(np.array(viewer_num_list))

    score_list.append(is_notad)
    score_list.append(week_view)
    score_df = pd.DataFrame([score_list],columns=item_list+['ad','weekly view'])
    score_list.insert(0,blogger_name)
    final_score_list.append(score_list)
    score_df.to_csv('./blogger score/'+blogger_name+'.csv')

item_list.insert(0,'blog id')
final_score_df = pd.DataFrame(final_score_list,columns=item_list+['ad','weekly view'])
final_score_df = final_score_df.set_index('blog id')
final_score_df.to_csv('./blogger score/all item matrixs__.csv')