from pandas import DataFrame, read_csv
import pandas as pd

######### 콘솔창에 행열 많이 보이게 #########
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

######### 파일합치기 #########

df = pd.read_csv('data/2019~2021.csv', encoding='ISO-8859-1')
print(df.shape)
print(df)

######## 위도 경도 한 줄 내려간거 없애기 #########
print(df['type'].isna().sum())
print('중간완료')
######## 열 9개로 맞추기위한 리스트화 #########
for i in range(1,len(df.index)):   
    if df.iloc[i,-1] == df.iloc[i,-1]: #NaN의 경우 같아도 False를 뱉음
        df.iloc[i,7] = df.iloc[i,-2]
        df.iloc[i,8] = df.iloc[i,-1]
    elif df.iloc[i,-2] == df.iloc[i,-2]:
        df.iloc[i,7] = df.iloc[i,-3]
        df.iloc[i,8] = df.iloc[i,-2]
    elif df.iloc[i,-3] == df.iloc[i,-3]:
        df.iloc[i,7] = df.iloc[i,-4]
        df.iloc[i,8] = df.iloc[i,-3]
    elif df.iloc[i,-4] == df.iloc[i,-4]:
        df.iloc[i,7] = df.iloc[i,-5]
        df.iloc[i,8] = df.iloc[i,-4]
    elif df.iloc[i,-5] == df.iloc[i,-5]:
        df.iloc[i,7] = df.iloc[i,-6]
        df.iloc[i,8] = df.iloc[i,-5]
    print('>',end='')
print('for문완료')
######## 쓸모없는 열 제거 #########
df = df.drop(df.columns[1:4], axis=1).drop(df.columns[5:7], axis=1).drop(df.columns[9:], axis=1)
print(df)

######### numpy 불러오기 #########
import numpy as np

# coordX와 coordY가 숫자가 아니면 행 지우기
# print(df['coordX'][2].type)
# df = df.select_dtypes(include=['datetime',float,'number'])
print(df)

# df.to_csv('./2019~2021.csv', header=False, index=False)
# print('2019~2021.csv 저장 완료')

# #========================================================================
# #================================test파트================================
# #========================================================================

# df = pd.read_csv('./2019~2021.csv',
#                  names=['Date','type','coordX', 'coordY'],header=None)
df = df.dropna()
print(df)
condition = df.coordX.str.contains('12') | df.coordX.str.contains('13')
df = df.loc[condition]

######### 위도 경도 소숫점 2 자리수까지 반올림 #########
# print(df['coordX'].dtype)
# print(df['coordY'].dtype)
df['coordX'] = df['coordX'].astype(np.float)
df['coordY'] = df['coordY'].astype(np.float)
# print(df['coordX'].dtype)
# print(df['coordY'].dtype)
# df['coordX'] = np.around(df['coordX'],2)
# df['coordY'] = np.around(df['coordY'],2)
# print(df)
print('type변경완료')

######### type '공사(0)', '사고(1)' 원인만 보기 #########
df =  df[(df.type==0) | (df.type==1)]
#print(df)

#df.to_csv('./2019~2021(공사,사고).csv', encoding='euc-kr', header=False, index=True)

df = df[(df.type==0)]
print(df,'\n공사')
#df = df[(df.type==1)]
#print(df,'\n사고')


#========================================================================
#================================ 구역화 ================================
#========================================================================

import requests
import json
#========================================================================
#========================= 공사, 사고 데이터 =============================
#========================================================================
#df = pd.read_csv('data/2019~2021(공사,사고).csv', encoding='ISO-8859-1',names=['dd','Date','type','coordX','coordY'] )
# import urllib

# district = ['강원도', '경기도', '경상도', '서울','전라도', '충청도']
# for i in district:
#     district_url = urllib.parse.quote(i)

#서울지역 json 파일
kr_distinct_geojson = 'https://raw.githubusercontent.com/onewool/traffico/main/Data%20Analysis/data/geojson/%EC%84%9C%EC%9A%B8.json'
print('json파일 불러옴')

response = requests.get(kr_distinct_geojson)
dictres = response.json()
c = response.content
jsonData = json.loads(c)

#json파일 dictionary로 바꿈
geo_dict = {}
for dict_row in dictres['features'] :
    geo_name = dict_row['properties']['SIG_KOR_NM'];
    geo_value = dict_row['geometry']['coordinates'][0];
    geo_dict[geo_name] = geo_value
print('geo_name 불러오기 완료')

from shapely.geometry import Point, Polygon

def get_GeoName(longi,lati):
    for geo_name, geo_poly in geo_dict.items():
        
        poly_obj = Polygon(geo_poly)
        point_obj = Point(longi,lati)
        
        if point_obj.within(poly_obj):
            return geo_name
    return None

df['geo_name'] = df.apply(lambda x : get_GeoName(x['coordX'], x['coordY']), axis=1)

print(df['geo_name'])
print(df.isnull().sum())
df = df.dropna(axis=0)
print(df)
print('geo_name 붙이기 완료')

######### 사고에서 같은 geo_name끼리 묶기 #########
grouped = df.groupby(['geo_name'])
print(grouped)
print('group화 완료')

######### 사고에서 같은 geo_name의 사고건수 count() #########
counts = grouped.count()
print(counts)
print('count 완료')

# 지도에 쓸 새로운 dataframe만들기
df = counts.reset_index()
print(df)


#========================================================================
#================================ 지도화 ================================
#========================================================================

import folium
#시도 center정하기
center = [37.540705, 126.956764]
m = folium.Map(location = center,zoom_start = 10)
folium.GeoJson(kr_distinct_geojson).add_to(m)
folium.Choropleth(geo_data=jsonData,
                  data=df,
                  columns=['geo_name','Date'],
                  key_on='feature.properties.SIG_KOR_NM',
                  fill_color="BuPu",
                  fill_opacity=0.6,
                  line_opacity=0.2,
                  legend_name="서울시"
                  ).add_to(m)
m.save('./2019~2021 서울시공사_heatmap.html')
print('html 저장완료')


#========================================================================
#===================== data 정제 =====================
#========================================================================

df = df.rename(index=df['geo_name']).drop(['geo_name','type', 'coordX','coordY'],axis=1)
df = df.rename(columns={'Date':'공사 건수'})
print(df)
print('dataframe 완료')


#========================================================================
#===================== 결측치 및 이상치 확인 및 처리 =====================
#========================================================================

import matplotlib.pyplot as plt
print(df.isna().sum())
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['figure.figsize'] = (4,6)
plt.title('서울 시군구별 공사건수 분포')
df.boxplot('공사 건수')
plt.show()


#========================================================================
#================================ pieplot ================================
#========================================================================

#상위 10개 시군구 sorting
df1 = df.sort_values(by='공사 건수', ascending=False).head(10)
print(df1)
#하위 10개 시군구 sorting
df2 = df.sort_values(by='공사 건수', ascending=True).head(10)
print(df2)

#pieplot설정
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10,6)
colors = ['#3F2DA5','#6146D9','#7354F4','#7E6CFB','#7E84F3','#7D99ED','#77ADE6','#70C2DF','#74D3DC','#9EDFE5','#C3EBEF']
wedgeprops={'width': 0.5, 'edgecolor': 'w', 'linewidth': 5}

tx = list(df1['공사 건수'])
#print(tx)
tx1 = list(df2['공사 건수'])
labels = df1.index
#print(labels)
labels1 = df2.index

fig, ax, autopcts= plt.pie(tx,labels=labels, autopct='%.0f%%',pctdistance=0.75, startangle=260, counterclock=False, colors=colors, wedgeprops=wedgeprops)
plt.setp(autopcts, **{'color':'white', 'weight':'bold', 'fontsize':11})
plt.title('서울 시군구별 공사건수 상위10개')
plt.ylabel(None)
plt.show()

plt.bar(labels1,tx1,color='purple')
plt.title('서울 시군구별 공사건수 하위10개')
plt.xticks(rotation=45)
plt.grid()
for x, y in enumerate(df2['공사 건수']):
    text = '%d건' %y
    plt.text(x,y,text, fontsize=12, c='red', horizontalalignment='center')
plt.show()