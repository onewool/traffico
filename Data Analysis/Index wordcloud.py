import time # sleep처리를 위해
from selenium import webdriver #webdriver가 브라우저 제어
from selenium.webdriver.support.ui import WebDriverWait
import requests
from wordcloud import WordCloud
from collections import Counter

#검색어 조건에 따른 url생성
def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/'+str(word)
    return url
#열린 페이지에서 첫번째 게시물 클릭 + sleep메소드 통하여 시차 두기
def select_first(driver):
    first = driver.find_elements_by_css_selector('div._9AhH0')[0]
    first.click()
    time.sleep(3)
    
    
#본문 내용, 작성일자, 좋아요 수, 위치정보, 해시태그 가져오기
import re
from bs4 import BeautifulSoup
def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    #본문 내용
    try:
        content = soup.select('div.MOdxS')[0].text
    except Exception:
        content = ''
    #해시태그
    tags = re.findall('#[A-Za-z0-9가-힣]+',content)
    return tags
    
#첫번째 게시물 클릭 후 다음 게시물 클릭
def move_next(driver):
    right = driver.find_element_by_css_selector('div.l8mY4.feth3')
    right.click()
    time.sleep(2)

#크롬 브라우저 열기
driver = webdriver.Chrome('data/chromedriver.exe')

driver.get('https://www.instagram.com')
time.sleep(5)

#인스타그램 로그인을 위한 계정 정보
email = 'clairule@gmail.com'
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)
password = '95spsaigin'
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
time.sleep(1)
input_pw.submit()

time.sleep(5)


#게시물을 조회할 검색 키워드 입력 요청
# word = input('검색어를 입력하세요 : ')
# word = str(word)
word = '교통'
url = insta_searching(word)

#검색 결과 페이지 열기
driver.get(url)
time.sleep(8) #코드 수행 환경에 따라 페이지가 로드되는 데 시간이 더 걸릴 수 있어 8초로 변경

#첫번째 게시물 클릭
select_first(driver)

#본격적으로 데이터 수집 시작
results = []
##수집할 게시물의 수
target = 2000
for i in range(target):
    try:
        data = get_content(driver)
        results.append(data)
        move_next(driver)
    except:
        time.sleep(2)
        move_next(driver)
print(results)
print(len(results))
#이중 list 풀기
tags_lst = sum(results, [])
print(tags_lst)
print(len(tags_lst))

#태그 하나당 얼마나 언급됐는지

from collections import Counter
tag_counts = Counter(tags_lst)
print(tag_counts)
tag_counts.most_common(100) #순위 100위
#stopword
STOPWORDS = ['#유머저장소','#꿀팁','#꿀팁정보','#좋반','#좋아요','#좋아요반사','#좋아요테러','#선팔하면맞팔','#꿀팁스타그램','#좋테','#꿀팁공유','#유머스타그램','#유머','#유머그램','#좋아요그램','#꿀잼','#리그램','#사랑해','#예능','#맞팔환영','#좋튀','#맞팔해요','#daily','#데일리','#일상', '#선팔', '#제주자연눈썹', '#제주눈썹문신', '#소통', '#맞팔','#제주속눈썹', '#제주일상', '#제주도','#jeju','#반영구','#제주살이','#제주도민', '#여행스타그램', '#제주반영구', '#제주메이크업', '#남자옷', '#맞팔','#jejuisland','#일상','#스톤패딩','#명품신발','#래플신발','#발리신발','#구찌신발', '#커플신발','#로렉스시계','#태그호이어시계','#명품시계','#명품클러치','#보테가클러치','#구찌클러치','#남자쇼핑몰','#남친선물','#고야드지갑','#고야드클러치','#발렌시아가','#웃긴짤','#오운완','#숙박할인혜택이','#빵빵터짐','#웃음지뢰','#유머짤','#풉1','#좋아요선팔','#피식','#선팔좋아요','#팔반','#ssul','#썰','#선팔은곧맞팔','#오늘의유머','#웃긴영상','#좋태','#짤','#육아웹툰','#대통령오세훈','#이준석','#윤석열','#썰전','#육아필수템','#헬창','#인천꽃집','#신용보증기금','#웃어요','#최신예능','#오세훈시장','#25살','#태그','#신혼부부','#고3','#위드코로나','소통', '#traffic', '#김승현', '#daily','#교통','#느티와까']
tag_total_selected = []

for tag in tags_lst:
   if not tag in STOPWORDS:
       tag_total_selected.append(tag)

print(tag_total_selected)
import pandas as pd
tag_count_df = Counter(tag_total_selected)
print(tag_count_df)


#wordcloud로 만들어보기
import matplotlib.pyplot as plt
from wordcloud import WordCloud
wc = WordCloud(font_path = 'data/NanumBarunGothic.ttf',
                    background_color = 'white',
                    colormap = 'YlGnBu',
                    max_words = 300,
                    relative_scaling = 0,
                    width = 800,
                    height = 400).generate_from_frequencies(tag_count_df)
plt.figure(figsize = (18,10))
plt.imshow(wc)
plt.axis('off')
plt.show()

#bar로 만들어보기

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] = 15
plt.rcParams['figure.figsize'] = (10,6)

#세로그래프 : barh
ten = Counter(tag_total_selected).most_common(10)
print(ten)
ten_barh = {}
for (i,v) in ten:
    ten_barh[i] = v
# ten_barh = list(ten_barh)
print(ten_barh.values())

from pandas import DataFrame
df = DataFrame(ten_barh.values(), index=list(ten_barh))
df = df.rename(columns={0:'태그건수'})
print(df)
df.plot.barh(color='indigo')
plt.grid()
# plt.xlim(1800,4000)
plt.title('최근 1000개 게시글 교통태그 관련 상위 10개 태그')
plt.xlabel('건수')
# plt.ylabel()

#문자열넣기
for i,v in enumerate(df['태그건수']):
    txt = '%d건' %v
    plt.text(v,i-0.2,txt,color='red', fontsize=12)
plt.show()
