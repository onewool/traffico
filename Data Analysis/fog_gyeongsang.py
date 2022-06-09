from pandas import DataFrame, read_excel
import pandas as pd
import matplotlib.pyplot as plt
import folium
import requests
import json

######### 데이터 불러오기 #########
df1 = read_excel('data/fog.xlsx', keep_default_na=False)
#print(df1)

######### 폰트 및 그래프 사이즈 설정 #########
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] =12
plt.rcParams['figure.figsize']= (6,4)

######### 필요한 열만 추출 #########
df1 = df1.filter(['구간명','구간길이','센터X좌표','센터Y좌표'])
#print(df1)

######### 열 이름 변경 #########
df1 = df1.rename(columns={'센터X좌표':'latitude','센터Y좌표':'longitude','구간길이':'properLength'})
#print(df1)

df1 = df1.drop(df1.index[0])
#print(df1)
df1['properLength'] = df1['properLength'].astype(float)

m = folium.Map(location=[35.954217, 128.664734], zoom_start=9)

kr_distinct_geojson = 'https://raw.githubusercontent.com/onewool/traffico/main/Data%20Analysis/data/geojson/%EA%B2%BD%EC%83%81%EB%8F%84.json'
print('json파일 불러옴')

response = requests.get(kr_distinct_geojson)
dictres = response.json()
c = response.content
jsonData = json.loads(c)

style1 = {'fillColor': '#A0BA71',  'fillOpacity': 0.5, 'color': '#228B22'} #00000000가 투
folium.GeoJson(jsonData, name='json_data',style_function=lambda x:style1).add_to(m)

for i in df1.index :
    marker = folium.Marker([df1.loc[i,'latitude'],df1.loc[i,'longitude']],  popup=df1['구간명'][i], icon = folium.Icon(color = 'blue', icon = 'info-sign'))
    marker.add_to(m)
m.save('Gyeongsang_fog.html')
