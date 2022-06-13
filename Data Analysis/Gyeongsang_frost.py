from pandas import DataFrame, read_excel
import pandas as pd
import matplotlib.pyplot as plt
import folium
import requests
import json

######### 데이터 불러오기 #########
df1 = read_excel('data/행정안전부_상습 결빙구간_20200921.xlsx', keep_default_na=False)
#print(df1)

######### 폰트 및 그래프 사이즈 설정 #########
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] =12
plt.rcParams['figure.figsize']= (6,4)

######### 필요한 열만 추출 #########
df1 = df1.filter(['구간명','구간길이','센터X좌표','센터Y좌표','시작주소'])
#print(df1)

######### 열 이름 변경 #########
df1 = df1.rename(columns={'구간길이':'properLength','센터X좌표':'latitude','센터Y좌표':'longitude'})
#print(df1)


df1 = df1.drop(df1.index[0])
#print(df1)
df1['properLength'] = df1['properLength'].astype(float)
location_data = df1[['latitude','longitude']].values[:len(df1)].tolist()
m = folium.Map(location=[35.994217, 128.664734], zoom_start=9)

kr_distinct_geojson = 'https://raw.githubusercontent.com/onewool/traffico/main/Data%20Analysis/data/geojson/%EA%B2%BD%EC%83%81%EB%8F%84.json'
print('json파일 불러옴')

response = requests.get(kr_distinct_geojson)
dictres = response.json()
c = response.content
jsonData = json.loads(c)

style1 = {'fillColor': '#7c5494',  'fillOpacity': 0.5, 'color': '#A91079'} #00000000가 투
folium.GeoJson(jsonData, name='json_data',style_function=lambda x:style1).add_to(m)

from folium import plugins
print(df1)
for i in range(1,len(df1)) :
    max_bc_count= float(df1['properLength'][i])
    print('>')
    folium.Circle(location = location_data[i], popup=(df1['구간명'][i]),
                  radius=max_bc_count).add_to(m)
plugins.MarkerCluster(location_data).add_to(m)

m.save('Gyeongsang_frost.html')

#======================== 상위 5개 결빙 구간 길이 sorting ========================
condition_area = df1.시작주소.str.contains('경남') | df1.시작주소.str.contains('경북') | df1.시작주소.str.contains('부산')
df_area = df1.loc[condition_area]
print(df_area)
print(len(df_area))

df2 = df_area.sort_values(by='properLength', ascending=False).head(5)
print(df2)

#pieplot설정
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10,6)
colors = ['#3F2DA5','#6146D9','#7354F4','#7E6CFB','#7E84F3','#7D99ED','#77ADE6','#70C2DF','#74D3DC','#9EDFE5','#C3EBEF']
wedgeprops={'width': 0.5, 'edgecolor': 'w', 'linewidth': 5}

tx = list(df2['properLength'])

labels = df2['구간명']


fig, ax, autopcts= plt.pie(tx,labels=labels, autopct='%.0f%%',pctdistance=0.75, startangle=260, counterclock=False, colors=colors, wedgeprops=wedgeprops)
plt.setp(autopcts, **{'color':'white', 'weight':'bold', 'fontsize':11})
plt.title('경상도 시군구별 결빙 길이 상위5개')
plt.ylabel(None)
plt.show()