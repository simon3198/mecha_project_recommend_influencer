# mecha_project

인플루언서 점수 계산법

좋은 글에 대해 높은 점수를 주는 점수식을 만들었다. 
좋은 글에 대한 판단 기준은
- 직접후기 처럼 썻냐
- 가독성이 좋냐

위의 두가지 기준으로 점수를 계산하는 식을 구성했다.


# 각 파일에 대한 설명

- blogger all post : 블로거가 쓴 최근 5년 글들의 title 와 link를 csv파일로 저장
- blogger score : 블로거의 아이템별 점수를 csv파일로 저장
- crawler : 네이버 블로그와 쿠팡 레뷰 등 데이터를 크롤링할 수 있는 코드가 있고 크롤링 데이터를 csvfile에 저장
- data_analysis : click 데이터와 설문조사 데이터를 분석
- image : 이미지 파일
- ML : 머신러닝 적용 파일
- score : 네이버 블로그 크롤러를 통해 크롤링한 데이터에 점수를 매겨본 파일
- survey : 설문조사 데이터 전처리 코드
- threshold : 점수를 계산할 때 각 아이템별 최대값과 최소값 또는 평균과 표준편차를 저장한 파일

# 각 코드에 대한 설명

- blogger crawler.py : 블로거의 모든 글들을 크롤링하는 크롤러
- make blogger itemlist.py : blogger item matrix를 만드는 크롤러
- make keyword list.py : tfidf_mecab.py 와 word_frequency.py를 이용해 아이템별 키워드 리스트를 write.csv로 만드는 코드 
- naver blog crawler.py : 네이버 블로그 크롤러
- naver blog crawler for all items : 아이템 목록을 지정하여 네이버 블로그 크롤러 실행
- score for blogger.py : 블로거의 아이템별 점수를 계산하는 코드
- score upgrade.py : 아이템별 특성의 정규화를 위한 최소값, 최댓값 표준화를 위하 표준편차 평균을 저장하는 코드
- tfidf_mecab.py : 아이템별 tfidf 값을 저장하는 코드
- word_frequency.py : 아이템별 단어빈도수를 저장하는 코드
- write.csv : 아이템별 키워드 리





