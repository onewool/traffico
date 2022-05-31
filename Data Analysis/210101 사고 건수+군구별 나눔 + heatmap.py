#================================================================================
#================================ dataframe 정제 ================================
#================================================================================

from pandas import DataFrame, read_csv
import pandas as pd

######### 콘솔창에 행열 많이 보이게 #########
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

######### 데이터 불러오기 #########
df = read_csv('data/AcDay/Ac_Day_20210101.csv', encoding='euc-kr', sep = ',',
              keep_default_na=False,
              names=['Date','accID','startDate','endDate','type','eventType','message','coordX', 'coordY',1,2,3,4,5],
              header=None)
#columns=['Date','accID','startDate','endDate','type','eventType','message','coordX', 'coordY']
print(df.shape)
print(df)

######## 열 9개로 맞추기위한 리스트화 #########
for i in range(1,len(df.index)):   
    if df.iloc[i,-1] != '':
        df.iloc[i,7] = df.iloc[i,-2]
        df.iloc[i,8] = df.iloc[i,-1]
    elif df.iloc[i,-2] != '':
        df.iloc[i,7] = df.iloc[i,-3]
        df.iloc[i,8] = df.iloc[i,-2]
    elif df.iloc[i,-3] != '':
        df.iloc[i,7] = df.iloc[i,-4]
        df.iloc[i,8] = df.iloc[i,-3]
    elif df.iloc[i,-4] != '':
        df.iloc[i,7] = df.iloc[i,-5]
        df.iloc[i,8] = df.iloc[i,-4]
    elif df.iloc[i,-5] != '':
        df.iloc[i,7] = df.iloc[i,-6]
        df.iloc[i,8] = df.iloc[i,-5]

######## 쓸모없는 열 제거 #########
df = df.drop(df.columns[1:5], axis=1).drop(df.columns[6], axis=1).drop(df.columns[9:], axis=1)
print(df)
# for i, v in  enumerate(df.loc[0]):
#     print(i)
#     print(v)

######### numpy 불러오기 #########
import numpy as np

######### 위도 경도 소숫점 2 자리수까지 반올림 #########
print(df['coordX'].dtype)
print(df['coordY'].dtype)
df['coordX'] = df['coordX'].astype(np.float)
df['coordY'] = df['coordY'].astype(np.float)
print(df['coordX'].dtype)
print(df['coordY'].dtype)
df['coordX'] = np.around(df['coordX'],2)
df['coordY'] = np.around(df['coordY'],2)
print(df)

######### eventType '기상', '사고' 원인만 보기 #########
df['eventType'] = df['eventType'].str.strip()
df =  df[(df.eventType=='기상') | (df.eventType=='사고')]
print(df)
weather = df[(df.eventType=='기상')]
print(weather)
accident = df[(df.eventType=='사고')]
print(accident)

######### 기상에서 같은 위도 경도끼리 묶기 #########
groupedAcci = accident.groupby(['coordX','coordY'])
print(groupedAcci)


######### 기상에서 같은 위도 경도의 사고건수 count() #########
counts = groupedAcci.count()
print(counts)
print(counts.index[3][0])

# 지도에 쓸 새로운 dataframe만들기
df = counts.reset_index()
print(df)

#================================================================================
#=================================구역나누는 코드=================================
#================================================================================

import requests
import json

#서울지역 json 파일
kr_distinct_geojson = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/juso/2015/json/seoul_municipalities_geo.json'

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
print(geo_dict)

#
from shapely.geometry import Point, Polygon
def get_GeoName(longi,lati):
    for geo_name, geo_poly in geo_dict.items():
        poly_obj = Polygon(geo_poly)
        point_obj = Point(longi,lati)
        if point_obj.within(poly_obj):
            return geo_name
    return None

#구역 이름 새로운 column으로 붙이기
df['geo_name'] = df.apply(lambda x : get_GeoName(x['coordX'], x['coordY']), axis=1)

print(df['geo_name'])

#df['geo_name']이 null값인, 서울지역이 아닌 갯수 세기
print(df.isnull().sum())
#df['geo_name']이 null값인 행 날리기
df = df.dropna(axis=0)
#출력
print(df)

#================================================================================
#================================= folium 그리기 =================================
#================================================================================

import folium
#시도 center정하기
center = [37.566345, 126.977893]
m = folium.Map(location = center,zoom_start = 11)
folium.GeoJson(kr_distinct_geojson).add_to(m)
folium.Choropleth(geo_data=jsonData,
                  data=df,
                  columns=['geo_name','Date'],
                  key_on='feature.properties.SIG_KOR_NM',
                  fill_color="BuPu",
                  fill_opacity=0.6,
                  line_opacity=0.2,
                  legend_name="Seoul"
                  ).add_to(m)
m.save('./210101_서울사고 heatmap.html')
print('저장완료')
