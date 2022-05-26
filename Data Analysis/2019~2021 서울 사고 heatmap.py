from pandas import DataFrame, read_csv
import pandas as pd

######### 콘솔창에 행열 많이 보이게 #########
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

######### 파일합치기 #########
import pandas as pd 
import numpy as np
import os

forders = os.listdir('data/AcDay')
#print(forders)
df_all = pd.DataFrame()
for i in range(0,len(forders)):
    if forders[i].split('.')[1] == 'csv':
        file = 'data/AcDay/'+forders[i]
        df= pd.read_csv(file,encoding='cp949', keep_default_na=False, names=['Date','accID','startDate','endDate','type','eventType','message','coordX', 'coordY',1,2,3,4,5], header=None) 
        df_all = pd.concat([df_all, df])
        
df_all.to_csv('./test.csv', encoding='euc-kr', header=False, index=False)
print('저장 완료')
df=pd.read_csv('test.csv', encoding='euc-kr', keep_default_na=False, names=['Date','accID','startDate','endDate','type','eventType','message','coordX', 'coordY',1,2,3,4,5], header=None)

df = pd.read_csv(r"C:\Jaeeun Huh\09_팀포폴\data\result_line.csv")
print(df.shape)
print(df)

######## 열 9개로 맞추기위한 리스트화 #########
for i in range(0,len(df.index)):   
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

######## 쓸모없는 열 제거 #########
df = df.drop(df.columns[1:4], axis=1).drop(df.columns[5:7], axis=1).drop(df.columns[9:], axis=1)
print(df)

######### numpy 불러오기 #########
import numpy as np

# coordX와 coordY가 숫자가 아니면 행 지우기
# print(df['coordX'][2].type)
# df = df.select_dtypes(include=['datetime',float,'number'])
print(df)

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

######### type '공사(0)', '사고(1)' 원인만 보기 #########
df =  df[(df.type==0) | (df.type==1)]
print(df)
fix = df[(df.type==0)]
print(fix)
accident = df[(df.type==1)]
print(accident)

######### 사고에서 같은 위도 경도끼리 묶기 #########
groupedAcci = accident.groupby(['coordX','coordY'])
print(groupedAcci)


######### 사고에서 같은 위도 경도의 사고건수 count() #########
counts = groupedAcci.count()
print(counts)


# 지도에 쓸 새로운 dataframe만들기
df = counts.reset_index()
print(df)

#================================================================================

import requests
import json


kr_distinct_geojson = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/juso/2015/json/seoul_municipalities_geo.json'

response = requests.get(kr_distinct_geojson)
dictres = response.json()
c = response.content
jsonData = json.loads(c)

geo_dict = {}

for dict_row in dictres['features'] :
    geo_name = dict_row['properties']['SIG_KOR_NM'];
    geo_value = dict_row['geometry']['coordinates'][0];
    geo_dict[geo_name] = geo_value
print(geo_dict)

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
m.save('./3년치 서울_사고건수 heatmap.html')
print('저장완료')
