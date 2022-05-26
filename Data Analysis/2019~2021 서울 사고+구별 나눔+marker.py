from pandas import DataFrame, read_csv
import pandas as pd

######### 콘솔창에 행열 많이 보이게 #########
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

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

######## 쓸모없는 열 제거 #########
df = df.drop(df.columns[1:4], axis=1).drop(df.columns[5:7], axis=1).drop(df.columns[9:], axis=1)
print(df)

######### numpy 불러오기 #########
import numpy as np

# coordX와 coordY가 숫자가 아니면 행 지우기
# print(df['coordX'][2].type)
# df = df.select_dtypes(include=['datetime',float,'number'])
print(df)

df = df.dropna()
print(df)
condition = df.coordX.str.contains('12') | df.coordX.str.contains('13')
df = df.loc[condition]


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

#지도만들기

import folium
import requests
import json

#시도 center정하기
center = [37.566345, 126.977893]

# 서울 행정구역 json raw파일(드라이브)
# map_osm = folium.Map(location=center)
# rfile = open('C:/Jaeeun Huh/09_팀포폴/data/seoul_municipalities_geo.json', 'r', encoding='utf-8').read()
# jsonData = json.loads(rfile)

# 서울 행정구역 json raw파일(githubcontent)
r = requests.get('https://raw.githubusercontent.com/southkorea/seoul-maps/master/juso/2015/json/seoul_municipalities_geo.json')
c = r.content
jsonData = json.loads(c)

# df로 map만들기
seoul_map = folium.Map(
    location = center,
    zoom_start = 11,) #지도 띄울 때 center 및 처음 확대비율 지정
print(df)
# for name, lat, lng in zip(df.index, df.coordY, df.coordX):
#     print(name, lat, lng)


#시도 boundary 포함
style1 = {'fillColor': '#A0BA71',  'fillOpacity': 0.5, 'color': '#228B22'} #00000000가 투
folium.GeoJson(jsonData, name='json_data',style_function=lambda x:style1).add_to(seoul_map)


#marker그리기
from folium.plugins import MarkerCluster
marker_cluster = MarkerCluster().add_to(seoul_map)
for name, lat, lng, r in zip(df.index, df.coordY, df.coordX, df.Date):
    folium.Marker([lat, lng],
                        radius = r*5,
                        weight = 1,
                        color = 'blue',
                        fill = True,
                        fill_opacity = 0.1,
                        popup = name).add_to(marker_cluster)

#Heatmap
# seoul_map.choropleth(geo_data=jsonData,
#              data=df.Date, 
#              fill_color='YlOrRd', # 색상 변경도 가능하다
#              fill_opacity=0.5,
#              line_opacity=0.2,
#              key_on='properties.name'
#             )


# 위치 정보를 CircleMarker로 표시
# popup = name은 해당 마커를 클릭하면 지정한 열의 값이 보임


marker_cluster.save('./2019~2021 서울 사고 marker2.html')
print('저장완료')


